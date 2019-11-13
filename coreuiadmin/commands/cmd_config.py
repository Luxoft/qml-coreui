import click
import logging
from coreuiadmin.utils import pass_options
from coreuiadmin.utils.shell import ask_path, cpu_count
from coreuiadmin.utils.echo import info

_log = logging.getLogger(__name__)


def interactive_configuration(opts):
    qmake = ask_path('qmake', opts.value('qmake'))
    opts.set_value('qmake', qmake)
    cmake = ask_path('cmake', opts.value('cmake'))
    opts.set_value('cmake', cmake)
    cpus = cpu_count()
    jobs = click.prompt('make jobs (cpu count = {})'.format(cpus), default=opts.value('jobs', cpus))
    if jobs:
        opts.set_value('jobs', jobs)


@click.command('config', help='configures qauto')
@click.option('--unset', help="unsets a value from config section")
@click.option('--edit/--no-edit', default=False, help="launches default editor with config file")
@click.option('--interactive/--no-interactive', default=False, help="asks users about primary config values")
@click.argument('name', required=False, nargs=1)
@click.argument('value', required=False, nargs=1)
@pass_options
def app(opts, name, value, unset, edit, interactive):
    _log.info('config')
    """Manages the config file. If called with no arguments lists the current configuration"""
    if edit:
        click.edit(filename=opts.config_path)
    elif unset:
        opts.unset_value(unset)
    elif interactive:
        interactive_configuration(opts)
    elif name and not value:
        value = opts.config.get(name, '')
        info('{0:16} | {1:<48}'.format(name, value))
    elif name and value:
        opts.set_value(name, value)
    else:
        for name, value in opts.config.items():
            value = value or ''
            info('{0:16} | {1:<48}'.format(name, value))
