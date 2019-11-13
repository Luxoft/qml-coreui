import logging
import sys
from path import Path
from jinja2 import Environment, Undefined, StrictUndefined
from jinja2 import FileSystemLoader, ChoiceLoader
from jinja2 import TemplateSyntaxError, TemplateNotFound, TemplateError
from jinja2 import Template
import click
from .filters import get_filters
import hashlib
from . import shell
from . import options

logger = logging.getLogger(__name__)



def template_error_handler(traceback):
    exc_type, exc_obj, exc_tb = traceback.exc_info
    error = exc_obj
    if isinstance(exc_type, TemplateError):
        error = exc_obj.message
    message = '{0}:{1}: error: {2}'.format(exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, error)
    options.warning(message)


class TestableUndefined(StrictUndefined):
    """Return an error for all undefined values, but allow testing them in if statements"""

    def __bool__(self):
        return False


class Generator(object):
    strict = True

    def __init__(self, path, context={}, workspace=Path.getcwd(), force=False):
        loader = ChoiceLoader([
            FileSystemLoader(path),
        ])
        self.template_folder = Path(path)
        self.env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,

        )
        self.env.exception_handler = template_error_handler
        self.env.filters.update(get_filters())
        self._destination = Path()
        self._source = ''
        self.context = context
        self.workspace = workspace
        self.force = force

    @property
    def destination(self):
        """destination prefix for generator write"""
        return self._destination

    @destination.setter
    def destination(self, dst):
        if dst:
            self._destination = Path(self.apply(dst, self.context))

    @property
    def source(self):
        """source prefix for template lookup"""
        return self._source

    @source.setter
    def source(self, source):
        if source:
            self._source = source

    @property
    def filters(self):
        return self.env.filters

    @filters.setter
    def filters(self, filters):
        self.env.filters.update(filters)

    def apply(self, template, context):
        """Return the rendered text of a template instance"""
        return self.env.from_string(template).render(context)

    def render(self, name, context):
        """Returns the rendered text from a single template file from the
        template loader using the given context data"""
        if Generator.strict:
            self.env.undefined = TestableUndefined
        else:
            self.env.undefined = Undefined
        template = self.get_template(name)
        return template.render(context)

    def get_template(self, name):
        """Retrieves a single template file from the template loader"""
        source = name
        # remove leading '/'
        if name.startswith('/'):
            source = name[1:]
        # prepend source
        elif self.source:
            source = '/'.join((self.source, name))
        return self.env.get_template(source)

    def write_all(self, paths, force=True):
        for path in paths:
            self.write(path, force=force)

    def write(self, file_path, template=None, context={}, preserve=False, force=False):
        """Using a template file name it renders a template
           into a file given a context
        """
        force = self.force or force
        template = template or file_path
        if not context:
            context = self.context
        error = False
        try:
            self._write(file_path, template, context, preserve, force)
        except TemplateSyntaxError as exc:
            message = '{0}:{1}: error: {2}'.format(exc.filename, exc.lineno, exc.message)
            options.warning(message)
            error = True
        except TemplateNotFound as exc:
            message = '{0}: error: Template not found'.format(exc.name)
            options.warning(message)
            error = True
        except TemplateError as exc:
            # Just return with an error, the generic template_error_handler takes care of printing it
            error = True

        if error and Generator.strict:
            sys.exit(1)

    def _write(self, file_path, template, context, preserve=False, force=False):
        file_path = Path(self.apply(file_path, context))
        path = self.destination / file_path
        shell.makedirs(path.parent, silent=True)
        logger.info('write {0}'.format(path))
        data = self.render(template, context)
        if path.exists() and not force:
            options.info('SKIP {} file exists'.format(Path.getcwd().relpathto(path)))
        elif self._has_different_content(data, path):
            if path.exists() and preserve and not force:
                options.echo('preserve {0}'.format(self.workspace.relpathto(path)))
            else:
                if options.dry_run():
                    options.info('DRY WRITE: {0}'.format(self.workspace.relpathto(path)))
                else:
                    options.info('WRITE: {0}'.format(self.workspace.relpathto(path)))
                    path.open('w', encoding='utf-8').write(data)

    def _has_different_content(self, data, path):
        if not path.exists():
            return True
        dataHash = hashlib.new('md5', data.encode('utf-8')).digest()
        pathHash = path.read_hash('md5')
        return dataHash != pathHash

    def register_filter(self, name, callback):
        """Register your custom template filter"""
        self.env.filters[name] = callback

    def patch(self, path, text, marker=None, ctx={}):
        self.context.update(ctx)
        path = self.apply(path, self.context)
        return Patcher(self.env, self.destination / path).patch(text, marker, self.context)


class Patcher(object):
    def __init__(self, env, path):
        self.env = env
        self.path = Path(path)

    def patch(self, template, marker=None, ctx={}):
        data = self.env.from_string(template).render(ctx).strip()
        if options.dry_run():
            options.info('DRY: PATCH {} with {}'.format(self.path, data))
            return
        if not self.path.exists():
            options.warning('document to patch does not exists: {}'.format(self.path))
            return
        body = self.path.text()
        if data in body:
            options.warning('{} is already patched'.format(self.path))
            return
        if marker:
            patched = self.patchMarker(body, data, marker)
        elif self.path.ext in ('.qml',):
            patched = self.patchLast(body, data, '}')
        elif self.path.ext in ('.pro', '.pri', '.qface'):
            patched = self.patchAppend(body, data)
        else:
            options.warning('unknown file format for patching')
            return
        options.info('PATCH {} with {}'.format(self.path, data))
        self.path.write_text(patched)

    def patchLast(self, text, data, sep='}'):
        a, b = text.rsplit(sep, 1)
        return "{}    {}\n{}{}".format(a, data, sep, b)

    def patchAppend(self, text, data):
        text = text.rstrip()
        return "{}\n\n{}".format(text, data)

    def patchMarker(self, text, data, marker):
        lines = []
        success = False
        for line in text.splitlines():
            lines.append(line)
            if marker in line:
                indent = (len(line) - len(line.lstrip())) * ' '
                lines.append(indent + data)
                success = True
        if not success:
            options.warning("unable to find marker {}".format(marker))
        return "\n".join(lines)



