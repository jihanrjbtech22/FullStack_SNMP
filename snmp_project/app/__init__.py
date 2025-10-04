from flask import Flask
import os

def create_app():
    # Get the absolute path to the templates directory
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    app = Flask(__name__, template_folder=template_dir)

    from .routes import main
    app.register_blueprint(main)

    return app
