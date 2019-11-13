from path import Path
from .machine import is_linux, is_macos
from .shell import run, rmtree, makedirs
import click
import logging

_log = logging.getLogger(__name__)


def qt_clone(source_path, branch, minimal=False):
    source_path = Path(source_path)
    qt_path = source_path / 'qt'
    if qt_path.exists():
        if not click.confirm("Qt source exists. I will be removed. Continue?"):
            return
        rmtree(qt_path)
    run('git clone git://code.qt.io/qt/qt5.git qt', path=source_path)
    run('git checkout {}'.format(branch), path=qt_path)
    if minimal:
        run('perl ./init-repository --module-subset=essential,addon,preview', path=qt_path)
    else:
        run('perl ./init-repository', path=qt_path)


def qt_config(source_path, build_path, install_path, minimal=False, release=False):
    qt_source = Path(source_path / 'qt')
    qt_build = Path(build_path / 'qt')
    qt_install = Path(install_path / 'qt')
    makedirs(qt_build)

    config = [
        '-opensource',
        '-confirm-license',
        '-nomake examples',
        '-nomake tests'
    ]
    if release:
        config.append('-release')
    else:
        config.append('-debug')
    if minimal:
        config.append('-skip qtandroidextras')
        config.append('-skip qtdatavis3d')
        config.append('-skip qtcharts')
        config.append('-skip qtdocgallery')
        config.append('-skip qtenginio')
        config.append('-skip qtfeedback')
        config.append('-skip qtpim')
        config.append('-skip qtpurchasing')
        config.append('-skip qtquick1')
        config.append('-skip qtscript')
        config.append('-skip qtspeech')
        config.append('-skip qtwebchannel')
        config.append('-skip qtwebengine')
        config.append('-skip qtwebglplugin')
        config.append('-skip qtwebview')
    if is_linux:
        config.append('-opengl es2')
    if is_macos:
        config.append('-no-framework')
    config = ' '.join(config)
    run('{0}/configure {1} -prefix {2}'.format(qt_source, config, qt_install), path=qt_build)


def qt_build(build_path, make_jobs):
    qt_build = build_path / 'qt'
    run('make --jobs={}'.format(make_jobs), path=qt_build)
    run('make install', path=qt_build)


def qt_clean(build_path, install_path):
    qt_build = Path(build_path / 'qt')
    qt_install = Path(install_path / 'qt')
    rmtree(qt_build)
    rmtree(qt_install)
