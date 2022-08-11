#################################################################################
## Autor: David Fernández Fuster                                               ##
## Data: 11/08/2022                                                            ## 
## Funció: Conté les rutes que desencandenen accions sobre la pàgina de inici. ##
#################################################################################

from flask import current_app as app, render_template

#################
##  Funcions  ###
#################
@app.route('/prova', methods=["GET"])
def provar_funcionament_de_flask() -> str:
    """Funció de prova per a verificar el funcionament de l'aplicació.

    Returns:
        str: Cadena de text de verificació.
    """
    return 'Hola Món!'
## ()

@app.route('/', methods=["GET"])
def mostrar_pagina_de_inici() -> str:
    """Mostra la pàgina de inici.

    Returns:
        str: Pàgina de inici.
    """
    return render_template(
        'home.jinja2',
        titol="Projecte d'Assignació",
        descripcio="Resolució d'un problema d'assignació d'alumne i professors a pràctiques d'empresa."
    )
## ()
#######################################################################################################
#######################################################################################################