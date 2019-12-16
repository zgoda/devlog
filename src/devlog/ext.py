from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from .utils.models import Model

login_manager = LoginManager()
babel = Babel()
db = SQLAlchemy(model_class=Model)
csrf = CSRFProtect()
