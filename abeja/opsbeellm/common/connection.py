import base64
import json
import os
import http
from typing import Optional, Union, Text, IO, MutableMapping, Any
from urllib.parse import urlparse
from distutils.util import strtobool

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError as RequestsHTTPError
from requests.packages.urllib3.util.retry import Retry

from abeja import VERSION
from abeja.common.auth import get_credential
from abeja.exceptions import (
    HttpError,
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    MethodNotAllowed,
    Conflict,
    InternalServerError
)

SDK_CONNECTION_TIMEOUT_ENV_KEY = 'ABEJA_SDK_CONNECTION_TIMEOUT'
SDK_MAX_RETRY_COUNT_ENV_KEY = 'ABEJA_SDK_MAX_RETRY_COUNT'

DEFAULT_MAX_RETRY_COUNT = 5
DEFAULT_CONNECTION_TIMEOUT = 30


class OpsBeeLLMConnection:
    """A connection to ABEJA Platform OpsBeeLLM API."""
    BASE_URL = os.environ.get('ABEJA_API_URL', 'https://api.stage.abeja.io')
    OPSBEELLM_BASE_URL = os.environ.get('ABEJA_OPSBEELLM_API_URL', 'https://opsbee-llm.stage.abeja.io')
    OPSBEELLM_API_TOKEN = os.environ.get('ABEJA_OPSBEELLM_API_TOKEN', 'dummy')

    def __init__(
            self,
            credential=None,
            timeout: Optional[int] = None,
            max_retry_count: Optional[int] = None):
        self.timeout = timeout or os.environ.get(
            SDK_CONNECTION_TIMEOUT_ENV_KEY) or DEFAULT_CONNECTION_TIMEOUT
        self.max_retry_count = max_retry_count or os.environ.get(
            SDK_MAX_RETRY_COUNT_ENV_KEY) or DEFAULT_MAX_RETRY_COUNT

        # ARMS 用 credential と OpsBeeLLM 用 credential を別々に管理
        # TODO: OpsBeeLLM API を ARMS の Gateway 経由で呼び出すようにしたあとは、この処理は不要になる。
        if credential is None:
            self.credential = get_credential() or {}
        else:
            self.credential = credential
        if 'user_id' in self.credential and not self.credential['user_id'].startswith(
                "user-"):
            self.credential['user_id'] = 'user-{}'.format(
                self.credential['user_id'])

        self.opsbee_credential = {"auth_token": self.OPSBEELLM_API_TOKEN}

    def api_request(
            self,
            method,
            path,
            data=None,
            json=None,
            headers=None,
            params=None,
            **kwargs):
        """call platform opsbee-llm api and handle errors if needed

        :param method:
        :param path:
        :param data:
        :param headers:
        :param params:
        :param json:
        :param kwargs:
        :return: (dict) api response
        """
        if headers is None:
            headers = {}

        # ARMS API にリクエストして、user_id と personal_access_token が正しいか確認。
        # TODO: OpsBeeLLM API を ARMS の Gateway 経由で呼び出すようにしたあとは、この処理は不要になる。
        USER_AUTH_ARMS = strtobool(os.environ.get('USER_AUTH_ARMS', 'True'))
        if USER_AUTH_ARMS:
            headers.update(self._set_user_agent())
            headers.update(self._get_auth_header(self.credential))
            try:
                res = self.request(
                    'GET',
                    '{}{}'.format(self.BASE_URL, "/users/me"),
                    data=data,
                    json=json,
                    headers=headers,
                    **kwargs
                )
            except RequestsHTTPError as e:
                http_error_handler(e)

        # OpsBeeLLM API へのリクエスト
        headers = {}
        headers.update(self._set_user_agent())
        headers.update(self._get_auth_header(self.opsbee_credential))
        try:
            res = self.request(
                method,
                '{}{}'.format(self.OPSBEELLM_BASE_URL, path),
                data=data,
                json=json,
                headers=headers,
                params=params,
                **kwargs
            )
            return res.json()
        except RequestsHTTPError as e:
            http_error_handler(e)

    def service_request(
            self,
            subdomain: str,
            path: str,
            data: Union[None, Text, bytes, IO]=None,
            json: Optional[Any]=None,
            headers: Optional[MutableMapping[Text, Text]]=None,
            params: Union[None, bytes, MutableMapping[Text, Text]]=None,
            **kwargs):
        """call service api and handle errors if needed

        :param subdomain:
        :param path:
        :param data:
        :param json:
        :param headers:
        :param params:
        :param kwargs:
        :return: (requests.Response)
        """
        if headers is None:
            headers = {}
        headers.update(self._set_user_agent())
        headers.update(self._get_auth_header())

        base = urlparse(self.BASE_URL)
        target_url = '{}://{}.{}{}'.format(base.scheme,
                                           subdomain, base.netloc, path)
        try:
            return self.request(
                method='POST',
                url=target_url,
                data=data,
                json=json,
                headers=headers,
                params=params,
                **kwargs)
        except RequestsHTTPError as e:
            http_error_handler(e)

    def request(
            self,
            method,
            url,
            data=None,
            json=None,
            headers=None,
            params=None,
            timeout=None,
            **kwargs):
        """make request with retry and timeout settings.

        :param method:
        :param url:
        :param data:
        :param json:
        :param headers:
        :param params:
        :param timeout:
        :param kwargs:
        :return: (Response)
        """
        if timeout is None:
            timeout = self.timeout
        with self._generate_session() as session:
            res = session.request(
                method,
                url,
                data=data,
                json=json,
                params=params,
                headers=headers,
                timeout=timeout,
                **kwargs)
            res.raise_for_status()
        return res

    def _generate_session(self):
        """generate simple session to retry
        :return: session
        """
        session = Session()
        try:
            retries = Retry(
                total=self.max_retry_count, backoff_factor=1, allowed_methods=(
                    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'), status_forcelist=(
                    500, 502, 503, 504), raise_on_status=False)
        except TypeError:
            retries = Retry(
                total=self.max_retry_count, backoff_factor=1, method_whitelist=(
                    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'), status_forcelist=(
                    500, 502, 503, 504), raise_on_status=False)

        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def _get_auth_header(self, credential):
        if credential.get('auth_token'):
            return {
                'Authorization': 'Bearer {}'.format(
                    credential['auth_token'])}
        if credential.get('user_id') and credential.get(
                'personal_access_token'):
            user_id = credential['user_id']
            personal_access_token = credential['personal_access_token']
            base = '{}:{}'.format(user_id, personal_access_token)
            encoded = base64.b64encode(base.encode('utf-8'))
            return {
                'Authorization': 'Basic {}'.format(encoded.decode('utf-8'))
            }
        return {}

    def _set_user_agent(self):
        return {'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}


STATUS_CODE_EXCEPTION_CLASS_MAP = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    409: Conflict,
    500: InternalServerError
}


def http_error_handler(e):
    status_code = e.response.status_code
    url = e.response.url
    general_error_name = http.client.responses.get(status_code, 'unknown')
    general_error_description = e.response.text
    cls = STATUS_CODE_EXCEPTION_CLASS_MAP.get(
        e.response.status_code, HttpError)
    try:
        res = e.response.json()
    except json.JSONDecodeError:
        raise cls(
            general_error_name,
            general_error_description,
            status_code=status_code,
            url=url)
    # retrieve messages from response
    error = res.get('error', general_error_name)
    error_description = res.get('error_description', general_error_description)
    error_detail = res.get('error_detail')
    raise cls(
        error,
        error_description,
        error_detail=error_detail,
        status_code=status_code,
        url=url)
