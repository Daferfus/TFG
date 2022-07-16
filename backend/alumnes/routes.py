from flask import Blueprint, render_template
from flask import current_app as app

import json
from flask import request, make_response, jsonify
from backend.controllers import controlador_alumnes, controlador_professors, controlador_empreses, controlador_usuaris, controlador_assignacions

# Blueprint Configuration
alumnes_bp = Blueprint(
    'alumnes_bp', __name__,
)

@alumnes_bp.route('/recuperar_dades_de_alumnes', methods=['GET'])
def iniciar_recerca_de_alumnes():
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_de_alumnes = controlador_alumnes.recuperar_dades_de_alumnes()
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(success=True, message=dades_de_alumnes), 200, headers)

@alumnes_bp.route('/recuperar_dades_del_alumne/<alumne>', methods=['GET'])
def iniciar_recerca_del_alumne(alumne):
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_del_alumne = controlador_alumnes.recuperar_dades_del_alumne(alumne)
    resp = jsonify(success=True, message=dades_del_alumne)
    return resp

@alumnes_bp.route('/insertar_alumne', methods=['POST'])
def recollir_dades_alumne():
    nom_i_cognom = request.form['nom_i_cognom_del_alumne']
    grup = request.form['grup_del_alumne']
    poblacio = request.form['poblacio_del_alumne']
    mobilitat = request.form['mobilitat_del_alumne']
    preferencies = json.loads(request.form['preferencies_del_alumne'])
    tipo_de_practica = request.form['tipo_de_practica_del_alumne']
    observacions = request.form['observacions_del_alumne']
    aporta_empresa = request.form['aporta_empresa_el_alumne']
    erasmus = request.form['erasmus_del_alumne']
    
    controlador_alumnes.insertar_alumne(
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
    resp = jsonify(success=True, message="S'ha insertat amb èxit el alumne "+nom_i_cognom+".")
    return resp

@alumnes_bp.route('/importar_alumnes', methods=['POST'])
def recollir_fitxer_alumnes():
    cicle = request.form['cicle']
    f = request.files['fichero']
    nom_de_fitxer = './'+cicle+'.csv';
    f.save(nom_de_fitxer)
    
    controlador_alumnes.importar_alumnes(nom_de_fitxer, cicle)
    resp = jsonify(success=True, message="S'han importat amb èxit els alumnes de "+cicle+".")
    return resp

@alumnes_bp.route('/actualitzar_alumne/<alumne>', methods=["PUT"])
def recollir_nom_de_alumne(alumne):
    nom_i_cognom = request.form['nom_i_cognom_del_alumne']
    grup = request.form['grup_del_alumne']
    poblacio = request.form['poblacio_del_alumne']
    mobilitat = request.form['mobilitat_del_alumne']
    preferencies = json.loads(request.form['preferencies_del_alumne'])
    tipo_de_practica = request.form['tipo_de_practica_del_alumne']
    observacions = request.form['observacions_del_alumne']
    aporta_empresa = request.form['aporta_empresa_el_alumne']
    erasmus = request.form['erasmus_del_alumne']

    controlador_alumnes.actualitzar_alumne(
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

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit el alumne "+nom_i_cognom+".")
    return resp


@alumnes_bp.route('/borrar_alumnes', methods=['DELETE'])
def eliminacio_de_alumnes():
    controlador_alumnes.borrar_alumnes()
    resp = jsonify(success=True, message="S'han eliminat tots els alumnes.")
    return resp

@alumnes_bp.route('/borrar_alumne/<alumne>', methods=['DELETE'])
def eliminacio_de_alumne(alumne):
    controlador_alumnes.borrar_alumne(alumne)
    resp = jsonify(success=True, message="S'ha eliminat el alumne "+alumne+".")
    return resp