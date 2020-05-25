import sys
from typing import Optional


def print_feature_deprecation(
        target: Optional[str] = None,
        additional_message: Optional[str] = None):
    if target is None:
        target = 'This feature'
    else:
        target = '`{}`'.format(target)

    message = '{} has been officially deprecated. ' \
        '{} continues to be available for a while, ' \
        'but it is already scheduled for shutdown.'.format(target, target)
    if additional_message is not None:
        message += ' ' + additional_message

    print(message, file=sys.stderr)     # noqa: T001


def print_feature_new(
        target: Optional[str] = None,
        additional_message: Optional[str] = None):
    if target is None:
        target = 'This feature'
    else:
        target = '`{}`'.format(target)

    message = '{} is a new feature and is an alpha release.'.format(target)
    if additional_message is not None:
        message += ' ' + additional_message

    print(message, file=sys.stderr)     # noqa: T001


def get_filter_archived_applied_params(
        _params: dict,
        filter_archived: Optional[bool]) -> dict:
    params = _params.copy()
    if filter_archived is None:
        return params
    params["filter_archived"] = 'exclude_archived' if filter_archived else 'include_archived'
    return params
