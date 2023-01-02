import time
from typing import Optional

import click


@click.command()
@click.option('-c', '--count', 'count', type=int, default=None,
              help='Count of ticks, unlimited when not given.', show_default=True)
@click.option('-i', '--interval', 'interval', type=float, default=0.5,
              help='Interval between ticks in seconds.', show_default=True)
def tick(count: Optional[int], interval: float):
    i = 0
    while True:
        i += 1
        print(f'tick: {i}')
        time.sleep(interval)
        if count is not None and i >= count:
            break


if __name__ == '__main__':
    tick()
