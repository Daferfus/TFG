from urllib.request import Request

from flask import Blueprint, Response, request, flash, redirect, url_for, render_template, jsonify
from flask_login import current_user
from projecte_assignacio.empreses import controlador_empreses
from projecte_assignacio.empreses.formulari_empreses import EmpresesForm
from projecte_assignacio.empreses.formulari_practiques import PractiquesForm
from projecte_assignacio.empreses.model_empreses import Empresa

# Blueprint Configuration
empreses_bp = Blueprint(
    'empreses_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@empreses_bp.route('/perfil_empresa', methods=["GET", "POST"])
def perfil_empresa():
    empresa: Empresa = controlador_empreses.recuperar_dades_de_la_empresa(current_user.nom)
    resposta = "No"
    if len(empresa.practiques) > 0:
        resposta = "Sí"
        
    form = EmpresesForm(
            nom=empresa.nom,
            poblacio=empresa.poblacio,
            telefon=empresa.telefon,
            correu=empresa.correu,
            nom_de_persona_de_contacte=empresa.persona_de_contacte,
            volen_practica=resposta
        )
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'perfil_empresa.jinja2',
        title="Perfil",
        nom_de_usuari=current_user.nom,
        form=form,
        template="perfil_empresa-template"
    )

@empreses_bp.route('/practiques')
def practiques():
    empresa: Empresa = controlador_empreses.recuperar_dades_de_la_empresa(current_user.nom)
    return render_template(
        'practiques_empresa.jinja2',
        title="Pràctiques",
        nom_de_usuari=current_user.nom,
        practiques_de_empresa=empresa.practiques,
        template="practiques_empresa-template"
    )

@empreses_bp.route('/anyadir_practica')
def anyadir_practica():
    form = PractiquesForm()
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'practica_empresa.jinja2',
        title="Anyadir Pràctica",
        accio="crear",
        nom_de_usuari=current_user.nom,
        form=form,
        template="practica_empresa-template"
    )
@empreses_bp.route('/editar_practica/<int:nombre_de_practica>')
def editar_practica(nombre_de_practica: int):
    empresa: Empresa = controlador_empreses.recuperar_dades_de_la_empresa(current_user.nom)
    practica = empresa.practiques[nombre_de_practica]
    form = PractiquesForm(
            nom=practica["Nom"],
            titulacio=practica["Titulacio"],
            descripcio=practica["Descripcio"],
            tecnologies_i_frameworks=practica["Tecnologies i Frameworks"]
        )
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'practica_empresa.jinja2',
        title="Editar Pràctica",
        accio="editar",
        nombre_de_practica =nombre_de_practica,
        nom_de_usuari=current_user.nom,
        form=form,
        template="practica_empresa-template"
    )

@empreses_bp.route('/recuperar_dades_de_empreses', methods=['GET'])
def iniciar_recerca_de_empreses() -> Response:
    """Crida a la funció per a obtindre les dades de totes les empreses.

    Returns:
        Response: Dades de totess les empreses.
    """
    dades_de_empreses: list[Empresa] = controlador_empreses.recuperar_dades_de_empreses()
    if dades_de_empreses is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat cap empresa.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_de_empreses)
        return resposta

@empreses_bp.route('/recuperar_dades_de_la_empresa/<string:usuari>', methods=['GET'])
def iniciar_recerca_de_la_empresa(usuari: str) -> Response:
    """Crida a la funció per a obtindre les dades d'una empresa determinada.

    Args:
        empresa (str): Nom de la empresa a buscar.

    Returns:
        Response: Dades de la empresa.
    """    
    dades_de_la_empresa: Empresa = controlador_empreses.recuperar_dades_de_la_empresa(usuari)
    if dades_de_la_empresa is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat la empresa.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_de_la_empresa)
        return resposta

