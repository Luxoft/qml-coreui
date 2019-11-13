import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils import repos
import logging
from coreuiadmin.utils.builder import BuildConfig, Repo, get_builder
from path import Path
from coreuiadmin.utils.shell import run

_log = logging.getLogger(__name__)

cwd = Path.getcwd()

message = """
Open project using Qt Creator from `{}`

* Set Qt Kit for `{}`
* Set build folder to `{}`
* Press configure

Build and run the project using Qt Creator
"""


@click.command('dev', short_help='starts the development for a repo')
@click.argument('repo_name', nargs=1)
@click.option('--pause/--no-pause', default=False, help="Pause after configure step")
@pass_options
def app(opts, repo_name, pause):
    """starts develoment on repo"""
    source_path = opts.dev_source_path
    build_path = opts.dev_build_path
    install_path = opts.dev_install_path
    qmake = opts.qmake_path

    data = opts.repo(repo_name)
    if data:
        repos.clone(source_path, repo_name, data["url"], data["branch"])

    config = BuildConfig(
        source_root=source_path,
        build_root=build_path,
        install_root=install_path,
        qmake=qmake,
        jobs=int(opts.value('jobs', 2)),
    )

    if not config.is_valid:
        return

    repo = Repo(repo_name, data)
    builder = get_builder(repo, config)
    if not builder.is_valid:
        return
    if config:
        builder.configure(pause)

    rel_source = builder.source_path.relpath()
    rel_build = builder.build_path.relpath()

    if repo.codereview:
        run('git remote add gerrit ssh://codereview.qt-project.org/{}'.format(repo.codereview), builder.source_path)
        run('gitdir=$(git rev-parse --git-dir); scp -p codereview.qt-project.org:hooks/commit-msg ${gitdir}/hooks/', builder.source_path)


    click.secho(message.format(rel_source, qmake, rel_build), fg="green")
