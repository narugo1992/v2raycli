import pytest
from hbutils.testing import simulate_entry

from v2raycli.config.meta import __VERSION__
from v2raycli.entry import v2raycli


@pytest.mark.unittest
class TestEntryDispatch:
    def test_version(self):
        result = simulate_entry(v2raycli, ['v2raycli', '-v'])
        assert result.exitcode == 0
        assert __VERSION__ in result.stdout
