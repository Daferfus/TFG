"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class UsuarisForm(FlaskForm):
    """Formulari d'usuaris."""
    nom_de_usuari = StringField(
        'Usuari',
        [DataRequired()]
    )
    contrasenya_de_usuari = PasswordField(
        'Contrasenya',
        [
            DataRequired(),
            Length(min=8,
            message=('La contrassenya ha de tindre un mínim de 8 caràcters.'))
        ]
    )
    submit = SubmitField('Submit')