import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils import repos
import logging

_log = logging.getLogger(__name__)


@click.command('pull', short_help='updates the qauto repositories')
@click.argument('target', nargs=1, required=True)
@pass_options
def app(opts, target):
    """
    Updates the repos given by target. Will hard reset the repo first. To clone all use target name 'all'.
    """
    _log.info('pull')
    source_path = opts.source_path
    names = opts.get_repos(target)
    for name in names:
        repo = opts.repo(name)
        repos.pull(source_path, name, repo["url"], repo["branch"])

