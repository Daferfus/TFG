##########################################################################
## Autor: David Fernández Fuster                                        ##
## Data: 13/08/2022                                                     ## 
## Funció: Conté les rutes que desencandenen accions sobre els alumnes. ##
##########################################################################

###################
## Base de Dades ##
###################
from flask_mongoengine import MongoEngine

db = MongoEngine()
class Alumne(db.Document):
    nom_de_usuari: str = db.StringField(required=True)
    nom_i_cognoms: str = db.StringField(required=True)
    grup: str = db.StringField(required=True)
    poblacio: str = db.StringField(required=True)
    mobilitat: str = db.StringField(required=True)
    tipo_de_practica: str =  db.StringField(required=False)
    preferencies: dict = db.DictField(required=False)
    accedeix_a_fct: str = db.StringField(required=False)
    observacions: str = db.StringField(required=False)
    aporta_empresa: str = db.StringField(required=False)
    erasmus: str = db.StringField(required=False)
    distancies: list[dict[str, str, float]] = db.ListField(required=False)
    assignacio: dict[str, str, str] = db.DictField(requiered=False)
## class
##########################################################################
##########################################################################