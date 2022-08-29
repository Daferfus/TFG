###################
## Base de Dades ##
###################
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Professor(db.Document):
    nom_de_usuari: str = db.StringField(required=True)
    nom: str = db.StringField(required=True)
    cognoms: str = db.StringField(required=True)
    titulacions: dict = db.DictField(required=True)
    hores_alliberades: int = db.IntField(required=True)
    hores_restants: int = db.IntField(required=True)
    rati_fct: str =  db.StringField(required=False)
    rati_dual: str = db.StringField(required=False)
    assignacions: list = db.ListField(required=False)