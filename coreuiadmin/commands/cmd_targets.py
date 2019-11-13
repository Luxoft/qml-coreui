import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils.echo import info
import logging

_log = logging.getLogger(__name__)


@click.command('targets', short_help='manages the buildable targets')
@click.option('--list', is_flag=True)
@click.option('--remove', is_flag=True)
@click.option('--set', is_flag=True)
@click.argument('name', nargs=1, required=False)
@click.argument('repos', nargs=-1, required=False)
@pass_options
def app(opts, list, remove, set, name, repos):
    """Manages the targets. A target is an orderd list of repositories.
    Called with no arguments will list all targets"""
    _log.info(name)
    if remove and name:
        _log.info('remove target %s' % name)
        opts.target_remove(name)
    elif set and name and repos:
        _log.info('set target %s' % name)
        opts.target_set(name, repos)
    elif name:
        _log.info('print target %s' % name)
        info('{0:_^16}|_{1:_^48}'.format('name', 'repos'))
        repos = opts.get_repos(name)
        info('{0:16}| {1:48}'.format(name, ', '.join(repos)))
    else:
        _log.info('print all targets')
        info('{0:_^16}|_{1:_^48}'.format('name', 'repos'))
        for name, repos in opts.targets.items():
            info('{0:16}| {1:48}'.format(name, ', '.join(repos)))
