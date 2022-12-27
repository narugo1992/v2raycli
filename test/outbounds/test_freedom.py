import pytest

from v2raycli.outbounds import FreedomServer


@pytest.fixture()
def fss():
    return FreedomServer()


@pytest.mark.unittest
class TestOutboundsFreedom:
    def test_simple(self, fss):
        assert isinstance(FreedomServer.parse('xxx'), FreedomServer)
        assert repr(fss) == '<FreedomServer>'
        assert fss.outbound('proxy') == {'protocol': 'freedom', 'settings': {}, 'tag': 'direct'}
