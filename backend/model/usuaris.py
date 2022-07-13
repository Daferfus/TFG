import mongoengine as me

class Usuari(me.Document):
    nom = me.StringField(required=True)
    contrasenya = me.StringField(required=True)
    rol = me.StringField(required=True)