def get_socks_inbounds(port: int, sniffing: bool = True, enable_udp: bool = True, **kwargs) -> dict:
    return {
        "port": port,
        "protocol": "socks",
        "sniffing": {
            "enabled": sniffing,
            "destOverride": ["http", "tls"]
        },
        "settings": {
            "auth": "noauth",
            "udp": enable_udp,
            **kwargs,
        }
    }


def get_http_inbounds(port: int, sniffing: bool = True, timeout: int = 300, **kwargs) -> dict:
    return {
        "port": port,
        "protocol": "http",
        "sniffing": {
            "enabled": sniffing,
            "destOverride": ["http", "tls"]
        },
        "settings": {
            "timeout": timeout,
            **kwargs
        }
    }
