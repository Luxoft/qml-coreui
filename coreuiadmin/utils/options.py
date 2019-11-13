from path import Path
import yaml
import click
import sys
import os
from string import Template
import logging
from .echo import echo
from collections import ChainMap

_log = logging.getLogger(__name__)


def resolve_workspace(cwd=Path.getcwd(), validate=True):
    # try to resolve workspace path
    workspace = None
    path = Path(cwd).expand()
    while not workspace:
        if path == HOME_DIR or path.parent == path:
            break
        if Path(path / CONFIG_NAME).exists():
            click.secho('using workspace `~/{}`'.format(HOME_DIR.relpathto(path)), fg='yellow')
            workspace = path
        path = path.parent
    if validate and not workspace:
        exit('Not a coreui project (or any of the parent directories). Run init first.')
    return workspace


CONFIG_NAME = 'coreui.yml'
HOME_DIR = Path('~').expanduser()
CWD = Path.getcwd()

_verbose = False
_dry_run = False


def verbose():
    return _verbose


def dry_run():
    return _dry_run


def pause():
    if dry_run():
        info('Press any key to continue ...')
    else:
        click.pause()


def info(msg):
    """standard info call"""
    click.secho(msg.strip(), fg='green')


def warning(msg):
    click.secho('WARN: {}'.format(msg.strip()), fg='magenta', err=True)


def error(msg, error_code=-1):
    """standard error call"""
    click.secho("ERROR: {}".format(msg.strip()), fg='red', err=True)
    sys.exit(error_code)


def exit(reason):
    """prints the reason and exits the script"""
    click.secho(reason, fg='red')
    sys.exit(-1)


def run_echo(msg, path=CWD):
    """standard echo call with optional path component"""
    dry = "DRY :" if dry_run() else ""
    click.secho('[{0}{1:16}]> '.format(dry, CWD.relpathto(path)), fg='green', nl=False)
    click.secho(msg, fg='blue')


def log(msg, *args):
    """logs a message to stderr."""
    if args:
        msg %= args
    click.echo(msg, file=sys.stderr)


def vlog(self, msg, *args):
    """logs a message to stderr only if verbose is enabled."""
    if verbose:
        log(msg, *args)


def get_env():
    return get_options().env


def get_options():
    # fails if options where never created
    if not _options:
        exit('options not yet initialized.')
    return _options


_options = None


# the central configuration, passed onto the commands
class Options(object):
    def __init__(self):
        self.assign_global()
        self.data = {}
        self.targets = {}
        self.repos = {}
        self.scripts = {}
        self.config = {}
        self.config_env = {}
        # config
        self.env_name = '.env.yml'
        self.workspace = resolve_workspace()
        self.config_path = self.workspace / CONFIG_NAME
        self.env_path = self.workspace / self.env_name
        self._read()
        self._read_env_file()

        self.env = ChainMap(self.config_env, os.environ)

    warning = staticmethod(warning)
    info = staticmethod(info)
    echo = staticmethod(echo)
    exit = staticmethod(exit)
    log = staticmethod(log)
    vlog = staticmethod(vlog)

    def assign_global(self):
        global _options
        if _options:
            exit('options can only be created once')
        _options = self

    def _write(self):
        self.data['targets'] = self.targets
        self.data['repos'] = self.repos
        self.data['scripts'] = self.scripts
        self.data['config'] = self.config
        text = yaml.safe_dump(self.data, default_flow_style=False)
        self.config_path.write_text(text)

    def _read(self):
        if not self.config_path.exists():
            return
        text = self.config_path.text()
        self.data.update(yaml.safe_load(text))
        self.repos = self.data.get('repos', {}) or {}
        self.targets = self.data.get('targets', {}) or {}
        self.scripts = self.data.get('scripts', {}) or {}
        self.config = self.data.get('config', {}) or {}
        env = self.data.get('env', {}) or {}
        if not isinstance(env, dict):
            exit('env in config section needs to be a dictionary')
        self.config_env = env

    def set_value(self, name, value):
        value = str(value)
        echo('config {0}={1}'.format(name, value))
        self.config.update({name: value})
        self._write()

    def value(self, name, default=''):
        return self.config.get(name, default)

    def unset_value(self, name):
        echo('unset value {}'.format(name))
        del self.config[name]
        self._write()

    def repo_add(self, name, url, branch, build):
        self.repos.update({
            name: {'url': url, 'branch': branch, "build": build}
        })
        self._write()

    def repo_remove(self, name):
        if name in self.repos:
            del self.repos[name]
            self._write()

    def repo(self, name):
        if name not in self.repos:
            echo('unknown repo: {}'.format(name))
            return {}
        return self.repos.get(name, {})

    @property
    def source_path(self):
        return self.workspace / self.value('source', 'source')

    @property
    def dev_source_path(self):
        return self.workspace / self.value('dev', 'dev') / self.value('source', 'source')

    @property
    def build_path(self):
        return self.workspace / self.value('build', 'build')

    @property
    def dev_build_path(self):
        return self.workspace / self.value('dev', 'dev') / self.value('build', 'build')

    @property
    def install_path(self):
        return self.workspace / self.value('install', 'install')

    @property
    def dev_install_path(self):
        return self.workspace / self.value('dev', 'dev') / self.value('install', 'install')

    @property
    def qmake_path(self):
        return self.value('qmake', "")

    @property
    def make_jobs(self):
        return self.value('jobs', 2)

    def target_set(self, name, repos):
        self.targets[name] = repos
        self._write()
        echo('target `{}` set to {}'.format(name, ','.join(repos)))

    def target_remove(self, name):
        if name in self.targets:
            echo('removed target {}'.format(name))
            del self.targets[name]
            self._write()
        else:
            echo('target `{}` does not exist'.format(name))

    def target(self, name):
        return self.targets.get(name, [])

    def get_repos(self, target):
        """return the repo names based on the given target
        or the repo name if its a valid name"""
        repos = []
        if target == 'all':
            repos = self.repos.keys()
        elif target in self.targets:
            repos = self.targets[target]
        elif target in self.repos:
            repos = [target]
        return repos

    def _read_env_file(self):
        if self.env_path.exists():
            text = self.env_path.text()
            env = yaml.safe_load(text)
            if not isinstance(env, dict):
                exit('env document {} must be a YAML dictionary'.format(self.env_path))
            self.config_env.update(env)

    def script(self, name):
        if name not in self.scripts:
            return None
        text = self.scripts.get(name)
        return Template(text).safe_substitute(self.env)

    def set_script(self, name, script):
        self.scripts[name] = script
        self._write()

    def update_scripts(self, scripts):
        scripts = scripts or {}
        self.scripts.update(scripts)
        self._write()

    def validate(self):
        if not self.config_path.exists():
            fatal("fatal: Not a qauto workspace")

# create a decorator to pass on the options object
pass_options = click.make_pass_decorator(Options, ensure=True)
