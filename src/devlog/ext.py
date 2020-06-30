from flask_assets import Bundle, Environment
from flask_babel import Babel
from flask_flatpages import FlatPages

babel = Babel()
pages = FlatPages()
assets = Environment()

_css = Bundle(
    'css/app.css', 'css/pgm_friendly.css', 'vendor/normalize.css',
    filters='cssmin', output='gen/packed.css',
)
assets.register('app_css', _css)
