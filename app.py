from flask import Flask

from contract_manager.config import Config
from controllers import register_controllers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_controllers(app)

    return app


app = create_app()
