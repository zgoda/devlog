import os

from devlog import make_app

application = make_app(os.environ.get("ENV"))
