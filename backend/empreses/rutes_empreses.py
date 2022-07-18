import json
from urllib.request import Request

from flask import Blueprint, Response, request, make_response, jsonify
from backend.empreses import controlador_empreses
from backend.empreses.model_empreses import Empresa

# Blueprint Configuration
empreses_bp = Blueprint(
    'empreses', __name__,
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

@empreses_bp.route('/recuperar_dades_de_la_empresa/<string:empresa>', methods=['GET'])
def iniciar_recerca_de_la_empresa(empresa: str) -> Response:
    """Crida a la funció per a obtindre les dades d'una empresa determinada.

    Args:
        empresa (str): Nom de la empresa a buscar.

    Returns:
        Response: Dades de la empresa.
    """    
    dades_de_la_empresa: Empresa = controlador_empreses.recuperar_dades_de_la_empresa(empresa)
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
    nom_del_fitxer: str = './empreses.xls'
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

@empreses_bp.route('/actualitzar_empresa/<string:empresa>', methods=["PUT"])
def recollir_nom_de_empresa(empresa: str) -> Response:
    """Crida a la funció per a actualitzar una empresa donada.

    Args:
        empresa (str): Nom de la empresa a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom_de_empresa'] 
    poblacio: str = request.form['poblacio_de_empresa'] 
    telefon: int = request.form['telefon_de_empresa'] 
    correu: str = request.form['correu_de_empresa'] 
    persona_de_contacte: str = request.form['persona_de_contacte_en_la_empresa']

    resultat: str = controlador_empreses.actualitzar_empresa(
        empresa,
        nom, 
        poblacio, 
        telefon, 
        correu,
        persona_de_contacte
        )

    if resultat=="L'empresa ha sigut actualitzada.":
        resposta: Response = jsonify(success=True, message=resultat)
    else:
        resposta: Response = jsonify(success=False, message=resultat)
    return resposta


@empreses_bp.route('/esborrar_empreses', methods=['DELETE'])
def eliminacio_de_empreses():
    """Esborra totes les empreses.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: str = controlador_empreses.esborrar_empreses()
    if resultat == "S'ha esborrat amb èxit totes les empreses.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(success=False, message=resultat)
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


@empreses_bp.route('/insertar_practica/<string:empresa>', methods=['POST'])
def recollir_dades_practica(empresa: str) -> Response:
    """Crida a la funció per a insertar una pràctica.

    Args:
        empresa (str): Nom de l'empresa que ofertarà la pràctica.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    practiques = json.loads(request.form['practiques_de_la_empresa'])

    resultat: str = controlador_empreses.insertar_practica(
        empresa,
        practiques
    )
    resposta: Response = jsonify(success=True, message=resultat)
    return resposta

@empreses_bp.route('/actualitzar_practica/<string:empresa>/<practica>', methods=["PUT"])
def recollir_nom_de_la_practica(empresa: str, practica_a_actualitzar: dict) -> Response:
    """Crida a la funció per a actualitzar una pràctica donada.

    Args:
        empresa (str): Nom de l'empresa que ofereix la pràctica.
        practica_a_actualitzar (dict): Pràctica que es vol actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    practica_actualitzada: dict = json.loads(request.form['practica_de_la_empresa'])

    resultat: str = controlador_empreses.actualitzar_practica(
        empresa,
        practica_a_actualitzar,
        practica_actualitzada
    )

    resposta: Response = jsonify(success=True, message=resultat)
    return resposta

@empreses_bp.route('/esborrar_practica/<string:empresa>', methods=['DELETE'])
def eliminacio_de_practica(empresa: str) -> Response:
    """Esborra una pràctica donada.

    Args:
        empresa (str): Nom de l'empresa que ofereix la pràctica.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    practica_a_esborrar = request.args.get("nom_de_la_practica")
    resultat: str = controlador_empreses.esborrar_practica(empresa, practica_a_esborrar)
    resposta: Response = jsonify(success=True, message=resultat)
    return resposta
