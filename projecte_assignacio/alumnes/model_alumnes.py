import mongoengine as me

class Alumne(me.Document):
    nom_i_cognoms: str = me.StringField(required=True)
    grup: str = me.StringField(required=True)
    poblacio: str = me.StringField(required=True)
    mobilitat: str = me.StringField(required=True)
    tipo_de_practica: str =  me.StringField(required=False)
    preferencies: dict = me.DictField(required=True)
    observacions: str = me.StringField(required=False)
    aporta_empresa: bool = me.BooleanField(required=False)
    erasmus: bool = me.BooleanField(required=False)
    distancies: list[dict[str, str, float]] = me.ListField(required=False)
    assignacio: dict[str, str, str] = me.DictField(requiered=False)