import click
import logging
import yaml
from path import Path

_log = logging.getLogger(__name__)

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


logger = logging.getLogger(__name__)


class RuleReader(object):
    def __init__(self):
        pass

    def process_rules(self, path):
        document = self.load_yaml(path)
        for module, rules in document.items():
            click.secho('process: {0}'.format(module), fg='green')

    def load_yaml(self, path):
        path = Path(path)
        if not path.exists():
            click.secho('yaml document does not exists: {0}'.format(path), fg='red', err=True)
            return {}
        try:
            return yaml.safe_load(path.text(), Loader=Loader)
        except yaml.YAMLError as exc:
            source = path
            if hasattr(exc, 'problem_mark'):
                source = '{0}:{1}'.format(source, exc.problem_mark.line + 1)
            click.secho('{0}: error: {1}'.format(source, str(exc)), fg='red', err=True)

        return {}
