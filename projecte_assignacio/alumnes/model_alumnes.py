import mongoengine as me

class Alumne(me.Document):
    nom_de_usuari: str = me.StringField(required=True)
    nom_i_cognoms: str = me.StringField(required=True)
    grup: str = me.StringField(required=True)
    poblacio: str = me.StringField(required=True)
    mobilitat: str = me.StringField(required=True)
    tipo_de_practica: str =  me.StringField(required=False)
    preferencies: dict = me.DictField(required=False)
    accedeix_a_fct: str = me.StringField(required=False)
    observacions: str = me.StringField(required=False)
    aporta_empresa: str = me.StringField(required=False)
    erasmus: str = me.StringField(required=False)
    distancies: list[dict[str, str, float]] = me.ListField(required=False)
    assignacio: dict[str, str, str] = me.DictField(requiered=False)