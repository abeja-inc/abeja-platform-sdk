import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import os
import re
import urllib.parse
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


def get_stage():
    sdk_branch_name = os.environ.get('CIRCLE_BRANCH')
    if re.match(r'^release\/.+$', sdk_branch_name):
        stage = 'staging'
    elif sdk_branch_name == 'master':
        stage = 'production'
    else:
        return None


def trigger_build_by_branch(stage):
    """https://circleci.com/docs/api/#trigger-a-new-job-with-a-branch
    """
    branch_name = 'deployment/{}'.format(stage)

    branch = urllib.parse.quote(branch_name, safe='')
    url = "{}/tree/{}".format(base_url, branch)
    params = {
        'circle-token': token,
    }
    session = get_request_session()
    r = session.post(url, params=params)
    r.raise_for_status()


def main():
    stage = get_stage()
    if stage is None:
        exit(1)
    trigger_build_by_branch(stage)

if __name__ == '__main__':
    main()