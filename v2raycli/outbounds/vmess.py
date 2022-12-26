import json
from urllib import parse as urlparse

from .base import NamedServer
from ..utils import base64_decode


class VMessServer(NamedServer):
    __protocol__ = 'vmess'

    def __init__(self, config: dict):
        NamedServer.__init__(self, config['ps'], config['add'], int(config['port']))
        self.__config = config

    @property
    def id_(self) -> str:
        return self.__config['id']

    def __getattr__(self, item):
        if item in self.__config:
            return self.__config[item]
        else:
            raise AttributeError(f'Attribute {item!r} not found.')

    def __repr__(self):
        return f'<{type(self).__name__} {self.name}, address: {self.address}:{self.port}>'

    def outbound(self, tag: str = 'proxy', ota: bool = False, level: int = 0) -> dict:
        return {
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": self.address,
                        "port": self.port,
                        "users": [
                            {
                                "alterId": self.__config['aid'],
                                "id": self.__config['id'],
                                "level": level,
                                "security": "auto",
                            }
                        ]
                    }
                ]
            },
            "tag": tag,
            "streamSettings": {
                "network": self.__config['net'],
                "security": self.__config['tls'],
                "tlssettings": {
                    "allowInsecure": True,
                    "serverName": self.__config['host'],
                } if self.__config['tls'] == 'tls' else {},
                "wssettings": {
                    "connectionReuse": True,
                    "headers": {
                        'Host': self.__config['host'],
                    },
                    'path': self.__config['path'].replace('\\', ''),
                } if self.__config['net'] == 'ws' else {},
            },
            "mux": {
                "enabled": False,
            }
        }

    @classmethod
    def parse(cls, raw_url: str) -> 'VMessServer':
        splitted = urlparse.urlsplit(raw_url)
        assert splitted.scheme == 'vmess'

        raw_config = base64_decode(splitted.netloc).decode()
        config = json.loads(raw_config)

        return VMessServer(config)
