import base64
from typing import Union


def base64_decode(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str):
        data = data + '=' * (4 - len(data) % 4)
    else:
        data = data + b'=' * (4 - len(data) % 4)
    return base64.b64decode(data)
