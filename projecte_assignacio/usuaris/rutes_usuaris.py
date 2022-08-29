##########################################################################
## Autor: David Fernández Fuster                                        ##
## Data: 11/08/2022                                                     ## 
## Funció: Conté les rutes que desencandenen accions sobre els usuaris. ##
##########################################################################

################
## Llibreries ##
################
import json


#############
##  Flask  ##
#############
from flask_login import login_user, logout_user, current_user
from flask import current_app as app, Blueprint, Response, flash, redirect, request, jsonify, render_template, url_for
from munch import DefaultMunch

##############
##  Mòduls  ##
##############
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
@usuaris_bp.route('/inici_de_sessio', methods=["GET"])
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
##############################################################
##############################################################

######################################
## Funcions de Retorn d'Informació  ##
######################################
@usuaris_bp.route('/usuaris', methods=['GET'])
def obtindre_dades_de_usuaris() -> list[Usuari]:
    """Retorna una llista d'usuaris.

    Returns:
        list[Usuari]: Llista d'usuaris.
    """
    dades_de_usuaris: list[Usuari] =  Usuari.objects()
    if len(dades_de_usuaris) > 0:
        resposta: Response = jsonify(
                success=True, 
                message=dades_de_usuaris
                )
        return resposta
    else:
        resposta: Response = jsonify(
            success=False, 
            message=dades_de_usuaris
            )
        return resposta
## ()

@usuaris_bp.route('/usuari/<string:usuari>', methods=['GET'])
def obtindre_dades_del_usuari(usuari: str) -> Usuari:
    """Retorna un usuari donat.

    Args:
        usuari (str): Nom del usuari a retornar.

    Returns:
        Usuari: Usuari a obtindre.
    """
    dades_de_usuari: Usuari|None = Usuari.objects(nom=usuari).first()
    if dades_de_usuari:
        resposta: Response = jsonify(
                success=True, 
                message=dades_de_usuari
                )
        return resposta
    else:
        resposta: Response = jsonify(
            success=False, 
            message=dades_de_usuari
            )
        return resposta
    ## if
## ()
##############################################################
##############################################################

#######################################
## Funcions de Modificació de Dades  ##
#######################################
@usuaris_bp.route('/registrar', methods=['POST'])
def registrar_usuari() -> Response:
    """Inserta un usuari en la base de dades de no existir.

    Args:
        nom (str): el nom del usuari.
        contrasenya (str): contrasenya no xifrada del usuari.
        rol (str): rol que tindrà l'usuari en l'aplicació (Alumne, Professor, Empresa o Coordinador)

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    ## Paràmetres POST:
    nom: str = request.form['nom'] 
    contrasenya: str = request.form['contrasenya'] 
    rol: str = request.form['rol'] 

    ## Verificació d'existència:
    resposta: Response = obtindre_dades_del_usuari(nom)
    usuari_existent: Usuari = json.loads(resposta.get_data(as_text=True))["message"]
    if usuari_existent is None:

        ## Inserció:
        usuari: Usuari = Usuari(
            nom=nom, 
            contrasenya=contrasenya, 
            rol=rol
        )
        usuari.establir_contrasenya(contrasenya)
        usuari.save()

        ## Verificació de la inserció:
        usuari_insertat: Usuari = obtindre_dades_del_usuari(nom) 
        if usuari_insertat:
            resposta: Response = jsonify(
                success=True, 
                message="L'usuari "+nom+" s'ha registrat amb èxit."
                )
            return resposta
        else:
            resposta: Response = jsonify(
                success=False, 
                message="Ha ocorregut un problema durant el registre."
                )
            return resposta
        ## if
    else:
        resposta: Response = jsonify(
            success=False, 
            message="Ja existeix un usuari amb aquest nom."
            )
        return resposta
    ## if
## ()

@usuaris_bp.route('/autenticar', methods=['POST'])
def autenticar() -> Response:
    """Autentica un usuari.

    Args:
        nom (str): Nom del usuari a autenticar.
        contrasenya (str): Contrasenya del usuari a autenticar.
       
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    ## Paràmetres POST:
    nom: str = request.form['nom'] 
    contrasenya: str = request.form['contrasenya']
    
    ## Validació:
    usuari: Usuari|None = Usuari.objects(nom=nom).first()
    if usuari and usuari.validar_contraseya(contrasenya=contrasenya):
        login_user(usuari)
        resposta: Response = jsonify(
            success=True, 
            message="Usuari Autenticat."
            )
        if app.config["DEBUG"]:
            return resposta
        else:
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if usuari.rol == "Alumne":
                return redirect(url_for('alumnes_bp.mostrar_perfil'))
            elif usuari.rol == "Professor":
                return redirect(url_for('professors_bp.mostrar_perfil'))
            elif usuari.rol == "Empresa":
                return redirect(url_for('empreses_bp.mostrar_perfil'))
            elif usuari.rol == "Coordinador":
                return redirect(url_for('assignacions_bp.mostrar_panel_de_assignacio'))
    else:
        resposta: Response = jsonify(
            success=False, 
            message="Les credencials no son valides."
            )
        if app.config["DEBUG"]:
            return resposta
        else:
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            return redirect(url_for('usuaris_bp.mostrar_pagina_de_inici_de_sessio'))
    ## if
