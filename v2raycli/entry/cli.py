from .dispatch import v2raycli
from .list import _add_list_subcommand
from .run import _add_run_subcommand

_DECORATORS = [
    _add_list_subcommand,
    _add_run_subcommand,
]

cli = v2raycli
for deco in _DECORATORS:
    cli = deco(cli)
