import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils.gen import Generator
from path import Path
import logging

_log = logging.getLogger(__name__)

here = Path(__file__).abspath().parent


@click.command('app', short_help='creates a new application')
@click.argument('uri', required=True)
@click.argument('title', required=True)
@pass_options
def app(opts, uri, title):
    """creates an application scaffold inside a project"""
    _log.info('create app in apps/%s' % click.format_filename(uri))
    g = Generator(path=here / 'templates/app', workspace=opts.workspace)
    g.destination = opts.workspace / 'ui/apps' / uri
    g.context.update({
        'uri': uri,
        'title': title,
    })
    g.write_all([
        'info.yaml',
        'AppShell.qml',
        'stores/RootStore.qml',
        'views/WelcomeView.qml',
        'panels/WelcomePanel.qml',
    ])
