import os
import re
import shutil
import subprocess
from typing import Optional, Tuple, List

from .check import get_proxy_check_daemon_func, DEFAULT_TARGET_SITE
from .run import subprocess_run_in_terminal, subprocess_run_in_terminal_with_daemon

V2RAY_BIN_ENV = 'V2RAY_BIN'


def get_v2ray_from_env() -> Optional[str]:
    if V2RAY_BIN_ENV in os.environ:
        return os.environ[V2RAY_BIN_ENV]
    else:
        return shutil.which('v2ray')


class V2RayBin:
    def __init__(self, exec_: str, version: Tuple[int, ...]):
        self.__executable = exec_
        self.__version = version

    @property
    def executable(self) -> str:
        return self.__executable

    @property
    def version(self) -> Tuple[int, ...]:
        return self.__version

    def _run_command(self, config_file: str) -> List[str]:
        raise NotImplementedError

    def run(self, config_file: str):
        subprocess_run_in_terminal(self._run_command(config_file))

    def run_with_daemon(self, config_file: str, proxy_address: Optional[str],
                        target_site: str = DEFAULT_TARGET_SITE, timeout: float = 5.0, max_retries: int = 3,
                        first_interval: float = 15.0, check_interval=120.0, cycle_interval: float = 0.2):
        if not proxy_address:
            return self.run(config_file)

        subprocess_run_in_terminal_with_daemon(
            self._run_command(config_file),
            get_proxy_check_daemon_func(proxy_address, target_site, timeout, max_retries),
            check_interval, first_interval, cycle_interval,
        )

    def __repr__(self):
        return f'<{type(self).__name__} {".".join(map(str, self.__version))}, exec: {self.__executable!r}>'


class V2Ray4Bin(V2RayBin):
    def _run_command(self, config_file: str) -> List[str]:
        return [self.executable, '-config', config_file]


class V2Ray5Bin(V2RayBin):
    def _run_command(self, config_file: str) -> List[str]:
        return [self.executable, 'run', '-c', config_file]


_VERSION_PATTERN = re.compile(r'^V2Ray\s+(?P<version>[0-9.]+)')


def load_v2ray_bin(v2ray_bin: Optional[str] = None) -> V2RayBin:
    v2ray_bin = v2ray_bin or get_v2ray_from_env()
    if not os.path.exists(v2ray_bin):
        raise FileNotFoundError(v2ray_bin)
    v2ray_bin = os.path.abspath(v2ray_bin)

    process = subprocess.run([v2ray_bin, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        process = subprocess.run([v2ray_bin, 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process.check_returncode()
    stdout_text = process.stdout.decode()
    findings = _VERSION_PATTERN.findall(stdout_text)
    if not findings:
        raise AssertionError('Version information not found.')

    version_text = findings[0]
    version: Tuple[int, ...] = tuple(map(int, version_text.split('.')))
    if version >= (5,):
        return V2Ray5Bin(v2ray_bin, version)
    else:
        return V2Ray4Bin(v2ray_bin, version)
