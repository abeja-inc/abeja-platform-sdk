import os


def get_token_from_environment():
    """get abeja platform jwt token from environment variables

    :return: dict
    {
        "auth_token": PLATFORM_AUTH_TOKEN
    }
    """
    auth_token = os.environ.get('PLATFORM_AUTH_TOKEN')
    if not auth_token:
        return None
    return {
        "auth_token": auth_token
    }


def get_basic_auth_from_environment():
    """get abeja platform basic auth id and pass from environment variables
    basic auth id : user_id
    basic auth pass : personal access token of the user

    :return: dict
    {
        "user_id": ABEJA_PLATFORM_USER_ID,
        "personal_access_token": ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN
    }
    """
    user_id = os.environ.get('ABEJA_PLATFORM_USER_ID')
    personal_access_token = os.environ.get('ABEJA_PLATFORM_PERSONAL_ACCESS_TOKEN')
    if not user_id or not personal_access_token:
        return None
    return {
        "user_id": user_id,
        "personal_access_token": personal_access_token
    }


def get_credential():
    """get credential in the following priority
    1. jwt token in environment
    2. basic auth in environment

    :return: dict
    """
    credential = get_token_from_environment() or get_basic_auth_from_environment()
    return credential
