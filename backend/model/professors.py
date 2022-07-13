import mongoengine as me

class Professor(me.Document):
    nom = me.StringField(required=True)
    cognoms = me.StringField(required=True)
    titulacions = me.DictField(required=True)
    hores_alliberades = me.IntField(required=True)
    hores_restants = me.IntField(required=True)
    rati_fct =  me.StringField(required=False)
    rati_dual = me.StringField(required=False)
    assignacions = me.ListField(required=False)