@empreses_bp.route('/insertar_empresa', methods=['POST'])
def recollir_dades_empresa() -> Response:
    """Crida a la funció per a insertar una empresa.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom_de_empresa'] 
    poblacio: str = request.form['poblacio_de_empresa'] 
    telefon: int = request.form['telefon_de_empresa'] 
    correu: str = request.form['correu_de_empresa'] 
    persona_de_contacte: str = request.form['persona_de_contacte_en_la_empresa']

    resultat: str = controlador_empreses.insertar_empresa(
        nom, 
        poblacio, 
        telefon, 
        correu,
        persona_de_contacte
        )
    if resultat == "L'empresa s'ha insertat amb èxit.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@empreses_bp.route('/importar_empreses', methods=['POST'])
def recollir_fitxer_empreses() -> Response:
    """Crida a la funció per a importar empreses a partir d'un arxiu.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    f: Request = request.files['fichero']
    nom_del_fitxer: str = './projecte_assignacio/empreses/static/file/empreses.xls'
    f.save(nom_del_fitxer)
    
    resultat: str = controlador_empreses.importar_empreses(nom_del_fitxer)
    
    if resultat == "Ha ocorregut un problema durant l'operació.":
        resposta: Response = jsonify(sucess=False, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta

@empreses_bp.route('/exportar_empreses', methods=['GET'])
def descarregar_fitxer_empreses() -> Response:
    """Crida a la funció per a exportar empreses de la base de dades.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat:bool = controlador_empreses.exportar_empreses()
    if resultat:
        resposta: Response = jsonify(success=resultat, message="S'han exportat amb èxit les dades de les empreses.")
        return resposta
    else:
        resposta: Response = jsonify(success=resultat, message="Hi ha hagut un problema durant l'exportació.")
    return resposta

@empreses_bp.route('/actualitzar_empresa/<string:usuari>', methods=["POST"])
def recollir_nom_de_empresa(usuari: str) -> Response:
    """Crida a la funció per a actualitzar una empresa donada.

    Args:
        empresa (str): Nom de la empresa a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom'] 
    poblacio: str = request.form['poblacio'] 
    telefon: int = request.form['telefon'] 
    correu: str = request.form['correu'] 
    persona_de_contacte: str = request.form['nom_de_persona_de_contacte']

    resultat: str = controlador_empreses.actualitzar_empresa(
        usuari,
        nom, 
        poblacio, 
        telefon, 
        correu,
        persona_de_contacte
        )

    if resultat=="L'empresa ha sigut actualitzada.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('empreses_bp.perfil_empresa'))
        return resposta


@empreses_bp.route('/esborrar_empreses', methods=['DELETE'])
def eliminacio_de_empreses() -> Response:
    """Crida a la funció per a esborrar totes les empreses.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_empreses.esborrar_empreses()
    if resultat == "S'ha esborrat amb èxit totes les empreses.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@empreses_bp.route('/esborrar_empresa/<string:empresa>', methods=['DELETE'])
def eliminacio_de_empresa(empresa: str):
    """Esborra una empresa donada.

    Args:
        empresa (str): Nom de la empresa a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    resultat: str = controlador_empreses.esborrar_empresa(empresa)
    if resultat == "S'ha esborrat amb èxit l'empresa.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(succes=False, message=resultat)
        return resposta


@empreses_bp.route('/insertar_practica/<string:usuari>', methods=['POST'])
def recollir_dades_practica(usuari: str) -> Response:
    """Crida a la funció per a insertar una pràctica.

    Args:
        empresa (str): Nom de l'empresa que ofertarà la pràctica.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    practiques: dict = {
        "Nom": request.form['nom'],
        "Titulacio": request.form["titulacio"],
        "Descripcio": request.form["descripcio"],
        "Tecnologies i Frameworks": request.form["tecnologies_i_frameworks"]
    }

    resultat: str = controlador_empreses.insertar_practica(
        usuari,
        practiques
    )
    if resultat=="Pràctica insertada.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@empreses_bp.route('/actualitzar_practica/<string:usuari>/<int:nombre_de_practica>', methods=["POST"])
def recollir_nom_de_la_practica(usuari: str, nombre_de_practica: int) -> Response:
    """Crida a la funció per a actualitzar una pràctica donada.

    Args:
        empresa (str): Nom de l'empresa que ofereix la pràctica.
        practica_a_actualitzar (dict): Pràctica que es vol actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    practica_actualitzada: dict = {
        "Nom": request.form['nom'],
        "Titulacio": request.form['titulacio'],
        "Descripcio": request.form['descripcio'],
        "Tecnologies i Frameworks": request.form['tecnologies_i_frameworks'],
    }
    practica_a_actualitzar: int = nombre_de_practica
    resultat: str = controlador_empreses.actualitzar_practica(
        usuari,
        practica_a_actualitzar,
        practica_actualitzada
    )

    if resultat=="La pràctica ha sigut actualitzada.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('empreses_bp.editar_practica'))
        #return resposta


@empreses_bp.route('/esborrar_practica/<string:usuari>/<int:nombre_de_practica>', methods=['POST'])
def eliminacio_de_practica(usuari: str, nombre_de_practica: int) -> Response:
    """Esborra una pràctica donada.

    Args:
        empresa (str): Nom de l'empresa que ofereix la pràctica.
        practica (dict): La pràctica a esborrar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_empreses.esborrar_practica(usuari, nombre_de_practica)
    if resultat=="La pràctica ha sigut esborrada.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('empreses_bp.practiques'))
        #return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('empreses_bp.practiques'))
        #return resposta
