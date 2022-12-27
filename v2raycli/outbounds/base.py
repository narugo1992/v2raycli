class BaseServer:
    def outbound(self, tag: str = 'proxy', ota: bool = False, level: int = 0) -> dict:
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def parse(cls, raw_url: str) -> 'BaseServer':
        raise NotImplementedError  # pragma: no cover


# noinspection PyAbstractClass
class NamedServer(BaseServer):
    __protocol__ = '<not given>'

    def __init__(self, name: str, address: str, port: int):
        self.__name = name
        self.__address = address
        self.__port = port

    @property
    def name(self) -> str:
        return self.__name

    @property
    def address(self) -> str:
        return self.__address

    @property
    def port(self) -> int:
        return self.__port
