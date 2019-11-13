import click
from coreuiadmin.utils import pass_options
from path import Path
import logging

_log = logging.getLogger(__name__)

here = Path(__file__).abspath().parent


def list_repos(opts):
    click.echo('{0:16} {1:48} {2:8} {3:8}'.format('name', 'url', 'branch', 'build').upper())
    for name, repo in opts.repos.items():
        click.echo('{0:16} {1:48} {2:8} {3:8}'.format(name, repo['url'], repo['branch'], repo['build']))


@click.command('repos', short_help='manages the listed repos')
@click.option('--list', is_flag=True)
@click.option('--remove')
@click.argument('name', nargs=1, required=False)
@click.argument('url', nargs=1, required=False)
@click.argument('branch', nargs=1, required=False, default='master')
@click.argument('build', nargs=1, required=False, type=click.Choice(['qmake', 'cmake']), default='qmake')
@pass_options
def app(opts, list, remove, name, url, branch, build):
    """manages the configured repositories"""
    _log.info('repos')
    if list:
        list_repos(opts)
    elif remove:
        opts.repo_remove(remove)
    elif name and url and branch:
        opts.repo_add(name, url, branch, build)
    else:
        list_repos(opts)
