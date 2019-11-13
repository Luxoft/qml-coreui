import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils import qt5
import logging

_log = logging.getLogger(__name__)


@click.command('qt', short_help='support for building qt')
@click.option('--clone/--no-config', help='clone qt')
@click.option('--config/--no-config', help='configure qt')
@click.option('--build/--no-build', help='build qt')
@click.option('--clean/--no-clean', help='clean qt build and install')
@click.option('--branch', default='5.12', help='branch to be used')
@click.option('--minimal/--no-minimal', help='creates a minimal build')
@click.option('--release/--no-release', help='creates a release build')
@pass_options
def app(opts, clone, config, clean, build, branch, minimal, release):
    """support for building qt"""
    _log.info('qt')
    if clean:
        qt5.qt_clean(opts.build_path, opts.install_path)
    if clone:
        qt5.qt_clone(opts.source_path, branch, minimal)
    if config:
        qt5.qt_config(opts.source_path, opts.build_path, opts.install_path, minimal, release)
    if build:
        qt5.qt_build(opts.build_path, opts.make_jobs)


