import base64
from typing import List
from typing import Mapping, Type
from urllib import parse as urlparse

import requests

from .outbounds import ShadowsocksServer, VMessServer, NamedServer

_UNKNOWN_PROTOCOLS: Mapping[str, Type[NamedServer]] = {
    'ss': ShadowsocksServer,
    'vmess': VMessServer,
}


def parse_subscription(raw_url: str) -> NamedServer:
    splitted = urlparse.urlsplit(raw_url)
    if splitted.scheme in _UNKNOWN_PROTOCOLS:
        return _UNKNOWN_PROTOCOLS[splitted.scheme].parse(raw_url)
    else:
        raise ValueError(f'Unknown scheme {splitted.scheme!r} - {raw_url!r}.')


def _get_content_from_subscription(url: str) -> List[str]:
    response = requests.get(url)
    subscription_text = base64.b64decode(response.content).decode()
    return subscription_text.splitlines(keepends=False)


def list_from_subscription(url: str) -> List[NamedServer]:
    return [
        parse_subscription(raw_url)
        for raw_url in _get_content_from_subscription(url)
    ]
