import pytest
import responses

from v2raycli.outbounds import ShadowsocksServer
from v2raycli.subscription import list_from_subscription, parse_subscription
from .testings import EXAMPLE_SUBSCRIPTION_URL


@pytest.mark.unittest
class TestSubscription:
    def test_parse_subscription(self, subline_1):
        s1 = parse_subscription(subline_1)
        assert isinstance(s1, ShadowsocksServer)
        assert s1.name == 'JMS-267288@c21s1.jamjams3.net:22890'
        assert s1.address == '176.122.175.196'
        assert s1.port == 22890
        assert s1.method == 'aes-256-gcm'

    def test_parse_subscription_with_error(self):
        with pytest.raises(ValueError):
            _ = parse_subscription('ff://kjdsfkljsdlfjlds')

    @responses.activate
    def test_list_from_subscription(self):
        subscriptions = list_from_subscription(EXAMPLE_SUBSCRIPTION_URL)
        assert len(subscriptions) == 6
