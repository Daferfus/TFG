import mongoengine as me

class Empresa(me.Document):
    nom: str = me.StringField(required=True)
    poblacio: str = me.StringField(required=True)
    telefon: int = me.IntField(required=False)
    correu: str = me.StringField(required=False)
    persona_de_contacte: str =  me.StringField(required=False)
    practiques: list[dict] = me.ListField(required=False)
    assignacions: list[dict] = me.ListField(required=False)