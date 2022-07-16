from flask import Blueprint, request, make_response, jsonify
from backend.controllers import controlador_usuaris

# Blueprint Configuration
usuaris_bp = Blueprint(
    'usuaris_bp', __name__,
)

@usuaris_bp.route('/recuperar_dades_de_usuaris', methods=['GET'])
def iniciar_recerca_de_usuaris():
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_de_usuaris = controlador_usuaris.recuperar_dades_de_usuaris()
    resp = jsonify(success=True, message=dades_de_usuaris)
    return resp

@usuaris_bp.route('/recuperar_dades_del_usuari/<string:usuari>', methods=['GET'])
def iniciar_recerca_del_usuari(usuari):
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_del_usuari = controlador_usuaris.recuperar_dades_del_usuari(usuari)
    resp = jsonify(success=True, message=dades_del_usuari)
    return resp

@usuaris_bp.route('/insertar_usuari', methods=['POST'])
def recollir_dades_usuari():
    nom = request.form['nom_de_usuari'] 
    contrasenya = request.form['contrasenya_de_usuari'] 
    rol = request.form['rol_de_usuari'] 
 
    controlador_usuaris.registrar_usuari(
        nom, 
        contrasenya, 
        rol
        )
    resp = jsonify(success=True, message="S'ha insertat amb èxit el usuari "+nom+".")
    return resp


@usuaris_bp.route('/actualitzar_usuari/<string:usuari>', methods=["PUT"])
def recollir_nom_de_usuari(usuari):
    nom = request.form['nom_de_usuari'] 
    contrasenya = request.form['contrasenya_de_usuari'] 
    rol = request.form['rol_de_usuari'] 
 
    controlador_usuaris.actualitzar_credencials_del_usuari(
        usuari,
        nom, 
        contrasenya, 
        rol
        )

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit el usuari "+nom+".")
    return resp

@usuaris_bp.route('/borrar_usuaris', methods=['DELETE'])
def eliminacio_de_usuaris():
    controlador_usuaris.borrar_usuaris()
    resp = jsonify(success=True, message="S'han eliminat tots els usuaris.")
    return resp

@usuaris_bp.route('/borrar_usuari/<string:usuari>', methods=['DELETE'])
def eliminacio_de_usuari(usuari):
    controlador_usuaris.borrar_usuari(usuari)
    resp = jsonify(success=True, message="S'ha eliminat el usuari "+usuari+".")
    return resp
