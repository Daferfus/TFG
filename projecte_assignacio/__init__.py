from flask import Flask
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_session import Session
from flask_assets import Environment  # Import `Environment`
from celery import Celery

################################
## Llibreries de Accés Global ##
################################
db = MongoEngine()
r = FlaskRedis()
login_manager = LoginManager()
sess = Session()
celery = Celery(__name__, broker='redis://localhost:6379/0', result_backend='redis://localhost:6379/0')

def init_app(configuracio):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(configuracio)
    assets = Environment()  # Create an assets environment

    # Initialize Plugins
    db.init_app(app)
    r.init_app(app)
    assets.init_app(app)  # Initialize Flask-Assets
    login_manager.init_app(app)
    sess.init_app(app)
    
    with app.app_context():
        # Include our Routes
        from .usuaris import sessio, rutes_usuaris as usuaris
        from .alumnes import rutes_alumnes as alumnes
        from .professors import rutes_professors as professors
        from .empreses import rutes_empreses as empreses
        from .assignacions import rutes_assignacions as assignacions
        from .assets import compile_static_assets
        from . import rutes
        
        # Register Blueprints
        app.register_blueprint(usuaris.usuaris_bp)
        app.register_blueprint(alumnes.alumnes_bp)
        app.register_blueprint(professors.professors_bp)
        app.register_blueprint(empreses.empreses_bp)
        app.register_blueprint(assignacions.assignacions_bp)

        # Compile static assets
        compile_static_assets(assets)  # Execute logic
        return app

####################################
####################################