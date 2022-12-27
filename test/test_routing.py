import pytest

from v2raycli.routing import get_generic_routing


@pytest.mark.unittest
class TestRouting:
    def test_get_generic_routing(self):
        assert get_generic_routing() == {
            'domainStrategy': 'IPOnDemand',
            'rules': [
                {'type': 'field', 'outboundTag': 'direct', 'ip': ['geoip:private']}
            ]
        }
        assert get_generic_routing(no_proxy_on_private=False) == {
            'domainStrategy': 'IPOnDemand',
            'rules': []
        }
        assert get_generic_routing(no_proxy_on_cn=True, direct_tag='custom_direct_tag') == {
            'domainStrategy': 'IPOnDemand',
            'rules': [
                {'type': 'field', 'outboundTag': 'custom_direct_tag', 'ip': ['geoip:private']},
                {'type': 'field', 'outboundTag': 'custom_direct_tag', 'domain': ['geosite:cn']},
                {'type': 'field', 'outboundTag': 'custom_direct_tag', 'ip': ['geoip:cn']},
            ]
        }
