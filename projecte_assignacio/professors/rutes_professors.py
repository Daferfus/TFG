#############################################################################
## Autor: David Fernández Fuster                                           ##
## Data: 22/08/2022                                                        ## 
## Funció: Conté les rutes que desencandenen accions sobre els professors. ##
#############################################################################

################
## Llibreries ##
################
import pandas as pd
import json
import os
from munch import DefaultMunch
from urllib.request import Request

#############
##  Flask  ##
#############
from flask import current_app as app, Blueprint, Response, request, jsonify, render_template, make_response, flash, redirect, url_for
from flask_login import current_user

##############
##  Mòduls  ##
##############
from projecte_assignacio.professors.formulari_professors import ProfessorsForm
from projecte_assignacio.professors.model_professors import Professor
from projecte_assignacio.usuaris.model_usuaris import Usuari

############################
## Configuració Blueprint ##
############################
professors_bp = Blueprint(
    'professors_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


###################################
## Funcions de Retorn de Pàgines ##
###################################
@professors_bp.route('/perfil_professor', methods=["GET"])
def perfil_professor() -> str:
    """Mostra la pàgina de perfil del professor.

    Returns:
        str: Pàgina de perfil del professor
    """    
    professor: Professor = controlador_professors.recuperar_dades_del_professor(current_user.nom)    
    form = ProfessorsForm(
            nom=professor.nom,
            cognoms=professor.cognoms,
            titulacions=professor.titulacions,
            hores_alliberades_setmanalment=professor.hores_alliberades
        )
    
    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'perfil_professor.jinja2',
        title="Perfil",
        nom_de_usuari=current_user.nom,
        form=form,
        template="perfil_professor-template"
    )
## ()

@professors_bp.route('/ajustos')
def ajustos() -> str:
    """Mostra la pàgina amb els ratis d'alumne per hora del professor actualment en sessió.

    Returns:
        str: Pàgina amb els ratis d'alumnes per hora.
    """
    form = ProfessorsForm()
    return render_template(
        'ajustos_professor.jinja2',
        title="Ajustos",
        nom_de_usuari=current_user.nom,
        form=form,
        template="ajustos_professor-template"
    )
## ()

@professors_bp.route('/llistat_professors', methods=['GET'])
@professors_bp.route('/llistat_professors/pagina/<int:pagina>')
def llistat(pagina=1) -> str:
    """Mostra una pàgina on s'enllista els professors de formma paginada.

    Args:
        pagina (int, optional): Nombre de pàgina del llistat de professors. Defaults to 1.
        
    Returns:
        str: Llista de professors en la pàgina indicada.
    """    
    dades_de_professors: list[Professor]|None = Professor.objects.paginate(page=pagina, per_page=5)
    return render_template(
        'llistat_professors.jinja2',
        title="Llistat de Professors",
        professors=dades_de_professors,
        template="llistat_professors-template"
    )
## ()

@professors_bp.route('/anyadir_professor', methods=["GET"])
def anyadir_professor() -> str:
    """Mostra el formulari d'inserció de professor.

    Returns:
        str: Pàgina amb el formulari d'inserció de professor.
    """
    form = ProfessorsForm()

    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_professors.jinja2',
        title="Anyadir Professor",
        accio="crear",
        form=form,
        template="formulari_professor-template"
    )
## ()

@professors_bp.route('/editar_professor/<string:usuari>', methods=['GET'])
def editar_professor(usuari: str) -> str:
    """Mostra el formulari d'edició de professor.

    Args:
        usuari (str): Nom d'usuari del professor a editar.

    Returns:
        str: Pàgina amb el formulari d'edició de professor.
    """
    professor: Professor = Professor.objects(nom_de_usuari=usuari).first()


    form = ProfessorsForm(
            nom=professor.nom,
            cognoms=professor.cognoms,
            titulacions=professor.titulacions,
            hores_alliberades_setmanalment=professor.hores_alliberades
        )

    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_professors.jinja2',
        title="Editar Professor",
        accio="editar",
        nom_de_usuari=usuari,
        form=form,
        template="formulari_professors-template"
    )
