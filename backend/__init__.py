from flask import Flask
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_login import LoginManager

################################
## Llibreries de Accés Global ##
################################
db = MongoEngine()
r = FlaskRedis()
login_manager = LoginManager()

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
    login_manager.init_app(app)
    
    with app.app_context():
        # Include our Routes
        from .usuaris import rutes_usuaris as usuaris
        from .alumnes import rutes_alumnes as alumnes
        from .professors import rutes_professors as professors
        from .empreses import rutes_empreses as empreses
        
        # Register Blueprints
        app.register_blueprint(usuaris.usuaris_bp)
        app.register_blueprint(alumnes.alumnes_bp)
        app.register_blueprint(professors.professors_bp)
        app.register_blueprint(empreses.empreses_bp)

        return app

####################################
####################################