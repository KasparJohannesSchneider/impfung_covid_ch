__all__ = ['is_page_up']

import requests.exceptions
from requests import request


def is_page_up(url: str) -> bool:
    """Tests if a webpage is up (returns 200)

    :param url: url to be tested
    :return: True if url is reachable (returns 200)
    """
    try:
        return request('GET', url).status_code == 200
    except requests.exceptions.ConnectionError:
        return False
