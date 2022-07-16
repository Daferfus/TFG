import mongoengine as me

class Alumne(me.Document):
    nom_i_cognoms = me.StringField(required=True)
    grup = me.StringField(required=True)
    poblacio = me.StringField(required=True)
    mobilitat = me.StringField(required=True)
    tipo_de_practica =  me.StringField(required=False)
    preferencies = me.DictField(required=True)
    observacions = me.StringField(required=False)
    aporta_empresa = me.BooleanField(required=False)
    erasmus = me.BooleanField(required=False)
    distancies = me.ListField(required=False)
    assignacio = me.DictField(requiered=False)