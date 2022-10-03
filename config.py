######################################################
## Autor: David Fernández Fuster                    ##
## Data: 09/09/2022                                 ## 
## Funció: Conté els paràmetres de configuració     ##
##         sobre els que es compilarà l'aplicació.  ##
######################################################

##############################################
## Llibreries per accedir al fitxer '.env'. ##
##############################################
import redis
from os import environ, path
from dotenv import load_dotenv
##############################################
##############################################

arrel = path.abspath(path.dirname(__file__))
load_dotenv(path.join(arrel, '.env'))

class Config:
    """Configuració compartida entre els distints modes de configuració.
    """
    SECRET_KEY = environ.get('SECRET_KEY') ## Clau secreta per al xifrat de contrassenyes.
    
    ##############################################
    ## Carpetes amb els recursos FrontEnd base. ##
    ##############################################
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    ##############################################
    ##############################################

    # Flask-Session
    SESSION_TYPE = environ.get('SESSION_TYPE')
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

    LESS_BIN = 'lessc' ## Programa per la compilació modularitzada d'estils.
    ASSETS_AUTO_BUILD = True ## Sempre que l'aplicació s'execute es compilaràn els estils.
## class    

class ProdConfig(Config):
    """Mode Producció.

    Args:
        Config (class): Configuració Base.
    """
    #FLASK_ENV = 'production'
    FLASK_ENV = 'development'
    DEBUG = False
    ASSETS_DEBUG = False
    TESTING = False
    
    ###############################
    ## Base de Dades Persistent. ##
    ###############################
    MONGODB_SETTINGS = {
        "db": environ.get('PROD_MONGO_DB'),
        "host": environ.get('PROD_MONGO_URI')
    }
    ###############################
    ###############################
    
    ############################
    ## Execució en Segón Pla. ##
    ##       (Worker)         ##
    ############################
    CELERY_CONFIG={
        'broker_url': 'redis://localhost:6379/0', ## Base de dades per a emmagatzemar el missatges.
        'result_backend': 'redis://localhost:6379/0', ## Base de dades on s'emmatgatzemen els resultats.
    }
    ###########################
    ###########################
## class

class DevConfig(Config):
    """Mode Desenvolupament.

    Args:
        Config (class): Configuració Base.
    """
    FLASK_ENV = 'development'
    DEBUG = True
    ASSETS_DEBUG = True
    TESTING = True

    ##################################
    ## Base de Dades no Persistent. ##
    ##################################
    MONGODB_SETTINGS = {
        "db": environ.get('DEV_MONGO_DB'),
        "host": environ.get('DEV_MONGO_URI')
        }
    ##################################
    ##################################

    ############################
    ## Execució en Segón Pla. ##
    ##       (Worker)         ##
    ############################
    CELERY_CONFIG={
        'broker_url': 'redis://localhost:6379/0', ## Base de dades per a emmagatzemar els missatges.
        'result_backend': 'redis://localhost:6379/0', ## Base de dades on s'emmatgatzemen els resultats.
    }
    ###########################
    ###########################
## class