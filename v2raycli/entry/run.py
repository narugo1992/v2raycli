import logging
import random
from typing import List

import click
from InquirerPy import inquirer
from hbutils.system import get_localhost_ip

from .base import CONTEXT_SETTINGS, command_wrap, ClickWarningException
from .list import _get_sublist, V2RAY_SUBSCRIPTION_ENV
from ..dispatch import put_config_to_tempfile
from ..execute import load_v2ray_bin, get_v2ray_from_env, V2RAY_BIN_ENV, DaemonInterrupt
from ..execute.check import DEFAULT_TARGET_SITE
from ..log import parse_log_level
from ..outbounds import NamedServer
from ..subscription import list_from_subscription


class NoSubscriptionFoundError(ClickWarningException):
    exit_code = 0x11


class NoSiteFoundError(ClickWarningException):
    exit_code = 0x12


def _get_address(protocol: str, port: int) -> str:
    if protocol == 'socks':
        _protocol = 'socks5'
    elif protocol == 'http':
        _protocol = 'http'
    else:
        assert False, f'Should not reach here! Protocol: {protocol!r}.'  # pragma: no cover

    return f'{_protocol}://{get_localhost_ip()}:{port}'


def _get_sites(sublist: List[str]) -> List[NamedServer]:
    sites = []
    for i, sub in enumerate(sublist):
        subscriptions = list_from_subscription(sub)
        for subitem in subscriptions:
            sites.append(subitem)

    if not sites:
        raise NoSiteFoundError('No site found in current subscriptions.')
    return sites


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
                  default=get_v2ray_from_env(), envvar=V2RAY_BIN_ENV, required=True,
                  help=f'V2Ray executable file, can be assigned in env {V2RAY_BIN_ENV!r}.', show_default=True)
    @click.option('--random', '-R', 'use_random', is_flag=True, default=False,
                  help='Randomly choose a site to connect to without interaction.', show_default=True)
    @click.option('--loglevel', '-L', 'log_level',
                  type=click.Choice(['DEBUG', 'INFO', 'WARN', 'ERROR'], case_sensitive=False), default='INFO',
                  help='Log level for v2raycli and v2ray core.', show_default=True)
    @click.option('--check_site', 'check_site', type=str, default=DEFAULT_TARGET_SITE,
                  help='Site to connect for checking the proxy service.', show_default=True)
    @click.option('--check_interval', 'check_interval', type=int, default=300,
                  help='Interval in seconds of checking the proxy service', show_default=True)
    @command_wrap()
    def run(sublist: List[str], port: int, protocol: str, executable: str, use_random: bool,
            log_level: str, check_site: str, check_interval: int):
        log_level: int = parse_log_level(log_level)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s][v2raycli] %(message)s",
            datefmt='%Y/%m/%d %H:%M:%S',
        )

        sublist = _get_sublist(sublist)
        if not sublist:
            raise NoSubscriptionFoundError('No subscription found.')

        sites = _get_sites(sublist)
        if not use_random:
            site_reprs = list(map(repr, sites))
            repr_text_maps = {t: i for i, t in enumerate(site_reprs)}
            select_id = repr_text_maps[inquirer.select(
                message='Select one proxy site for connection establishing:',
                choices=list(map(repr, sites)),
            ).execute()]
        else:
            select_id = random.choice(range(len(sites)))

        selected_site = sites[select_id]
        base_site_name = selected_site.name
        while True:
            try:
                with put_config_to_tempfile(
                        selected_site, protocol=protocol, port=port,
                        log_level=log_level
                ) as config_file:
                    proxy_address = _get_address(protocol, port)
                    logging.info(
                        click.style(f'Proxy site ', fg='blue') +
                        click.style(f'{selected_site.name}', fg='blue', underline=True) +
                        click.style(f'({selected_site.__protocol__}://{selected_site.address}:{selected_site.port})'
                                    f' is selected to connect.', fg='blue')
                    )
                    logging.warning(
                        click.style(f'Proxy service will be hosted at ', fg='cyan') +
                        click.style(proxy_address, fg='bright_cyan', underline=True, bold=True) +
                        click.style('.', fg='cyan')
                    )
                    load_v2ray_bin(executable).run_with_daemon(
                        config_file, proxy_address,
                        target_site=check_site,
                        first_interval=1,
                        check_interval=check_interval,
                    )
            except DaemonInterrupt:
                logging.warning(
                    click.style('Current proxy site failed, try refreshing the subscriptions.', fg='yellow'))
                sites = _get_sites(sublist)
                found_exist_name = False
                logging.debug(click.style(f'Try to find server {base_site_name!r} ...', fg='blue'))
                for site in sites:
                    if site.name == base_site_name:
                        found_exist_name, selected_site = True, site
                        break

                if not found_exist_name:
                    selected_site = random.choice(sites)
                    logging.debug(click.style(f'Randomly choose one server, {selected_site!r} chosen.', fg='blue'))
                else:
                    logging.debug(click.style(f'Server {selected_site!r} found.', fg='blue'))
            else:
                break

    return cli
