from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from celery import Celery

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

celery = Celery("banking_system", broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import routes, models, errors
