import click
from coreuiadmin.utils import pass_options, warning
from coreuiadmin.utils.shell import run
import logging

_log = logging.getLogger(__name__)


@click.command('run', short_help='runs a script from the config script section by name')
@click.argument('name', required=True)
@click.argument('args', nargs=-1)
@pass_options
def app(opts, name, args):
    """starts a script given by name and passes on all other arguments"""
    args = " ".join(args)
    _log.info('run `%s %s`' % (name, args))
    script = opts.script(name)
    if script:
        run('{} {}'.format(script, args), opts.workspace)
    else:
        warning('No such script `{}`.'.format(name))
