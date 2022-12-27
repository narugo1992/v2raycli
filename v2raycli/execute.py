import os
import re
import shlex
import shutil
import subprocess
import sys
from typing import Optional, Tuple, List, Union


def _repr_command(command: Union[List[str], str]) -> str:
    return ' '.join(map(shlex.quote, command))


def subprocess_run_in_terminal(cmd: List[str]):
    print(f'Running {_repr_command(cmd)} ...', file=sys.stdout)
    try:
        process = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    except KeyboardInterrupt:
        print(f'Process {_repr_command(cmd)} interrupted.', file=sys.stderr)
    else:
        if process.returncode:
            print(f'Process {_repr_command(cmd)} quit with exitcode {process.returncode!r}.', file=sys.stderr)
        else:
            print(f'Process {_repr_command(cmd)} quit.', file=sys.stdout)


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
