import mongoengine as me

class Empresa(me.Document):
    nom: str = me.StringField(required=True)
    poblacio: str = me.StringField(required=True)
    telefon: int = me.IntField(required=False)
    correu: str = me.StringField(required=False)
    persona_de_contacte: str =  me.StringField(required=False)
    practiques: list[dict] = me.ListField(required=False)
    # +[Text] Tutor del Centre
    # +[Buleà] Volen Pràctica
    # +[Text] Titulació
    # +[Text] Descripció
    # +[<Text>] Tecnologíes i Frameworks
    # +[Natural] Total de Pràctiques
    # +[Natural] Pràctiques per Assignar
    assignacions: list[dict] = me.ListField(required=False)