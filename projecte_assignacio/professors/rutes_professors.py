import json
from urllib.request import Request

from flask import Blueprint, Response, request, jsonify, render_template, flash, redirect, url_for
from flask_login import current_user
from projecte_assignacio.professors import controlador_professors
from projecte_assignacio.professors.formulari_professors import ProfessorsForm
from projecte_assignacio.professors.model_professors import Professor

# Blueprint Configuration
professors_bp = Blueprint(
    'professors_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@professors_bp.route('/perfil_professor', methods=["GET", "POST"])
def perfil_professor():
    professor: Professor = controlador_professors.recuperar_dades_del_professor(current_user.nom)    
    form = ProfessorsForm(
            nom=professor.nom,
            cognoms=professor.cognoms,
            titulacions=professor.titulacions,
            hores_alliberades_setmanalment=professor.hores_alliberades
        )
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'perfil_professor.jinja2',
        title="Perfil",
        nom_de_usuari=current_user.nom,
        form=form,
        template="perfil_professor-template"
    )

@professors_bp.route('/ajustos')
def ajustos():
    professor: Professor = controlador_professors.recuperar_dades_del_professor(current_user.nom)
    form = ProfessorsForm()
    return render_template(
        'ajustos_professor.jinja2',
        title="Ajustos",
        nom_de_usuari=current_user.nom,
        form=form,
        template="ajustos_professor-template"
    )

@professors_bp.route('/recuperar_dades_de_professors', methods=['GET'])
def iniciar_recerca_de_professors() -> Response:
    """Crida a la funció per a obtindre les dades de tots els professors.

    Returns:
        Response: Dades de tots els professors.
    """
    dades_de_professors: list[Professor] = controlador_professors.recuperar_dades_de_professors()
    if dades_de_professors is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat cap professor.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_de_professors)
        return resposta

@professors_bp.route('/recuperar_dades_del_professor/<string:nom_del_professor>/<string:cognoms_del_professor>', methods=['GET'])
def iniciar_recerca_del_professor(nom_del_professor: str, cognoms_del_professor: str) -> Response:
    """Crida a la funció per a obtindre les dades d'un professor determinat.

    Args:
        nom_del_professor (str): Nom del professor a buscar.
        cognoms_del_professor (str): Cognoms del professor a buscar.

    Returns:
        Response: Dades del professor.
    """
    dades_del_professor: Professor = controlador_professors.recuperar_dades_del_professor(nom_del_professor, cognoms_del_professor)
    if dades_del_professor is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat el professor.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_del_professor)
        return resposta


@professors_bp.route('/insertar_professor', methods=['POST'])
def recollir_dades_professor() -> Response:
    """Crida a la funció per a insertar un professor.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom_del_professor']
    cognoms: str = request.form['cognoms_del_professor'] 
    titulacions: dict = json.loads(request.form["titulacions_del_professor"]) 
    hores_alliberades: int = request.form["hores_alliberades_del_professor"] 
    hores_restants: int = request.form["hores_alliberades_del_professor"]
    
    resultat: str = controlador_professors.insertar_professor(
        nom, 
        cognoms, 
        titulacions, 
        hores_alliberades, 
        hores_restants
        )
    if resultat == "El professor s'ha insertat amb èxit.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta


@professors_bp.route('/importar_professors', methods=['POST'])
def recollir_fitxer_professors() -> Response:
    """Crida a la funció per a importar professors a partir d'un arxiu.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    f: Request = request.files['fichero']
    nom_del_fitxer: str = './professors.xlsx'
    f.save(nom_del_fitxer)
    resultat:str = controlador_professors.importar_professors(nom_del_fitxer)

    if resultat == "Ha ocorregut un problema durant l'operació.":
        resposta: Response = jsonify(sucess=False, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta

@professors_bp.route('/exportar_professors', methods=['GET'])
def descarregar_fitxer_professors() -> Response:
    """Crida a la funció per a exportar professors de la base de dades.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat:bool = controlador_professors.exportar_professors()
    if resultat:
        resposta: Response = jsonify(success=resultat, message="S'han exportat amb èxit les dades dels professors.")
        return resposta
    else:
        resposta: Response = jsonify(success=resultat, message="Hi ha hagut un problema durant l'exportació.")
    return resposta

@professors_bp.route('/actualitzar_professor/<string:usuari>', methods=["POST"])
def recollir_nom_de_professor(usuari: str) -> Response:
    """Crida a la funció per a actualitzar un professor donat.

    Args:
        nom_del_professor (str): Nom del professor a actualitzar.
        cognoms_del_professor (str): Cognoms del professor a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom']
    cognoms: str = request.form['cognoms'] 
    titulacions: str = request.form["titulacions"] 
    hores_alliberades: int = request.form["hores_alliberades_setmanalment"] 
    hores_restants: int = request.form["hores_alliberades_setmanalment"]

    resultat: str = controlador_professors.actualitzar_professor(
        usuari,
        nom,
        cognoms, 
        titulacions, 
        hores_alliberades, 
        hores_restants
        )

    if resultat=="El professor ha sigut actualitzat.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
        
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('professors_bp.perfil_professor'))
        #return resposta

@professors_bp.route('/actualitzar_ratis/<string:usuari>', methods=["POST"])
def ratis(usuari: str) -> Response:
    """Crida a la funció per a actualitzar un professor donat.

    Args:
        nom_del_professor (str): Nom del professor a actualitzar.
        cognoms_del_professor (str): Cognoms del professor a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    print(request.form)
    alumnes_fct: int = request.form['ajustos_fct-quantitat_alumnes']
    hores_alliberades_fct: int = request.form['ajustos_fct-hores_alliberades'] 
    alumnes_dual: int = request.form["ajustos_dual-quantitat_alumnes"] 
    hores_alliberades_dual: int = request.form["ajustos_dual-hores_alliberades"] 
    
    rati_fct: str = str(alumnes_fct)+" alumnes per cada "+str(hores_alliberades_fct)+" hores alliberades."
    rati_dual: str = str(alumnes_dual)+" alumnes per cada "+str(hores_alliberades_dual)+" hores alliberades."
    resultat: str = controlador_professors.actualitzar_ratis(
        usuari,
        rati_dual,
        rati_fct
        )

    if resultat=="El professor ha sigut actualitzat.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
        
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('professors_bp.ajustos'))
        #return resposta

@professors_bp.route('/esborrar_professors', methods=['DELETE'])
def eliminacio_de_professors() -> Response:
    """Esborra tots els professors.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: str = controlador_professors.esborrar_professors()
    if resultat == "S'ha esborrat amb èxit tots els professors.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(success=False, message=resultat)
        return resposta

@professors_bp.route('/esborrar_professor/<string:nom_del_professor>/<string:cognoms_del_professor>', methods=['DELETE'])
def eliminacio_de_professor(nom_del_professor: str, cognoms_del_professor: str) -> Response:
    """Esborra un professor donat.

    Args:
        nom_del_professor (str): Nom del professor a esborrar.
        cognoms_del_professor (str): Cognoms del professor a esborrar.
            
    Returns:
        str: Resultat de l'operació.
    """
    resultat: str = controlador_professors.esborrar_professor(nom_del_professor, cognoms_del_professor)
    if resultat == "S'ha esborrat amb èxit el professor.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(succes=False, message=resultat)
        return resposta