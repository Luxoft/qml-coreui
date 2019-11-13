import logging
from .options import warning
from .shell import run, makedirs

_log = logging.getLogger(__name__)


def clone(path, name, url, branch):
    """clones or updated a repo"""
    repo_path = path / name

    if repo_path.exists():
        warning('{} already exists. skip cloning'.format(name))
        return

    makedirs(path)
    run("git clone {} {}".format(url, name), path=path)
    run('git checkout {}'.format(branch), path=repo_path)
    run('git submodule init', path=repo_path)
    run('git submodule update', path=repo_path)


def pull(path, name, url, branch):
    """pull the repo using git. Does reset the repo first"""
    repo_path = path / name
    if not repo_path.exists():
        warning('repository not exists {}, clone first.'.format(name))
        return
    run('git reset --hard', path=repo_path)
    run('git checkout {}'.format(branch), path=repo_path)
    run('git pull', path=repo_path)
    run('git submodule init', path=repo_path)
    run('git submodule update', path=repo_path)

