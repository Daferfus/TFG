import json
from urllib.request import Request
from flask import Blueprint, Response, request, make_response, jsonify
from backend.alumnes import controlador_alumnes
from backend.alumnes.model_alumnes import Alumne

# Blueprint Configuration
alumnes_bp = Blueprint(
    'alumnes_bp', __name__,
)

@alumnes_bp.route('/recuperar_dades_de_alumnes', methods=['GET'])
def iniciar_recerca_de_alumnes() -> Response:
    """Crida a la funció per a obtindre les dades de tots els alumnes.

    Returns:
        Response: Dades de tots els alumnes.
    """
    dades_de_alumnes: list[Alumne]|None = controlador_alumnes.recuperar_dades_de_alumnes()
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if dades_de_alumnes is None:
        resposta: Response = make_response(jsonify(success=True, message="No s'ha trovat cap alumne."), 200, headers)
        return resposta
    else:
        resposta: Response = make_response(jsonify(success=True, message=dades_de_alumnes), 200, headers)
        return resposta

@alumnes_bp.route('/recuperar_dades_del_alumne/<string:alumne>', methods=['GET'])
def iniciar_recerca_del_alumne(alumne: str) -> Response:
    """Crida a la funció per a obtindre les dades d'un alumne determinat.

    Args:
        alumne (str): Nom de l'alumne a buscar.

    Returns:
        Response: Dades de l'alumne.
    """    
    dades_del_alumne: Alumne|None = controlador_alumnes.recuperar_dades_del_alumne(alumne)
    if dades_del_alumne is None:
        resposta: Response = jsonify(success=False, message="No s'ha trovat el alumne.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=dades_del_alumne)
        return resposta

@alumnes_bp.route('/insertar_alumne', methods=['POST'])
def recollir_dades_alumne() -> Response:
    """Crida a la funció per a insertar un alumne.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom_i_cognom: str = request.form['nom_i_cognom_del_alumne']
    grup: str = request.form['grup_del_alumne']
    poblacio: str = request.form['poblacio_del_alumne']
    mobilitat: str = request.form['mobilitat_del_alumne']
    preferencies: dict = json.loads(request.form['preferencies_del_alumne'])
    tipo_de_practica: str = request.form['tipo_de_practica_del_alumne']
    observacions: str = request.form['observacions_del_alumne']
    aporta_empresa: bool = request.form['aporta_empresa_el_alumne']
    erasmus: bool = request.form['erasmus_del_alumne']
    
    resultat: str = controlador_alumnes.insertar_alumne(
        nom_i_cognom, 
        grup, 
        poblacio, 
        mobilitat, 
        preferencies, 
        tipo_de_practica, 
        observacions, 
        aporta_empresa, 
        erasmus
        )
    if resultat == "L'alumne s'ha insertat amb èxit.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@alumnes_bp.route('/importar_alumnes', methods=['POST'])
def recollir_fitxer_alumnes() -> Response:
    """Crida a la funció per a importar alumnes a partir d'un arxiu.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    cicle: str = request.form['cicle']
    f: Request = request.files['fichero']
    nom_de_fitxer: str = './'+cicle+'.csv';
    f.save(nom_de_fitxer)
    
    resultat: str = controlador_alumnes.importar_alumnes(nom_de_fitxer, cicle)
    if resultat == "Ha ocorregut un problema durant l'operació.":
        resposta: Response = jsonify(sucess=False, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta

@alumnes_bp.route('/exportar_alumnes', methods=['GET'])
def descarregar_fitxer_alumnes() -> Response:
    """Crida a la funció per a exportar alumnes de la base de dades.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat:bool = controlador_alumnes.exportar_alumnes()
    if resultat:
        resposta: Response = jsonify(success=resultat, message="S'han exportat amb èxit les dades dels alumnes.")
        return resposta
    else:
        resposta: Response = jsonify(success=resultat, message="Hi ha hagut un problema durant l'exportació.")
    return resposta

@alumnes_bp.route('/actualitzar_alumne/<string:alumne>', methods=["PUT"])
def recollir_nom_de_alumne(alumne: str) -> Response:
    """Crida a la funció per a actualitzar un alumne donat.

    Args:
        alumne (str): Nom de l'alumne a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom_i_cognom: str = request.form['nom_i_cognom_del_alumne']
    grup: str = request.form['grup_del_alumne']
    poblacio: str = request.form['poblacio_del_alumne']
    mobilitat: str = request.form['mobilitat_del_alumne']
    preferencies: dict = json.loads(request.form['preferencies_del_alumne'])
    tipo_de_practica: str = request.form['tipo_de_practica_del_alumne']
    observacions: str = request.form['observacions_del_alumne']
    aporta_empresa: bool = request.form['aporta_empresa_el_alumne']
    erasmus: bool = request.form['erasmus_del_alumne']

    resultat: str = controlador_alumnes.actualitzar_alumne(
        alumne,
        nom_i_cognom, 
        grup, 
        poblacio, 
        mobilitat, 
        preferencies, 
        tipo_de_practica, 
        observacions, 
        aporta_empresa, 
        erasmus
        )

    if resultat=="L'alumne ha sigut actualitzat.":
        resposta: Response = jsonify(success=True, message=resultat)
    else:
        resposta: Response = jsonify(success=False, message=resultat)
    return resposta


@alumnes_bp.route('/esborrar_alumnes', methods=['DELETE'])
def eliminacio_de_alumnes() -> Response:
    """Crida a la funció per a esborrar tots els alumnes.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_alumnes.esborrar_alumnes()
    if resultat == "S'ha esborrat amb èxit tots els alumnes.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta

@alumnes_bp.route('/esborrar_alumne/<string:alumne>', methods=['DELETE'])
def eliminacio_de_alumne(alumne: str) -> Response:
    """Crida a la funció per a esborrar un alumne donat.

    Args:
        alumne (str): Nom de l'alummne a esborrar.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_alumnes.esborrar_alumne(alumne)
    if resultat == "S'ha esborrat amb èxit l'alumne.":
        resposta: Response = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        return resposta