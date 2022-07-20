import json
from unittest import result
from flask import Blueprint, Response, jsonify, request
from backend.assignacions import controlador_assignacions

# Blueprint Configuration
assignacions_bp = Blueprint(
    'assignacions_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@assignacions_bp.route('/insertar_assignacio_manual/<string:alumne>/<string:nom_de_professor>/<string:cognoms_de_professor>/<string:empresa>', methods=['POST'])
def recollir_dades_assignacio(alumne: str, nom_de_professor: str, cognoms_de_professor: str, empresa: str) -> Response:
    """Crida a la funció per a assignar a cascuna de les parts a una pràctica.

    Args:
        alumne (str): Alumne protagonista de l'assignació.
        nom_de_professor (str): Nom del professor que farà el seguiment de l'alumne.
        cognoms_de_professor (str): Cognoms del professor encarregat de fer el seguiment de l'alumne.
        empresa (str): Empresa en la que el alumne farà la practica.
        practica (str): Pràctica a la que s'assigna l'alumne.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    assignacio: dict[str, str] = json.loads(request.form['assignacio'])
    resultat: str = controlador_assignacions.insertar_assignacio_manual(
        alumne,
        nom_de_professor,
        cognoms_de_professor,
        empresa,
        assignacio
    )
    if resultat == "L'assignació s'ha insertat.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@assignacions_bp.route('/actualitzar_assignacio/<string:alumne>/<string:nom_de_professor>/<string:cognoms_de_professor>/<string:empresa>/<string:practica>', methods=['PUT'])
def actualitzar_assignacio(alumne: str, nom_de_professor: str, cognoms_de_professor: str, empresa: str, practica:str) -> Response:
    """Crida a la funció per a actualitzar una assignació donada.

    Args:
        alumne (str): Alumne al que se li vol actualitzar l'assignació.
        nom_de_professor (str): Nom del professor encarregat de fer un seguiment de la pràctica.
        cognoms_de_professor (str): Cognoms del professor encarregat de fer un seguiment de la pràctica.
        empresa (str): Empresa que oferta la pràctica.
        practica (str): Pràctica a la que s'assigna.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    assignacio: dict[str, str] = json.loads(request.form['assignacio'])
    resultat: str = controlador_assignacions.actualitzar_assignacio(
        alumne,
        nom_de_professor,
        cognoms_de_professor,
        empresa,
        practica,
        assignacio
    )

    if resultat == "S'ha actualitzat l'assignació.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@assignacions_bp.route('/esborrar_assignacio/<string:alumne>/<string:nom_de_professor>/<string:cognoms_de_professor>/<string:empresa>/<string:practica>', methods=['DELETE'])
def eliminacio_de_assignacio(alumne: str, nom_de_professor: str, cognoms_de_professor: str, empresa: str, practica:str) -> Response:
    """Crida a la funció per a esborrar un assignació.

    Args:
        alumne (str): Alumne al que se li vol esborrar l'assignació.
        nom_de_professor (str): Nom del professor al que se li vol esborrar l'assignació.
        cognoms_de_professor (str): Cognoms del professor al que se li vol esborrar l'assignació.
        empresa (str): Empresa a la que se li vol esborrar l'assignació.
        practica (str): Pràctica a la que s'assigna el reste de parts.

    Returns:
        Response: Informació sobre el resultat de l'operació.
    """
    professor = nom_de_professor+' '+cognoms_de_professor
    assignacio = {"Alumne": alumne, "Practica": empresa+"("+practica+")", "Professor": professor}
    resultat: str = controlador_assignacions.esborrar_assignacio(
        nom_de_professor, 
        cognoms_de_professor, 
        empresa,
        assignacio
    )

    if resultat == "S'ha esborrat l'assignació.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta

@assignacions_bp.route('/realitzar_assignacio_automatica', methods=['POST'])
def assignar_automaticament() -> Response:
    """Crida a la funció que assigna automàticament d'alumnes i professors a pràctiques d'empresa.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_assignacions.realitzar_assignacio_automatica()
    if resultat=="L'assignació automàtica a ocorregut sense cap problema.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta