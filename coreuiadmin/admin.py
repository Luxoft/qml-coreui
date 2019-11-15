#!/usr/bin/env python

import click
from path import Path
import sys
from coreuiadmin.utils import options
import logging

log = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

CONTEXT_SETTINGS = dict(auto_envvar_prefix='COREUI')

PY2 = sys.version_info[0] == 2

here = Path(__file__).parent


cmd_folder = here.joinpath('commands').abspath()


class CommandLine(click.MultiCommand):
    def list_commands(self, ctx):
        result = []
        for path in cmd_folder.listdir():
            name = path.name
            if name.startswith('cmd_') and name.endswith('.py'):
                result.append(name[4:-3])
        result.sort()
        return result

    def get_command(self, ctx, name):
        try:
            if PY2:
                name = name.encode('ascii', 'replace')
            mod = __import__('coreuiadmin.commands.cmd_' + name, None, None, ['app'])
        except ImportError as err:
            if 'verbose' in ctx.params:
                options.warning(err.msg)
            return
        return mod.app


@click.command(cls=CommandLine, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--dry-run/--no-dry-run', help='operations are not executed, only printed')
@click.option(
    '--log-level', type=click.Choice(['info', 'debug', 'warning', 'error']),
    default='error', help='sets the log level'
)
@click.pass_context
def app(ctx, verbose, dry_run, log_level):
    """CoreUI adminstration tool. Allows you to build a CoreUI based project and much more.
    More documentation available at https://jryannel.gitlab.io/coreui-admin/.
    See 'coreui-admin help <command>' to read about a specific command.
    """

    logging.root.setLevel(log_level.upper())
    log.info('app')
    options._verbose = verbose
    options._dry_run = dry_run
