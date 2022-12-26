"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import SearchField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AssignacionsForm(FlaskForm):
    """Formulari d'assignacions."""

    filtrar_assignacions = SearchField(
        'Filtrar'
    )
    ver = RadioField(
        'Ver', 
        choices=[
            ('Tots','Tots'),('No Assignats','No Assignats')
        ]
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