import mongoengine as me

class Professor(me.Document):
    nom_de_usuari: str = me.StringField(required=True)
    nom: str = me.StringField(required=True)
    cognoms: str = me.StringField(required=True)
    titulacions: dict = me.DictField(required=True)
    hores_alliberades: int = me.IntField(required=True)
    hores_restants: int = me.IntField(required=True)
    rati_fct: str =  me.StringField(required=False)
    rati_dual: str = me.StringField(required=False)
    assignacions: list = me.ListField(required=False)