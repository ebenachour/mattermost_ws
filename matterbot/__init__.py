from flask import Flask
from matterbot.views import bot


def create_app():
    app = Flask(__name__)
    # existing code omitted
    app.register_blueprint(bot)
    return app
