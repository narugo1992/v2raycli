import pytest
import responses
from hbutils.testing import simulate_entry

from v2raycli.entry import v2raycli
from ..testings import EXAMPLE_SUBSCRIPTION_URL


@pytest.mark.unittest
class TestEntryList:
    @responses.activate
    def test_list(self, env_v2ray_subscription):
        result = simulate_entry(v2raycli, ['v2raycli', 'list'])
        assert result.exitcode == 0
        assert EXAMPLE_SUBSCRIPTION_URL in result.stdout

        assert 'JMS-267288@c21s1.jamjams3.net:22890' in result.stdout
        assert '176.122.175.196:22890' in result.stdout

        assert 'JMS-267288@c21s3.jamjams3.net:22890' in result.stdout
        assert '216.24.185.154:22890' in result.stdout

        assert 'JMS-267288@c21s801.jamjams3.net:22890' in result.stdout
        assert '174.137.58.128:22890' in result.stdout
