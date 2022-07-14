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
        import backend.routes
        
        # Register Blueprints
        #app.register_blueprint(auth.auth_bp)
        #app.register_blueprint(admin.admin_bp)

        return app

####################################
####################################