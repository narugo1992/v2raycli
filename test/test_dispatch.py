import json
import os.path

import pytest

from v2raycli.dispatch import get_full_config, put_config_to_tempfile


@pytest.mark.unittest
class TestDispatch:
    def test_get_full_config_socks(self, site_1, site_3):
        assert get_full_config(site_1, 17890, protocol='socks', auth=[('sampleuser', 'p@ssword')]) == {
            'routing': {
                'domainStrategy': 'IPOnDemand',
                'rules': [
                    {'type': 'field', 'outboundTag': 'direct', 'ip': ['geoip:private']}
                ]
            },
            'inbounds': [
                {
                    'port': 17890,
                    'protocol': 'socks',
                    'sniffing': {
                        'enabled': True,
                        'destOverride': ['http', 'tls']
                    },
                    'settings': {
                        'auth': 'password',
                        'accounts': [{'user': 'sampleuser', 'pass': 'p@ssword'}],
                        'udp': True,
                        'ip': '127.0.0.1',
                        'userLevel': 0
                    }
                }
            ],
            'outbounds': [
                {
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
                            }
                        ]
                    },
                    'tag': 'proxy'
                },
                {
                    'protocol': 'freedom',
                    'settings': {},
                    'tag': 'direct',
                }
            ]
        }
        assert get_full_config(site_3, 17890, protocol='socks', user_level=8) == {
            'routing': {
                'domainStrategy': 'IPOnDemand',
                'rules': [
                    {'type': 'field', 'outboundTag': 'direct', 'ip': ['geoip:private']}
                ]
            },
            'inbounds': [
                {
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
                        'userLevel': 8,
                    }
                }
            ],
            'outbounds': [
                {
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
                    },
                    'mux': {
                        'enabled': False
                    }
                },
                {
                    'protocol': 'freedom',
                    'settings': {},
                    'tag': 'direct',
                }
            ]
        }

    def test_get_full_config_http(self, site_3):
        assert get_full_config(site_3, 17890, protocol='http', user_level=8) == {
            'routing': {
                'domainStrategy': 'IPOnDemand',
                'rules': [
                    {'type': 'field', 'outboundTag': 'direct', 'ip': ['geoip:private']}
                ]
            },
            'inbounds': [
                {
                    'port': 17890,
                    'protocol': 'http',
                    'sniffing': {
                        'enabled': True,
                        'destOverride': ['http', 'tls']
                    },
                    'settings': {
                        'accounts': None,
                        'timeout': 300,
                        'userLevel': 8
                    },
                }
            ],
            'outbounds': [
                {
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
                    },
                    'mux': {
                        'enabled': False
                    }
                },
                {
                    'protocol': 'freedom',
                    'settings': {},
                    'tag': 'direct',
                }
            ]
        }

    def test_get_full_config_error(self, site_3):
        with pytest.raises(ValueError):
            _ = get_full_config(site_3, 17890, protocol='httpxxxx', user_level=8)

    def test_put_config_to_tempfile(self, site_3):
        with put_config_to_tempfile(site_3, 17890, protocol='socks', user_level=8) as tconfig:
            assert os.path.exists(tconfig)
            assert os.path.isfile(tconfig)
            with open(tconfig, 'r') as f:
                assert json.load(f) == {
                    'routing': {
                        'domainStrategy': 'IPOnDemand',
                        'rules': [
                            {'type': 'field', 'outboundTag': 'direct', 'ip': ['geoip:private']}
                        ]
                    },
                    'inbounds': [
                        {
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
                                'userLevel': 8,
                            }
                        }
                    ],
                    'outbounds': [
                        {
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
                            },
                            'mux': {
                                'enabled': False
                            }
                        },
                        {
                            'protocol': 'freedom',
                            'settings': {},
                            'tag': 'direct',
                        }
                    ]
                }
