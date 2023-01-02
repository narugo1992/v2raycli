import logging
import shlex
import signal
import subprocess
import sys
import time
from threading import Event, Thread
from typing import List, Union, Callable, Optional

import click


def _repr_command(command: Union[List[str], str]) -> str:
    return ' '.join(map(shlex.quote, command))


def subprocess_run_in_terminal(cmd: List[str]):
    logging.info(
        click.style(f'Running ', fg='cyan') +
        click.style(f'{_repr_command(cmd)}', fg='bright_cyan', underline=True) +
        click.style(f' ...', fg='cyan')
    )
    try:
        process = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    except KeyboardInterrupt:
        logging.warning(click.style('Process interrupted.', fg='yellow'))
    else:
        if process.returncode:
            logging.error(click.style(f'Process quit with exitcode {process.returncode!r}.', fg='red'))
        else:
            logging.info(click.style('Process quit.', fg='blue'))


class DaemonInterrupt(BaseException):
    pass


def subprocess_run_in_terminal_with_daemon(cmd: List[str], daemon_check: Callable[[], bool],
                                           check_interval: float, first_interval: Optional[float] = None,
                                           cycle_interval: float = 0.5):
    first_interval = first_interval if first_interval is not None else check_interval
    logging.info(
        click.style(f'Running ', fg='cyan') +
        click.style(f'{_repr_command(cmd)}', fg='bright_cyan', underline=True) +
        click.style(f' ...', fg='cyan')
    )
    try:
        with subprocess.Popen(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr) as process:
            process_is_over = Event()
            process_is_killed = Event()

            def _daemon():
                _last_cycle = time.time()
                _last_check = _last_cycle
                _is_first = True
                while not process_is_over.is_set():
                    _last_cycle += cycle_interval
                    if time.time() < _last_cycle:
                        time.sleep(_last_cycle - time.time())

                    if _last_check + (first_interval if _is_first else check_interval) <= time.time():
                        _last_check = time.time()
                        _is_first = False
                        if not daemon_check():
                            process.send_signal(signal.SIGTERM)
                            process_is_killed.set()
                            break

            daemon_thread = Thread(target=_daemon)
            daemon_thread.start()

            try:
                process.communicate()
            except:  # Including KeyboardInterrupt, communicate handled that.
                process.kill()
                # We don't call process.wait() as .__exit__ does that for us.
                raise
            else:
                retcode = process.poll()
            finally:
                process_is_over.set()
                daemon_thread.join()

    except KeyboardInterrupt:
        logging.warning(click.style('Process interrupted.', fg='yellow'))
    else:
        if process_is_killed.is_set():
            logging.error(click.style(f'Process is killed by the daemon thread.', fg='red'))
            raise DaemonInterrupt
        elif process.returncode:
            logging.error(click.style(f'Process quit with exitcode {retcode!r}.', fg='red'))
        else:
            logging.info(click.style('Process quit.', fg='blue'))
