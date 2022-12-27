import sys

import pytest
from hbutils.testing import capture_output

from v2raycli.execute import subprocess_run_in_terminal


@pytest.mark.unittest
class TestExecute:
    def test_subprocess_run_in_terminal(self):
        with capture_output() as co:
            subprocess_run_in_terminal([sys.executable, '-c', 'print(1 + 2)'])

        assert '3' in co.stdout.splitlines(keepends=False)
        assert not co.stderr.strip()

        with capture_output() as co:
            subprocess_run_in_terminal([sys.executable, '-c', 'raise KeyError'])

        assert 'KeyError' in co.stderr.strip()
