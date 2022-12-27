from typing import Optional, Tuple, List


def get_socks_inbounds(port: int, sniffing: bool = True, enable_udp: bool = True,
                       auth: Optional[List[Tuple[str, str]]] = None, local_ip: str = "127.0.0.1",
                       user_level: int = 0, **kwargs) -> dict:
    enable_auth = "password" if auth else "noauth"
    accounts = [{"user": user, "pass": passwd} for user, passwd in auth] if auth else None
    return {
        "port": port,
        "protocol": "socks",
        "sniffing": {
            "enabled": sniffing,
            "destOverride": ["http", "tls"]
        },
        "settings": {
            "auth": enable_auth,
            "accounts": accounts,
            "udp": enable_udp,
            "ip": local_ip,
            "userLevel": user_level,
            **kwargs,
        }
    }


def get_http_inbounds(port: int, sniffing: bool = True, timeout: int = 300,
                      auth: Optional[List[Tuple[str, str]]] = None, user_level: int = 0, **kwargs) -> dict:
    accounts = [{"user": user, "pass": passwd} for user, passwd in auth] if auth else None
    return {
        "port": port,
        "protocol": "http",
        "sniffing": {
            "enabled": sniffing,
            "destOverride": ["http", "tls"]
        },
        "settings": {
            "timeout": timeout,
            "accounts": accounts,
            "userLevel": user_level,
            **kwargs
        }
    }