## ()

@usuaris_bp.route('/tancar_sessio', methods=['GET'])
def tancar_sessio() -> Response:
    """Tanca la sessió de l'usuari actual.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    logout_user()

    ## Validació:
    if current_user.is_authenticated:
        resposta: Response = jsonify(
            success=False, 
            message="No s'ha tancat la sessió amb èxit."
            )
        if app.config["DEBUG"]:
            return resposta
        else:
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            return redirect(url_for('mostrar_pagina_de_inici'))
    else:
        resposta: Response = jsonify(
            success=True, 
            message="S'ha tancat la sessió amb èxit."
            )
        if app.config["DEBUG"]:
            return resposta
        else:
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            return redirect(url_for('mostrar_pagina_de_inici'))
    ## if
## ()


@usuaris_bp.route('/actualitzar_usuari/<string:usuari>', methods=["PUT"])
def actualitzar_usuari(usuari: str) -> Response:
    """Actualitza les dades d'un usuari donat.

    Args:
        usuari (str): nom antic del usuari, per a temes de recerca.
        nom (str): nou nom del usuari.
        contrasenya (str): nova contrasenya del usuari.
        rol (str): nou rol del usuari.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    ## Paràmetres PUT:
    nom: str = request.form['nom'] 
    contrasenya: str = request.form['contrasenya'] 
    rol: str = request.form['rol'] 

    ## Verificació d'existència:
    usuari: Usuari|None = Usuari.objects(nom=usuari).first()
    if usuari:        
        
        ## Actualització:
        usuari.nom = nom
        usuari.establir_contrasenya(contrasenya)
        usuari.rol = rol
        usuari.save()
        
        ## Validació:
        usuari_actualitzat: Usuari = Usuari.objects(nom=nom, rol=rol).first()
        if usuari_actualitzat and usuari.validar_contraseya(contrasenya=contrasenya):
            resposta: Response = jsonify(
                success=True, 
                message="L'usuari ha sigut actualitzat."
                )
            return resposta
        else:
            resposta: Response = jsonify(
                success=False, 
                message="Error al actualitzar."
                )
            return resposta
    else:
        resposta: Response = jsonify(
            success=False, 
            message="L'usuari no existeix."
            )
        return resposta
    ## if
## ()

@usuaris_bp.route('/esborrar_usuaris', methods=['DELETE'])
def esborrar_usuaris() -> Response:
    """Esborra tots els usuaris.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    Usuari.objects.delete()

    ## Validació:
    resultat: Response = obtindre_dades_de_usuaris()
    usuaris: list[Usuari] = json.loads(resultat.get_data())["message"]    
    if len(usuaris) == 0:
        resposta = jsonify(
            success=True, 
            message="S'ha esborrat amb èxit tots els usuaris."
            )
        return resposta
    else:
        resposta = jsonify(
            success=False, 
            message="Ha ocorregut un problema durant el esborrament."
            )
        return resposta
    ## if
## ()

@usuaris_bp.route('/esborrar_usuari/<string:usuari>', methods=['DELETE'])
def esborrar_usuari(usuari: str) -> Response:
    """Esborra un usuari donat.

    Args:
        usuari (str): Nom del usuari a esborrar.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    Usuari.objects(nom=usuari).delete()

    ## Validació:
    resposta: Response = obtindre_dades_del_usuari(usuari)
    usuari: Usuari = json.loads(resposta.get_data())["message"]
    if usuari is None:
        resposta = jsonify(
            success=True, 
            message="S'ha esborrat amb èxit l'usuari."
        )
        return resposta
    else:
        resposta = jsonify(
            succes=False, 
            message="Ha ocorregut un problema durant el esborrament."
            )
        return resposta
    ## if
## ()
##############################################################
##############################################################