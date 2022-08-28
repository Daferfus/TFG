##############################################################
## Autor: David Fernández Fuster                            ##
## Data: 12/08/2022                                         ## 
## Funció: Conté els camps del formulari d'inici de sessió. ##
##############################################################

################################
## Llibreríes de Formularis.  ##
################################
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class UsuarisForm(FlaskForm):
    """Formulari d'usuaris."""

    nom = StringField(
        'Usuari',
        [DataRequired()]
    )
    
    contrasenya = PasswordField(
        'Contrasenya',
        [
            DataRequired(),
            Length(min=8,
            message=('La contrasenya ha de tindre un mínim de 8 caràcters.'))
        ]
    )
    
    submit = SubmitField('Iniciar Sessió')
## class
##############################################################
##############################################################