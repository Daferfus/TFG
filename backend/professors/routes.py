from flask import Blueprint, render_template
from flask import current_app as app

import json
from flask import request, make_response, jsonify
from backend.controllers import controlador_alumnes, controlador_professors, controlador_empreses, controlador_usuaris, controlador_assignacions

# Blueprint Configuration
professors_bp = Blueprint(
    'professors_bp', __name__,
)

@professors_bp.route('/recuperar_dades_de_professors', methods=['GET'])
def iniciar_recerca_de_professors():
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_de_professors = controlador_professors.recuperar_dades_de_professors()
    resp = jsonify(success=True, message=dades_de_professors)
    return resp

@professors_bp.route('/recuperar_dades_del_professor/<string:nom_del_professor>/<string:cognoms_del_professor>', methods=['GET'])
def iniciar_recerca_del_professor(nom_del_professor, cognoms_del_professor):
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_del_professor = controlador_professors.recuperar_dades_del_professor(nom_del_professor, cognoms_del_professor)
    resp = jsonify(success=True, message=dades_del_professor)
    return resp

@professors_bp.route('/insertar_professor', methods=['POST'])
def recollir_dades_professor():
    nom = request.form['nom_del_professor']
    cognoms = request.form['cognoms_del_professor'] 
    titulacions = json.loads(request.form["titulacions_del_professor"]) 
    hores_alliberades = request.form["hores_alliberades_del_professor"] 
    hores_restants = request.form["hores_alliberades_del_professor"]
    
    controlador_professors.insertar_professor(
        nom, 
        cognoms, 
        titulacions, 
        hores_alliberades, 
        hores_restants
        )
    resp = jsonify(success=True, message="S'ha insertat amb èxit el professor "+nom+" " +cognoms+".")
    return resp


@professors_bp.route('/importar_professors', methods=['POST'])
def recollir_fitxer_professors():
    f = request.files['fichero']
    nom_del_fitxer = './professors.xls'
    f.save(nom_del_fitxer)
    controlador_professors.importar_professors(nom_del_fitxer)
    resp = jsonify(success=True, message="S'han importat amb èxit els professors.")
    return resp

@professors_bp.route('/actualitzar_professor/<string:nom_del_professor>/<string:cognoms_del_professor>', methods=["PUT"])
def recollir_nom_de_professor(nom_del_professor, cognoms_del_professor):
    nom = request.form['nom_del_professor']
    cognoms = request.form['cognoms_del_professor'] 
    titulacions = json.loads(request.form["titulacions_del_professor"]) 
    hores_alliberades = request.form["hores_alliberades_del_professor"] 
    hores_restants = request.form["hores_alliberades_del_professor"]

    controlador_professors.actualitzar_professor(
        nom_del_professor,
        cognoms_del_professor,
        nom,
        cognoms, 
        titulacions, 
        hores_alliberades, 
        hores_restants
        )

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit el professor "+nom+" "+cognoms+".")
    return resp

@professors_bp.route('/borrar_professors', methods=['DELETE'])
def eliminacio_de_professors():
    controlador_professors.borrar_professors()
    resp = jsonify(success=True, message="S'han eliminat tots els professors.")
    return resp

@professors_bp.route('/borrar_professor/<string:nom_del_professor>/<string:cognoms_del_professor>', methods=['DELETE'])
def eliminacio_de_professor(nom_del_professor, cognoms_del_professor):
    controlador_professors.borrar_professor(nom_del_professor, cognoms_del_professor)
    resp = jsonify(success=True, message="S'ha eliminat el professor "+nom_del_professor+" "+cognoms_del_professor+".")
    return resp