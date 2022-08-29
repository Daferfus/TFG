"""Form object declaration."""
from flask_wtf import FlaskForm
from projecte_assignacio.alumnes.formulari_preferencies import PreferenciesASIR, PreferenciesDAM, PreferenciesDAW, PreferenciesTSMR
from wtforms import SearchField, StringField, IntegerField, EmailField, RadioField, SubmitField
from wtforms.validators import DataRequired


class EmpresesForm(FlaskForm):
    """Formulari d'empreses."""

    filtrar = SearchField(
        'Filtrar'
    )

    nom = StringField(
        'Nom',
        [
            DataRequired(),
            
        ]
    )
    poblacio = StringField(
        'Població',
        [
            DataRequired(),
            
        ]
    )

    telefon = IntegerField(
        'Telèfon',
        [
            DataRequired(),
        ]
    )

    correu = EmailField(
        'Correu',
        [
            DataRequired(),
        ]
    )

    nom_de_persona_de_contacte = StringField(
        'Nom de Persona de Contacte',
        [
            DataRequired(),
        ]
    )

    volen_practica = RadioField(
        'Volen Pràctica', 
        choices=[
            ('Sí','Sí'),('No','No')
        ]
    )

    submit = SubmitField('Actualitzar')