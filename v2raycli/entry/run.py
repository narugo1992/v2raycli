from typing import List

import click
from InquirerPy import inquirer
from tabulate import tabulate

from .base import CONTEXT_SETTINGS, command_wrap
from .list import _get_sublist, V2RAY_SUBSCRIPTION_ENV
from ..dispatch import put_config_to_tempfile
from ..execute import load_v2ray_bin, get_v2ray_from_env
from ..subscription import list_from_subscription

V2RAY_EXEC_ENV = 'V2RAY_EXEC'


def _add_run_subcommand(cli: click.Group) -> click.Group:
    @cli.command('run', help='Start a proxy connections in subscription.',
                 context_settings=CONTEXT_SETTINGS)
    @click.option('--subscription', '-s', 'sublist', multiple=True, type=str,
                  help=f'Subscription of proxy sites, can be assigned in env {V2RAY_SUBSCRIPTION_ENV!r}.')
    @click.option('--port', '-p', 'port', type=int, default=17777,
                  help='Port to start the v2ray local service.', show_default=True)
    @click.option('--protocol', '-P', 'protocol', type=click.Choice(['socks', 'http']), default='socks',
                  help='Protocol to start the v2ray local service.', show_default=True)
    @click.option('--executable', '-e', 'executable',
                  type=click.Path(exists=True, file_okay=True, dir_okay=False, executable=True),
                  default=get_v2ray_from_env(), envvar=V2RAY_EXEC_ENV, required=True,
                  help=f'V2Ray executable file, can be assigned in env {V2RAY_EXEC_ENV!r}.', show_default=True)
    @command_wrap()
    def run(sublist: List[str], port: int, protocol: str, executable: str):
        sublist = _get_sublist(sublist)
        if not sublist:
            sublist = [inquirer.text(message="No Subscription given, please enter one:").execute()]

        click.echo(f'{len(sublist)} subscription(s) detected: ')
        click.echo(tabulate(enumerate(sublist), headers=['#', 'Subscription Site'], tablefmt="psql"))

        sites = []
        for i, sub in enumerate(sublist):
            subscriptions = list_from_subscription(sub)
            for subitem in subscriptions:
                sites.append(subitem)

        site_reprs = list(map(repr, sites))
        repr_text_maps = {t: i for i, t in enumerate(site_reprs)}
        select_id = repr_text_maps[inquirer.select(
            message='Select one proxy site for connection establishing:',
            choices=list(map(repr, sites)),
        ).execute()]

        selected_site = sites[select_id]
        with put_config_to_tempfile(selected_site, protocol=protocol, port=port) as config_file:
            load_v2ray_bin(executable).run(config_file)

    return cli
