import sys
import time

import pytest
from hbutils.testing import capture_output

from v2raycli.execute import subprocess_run_in_terminal, subprocess_run_in_terminal_with_daemon, DaemonInterrupt


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

    def test_subprocess_run_in_terminal_with_daemon_normal(self):
        with capture_output() as co:
            _last_time = time.time()

            def _check():
                nonlocal _last_time
                return time.time() - _last_time <= 5.0

            subprocess_run_in_terminal_with_daemon(
                [sys.executable, '-m', 'test.execute', '-c', '5'],
                daemon_check=_check, check_interval=1.0,
            )

        assert len(co.stdout.strip().splitlines(keepends=False)) == 5

    def test_subprocess_run_in_terminal_with_daemon_interrupt(self):
        with capture_output() as co:
            _last_time = time.time()

            def _check():
                nonlocal _last_time
                return time.time() - _last_time <= 3.0

            with pytest.raises(DaemonInterrupt):
                subprocess_run_in_terminal_with_daemon(
                    [sys.executable, '-m', 'test.execute', '-c', '20'],
                    daemon_check=_check, check_interval=1.0,
                )
