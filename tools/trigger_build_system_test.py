import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import os
import re
token = os.environ.get('CIRCLE_CI_TOKEN')
base_url = "https://circleci.com/api/v1.1/project/gh/abeja-inc/platform-system-test"


def get_request_session():
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[ 500, 502, 503, 504 ])

    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s

def get_latest_build_num_for_stage(stage):
    limit = 1000
    branch_name = f'deployment/{stage}'
    session = get_request_session()
    for i in range(100):
        offset = limit * i
        params = {
            'circle-token': token,
            'limit': limit,
            'offset': offset,
            'filter': 'completed',
            'sharrow': True
        }
        r = session.get(base_url, params=params)
        r.raise_for_status()
        builds = [_ for _ in r.json() if _['branch'] == branch_name]
        if len(builds) > 0:
            build_num = builds[0]['build_num']
            return build_num
    return None

def get_latest_build_num():
    sdk_branch_name = os.environ.get('CIRCLE_BRANCH')
    if re.match(r'^release\/.+$', sdk_branch_name):
        stage = 'staging'
    elif sdk_branch_name == 'master':
        stage = 'production'
    else:
        return None

    return get_latest_build_num_for_stage(stage)

def trigger_build(build_num):
    url = f"{base_url}/{build_num}/retry"
    params = {
        'circle-token': token,
    }
    session = get_request_session()
    r = session.post(url, params=params)
    r.raise_for_status()

def main():
    build_num = get_latest_build_num()
    if build_num is None:
        exit(1)
    trigger_build(build_num)

if __name__ == '__main__':
    main()