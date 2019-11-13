import click
from coreuiadmin.utils.options import resolve_workspace
from coreuiadmin.utils.gen import Generator
from coreuiadmin.utils.shell import download
from path import Path
import logging


_log = logging.getLogger(__name__)

here = Path(__file__).abspath().parent


def generate_config(dst):
        g = Generator(path=here / 'templates', context={'dst': dst})
        g.destination = dst
        g.source = 'config'
        g.write('coreui.yml')


@click.command('init', help='creates an empty coreui workspace')
@click.option('--source', required=False, help="uses the config file from given location")
@click.option('--force/--no-force', required=False, help="overwrites an existing configuration if exists")
def app(source, force):
    """Initialized the workspace by writing the `coreui.yml` setup document"""
    _log.info('init')
    workspace = resolve_workspace(validate=False)
    if workspace and not force:
        click.echo('workspace already exists. Delete first')
        return
    else:
        workspace = Path.getcwd()
    with workspace:
        if source:
            if source.endswith('coreui.yml'):
                Path('coreui.yml').remove_p()
                download(source, 'coreui.yml')
            else:
                click.secho('source needs to point to a `coreui.yml` document')
        else:
            generate_config(workspace)
