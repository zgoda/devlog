from flask_assets import Environment
from flask_babel import Babel
from flask_flatpages import FlatPages

from .utils.cache import DevlogCache as Cache

assetenv = Environment()
babel = Babel()
pages = FlatPages()
cache = Cache()
