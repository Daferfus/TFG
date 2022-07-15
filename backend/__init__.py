from flask import Flask
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis

################################
## Llibreries de Accés Global ##
################################
db = MongoEngine()
r = FlaskRedis()

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # Using a production configuration
    #app.config.from_object('config.ProdConfig')

    # Using a development configuration
    app.config.from_object('config.DevConfig')


    # Initialize Plugins
    db.init_app(app)
    r.init_app(app)
    
    with app.app_context():
        # Include our Routes
        from . import routes
        from .usuaris import routes as usuaris
        from .alumnes import routes as alumnes
        from .professors import routes as professors
        from .empreses import routes as empreses
        
        # Register Blueprints
        app.register_blueprint(usuaris.usuaris_bp)
        app.register_blueprint(alumnes.alumnes_bp)
        app.register_blueprint(professors.professors_bp)
        app.register_blueprint(empreses.empreses_bp)

        return app

####################################
####################################