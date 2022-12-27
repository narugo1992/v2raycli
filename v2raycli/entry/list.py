import os
from typing import List

import click
from tabulate import tabulate

from .base import CONTEXT_SETTINGS, command_wrap
from ..subscription import list_from_subscription

V2RAY_SUBSCRIPTION_ENV = 'V2RAY_SUBSCRIPTION'


def _get_sublist(sublist: List[str]) -> List[str]:
    if os.environ.get(V2RAY_SUBSCRIPTION_ENV, None):
        sublist = [*sublist, *os.environ[V2RAY_SUBSCRIPTION_ENV].split(';')]

    return sublist


def _add_list_subcommand(cli: click.Group) -> click.Group:
    @cli.command('list', help='List information of current subscription.',
                 context_settings=CONTEXT_SETTINGS)
    @click.option('--subscription', '-s', 'sublist', multiple=True, type=str,
                  help=f'Subscription of proxy sites, can be assigned in env {V2RAY_SUBSCRIPTION_ENV!r}.')
    @command_wrap()
    def list_(sublist: List[str]):
        sublist = _get_sublist(sublist)
        click.echo(tabulate(enumerate(sublist, start=1), headers=['#', 'Subscription Site'], tablefmt="psql"))

        rows = []
        headers = ['#', 'Sub', 'Name', 'Protocol', 'Address']
        for i, sub in enumerate(sublist, start=1):
            subscriptions = list_from_subscription(sub)
            for subitem in subscriptions:
                rows.append((len(rows), i, subitem.name, subitem.__protocol__, f'{subitem.address}:{subitem.port}'))
        click.echo(tabulate(rows, headers=headers, tablefmt='psql'))

    return cli