## ()
##############################################################
##############################################################

######################################
## Funcions de Retorn d'Informació  ##
######################################
@professors_bp.route('/professors', methods=['GET'])
def obtindre_dades_de_professors() -> Response:
    """Retorna una llista de professors.

    Returns:
        Response: Llista de professors.
    """
    professors: list[Professor]|None = Professor.objects()
    
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if professors is None:
        resposta: Response = make_response(
            jsonify(
                success=True, 
                message="No s'ha trovat cap professor."
            ), 
            200, 
            headers
        )
        return resposta
    else:
        resposta: Response = make_response(
            jsonify(
                success=True, 
                message=professors
            ), 
            200, 
            headers
        )
        return resposta
    ## if
## ()

@professors_bp.route('/professor/<string:usuari>', methods=['GET'])
def obtindre_dades_del_professor(usuari: str) -> Response:
    """Retorna un professor donat.

    Args:
        usuari (str): nom d'usuari del professor a retornar.

    Returns:
        Response: Dades del professor.
    """    
    professor: Professor = Professor.objects(nom_de_usuari=usuari).first()
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if professor is None:
        resposta: Response =  make_response(
            jsonify(
            success=False, 
            message=professor
            ),
            200,
            headers
        )
        return resposta
    else:
        resposta: Response = make_response(
            jsonify(
            success=True, 
            message=professor
            ),
            200,
            headers
        )
        return resposta
    ## if
## ()
##############################################################
##############################################################

