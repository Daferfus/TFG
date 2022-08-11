#####################################################
## Autor: David Fernández Fuster                   ##
## Data: 11/08/2022                                ## 
## Funció: Conté les rutes centrades en el usuari. ##
#####################################################

################
## Llibreries ##
################
import json


#############
##  Flask  ##
#############
from flask_login import logout_user, current_user
from flask import Blueprint, Response, flash, redirect, request, jsonify, render_template, url_for


##############
##  Mòduls  ##
##############
from projecte_assignacio.usuaris import controlador_usuaris
from projecte_assignacio import login_manager
from projecte_assignacio.usuaris.model_usuaris import Usuari
from .formulari_usuaris import UsuarisForm


############################
## Configuració Blueprint ##
############################
usuaris_bp = Blueprint(
    'usuaris_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


###################################
## Funcions de Retorn de Pàgines ##
###################################
@usuaris_bp.route('/prova', methods=["GET"])
def provar_funcionament_de_flask() -> str:
    """Funció de prova per a verificar el funcionament de l'aplicació.

    Returns:
        str: Cadena de text de verificació.
    """
    return 'Hola Món!'
## ()

@usuaris_bp.route('/', methods=["GET"])
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


@usuaris_bp.route('/inici_de_sessio', methods=["GET", "POST"])
def mostrar_pagina_de_inici_de_sessio() -> str:
    """Mostra la pàgina de inici de sessió.

    Returns:
        str: Pàgina de inici de sessió.
    """
    form: object = UsuarisForm()

    ## Valida que les dades estiguen correctes.
    ## D'estar-ho, es continua en la funció que executa el formulari.
    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        "inici_de_sessio.jinja2",
        form=form,
        template="inici_de_sessio-template"
    )
## ()

#####################################
## Funcions de Retorn de Resposta  ##
#####################################
@usuaris_bp.route('/recuperar_dades_de_usuaris', methods=['GET'])
def iniciar_recerca_de_usuaris() -> Response:
    """Crida a la funció per a obtindre les dades de tots els usuaris.

    Returns:
        Response: Dades de tots els usuaris.
    """
    dades_de_usuaris: list[Usuari] = controlador_usuaris.recuperar_dades_de_usuaris()
    if dades_de_usuaris is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat cap usuari.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_de_usuaris)
        return resposta

@usuaris_bp.route('/recuperar_dades_del_usuari/<string:usuari>', methods=['GET'])
def iniciar_recerca_del_usuari(usuari: str) -> Response:
    """Crida a la funció per a obtindre les dades d'un usuari determinat.

    Args:
        usuari (str): Nom del usuari a buscar.

    Returns:
        Response: Dades del usuari.
    """
    dades_del_usuari: Usuari = controlador_usuaris.recuperar_dades_del_usuari(usuari)
    if dades_del_usuari is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat l'usuari.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_del_usuari)
        return resposta

@usuaris_bp.route('/registrar_usuari', methods=['POST'])
def recollir_dades_usuari() -> Response:
    """Crida a la funció per a registrar un usuari.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom_de_usuari'] 
    contrasenya: str = request.form['contrasenya_de_usuari'] 
    rol: str = request.form['rol_de_usuari'] 
 
    resultat: str = controlador_usuaris.registrar_usuari(
        nom, 
        contrasenya, 
        rol
        )
    if resultat == "L'usuari s'ha registrat amb èxit.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@usuaris_bp.route('/autenticar_usuari', methods=['POST'])
def comprovar_dades_del_usuari() -> Response:
    """Crida a la funció per a autenticar un usuari.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """   
    nom: str = request.form['nom_de_usuari'] 
    contrasenya: str = request.form['contrasenya_de_usuari']
    resultat: str = controlador_usuaris.autenticar_usuari(nom, contrasenya)
    
        
    if resultat == "Usuari autenticat.":
        resposta: Response = jsonify(success=True, message=resultat)
        #return resposta
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.mostrar_pantalla_de_inici_de_sessio'))
        #return resposta

@usuaris_bp.route('/logout', methods=['GET'])
def logout() -> Response:
    """Tanca la sessió del usuari actual.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    logout_user()

    if current_user.is_authenticated:
        resposta: Response = jsonify(success=False, message="No s'ha tancat la sessió amb èxit.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        # return resposta
    else:
        resposta: Response = jsonify(success=True, message="S'ha tancat la sessió amb èxit.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        return redirect(url_for('usuaris_bp.home'))
        #return resposta

@usuaris_bp.route('/actualitzar_usuari/<string:usuari>', methods=["PUT"])
def recollir_nom_de_usuari(usuari: str) -> Response:
    """Crida a la funció per a actualitzar un usuari donat.

    Args:
        usuari (str): Usuari a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom_de_usuari'] 
    contrasenya: str = request.form['contrasenya_de_usuari'] 
    rol: str = request.form['rol_de_usuari'] 
 
    resultat: str = controlador_usuaris.actualitzar_credencials_del_usuari(
        usuari,
        nom, 
        contrasenya, 
        rol
        )

    if resultat=="L'usuari ha sigut actualitzat.":
        resposta: Response = jsonify(success=True, message=resultat)
    else:
        resposta: Response = jsonify(success=False, message=resultat)
    return resposta

@usuaris_bp.route('/esborrar_usuaris', methods=['DELETE'])
def eliminacio_de_usuaris() -> Response:
    """Crida la funció per a esborrar tots els usuaris.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_usuaris.esborrar_usuaris()

    if resultat == "S'ha esborrat amb èxit tots els usuaris.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(success=False, message=resultat)
        return resposta

@usuaris_bp.route('/esborrar_usuari/<string:usuari>', methods=['DELETE'])
def eliminacio_de_usuari(usuari: str) -> Response:
    """Crida a la funció per a esborrar un usuari determinat.

    Args:
        usuari (str): Usuari a esborrar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_usuaris.esborrar_usuari(usuari)
    
    if resultat == "S'ha esborrat amb èxit l'usuari.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(succes=False, message=resultat)
        return resposta

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


# @login_manager.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash('You must be logged in to view that page.')
#     return redirect(url_for('auth_bp.login'))