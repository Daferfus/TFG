import mongoengine as me

class Empresa(me.Document):
    nom = me.StringField(required=True)
    poblacio = me.StringField(required=True)
    telefon = me.IntField(required=False)
    correu = me.StringField(required=False)
    persona_de_contacte =  me.StringField(required=False)
    practiques = me.ListField(required=False)
    assignacions = me.ListField(required=False)