"""Form object declaration."""
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
            message=('La contrassenya ha de tindre un mínim de 8 caràcters.'))
        ]
    )
    
    submit = SubmitField('Iniciar Sessió')