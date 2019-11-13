import subprocess
from path import Path
from .options import dry_run, CWD, get_env, run_echo, error
import logging
import wget
import click
import distutils.spawn
import multiprocessing

_log = logging.getLogger(__name__)


def run(cmd, path=Path('.'), env={}):
    """prints the call and executes the call"""
    _log.info('run {} in {}'.format(cmd, path))
    run_echo(cmd, path)
    if dry_run():
        return
    path.makedirs_p()
    with path:
        retcode = subprocess.call(cmd, shell=True, env=get_env())
    if retcode:
        error('call failed: {0} with error code {1}'.format(cmd, retcode), error_code=retcode)
    return retcode


def rmtree(path):
    """prints the rmtree call and executes the call"""
    _log.info('rmtree {}'.format(path))
    run_echo('rmtree ./{}'.format(CWD.relpathto(path)))
    if dry_run():
        return
    path.rmtree_p()


def makedirs(path, silent=False):
    """prints the makedirs call and executes the call"""
    _log.info('makedirs {}'.format(path))
    if path.exists():
        return
    if not silent:
        run_echo('makedirs ./{}'.format(CWD.relpathto(path)))
    if dry_run():
        return
    path.makedirs_p()


def download(url, out=None):
    click.secho('download file: {}'.format(url))
    if dry_run():
        return
    return wget.download(url, out)


def which(name):
    return distutils.spawn.find_executable(name)


def ask_path(name, default=''):
    path = default if default else which(name)
    while True:
        path = Path(click.prompt('{0} path:'.format(name), default=path))
        path = path.expand()
        if not path.exists():
            click.secho('wrong {0} path'.format(name))
        else:
            break
    return path


def cpu_count():
    return multiprocessing.cpu_count()
