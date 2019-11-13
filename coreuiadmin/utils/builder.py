import click
import sh
from path import Path
import platform
import logging
from . import options
from . import shell

_log = logging.getLogger(__name__)

is_linux = platform.system() == 'Linux'
is_macos = platform.system() == 'Darwin'


def echo_dot(msg):
    """for each call echos a dot "." """
    click.secho('.', fg='blue', nl=False)


def echo_header(title):
    echo()
    click.secho(40 * '#', fg='green')
    click.secho('\t{0}'.format(title))
    click.secho(40 * '#', fg='green')


def make_error(msg):
    if msg.startswith('Project MESSAGE:'):
        # ignore qmake messages
        return
    click.secho(msg.strip(), fg='red')


def get_builder(repo, config):
    if repo.build == 'qmake':
        return QMakeBuilder(repo, config)
    if repo.build == 'cmake':
        return CMakeBuilder(repo, config)


make = sh.Command('make').bake(_out=options.echo, _err=make_error)


class Repo(object):
    def __init__(self, name, data):
        self.name = name
        self.url = data.get('url', None)
        self.build = data.get('build', None)
        self.branch = data.get('branch', 'master')
        self.os = data.get('os')
        self.codereview = data.get('codereview', '')
        self.is_qt_module = data.get('qt_module', False)


class BuildConfig(object):
    def __init__(self, source_root, build_root, install_root, qmake, jobs=1):
        self.source_root = Path(source_root).abspath()
        self.build_root = Path(build_root).abspath()
        self.install_root = Path(install_root).abspath()
        self.qmake = Path(qmake).abspath() if qmake else Path()
        self.jobs = jobs

        self.qt_root = self.qmake.parent.parent
        self.is_valid = self._validate()

    def _validate(self):
        result = True
        if not self.qmake.exists() or not self.qmake.isfile():
            options.warning('invalid qmake {}. Please set qmake using `coreui-admin config qmake <path>`'.format(self.qmake))
            result = False
        if result and not self.jobs > 0:
            options.warning('make jobs must be greater 0', fg='red')
            result = False

        return result

    def dump(self):
        options.echo('source_root: {}'.format(self.source_root))
        options.echo('build_root: {}'.format(self.build_root))
        options.echo('install_root: {}'.format(self.install_root))
        options.echo('qmake: {}'.format(self.qmake))
        options.echo('jobs: {}'.format(self.jobs))


class Builder(object):
    def __init__(self, repo, config):
        self.is_valid = True
        self.repo = repo
        self.source_root = config.source_root
        self.install_root = config.install_root
        self.build_root = config.build_root
        self.qt_root = config.qt_root
        self.qmake_path = config.qmake
        self.jobs = config.jobs
        self.qmake = self.qmake_path
        self.source_path = self.source_root / self.repo.name
        self.build_path = self.build_root / self.repo.name
        self.install_path = config.install_root / self.repo.name

        self.validate()
        if not self.is_valid:
            msg = ''
            if options.dry_run():
                msg = "DRY MODE. Continue anyway"
                self.is_valid = True
            options.warning('no valid build configuration for {}. {}'.format(self.repo.name, msg))


    def validate_path(self, path, name):
        if not path.exists():
            options.warning('{} not valid: {}'.format(name, path))
            self.is_valid = False
            return False
        return True

    def ensure_path(self, path):
        if not path.exists():
            shell.makedirs(path)

    def check_os(self):
        if is_linux and 'linux' not in self.repo.os:
            options.echo('linux is not supported')
            self.is_valid = False
        if is_macos and 'macos' not in self.repo.os:
            options.echo('macos is not supported')
            self.is_valid = False

    def validate(self):
        self.validate_path(self.source_path, 'source path')
        self.ensure_path(self.build_path)
        self.check_os()

    def install(self):
        """installs the build"""
        options.echo('install {}'.format(self.repo.name))
        if not self.is_valid:
            return
        shell.run('make install', self.build_path)

    def rebuild(self):
        """rebuilds the source"""
        options.echo('rebuild {}'.format(self.repo.name))
        if not self.is_valid:
            return
        self.clean()
        self.build()

    def configure(self, pause=True):
        """configure the source"""
        if not self.is_valid:
            return
        options.echo('configure {}'.format(self.repo.name))

    def build(self):
        """build the source code"""
        if not self.is_valid:
            return
        options.echo('build {}'.format(self.repo.name))
        self.ensure_path(self.build_path)
        shell.run('make --jobs={}'.format(self.jobs), self.build_path)

    def clean(self):
        """clean the build folder"""
        if not self.is_valid:
            return
        options.echo('clean {}'.format(self.repo.name))
        shell.rmtree(self.build_path)
        shell.rmtree(self.install_path)


class QMakeBuilder(Builder):
    def configure(self, pause=True):
        if self.repo.is_qt_module:
            shell.run('{} {}'.format(self.qmake, self.source_path), self.build_path)
        else:
            shell.run('{} {} INSTALL_PREFIX={}'.format(self.qmake, self.source_path, self.install_root), self.build_path)
        if pause:
            options.pause()


class CMakeBuilder(Builder):
    def validate(self):
        super(CMakeBuilder, self).validate()

    def configure(self, pause=True):
        if self.repo.is_qt_module:
            shell.run('cmake {} -DCMAKE_PREFIX_PATH={}/lib/cmake'.format(self.source_path, self.qt_root), self.build_path)
        else:
            shell.run('cmake {} -DCMAKE_PREFIX_PATH={}/lib/cmake -DCMAKE_INSTALL_PREFIX={}'.format(self.source_path, self.qt_root, self.install_root), self.build_path)

        if pause:
            options.pause()
