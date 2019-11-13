import click
from coreuiadmin.utils import pass_options, warning
from coreuiadmin.utils.shell import run
import logging

_log = logging.getLogger(__name__)


def echo_out(msg):
    click.secho(msg, fg='blue')


def echo_error(msg):
    click.secho(msg, fg='red')


@click.command('start', short_help='starts a project')
@click.argument('args', nargs=-1)
@pass_options
def app(opts, args):
    """starts the script named `start` and passes on all given arguments after `--`"""
    args = " ".join(args)
    _log.info('start "start" script with %s' % args)
    script = opts.script("start")
    if script:
        run('{} {}'.format(script, args), opts.workspace)
    else:
        warning('No such script `start`.')
