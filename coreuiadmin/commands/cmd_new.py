import click
from coreuiadmin.utils import pass_options, echo
from coreuiadmin.utils.gen import Generator
from path import Path
import logging

_log = logging.getLogger(__name__)

here = Path(__file__).abspath().parent


def generate_simple_process(path, force):
    dst = path
    project = Path(path).name
    print(project, dst)
    g = Generator(path=here / 'templates', context={'project': project, 'dst': dst})
    g.destination = dst
    g.source = 'new/simple'
    g.write_all([
        'Main.qml',
        '{{project}}.qmlproject',
        'qtquickcontrols2.conf',
        'stores/RootStore.qml',
        'views/WelcomeView.qml',
        'views/StackView.qml',
        'views/CounterView.qml',
        'views/ViewRegistry.qml',
        'tests/tst_stackstore.qml',
        'tests/tst_viewstack.qml',
        'stores/RootStore.qml',
        'stores/StackStore.qml',
        'stores/CounterStore.qml',
        'panels/StatusBar.qml',
        'imports/sys/ui/qmldir',
        'imports/sys/ui/Store.qml',
        'imports/sys/ui/View.qml',
        'helpers/qmldir',
        'helpers/Notifier.qml',
        'helpers/utils.js',
        'helpers/viewstack.js',
        'coreui.yml',
    ], force=force)
    echo('run the UI form the project folder with `coreui-admin start')


def generate_appman_process(path, force):
    dst = path
    project = Path(path).name
    g = Generator(path=here / 'templates', context={'project': project, 'dst': dst})
    g.destination = dst
    g.source = 'new/appman'
    g.write_all([
        'README.md',
        '{{project}}.pro',
        '.qmake.conf',
        'Makefile',
        'coreui.yml',
        'ui/Main.qml',
        'ui/am-config.yml',
        'ui/{{project}}-ui.qmlproject',
        'ui/qtquickcontrols2.conf',
        'ui/sysui/AppShell.qml',
        'ui/sysui/views/AppContainerView.qml',
        'ui/sysui/views/DialogView.qml',
        'ui/sysui/views/HomeView.qml',
        'ui/sysui/views/OverlaysView.qml',
        'ui/sysui/views/StatusView.qml',
        'ui/sysui/stores/RootStore.qml',
        'native/native.pro',
        'native/plugins/plugins.pro',
        'native/services/services.pro',
    ], force=force)
    echo('CONSOLE: cd {}'.format(project))
    echo('CONSOLE: create .env.yml setting QTDIR: "path/to/your/Qt/bin"')
    echo('CONSOLE: run `coreui-admin start` to start ui')
    echo('QTCREATOR: open {}.qmlproject and register custom executable:'.format(project))
    echo('QTCREATOR: Executable: "%{Qt:QT_INSTALL_BINS}/appman"; Arguments: "-r -c am-config.yaml"')
    echo('QTCREATOR: WorkingDirectory: "%{CurrentProject:Path}"')
    echo('QTCREATOR: Register Run Environment: "QT_QUICK_CONTROLS_CONF=./qtquickcontrols2.conf"')


@click.command('new', short_help='creates a new coreui project')
@click.option(
    '--template',
    type=click.Choice(['appman']),
    default='appman',
    help='Project template. Default is "appmen", a QtAuto process. There are no other templates currently available.'
)
@click.option('--force/--no-force', help="forces writing of files also when file exists already")
@click.argument('path', required=True, type=click.Path(resolve_path=True))
def app(template, path, force):
    """creates a new coreui project using a template.

    \b
    The following templates are supported:
    * `simple` - single-process UI for small or simple user interfaces
    * `appman` - A multi process UI for larger or complex user interfaces
    """
    _log.info('create project in %s', click.format_filename(path))
    if template == 'simple':
        generate_simple_process(path, force)
    elif template == 'appman':
        generate_appman_process(path, force)
