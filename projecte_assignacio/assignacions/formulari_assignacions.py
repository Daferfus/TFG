"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import SearchField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AssignacionsForm(FlaskForm):
    """Formulari d'assignacions."""

    filtrar_assignacions = SearchField(
        'Filtrar'
    )

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