#######################################
## Funcions de Modificació de Dades  ##
#######################################
@professors_bp.route('/insertar_professor', methods=['POST'])
def insertar_professor() -> Response:
    """Crida a la funció per a insertar un professor.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom']
    cognoms: str = request.form['cognoms'] 
    titulacions: dict = {
        "Titulacions": request.form["titulacions"]
    } 
    hores_alliberades: int = request.form["hores_alliberades_setmanalment"] 
    hores_restants: int = request.form["hores_alliberades_setmanalment"]
    
    resposta: Response = obtindre_dades_del_professor(nom)
    professor_existent: Professor|None = json.loads(resposta.get_data(as_text=True))["message"]

    if professor_existent is None:
        professor: Professor = Professor(
            nom_de_usuari=nom,
            nom=nom, 
            cognoms=cognoms, 
            titulacions=titulacions, 
            hores_alliberades=hores_alliberades, 
            hores_restants=hores_restants, 
            rati_fct="", 
            rati_dual="", 
            assignacions=[],
        )
        professor.save()
        resposta: Response = obtindre_dades_del_professor(nom)
        professor_insertat: Professor|None = json.loads(resposta.get_data(as_text=True))["message"]

        if professor_insertat:
            dades: dict[str, str] = {
                "nom": professor.nom,
                "contrasenya": professor.nom+"_2022",
                "rol": "Professor"
            }

            app.post('/registrar', data=dades)

            resposta: Response = jsonify(
                success=True, 
                message="El professor s'ha insertat amb èxit."
            )
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if app.config["DEBUG"]:
                return resposta
            else:
                return redirect(url_for('usuaris_bp.home'))
        else:
            resposta: Response = jsonify(
                success=False, 
                message="Ha ocorregut un problema durant la inserció."
            )
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if app.config["DEBUG"]:
                return resposta
            else:
                return redirect(url_for('professors_bp.anyadir_professor'))
        ## if
    else:
        resposta: Response = jsonify(
                success=False, 
                message="Ja existeix un professor amb aquest usuari."
            )
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
                return resposta
        else:
            return redirect(url_for('professors_bp.anyadir_professor'))
        ## if
    ## if
## ()
@professors_bp.route('/importar_professors', methods=['POST'])
def importar_professors() -> Response:
    """Inserta cada alumne trovat en un fitxer.

    Args:
        nom_del_fitxer (str): Ubicació local del fitxer.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    f: Request = request.files['fichero']
    nom_del_fitxer: str = './professors.xlsx'
    f.save(nom_del_fitxer)

    df: any = pd.read_excel(nom_del_fitxer)

    nombre_de_fila: int = 0
    contador_de_insertats: int = 0
    quantitat_de_professors_ja_insertats: int = 0

    while nombre_de_fila < len(df):

        professor: dict = {}
        titulacions: dict = {}

        for columna in df:
            if not pd.isnull(df.loc[nombre_de_fila, columna]):
            
                ## Nom del professor.
                if columna == "NOM":
                    professor[columna]: str = df.loc[nombre_de_fila, columna]

                ## Hores lliures del professor.
                elif columna == "HORES":
                    professor[columna]: int = df.loc[nombre_de_fila, columna]

                ## Preferències.
                else:
                    titulacions[columna]: dict = df.loc[nombre_de_fila, columna]
                ## if

            professor["Titulacions"] = titulacions
        ## for

        professor: Professor = Professor(
            nom_de_usuari=professor["NOM"],
            nom=professor["NOM"], 
            cognoms=professor["NOM"], 
            titulacions=professor["Titulacions"], 
            hores_alliberades=professor["HORES"], 
            hores_restants=professor["HORES"], 
            rati_fct="", 
            rati_dual="", 
            assignacions=[],
        )
        professor.save()
        nombre_de_fila+=1
        
        usuari: Usuari = Usuari(
            nom=professor.nom, 
            contrasenya=professor.nom+"_2022", 
            rol="Professor"
        )
        usuari.establir_contrasenya(professor.nom+"_2022")
        resultat = usuari.save()
        
        if len(resultat) > 0:
            contador_de_insertats+=1
        else:
            quantitat_de_professors_ja_insertats+=1
        ## if
    ## while

    if contador_de_insertats == 0 and quantitat_de_professors_ja_insertats == 0:
        resposta: Response = jsonify(sucess=False, message="Ha ocorregut un problema durant l'operació.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message="S'han insertat " +str(contador_de_insertats)+ " de 44 professors." +str(quantitat_de_professors_ja_insertats)+ " ja estaven insertades.")
        return resposta
## ()

@professors_bp.route('/exportar_professors', methods=['GET'])
def exportar_professors() -> Response:
    """Exporta els professors de la base de dades a un fitxer xlsx.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resposta: Response = obtindre_dades_de_professors()
    professors: list[Professor]|None = DefaultMunch.fromDict(json.loads(resposta.get_data(as_text=True))["message"])

    professors_dict: list[dict] = []

    for professor in professors:
        professor_dict: dict = {
            "Nom": professor.nom,
            "Cognoms": professor.cognoms,
            "Titulacions": str(professor.titulacions),
            "Hores Alliberades": professor.hores_alliberades,
            "Hores Restants": professor.hores_restants,
            "Rati FCT": professor.rati_fct,
            "Rati DUAL": professor.rati_dual,
            "Assignacions": professor.assignacions
        }
        professors_dict.append(professor_dict)
    ## for

    dades = pd.DataFrame.from_dict(professors_dict)
    dades.to_excel("professors_ex.xlsx",header=True)

    if os.path.exists("professors_ex.xlsx"):
        resposta: Response = jsonify(success=True, message="S'han exportat amb èxit les dades dels professors.")
        return resposta
    else:
        resposta: Response = jsonify(success=False, message="Hi ha hagut un problema durant l'exportació.")
    return resposta
    ## if
## ()

@professors_bp.route('/actualitzar_professor/<string:usuari>', methods=["POST"])
def actualitzar_professor(usuari: str) -> Response:
    """Actualitza les dades d'un professor donat.

    Args:
        nom_de_professor_per_a_filtrar (str): Nom del professor a actualitzar.
        cognoms_de_professor_per_a_filtrar (str): Cognoms del professor a actualitzar.
        nom_del_professor (str): Nou nom del professor.
        cognoms_del_professor (str): Nous cognoms del professor.
        titulacions_del_professor (dict): Noves titulacions del professor.
        hores_alliberades_del_professor (int): Noves hores alliberades del professor.
        hores_restants_del_professor (str): Noves hores restants del professor.

    Returns:
        str: Resultat de l'operació.
    """
    nom: str = request.form['nom']
    cognoms: str = request.form['cognoms'] 
    titulacions: str = request.form["titulacions"] 
    hores_alliberades: int = request.form["hores_alliberades_setmanalment"] 
    hores_restants: int = request.form["hores_alliberades_setmanalment"]

    resultat: int = Professor.objects(nom_de_usuari=usuari).update(__raw__=
            {"$set": {
                "nom": nom,
                "cognoms": cognoms,
                "titulacions": titulacions,
                "hores_alliberades": hores_alliberades,
                "hores_restants": hores_restants
                }
            }
        )
    if resultat > 0:
        resposta: Response = jsonify(success=True, message="El professor ha sigut actualitzat.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
    else:
        resposta: Response = jsonify(success=False, message="No s'ha canviat res del professor.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('professors_bp.perfil'))
    ## if
## ()


@professors_bp.route('/actualitzar_ratis/<string:usuari>', methods=["POST"])
def ratis(usuari: str) -> Response:
    """Actualitza les dades d'un professor donat.

    Args:
        nom_de_professor_per_a_filtrar (str): Nom del professor a actualitzar.
        cognoms_de_professor_per_a_filtrar (str): Cognoms del professor a actualitzar.
        nom_del_professor (str): Nou nom del professor.
        cognoms_del_professor (str): Nous cognoms del professor.
        titulacions_del_professor (dict): Noves titulacions del professor.
        hores_alliberades_del_professor (int): Noves hores alliberades del professor.
        hores_restants_del_professor (str): Noves hores restants del professor.

    Returns:
        str: Resultat de l'operació.
    """
    alumnes_fct: int = request.form['ajustos_fct-quantitat_alumnes']
    hores_alliberades_fct: int = request.form['ajustos_fct-hores_alliberades'] 
    alumnes_dual: int = request.form["ajustos_dual-quantitat_alumnes"] 
    hores_alliberades_dual: int = request.form["ajustos_dual-hores_alliberades"] 
    
    rati_fct: str = str(alumnes_fct)+" alumnes per cada "+str(hores_alliberades_fct)+" hores alliberades."
    rati_dual: str = str(alumnes_dual)+" alumnes per cada "+str(hores_alliberades_dual)+" hores alliberades."
   
    resultat: int = Professor.objects(nom_de_usuari=usuari).update(__raw__=
            {"$set": {
                "rati_fct": rati_fct,
                "rati_dual": rati_dual                }
            }
        )
    if resultat > 0:
            return "El professor ha sigut actualitzat."
    else:
        return "No s'ha canviat res del professor."
    ## if
## ()

@professors_bp.route('/esborrar_professors', methods=['DELETE'])
def esborrar_professors() -> Response:
    """Esborra tots els professors.

    Returns:
        str: Resultat de l'operació.
    """
    Professor.objects.delete()

    professors: list[Professor] = obtindre_dades_de_professors()
    if len(json.loads(professors.get_data(as_text=True))["message"]) == 0:
        resposta: Response = jsonify(
            success=True, 
            message="S'ha esborrat amb èxit tots els professors."
            )
        return resposta
    else:
        resposta: Response = jsonify(
            success=False, 
            message="Ha ocorregut un problema durant el esborrament."
            )
        return resposta
    ## if
## ()

@professors_bp.route('/esborrar_professor/<string:usuari>', methods=['POST'])
def esborrar_professor(usuari: str) -> Response:
    """Esborra un professor donat.

    Args:
        nom_del_professor (str): Nom del professor a esborrar.
        cognoms_del_professor (str): Cognoms del professor a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    Professor.objects(nom_de_usuari=usuari).delete()

    professor: Professor = Professor.objects(nom_de_usuari=usuari).first()
    if professor:
        resposta: Response = jsonify(success=False, message="Ha ocorregut un problema durant el esborrament.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
        ## if
    else:
        resposta: Response = jsonify(success=True, message="S'ha esborrat amb èxit el professor.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('professors_bp.llistat'))
        ## if
    ## if
## ()
##############################################################
##############################################################