import shlex
import subprocess
import sys
from typing import List, Union


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
