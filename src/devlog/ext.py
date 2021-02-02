from flask_assets import Environment
from flask_babel import Babel
from flask_caching import Cache
from flask_flatpages import FlatPages

assetenv = Environment()
babel = Babel()
pages = FlatPages()
cache = Cache()
