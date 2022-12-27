import pytest

from v2raycli.outbounds import ShadowsocksServer


@pytest.mark.unittest
class TestOutboundsShadowsocks:
    def test_parse_1(self, subline_1):
        ss = ShadowsocksServer.parse(subline_1)
        assert isinstance(ss, ShadowsocksServer)
        assert ss.name == 'JMS-267288@c21s1.jamjams3.net:22890'
        assert ss.address == '176.122.175.196'
        assert ss.port == 22890
        assert ss.method == 'aes-256-gcm'

        assert repr(ss) == '<ShadowsocksServer JMS-267288@c21s1.jamjams3.net:22890, ' \
                           'method: aes-256-gcm, address: 176.122.175.196:22890>'
        assert ss.outbound('proxy') == {
            'protocol': 'shadowsocks',
            'settings': {
                'servers': [
                    {
                        'address': '176.122.175.196',
                        'port': 22890,
                        'method': 'aes-256-gcm',
                        'password': '5D6gtC8hH3',
                        'ota': False,
                        'level': 0
                    },
                ],
            },
            'tag': 'proxy',
        }

    def test_parse_2(self, subline_2):
        ss = ShadowsocksServer.parse(subline_2)
        assert isinstance(ss, ShadowsocksServer)
        assert ss.name == 'JMS-267288@c21s2.jamjams3.net:22890'
        assert ss.address == '176.122.177.36'
        assert ss.port == 22890
        assert ss.method == 'aes-256-gcm'

        assert repr(ss) == '<ShadowsocksServer JMS-267288@c21s2.jamjams3.net:22890, ' \
                           'method: aes-256-gcm, address: 176.122.177.36:22890>'
        assert ss.outbound('proxy') == {
            'protocol': 'shadowsocks',
            'settings': {
                'servers': [
                    {
                        'address': '176.122.177.36',
                        'port': 22890,
                        'method': 'aes-256-gcm',
                        'password': '5D6gtC8hH3',
                        'ota': False,
                        'level': 0
                    },
                ],
            },
            'tag': 'proxy',
        }

    def test_parse_error(self, subline_3):
        with pytest.raises(AssertionError):
            _ = ShadowsocksServer.parse(subline_3)
