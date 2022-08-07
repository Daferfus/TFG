"""Form object declaration."""
from flask_wtf import FlaskForm
from projecte_assignacio.professors.formulari_ajustos import AjustosDUAL, AjustosFCT
from wtforms import StringField, IntegerField, SubmitField, Field, widgets, FormField
from wtforms.validators import DataRequired


class TagListField(Field):
    widget = widgets.TextInput()
    def _value(self):
        if self.data:
            return ', '.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

class BetterTagListField(TagListField):
    def __init__(self, label=None, validators=None, remove_duplicates=True, **kwargs):
        super(BetterTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item

class ProfessorsForm(FlaskForm):
    """Formulari de pràctiques."""

    nom = StringField(
        'Nom',
        [
            DataRequired(),
            
        ]
    )
    cognoms = StringField(
        'Cognoms',
        [
            DataRequired(),
            
        ]
    )

    titulacions = BetterTagListField(
        'Titulacions',
        [
            DataRequired(),
        ]
    )

    hores_alliberades_setmanalment = IntegerField(
        'Hores Alliberades Setmanalment'
    )

    ajustos_fct = FormField(AjustosFCT)
    ajustos_dual = FormField(AjustosDUAL)
    
    submit = SubmitField('Submit')