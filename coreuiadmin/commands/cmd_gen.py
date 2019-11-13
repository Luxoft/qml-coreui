import click
from coreuiadmin.utils import pass_options
from coreuiadmin.utils.gen import Generator
from path import Path
import logging

_log = logging.getLogger(__name__)

here = Path(__file__).abspath().parent

gen_choices = [
    'view', 'panel', 'control', 'helper',
    'store',
    'plugin', 'service', 'interface'
]


@click.command('gen', short_help='creates a new application aspect')
@click.option('--force/--no-force', help="forces writing of files also when file exists already")
@click.argument('aspect', type=click.Choice(gen_choices), required=True)
@click.argument('arg1', required=False)
@click.argument('arg2', required=False)
@pass_options
def app(opts, aspect, arg1, arg2, force):
    """Generates a new aspect of your project in the named app.
    The aspect is generated inside the given application using name as a parameter

    \b
    Supported aspects:
    * `store`: interface to the services and container for logic
    * `view`: highlivel UI component using a store
    * `panel`: container for other panels or controls
    * `control`: A ui type for a defines use case
    * `helper`: helper module to collect computing operations
    * `service`: creates a native service using qt services
    * `interface`: creates an interface inside a qt service
    """
    _log.info('generate')
    path = Path('apps')
    opts.log('generate aspect %s in project %s', aspect, click.format_filename(path))
    g = Generator(path=here / 'templates/generate', workspace=opts.workspace, force=force)
    g.destination = opts.workspace
    if aspect == 'view':
        g.context.update({'app': arg1, 'name': arg2})
        g.write('ui/apps/{{app}}/views/{{name}}View.qml', 'view/View.qml')
    elif aspect == 'store':
        g.context.update({'app': arg1, 'name': arg2})
        g.write('ui/apps/{{app}}/stores/{{name}}Store.qml', 'store/Store.qml')
        if arg2 is not 'Root':
            g.patch('ui/apps/{{app}}/stores/RootStore.qml', 'property {{name}}Store {{name|lower}}Store: {{name}}Store { }')
    elif aspect == 'panel':
        g.context.update({'app': arg1, 'name': arg2})
        g.write('ui/apps/{{app}}/panels/{{name}}Panel.qml', 'panel/Panel.qml')
    elif aspect == 'control':
        g.context.update({'app': arg1, 'name': arg2})
        g.write('ui/apps/{{app}}/controls/{{name}}Control.qml', 'control/Control.qml')
    elif aspect == 'helper':
        g.context.update({'app': arg1, 'name': arg2})
        g.write('ui/apps/{{app}}/helpers/{{name}}Helper.js', 'helper/Helper.js')
    elif aspect == 'plugin':
        name = arg1.replace('.', '_').lower()
        g.context.update({'name': name, 'uri': arg1})
        g.write('native/plugins/{{name}}/{{name}}.pro', 'plugin/plugin.pro')
        g.write('native/plugins/{{name}}/plugin.h', 'plugin/plugin.h')
        g.write('native/plugins/{{name}}/plugin.cpp', 'plugin/plugin.cpp')
        g.patch('native/plugins/plugins.pro', 'SUBDIRS += {{name}}')
    elif aspect == 'service':
        id = arg1.replace('.', '_').lower()
        module = arg1.rsplit('.')[-1]
        g.context.update({'name': arg2, 'uri': arg1, 'id': id, 'module': module})
        # initial
        click.secho('write initial service ..', fg='blue')
        g.write('native/services/interfaces/{{id}}.qface', 'service/interface/interface.qface')
        g.write('native/services/{{id}}/{{id}}.pro', 'service/service.pro')
        g.patch('native/services/services.pro', 'SUBDIRS += {{id}}')
        g.patch('native/services/services.pro', 'OTHER_FILES += interfaces/{{id}}.qface')
        # frontend
        click.secho('write frontend library...', fg='blue')
        g.write('native/services/{{id}}/frontend/frontend.pro', 'service/frontend/frontend.pro')
        # plugin
        click.secho('write qml-plugin...', fg='blue')
        g.write('native/services/{{id}}/plugin/plugin.pro', 'service/plugin/plugin.pro')
        g.write('native/services/{{id}}/plugin/plugin.h', 'service/plugin/plugin.h')
        g.write('native/services/{{id}}/plugin/plugin.cpp', 'service/plugin/plugin.cpp')
        g.write('native/services/{{id}}/plugin/qmldir', 'service/plugin/qmldir')
        # backend
        click.secho('write custom backend ivi-plugin..', fg='blue')
        g.write('native/services/{{id}}/backend/backend.pro', 'service/backend/backend.pro')
        g.write('native/services/{{id}}/backend/plugin.h', 'service/backend/plugin.h')
        g.write('native/services/{{id}}/backend/plugin.cpp', 'service/backend/plugin.cpp')
        g.write('native/services/{{id}}/backend/{{module|lower}}.json', 'service/backend/plugin.json')
        # g.write('native/services/{{id}}/backend/counterbackend.cpp', 'service/backend/backend.cpp')
        # g.write('native/services/{{id}}/backend/counterbackend.h', 'service/backend/backend.h')
        # backend_simu
        click.secho('write simulation backend ivi-plugin...', fg='blue')
        g.write('native/services/{{id}}/backend_simu/backend_simu.pro', 'service/backend_simu/backend_simu.pro')
        g.write('native/services/{{id}}/backend_simu/plugin_resource.qrc', 'service/backend_simu/plugin_resource.qrc')
        g.write('native/services/{{id}}/backend_simu/simulation.qml', 'service/backend_simu/simulation.qml')
        # backend_qtro
        click.secho('write qtro backend ivi-plugin...', fg='blue')
        g.write('native/services/{{id}}/backend_qtro/backend_qtro.pro', 'service/backend_qtro/backend_qtro.pro')
        # server_qtro
        click.secho('write qtro server executable...', fg='blue')
        g.write('native/services/{{id}}/server_qtro/server_qtro.pro', 'service/server_qtro/server_qtro.pro')
        g.write('native/services/{{id}}/server_qtro/main.cpp', 'service/server_qtro/main.cpp')
        g.write('native/services/{{id}}/server_qtro/server.cpp', 'service/server_qtro/server.cpp')
        g.write('native/services/{{id}}/server_qtro/server.h', 'service/server_qtro/server.h')
    elif aspect == 'interface':
        id = arg1.replace('.', '_').lower()
        module = arg1.rsplit('.')[-1]
        interface = arg2
        g.context.update({'name': arg2, 'uri': arg1, 'id': id, 'module': module, 'interface': interface})
        g.patch('native/services/interfaces/{{id}}.qface', 'interface {{interface}} {\n}')
        g.write('native/services/{{id}}/backend/{{interface|lower}}backend.cpp', 'interface/backend/backend.cpp')
        g.write('native/services/{{id}}/backend/{{interface|lower}}backend.h', 'interface/backend/backend.h')
        g.patch('native/services/{{id}}/backend/backend.pro', 'SOURCES += {{interface|lower}}backend.cpp')
        g.patch('native/services/{{id}}/backend/backend.pro', 'HEADERS += {{interface|lower}}backend.h')
        g.patch(
            'native/services/{{id}}/backend/plugin.cpp',
            '#include "{{interface|lower}}backend.h"',
            "// <interface-includes>"
        )
        g.patch(
            'native/services/{{id}}/backend/plugin.cpp',
            'list << {{module|title}}_{{interface}}_iid;',
            "// <interface-id>"
        )
        g.patch(
            'native/services/{{id}}/backend/plugin.cpp',
            'm_interfaces << new {{interface}}Backend(this);',
            "// <interface-new>"
        )
        g.write('native/services/{{id}}/server_qtro/{{interface|lower}}service.h', 'interface/server_qtro/service.h')
        g.write('native/services/{{id}}/server_qtro/{{interface|lower}}service.cpp', 'interface/server_qtro/service.cpp')
        g.patch(
            'native/services/{{id}}/server_qtro/server_qtro.pro',
            'SOURCES += {{interface|lower}}service.cpp\nHEADERS += {{interface|lower}}service.h\n'
        )
        g.patch(
            'native/services/{{id}}/server_qtro/server.cpp',
            'm_{{interface|lower_first}} = new {{interface}}Service(this);\n    enableService(m_{{interface|lower_first}}, "{{uri}}.{{interface}}");',
            '// <service-list>'
        )
        g.patch(
            'native/services/{{id}}/server_qtro/server.h',
            '#include "{{interface|lower}}service.h"',
            '// <service-includes>'
        )
        g.patch(
            'native/services/{{id}}/server_qtro/server.h',
            '{{interface}}Service* m_{{interface|lower_first}};',
            '// <service-members>'
        )