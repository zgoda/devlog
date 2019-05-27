from .app import make_app  # noqa

from ._version import get_version
__version__ = get_version()
del get_version
