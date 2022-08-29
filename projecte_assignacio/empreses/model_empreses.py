###################
## Base de Dades ##
###################
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Empresa(db.Document):
    nom_de_usuari: str = db.StringField(required=True)
    nom: str = db.StringField(required=True)
    poblacio: str = db.StringField(required=True)
    telefon: int = db.IntField(required=False)
    correu: str = db.StringField(required=False)
    persona_de_contacte: str =  db.StringField(required=False)
    volen_practica: str = db.StringField(required=False)
    practiques: list[dict] = db.ListField(required=False)
    # +[Text] Tutor del Centre
    # +[Buleà] Volen Pràctica
    # +[Text] Titulació
    # +[Text] Descripció
    # +[<Text>] Tecnologíes i Frameworks
    # +[Natural] Total de Pràctiques
    # +[Natural] Pràctiques per Assignar
    assignacions: list[dict] = db.ListField(required=False)