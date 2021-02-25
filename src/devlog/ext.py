from flask_assets import Environment
from flask_babel import Babel
from flask_flatpages import FlatPages
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .utils.cache import DevlogCache as Cache

assetenv = Environment()
babel = Babel()
csrf = CSRFProtect()
login_manager = LoginManager()
pages = FlatPages()
cache = Cache()
