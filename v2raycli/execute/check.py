import logging
from typing import Callable, Optional, Tuple

import click
import requests
from requests import RequestException
from requests.adapters import HTTPAdapter

DEFAULT_TARGET_SITE = 'https://pixiv.net'


def proxy_check(proxy: str, target_site: str = DEFAULT_TARGET_SITE,
                timeout: float = 5.0, max_retries: int = 3) -> Tuple[bool, Optional[Exception]]:
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=max_retries))
    session.mount('https://', HTTPAdapter(max_retries=max_retries))
    try:
        response = session.get(
            target_site, timeout=timeout,
            proxies={'all': proxy}
        )
        response.raise_for_status()
    except (RequestException, IOError) as err:
        return False, err
    else:
        return True, None


def get_proxy_check_daemon_func(proxy: str, target_site: str = DEFAULT_TARGET_SITE,
                                timeout: float = 5.0, max_retries: int = 3) \
        -> Callable[[], bool]:
    def _check_func():
        success, err = proxy_check(proxy, target_site, timeout, max_retries)
        if success:
            logging.info(click.style(f'Proxy works fine.', fg='blue'))
            return True
        else:
            logging.error(
                click.style(f'Connect to {target_site!r} with proxy failed, here is the error:\n{err!r}', fg='red'))
            return False

    return _check_func
