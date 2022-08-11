from flask import Response, flash, redirect, url_for


from projecte_assignacio import login_manager
from projecte_assignacio.usuaris.model_usuaris import Usuari

#########################
## Funcions de Sessió  ##
#########################
@login_manager.user_loader
def load_user(id_de_usuari: str) -> Usuari:
    """Cada volta que l'usuari accedeix a una ruta, manté la seua sessió iniciada.

    Args:
        id_de_usuari (str): El nombre d'identificació de l'usuari en la base de dades.

    Returns:
        Usuari: El usuari actual.
    """
    if id_de_usuari is not None:
        return Usuari.objects(pk=id_de_usuari).first()
    return None


@login_manager.unauthorized_handler
def unauthorized() -> Response:
    """Redirigix als usuaris no autoritzats a la pàgina d'inici de sessió.

    Returns:
        Response: Pàgina d'inici de sessio.
    """
    flash('Tens que estar autenticat per a accedir a la pàgina.')
    return redirect(url_for('usuaris_bp.mostrar_pagina_de_inici_de_sessio'))