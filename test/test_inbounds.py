import pytest

from v2raycli.inbounds import get_socks_inbounds, get_http_inbounds


@pytest.mark.unittest
class TestInbounds:
    def test_get_socks_inbounds(self):
        assert get_socks_inbounds(17890, sniffing=True, enable_udp=True, auth=None) == {
            'port': 17890,
            'protocol': 'socks',
            'sniffing': {
                'enabled': True,
                'destOverride': ['http', 'tls']
            },
            'settings': {
                'auth': 'noauth',
                'accounts': None,
                'udp': True,
                'ip': '127.0.0.1',
                'userLevel': 0
            }
        }
        assert get_socks_inbounds(17890, sniffing=False, enable_udp=False,
                                  auth=[('sampleuser', 'p@ssword')], user_level=8) == {
                   'port': 17890,
                   'protocol': 'socks',
                   'sniffing': {
                       'enabled': False,
                       'destOverride': ['http', 'tls']
                   },
                   'settings': {
                       'auth': 'password',
                       'accounts': [
                           {
                               'user': 'sampleuser',
                               'pass': 'p@ssword',
                           }
                       ],
                       'udp': False,
                       'ip': '127.0.0.1',
                       'userLevel': 8,
                   }
               }

    def test_get_http_inbounds(self):
        assert get_http_inbounds(17890, sniffing=True, auth=None) == {
            'port': 17890,
            'protocol': 'http',
            'sniffing': {
                'enabled': True,
                'destOverride': ['http', 'tls']
            },
            'settings': {
                'accounts': None,
                'timeout': 300,
                'userLevel': 0,
            },
        }
        assert get_http_inbounds(17890, sniffing=True, timeout=301,
                                 auth=[('sampleuser', 'p@ssword')], user_level=8) == {
                   'port': 17890,
                   'protocol': 'http',
                   'sniffing': {
                       'enabled': True,
                       'destOverride': ['http', 'tls']
                   },
                   'settings': {
                       'accounts': [
                           {
                               'user': 'sampleuser',
                               'pass': 'p@ssword',
                           }
                       ],
                       'timeout': 301,
                       'userLevel': 8,
                   },
               }
