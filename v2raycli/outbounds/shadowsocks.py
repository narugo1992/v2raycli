import base64
from urllib import parse as urlparse

from .base import NamedServer


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

        raw_netloc = splitted.netloc
        raw_netloc = raw_netloc + '=' * (4 - len(raw_netloc) % 4)
        netloc = base64.b64decode(raw_netloc).decode()

        loc_splitted = urlparse.urlsplit(f'{splitted.scheme}://{netloc}')
        method = loc_splitted.username
        password = loc_splitted.password
        address = loc_splitted.hostname
        port = int(loc_splitted.port)

        return ShadowsocksServer(name, method, password, address, port)
