import click
from coreuiadmin.utils import pass_options, dry_run, info
from coreuiadmin.utils.shell import rmtree
import logging

_log = logging.getLogger(__name__)



def confirm(msg):
    if dry_run():
        info("DRY: {} - YES".format(msg))
        return True
    else:
        return click.confirm(msg)

@click.command('clean', short_help='cleans the build, install and optional the source folder')
@click.option('--clean-source/--no-clean-source', default=False, help="Cleans also source folder. [default is false]")
@click.option('--yes/--no-yes', default=False, help="Answers all questions with yes. [default is false]")
@click.option('--dev/--no-dev', help="clean developer folders")
@click.argument('target', nargs=1)
@pass_options
def app(opts, clean_source, yes, target, dev):
    """cleans the build/install folder according to target."""
    _log.info('clean')
    source_path = opts.source_path if not dev else opts.dev_source_path
    build_path = opts.build_path if not dev else opts.dev_build_path
    install_path = opts.install_path if not dev else opts.dev_install_path
    for repo_name in opts.get_repos(target):
        source = source_path / repo_name
        build = build_path / repo_name
        install = install_path / repo_name
        if yes or confirm('delete {0}?'.format(build)):
            rmtree(build)
        if yes or confirm('delete {0}?'.format(install)):
            rmtree(install)
        if clean_source:
            if yes or confirm('delete {0}?'.format(source)):
                rmtree(source)


