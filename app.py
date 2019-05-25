import os
import config
from flask import Flask
from flask_dotenv import DotEnv
from flask_wtf.csrf import CSRFProtect
from models.base_model import db


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'cust_app_web')


app = Flask('Ad Automator', root_path=web_dir)


app.config["TEMPLATES_AUTO_RELOAD"] = True


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()

# https://stackoverflow.com/questions/30521112/how-teardown-request-works-with-python-flask
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
