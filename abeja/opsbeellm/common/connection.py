import base64
import json
import os
import http
import time
import jwt
from typing import Optional, Union, Text, IO, MutableMapping, Any
from urllib.parse import urlparse

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
from abeja.opsbeellm.common.constants import OperationMode

SDK_CONNECTION_TIMEOUT_ENV_KEY = 'ABEJA_SDK_CONNECTION_TIMEOUT'
SDK_MAX_RETRY_COUNT_ENV_KEY = 'ABEJA_SDK_MAX_RETRY_COUNT'

DEFAULT_MAX_RETRY_COUNT = 5
DEFAULT_CONNECTION_TIMEOUT = 30


class OpsBeeLLMConnection:
    """A connection to ABEJA Platform OpsBeeLLM API."""
    ABEJA_API_URL = os.environ.get('ABEJA_API_URL', 'https://api.abeja.io')

    def __init__(
            self,
            credential=None,
            timeout: Optional[int] = None,
            max_retry_count: Optional[int] = None):
        self.timeout = timeout or os.environ.get(
            SDK_CONNECTION_TIMEOUT_ENV_KEY) or DEFAULT_CONNECTION_TIMEOUT
        self.max_retry_count = max_retry_count or os.environ.get(
            SDK_MAX_RETRY_COUNT_ENV_KEY) or DEFAULT_MAX_RETRY_COUNT

        if credential is None:
            self.credential = get_credential() or {}
        else:
            self.credential = credential
        # ユーザーIDとパーソナルアクセストークンでの Basic 認証の場合
        if 'user_id' in self.credential and not self.credential['user_id'].startswith(
                "user-"):
            self.credential['user_id'] = 'user-{}'.format(
                self.credential['user_id'])

        self.jwt_token = None
        # auth API を呼び出し、JWT トークンを取得
        # if OperationMode.is_edge(self._get_operation_mode()):
        #     self.jwt_token = self.auth_request()

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

        # ABEJA Platform OpsBeeLLM API の場合
        if self._get_operation_mode() == OperationMode.ABEJA.value:
            headers.update(self._set_user_agent())
            headers.update(self._get_auth_header())
            try:
                res = self.request(method,
                                   '{}{}'.format(self.ABEJA_API_URL, path),
                                   data=data,
                                   json=json,
                                   headers=headers,
                                   params=params,
                                   **kwargs)
                return res.json()
            except RequestsHTTPError as e:
                http_error_handler(e)
        # Customer OpsBeeLLM API の場合
        elif OperationMode.is_edge(self._get_operation_mode()):
            # JWT トークン未取得の場合は、再取得
            if not self.jwt_token:
                self.jwt_token = self.auth_request()

            # 有効期限切れの場合は、JWT トークン再取得
            try:
                if self.is_jwt_expired(self.jwt_token):
                    self.jwt_token = self.auth_request()
            except Exception as e:
                raise Exception(f'Failed to refresh JWT token! | {e}')

            # JWT トークンで OpsBeeLLM API へリクエスト
            headers.update(self._set_user_agent())
            headers.update({'Authorization': f'Bearer {self.jwt_token}'})
            try:
                res = self.request(
                    method,
                    '{}{}'.format(self.ABEJA_API_URL, path),
                    data=data,
                    json=json,
                    headers=headers,
                    params=params,
                    **kwargs
                )
                return res.json()
            except RequestsHTTPError as e:
                http_error_handler(e)
        else:
            raise ValueError(
                'Invalid OPERATION_MODE: {}'.format(self._get_operation_mode()))

    def auth_request(self):
        jwt_token = None
        try:
            auth_headers = {}
            auth_headers.update(self._set_user_agent())
            auth_headers.update(self._get_auth_header())
            auth_body = {
                'email': self.credential['email'],
                'password': self.credential['password']
            }
            res = self.request(
                'POST',
                f'{self.ABEJA_API_URL}/authnz/v1/token',
                json=auth_body,
                headers=auth_headers
            )
            jwt_token = res.json()["token"]
        except RequestsHTTPError as e:
            http_error_handler(e)

        return jwt_token

    def is_jwt_expired(self, token: str) -> bool:
        current_unix_time = int(time.time())
        payload = jwt.decode(token, options={"verify_signature": False})
        expiration = payload['exp']
        return expiration < current_unix_time

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

    def _get_auth_header(self):
        # JWT トークンの場合
        if self.credential.get('auth_token'):
            return {
                'Authorization': 'Bearer {}'.format(
                    self.credential['auth_token'])}

        # ユーザーIDとパーソナルアクセストークンでの Basic 認証の場合
        if self.credential.get('user_id') and self.credential.get(
                'personal_access_token'):
            user_id = self.credential['user_id']
            personal_access_token = self.credential['personal_access_token']
            base = '{}:{}'.format(user_id, personal_access_token)
            encoded = base64.b64encode(base.encode('utf-8'))
            return {
                'Authorization': 'Basic {}'.format(encoded.decode('utf-8'))
            }
        return {}

    def _set_user_agent(self):
        return {'User-Agent': 'abeja-platform-sdk/{}'.format(VERSION)}

    def _get_operation_mode(self):
        return os.environ.get('OPERATION_MODE', OperationMode.ABEJA.value)


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
