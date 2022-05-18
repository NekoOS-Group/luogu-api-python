__all__ = [
    'post',
    'verify_params'
]

import requests
import json
from . import ultility


def post(url: str, params=None, proxy=None):
    """
    Wrapper of requests.post()

    Args:
        url: the distinction to post
        params: request params
        proxy: proxies

    Returns:
        the dict that server return

    Raises:
        Exception: 404 not found
    """
    try:
        r = requests.post(url, params=params, proxies=proxy)
    except Exception:
        raise Exception("Network Error")

    if r.status_code != 200:
        raise Exception("404 not found")

    return json.loads(r.content)


def verify_params(params_table, params):
    """Verify the type of params to be posted

    Args:
        params_table:
        params:

    Returns:
        True if passed this verification

    Raises:
        Exception1: Invalid param
        Exception2: Invalid type
    """
    for arg_name, arg_val in params.items():
        if params_table[arg_name] is None:
            raise Exception(f"Invalid param : '{arg_name}'")
        arg_type = ultility.make_list(params_table[arg_name])
        if ultility.exist(arg_type, lambda _: isinstance(arg_val, _)):
            continue
        raise Exception(f"For param '{arg_name}', {str(params_table[arg_name])} need, but {str(type(arg_val))} given")

    return True
