"""Form object declaration."""
from wtforms import Form, IntegerField


class AjustosFCT(Form):
    quantitat_alumnes = IntegerField(
        "alumne de FCT per cada"
    )
    hores_alliberades = IntegerField(
        "hores alliberades"
    )

class AjustosDUAL(Form):
    quantitat_alumnes = IntegerField(
        "alumne de FCT per cada"
    )
    hores_alliberades = IntegerField(
        "hores alliberades"
    )
 
