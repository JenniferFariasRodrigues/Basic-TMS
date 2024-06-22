from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('index.html')

    # Blueprints or rotes
    with app.app_context():
        from .routes import init_app
        init_app(app)

    with app.app_context():
        from .swagger import blueprint as swagger_blueprint
        app.register_blueprint(swagger_blueprint)
    return app
