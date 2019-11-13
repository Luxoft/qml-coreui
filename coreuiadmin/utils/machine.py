import platform
import logging

_log = logging.getLogger(__name__)

is_linux = platform.system() == 'Linux'
is_macos = platform.system() == 'Darwin'
