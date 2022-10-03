#################################################################################
## Autor: David Fernández Fuster                                               ##
## Data: 09/09/2022                                                            ## 
## Funció: Compila l'aplicació amb la configuració i extensions especficades.  ##
#################################################################################

###########
## Flask ##
###########
from flask import Flask

################
## Extensions ##
################
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_session import Session
from flask_assets import Environment

############
## Worker ##
############
from celery import Celery

################################
## Llibreries d'Accés Global ##
################################
db = MongoEngine()
r = FlaskRedis()
login_manager = LoginManager()
sess = Session()
celery = Celery(
    __name__, 
    broker='redis://localhost:6379/0', 
    result_backend='redis://localhost:6379/0'
)

def init_app(configuracio: str) -> Flask:
    """Inicialitza el nucli de l'aplicació.

    Args:
        configuracio (str): Mode de configuració seleccionat.

    Returns:
        Flask: Aplicació Flask compilada.
    """
    app: Flask = Flask(__name__, instance_relative_config=False)
    app.config.from_object(configuracio)
    assets = Environment()

    ###############################
    # Inicialització d'Extensions #
    ###############################
    db.init_app(app)
    r.init_app(app)
    assets.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)
    ###############################
    ###############################

    with app.app_context():
        #####################
        # Inclusió de Rutes #
        #####################
        from .usuaris import sessio, rutes_usuaris as usuaris
        from .alumnes import rutes_alumnes as alumnes
        from .professors import rutes_professors as professors
        from .empreses import rutes_empreses as empreses
        from .assignacions import rutes_assignacions as assignacions
        from .assets import compilar_actius_estatics
        from . import rutes
        ############################################################
        ############################################################
            
        ####################
        # Registrar Mòduls #
        ####################
        app.register_blueprint(usuaris.usuaris_bp)
        app.register_blueprint(alumnes.alumnes_bp)
        app.register_blueprint(professors.professors_bp)
        app.register_blueprint(empreses.empreses_bp)
        app.register_blueprint(assignacions.assignacions_bp)
        ####################################################
        ####################################################

        compilar_actius_estatics(assets)
        return app
    ## with
## ()
####################################
####################################