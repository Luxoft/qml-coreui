import click
from coreuiadmin.utils import pass_options, echo
from coreuiadmin.utils.shell import run
from coreuiadmin.utils.machine import is_linux
import logging

_log = logging.getLogger(__name__)

packages = [
    "build-essential", "qt5-default", "libxcb-xinerama0-dev", "^libxcb.*-dev",
    "libx11-xcb-dev", "libglu1-mesa-dev", "libxrender-dev", "libxi-dev",
    "libssl-dev", "libxcursor-dev", "libxcomposite-dev", "libxdamage-dev",
    "libxrandr-dev", "libdbus-1-dev", "libfontconfig1-dev", "libcap-dev",
    "libxtst-dev", "libpulse-dev", "libudev-dev", "libpci-dev", "libnss3-dev",
    "libasound2-dev", "libxss-dev", "libegl1-mesa-dev", "gperf", "bison",
    "libwayland-dev", "libwayland-egl1-mesa", "libwayland-server0",
    "libgles2-mesa-dev", "libxkbcommon-dev", "cmake", "zlib1g-dev",
    "libdbus-glib-1-dev", "flex", "python3-virtualenv", "python-virtualenv", "curl"
]


@click.command('os', short_help='prepares the OS to build qauto')
@click.option('--init', is_flag=True, help="installs required packages")
@click.option('--check', is_flag=True, help="check if required packages are installed")
@pass_options
def app(opts, init, check):
    """ initializes a fresh OS by installing and checking for required packages"""
    _log.info('os')
    if is_linux:
        if init:
            _log.info('start ubuntu init')
            for package in packages:
                _log.info('start package installation')
                run("sudo apt install -qqq -y {0}".format(package))
            _log.info('start git lfs installation')
            run("curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash")
            run('sudo apt-get install -qqq -y git-lfs')
            run("git lfs install")
        elif check:
            for package in packages:
                run("apt -qqq list {0}".format(package))
        else:
            _log.info('print unix name')
            run('uname -a')
    else:
        echo('currently only available on linux')



