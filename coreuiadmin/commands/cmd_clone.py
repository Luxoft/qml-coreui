import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils import repos
import logging

_log = logging.getLogger(__name__)


@click.command('clone', short_help='clones the qauto repositories into this workspace')
@click.argument('target', nargs=1, required=True)
@click.option('--dev/--no-dev', help="clone repo as developer repo into dev/source folder")
@pass_options
def app(opts, target, dev):
    """Clones a target or repo. To clone all repos use target name 'all'. """
    _log.info('clone')
    source_path = opts.source_path if not dev else opts.dev_source_path
    for repo_name in opts.get_repos(target):
        repo = opts.repo(repo_name)
        if repo:
            repos.clone(source_path, repo_name, repo["url"], repo["branch"])

