from fnmatch import fnmatch
from coreuiadmin.utils import pass_options, echo, get_env
import click
import logging

_log = logging.getLogger(__name__)


def echo_env(env):
    click.secho('{:_^16}_|_{:_^32}'.format('name', 'value'), fg="green")
    for name, value in env.items():
        click.secho('{:16} | {:<32}'.format(name, value), fg="green")


@click.command('env', short_help='display env variables')
@click.option('--edit', is_flag=True, help="opens the .env file in the editor")
@click.argument('name', required=False)
@click.option('--os', is_flag=True, help="shows also os environment variables")
@pass_options
def app(opts, edit, name, os):
    """ displays the used environment variables
    """
    _log.info('env')
    env = opts.config_env if not os else opts.env
    if edit:
        click.edit(filename=opts.env_path)
    elif name:
        for key in env:
            if fnmatch(key.lower(), name.lower()):
                echo("{}={}".format(key, env[key]))
    else:
        echo_env(env)
