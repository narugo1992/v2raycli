from .base import BaseServer


class FreedomServer(BaseServer):
    def __repr__(self):
        return f'<{type(self).__name__}>'

    def outbound(self, tag: str = 'direct', ota: bool = False, level: int = 0) -> dict:
        return {
            "protocol": "freedom",
            "settings": {},
            "tag": "direct",
        }

    @classmethod
    def parse(cls, raw_url: str) -> 'BaseServer':
        return FreedomServer()
