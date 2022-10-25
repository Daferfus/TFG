"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class AssignacionsForm(FlaskForm):
    """Formulari d'assignacions."""

    alumne = SelectField(
        'Alumne',
        [
            DataRequired(),
            
        ]
    )

    professor = SelectField(
        'Professor',
        [
            DataRequired(),
            
        ]
    )

    empresa = SelectField(
        'Empresa',
        [
            DataRequired(),
            
        ]
    )

    submit = SubmitField('Assignar')