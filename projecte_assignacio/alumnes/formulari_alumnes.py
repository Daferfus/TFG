"""Form object declaration."""
from flask_wtf import FlaskForm
from projecte_assignacio.alumnes.formulari_preferencies import PreferenciesASIR, PreferenciesDAM, PreferenciesDAW, PreferenciesTSMR
from wtforms import StringField, RadioField, FormField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AlumnesForm(FlaskForm):
    """Formulari d'alumnes."""

    nom_i_cognoms = StringField(
        'Nom i Cognoms',
        [
            DataRequired(),
            
        ]
    )
    ciutat_de_residencia = StringField(
        'Ciutat de Residencia',
        [
            DataRequired(),
            
        ]
    )

    disponibilitat_de_cotxe = RadioField(
        'Disponibilitat de Cotxe', 
        choices=[
            ('Sí','Sí'),('No','No')
        ]
    )

    preferencies_asir = FormField(PreferenciesASIR)
    preferencies_tsmr = FormField(PreferenciesTSMR)
    preferencies_dam = FormField(PreferenciesDAM)
    preferencies_daw = FormField(PreferenciesDAW)
    
    observacions = TextAreaField(
        'Observacions',
        render_kw={'rows': 15, 'cols': 50}
    )

    submit = SubmitField('Submit')