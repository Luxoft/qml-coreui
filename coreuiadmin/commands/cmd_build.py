import click
from path import Path
import logging
from coreuiadmin.utils import pass_options, warning
from coreuiadmin.utils.builder import BuildConfig, Repo, get_builder

here = Path(__file__).abspath().parent

_log = logging.getLogger(__name__)


@click.command('build', short_help='builds one or more repos')
@click.argument('target', nargs=1, required=True)
@click.option('--pause/--no-pause', default=True, help="Pause after configure step")
@click.option('--config/--no-config', default=True, help="Configures before building")
@click.option('--dev/--no-dev', help="build repo as developer repo insode dev/build folder")
@pass_options
def app(opts, target, pause, config, dev):
    """Builds a target. To build all repositories use target named 'all'.
    """
    _log.debug('cmd_build')
    source_path = opts.source_path if not dev else opts.dev_source_path
    build_path = opts.build_path if not dev else opts.dev_build_path
    install_path = opts.install_path if not dev else opts.dev_install_path
    qmake = opts.qmake_path

    config = BuildConfig(
        source_root=source_path,
        build_root=build_path,
        install_root=install_path,
        qmake=qmake,
        jobs=int(opts.value('jobs', 2)),
    )

    if not config.is_valid:
        return

    names = opts.get_repos(target)
    if not names:
        warning('no repository found named: {}'.format(names))
    for name in names:
        data = opts.repo(name)
        repo = Repo(name, data)
        builder = get_builder(repo, config)
        if not builder.is_valid:
            continue
        if config:
            builder.configure(pause)
        builder.build()
        builder.install()
        opts.update_scripts(data.get('scripts', {}))
