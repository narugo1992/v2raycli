from urllib import parse as urlparse

from .base import NamedServer
from ..utils import base64_decode


class ShadowsocksServer(NamedServer):
    __protocol__ = 'shadowsocks'

    def __init__(self, name: str, method: str, password: str, address: str, port: int):
        NamedServer.__init__(self, name, address, port)
        self.method = method
        self.password = password

    def __repr__(self):
        return f'<{type(self).__name__} {self.name}, method: {self.method}, address: {self.address}:{self.port}>'

    def outbound(self, tag: str = 'proxy', ota: bool = False, level: int = 0) -> dict:
        return {
            "protocol": "shadowsocks",
            "settings": {
                "servers": [
                    {
                        "address": self.address,
                        "port": self.port,
                        "method": self.method,
                        "password": self.password,
                        "ota": ota,
                        "level": level,
                    }
                ]
            },
            "tag": tag,
        }

    @classmethod
    def parse(cls, raw_url: str) -> 'ShadowsocksServer':
        splitted = urlparse.urlsplit(raw_url)
        assert splitted.scheme == 'ss'
        name = splitted.fragment
        netloc = base64_decode(splitted.netloc).decode()

        loc_splitted = urlparse.urlsplit(f'{splitted.scheme}://{netloc}')
        method = loc_splitted.username
        password = loc_splitted.password
        address = loc_splitted.hostname
        port = int(loc_splitted.port)

        return ShadowsocksServer(name, method, password, address, port)
