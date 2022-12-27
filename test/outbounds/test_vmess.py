import pytest

from v2raycli.outbounds import VMessServer


@pytest.mark.unittest
class TestOutboundsVmess:
    def test_parse_3(self, subline_3):
        ss = VMessServer.parse(subline_3)
        assert isinstance(ss, VMessServer)
        assert ss.name == 'JMS-267288@c21s3.jamjams3.net:22890'
        assert ss.id_ == '5428c123-4736-429f-853b-36c741a4ba35'
        assert ss.address == '216.24.185.154'
        assert ss.port == 22890
        assert ss.aid == 0
        with pytest.raises(AttributeError):
            _ = ss.not_found_attr

        assert repr(ss) == '<VMessServer JMS-267288@c21s3.jamjams3.net:22890, address: 216.24.185.154:22890>'
        assert ss.outbound('proxy') == {
            'protocol': 'vmess',
            'settings': {
                'vnext': [
                    {
                        'address': '216.24.185.154',
                        'port': 22890,
                        'users': [
                            {
                                'alterId': 0,
                                'id': '5428c123-4736-429f-853b-36c741a4ba35',
                                'level': 0,
                                'security': 'auto'
                            }
                        ]
                    }
                ]
            },
            'tag': 'proxy',
            'streamSettings': {
                'network': 'tcp',
                'security': 'none',
                'tlssettings': {},
                'wssettings': {}
            }, 'mux': {
                'enabled': False
            }
        }

    def test_parse_6(self, subline_6):
        ss = VMessServer.parse(subline_6)
        assert isinstance(ss, VMessServer)
        assert ss.name == 'JMS-267288@c21s801.jamjams3.net:22890'
        assert ss.id_ == '5428c123-4736-429f-853b-36c741a4ba35'
        assert ss.address == '174.137.58.128'
        assert ss.port == 22890
        assert ss.aid == 0
        with pytest.raises(AttributeError):
            _ = ss.not_found_attr

        assert repr(ss) == '<VMessServer JMS-267288@c21s801.jamjams3.net:22890, address: 174.137.58.128:22890>'
        assert ss.outbound('proxy') == {
            'protocol': 'vmess',
            'settings': {
                'vnext': [
                    {
                        'address': '174.137.58.128',
                        'port': 22890,
                        'users': [
                            {
                                'alterId': 0,
                                'id': '5428c123-4736-429f-853b-36c741a4ba35',
                                'level': 0,
                                'security': 'auto'
                            }
                        ]
                    }
                ]
            },
            'tag': 'proxy',
            'streamSettings': {
                'network': 'tcp',
                'security': 'none',
                'tlssettings': {},
                'wssettings': {}
            }, 'mux': {
                'enabled': False
            }
        }

    def test_parse_error(self, subline_1):
        with pytest.raises(AssertionError):
            _ = VMessServer.parse(subline_1)
