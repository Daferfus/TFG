from flask import Blueprint, render_template
from flask import current_app as app

import json
from flask import request, make_response, jsonify
from backend.controllers import controlador_alumnes, controlador_professors, controlador_empreses, controlador_usuaris, controlador_assignacions

# Blueprint Configuration
empreses_bp = Blueprint(
    'empreses', __name__,
)

@empreses_bp.route('/recuperar_dades_de_empreses', methods=['GET'])
def iniciar_recerca_de_empreses():
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_de_empreses = controlador_empreses.recuperar_dades_de_empreses()
    resp = jsonify(success=True, message=dades_de_empreses)
    return resp

@empreses_bp.route('/recuperar_dades_de_la_empresa/<empresa>', methods=['GET'])
def iniciar_recerca_de_la_empresa(empresa):
    if request.method != 'GET':
        return make_response('Tipo de Petición Incorrecto', 400)
    dades_de_la_empresa = controlador_empreses.recuperar_dades_de_la_empresa(empresa)
    resp = jsonify(success=True, message=dades_de_la_empresa)
    return resp

@empreses_bp.route('/insertar_empresa', methods=['POST'])
def recollir_dades_empresa():
    nom = request.form['nom_de_empresa'] 
    poblacio = request.form['poblacio_de_empresa'] 
    telefon = request.form['telefon_de_empresa'] 
    correu = request.form['correu_de_empresa'] 
    persona_de_contacte = request.form['persona_de_contacte_en_la_empresa']

    controlador_empreses.insertar_empresa(
        nom, 
        poblacio, 
        telefon, 
        correu,
        persona_de_contacte
        )
    resp = jsonify(success=True, message="S'ha insertat amb èxit el professor "+nom+".")
    return resp

@empreses_bp.route('/importar_empreses', methods=['POST'])
def recollir_fitxer_empreses():
    f = request.files['fichero']
    nom_del_fitxer = './empreses.xls'
    f.save(nom_del_fitxer)
    controlador_empreses.importar_empreses(nom_del_fitxer)
    resp = jsonify(success=True, message="S'han importat amb èxit les empreses.")
    return resp

@empreses_bp.route('/actualitzar_empresa', methods=["PUT"])
def recollir_nom_de_empresa():
    nom_de_empresa_per_a_filtrar = request.args.get("nom")
    nom = request.form['nom_de_empresa'] 
    poblacio = request.form['poblacio_de_empresa'] 
    telefon = request.form['telefon_de_empresa'] 
    correu = request.form['correu_de_empresa'] 
    persona_de_contacte = request.form['persona_de_contacte_en_la_empresa']

    controlador_empreses.actualitzar_empresa(
        nom_de_empresa_per_a_filtrar,
        nom, 
        poblacio, 
        telefon, 
        correu,
        persona_de_contacte
        )
    resp = jsonify(success=True, message="S'ha actualitzat amb èxit l'empresa "+nom+".")
    return resp


@empreses_bp.route('/borrar_empreses', methods=['DELETE'])
def eliminacio_de_empreses():
    controlador_empreses.borrar_empreses()
    resp = jsonify(success=True, message="S'han eliminat totes les empreses.")
    return resp

@empreses_bp.route('/borrar_empresa', methods=['DELETE'])
def eliminacio_de_empresa():
    nom_de_empresa_per_a_filtrar = request.args.get("nom_de_empresa")
    controlador_empreses.borrar_empresa(nom_de_empresa_per_a_filtrar)
    resp = jsonify(success=True, message="S'ha eliminat la empresa "+nom_de_empresa_per_a_filtrar+".")
    return resp


@empreses_bp.route('/insertar_practica', methods=['POST'])
def recollir_dades_practica():
    nom_de_empresa_per_a_filtrar = request.args.get("nom")
    practiques = json.loads(request.form['practiques_de_la_empresa'])

    controlador_empreses.insertar_practica(
        nom_de_empresa_per_a_filtrar,
        practiques
    )

    resp = jsonify(success=True, message="S'ha anyadit amb èxit una nova oferta de pràctica de l'empresa "+nom_de_empresa_per_a_filtrar+".")
    return resp

@empreses_bp.route('/actualitzar_practica', methods=["PUT"])
def recollir_nom_de_la_practica():
    nom_de_empresa_per_a_filtrar = request.args.get("nom_empresa")
    practica_a_filtrar = request.args.get("practica")
    practica = json.loads(request.form['practica_de_la_empresa'])

    controlador_empreses.actualitzar_practica(
        nom_de_empresa_per_a_filtrar,
        practica_a_filtrar,
        practica
    )

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit l'oferta de pràctiques de l'empresa "+str(practica_a_filtrar)+".")
    return resp

@empreses_bp.route('/borrar_practica', methods=['DELETE'])
def eliminacio_de_practica():
    nom_de_empresa_per_a_filtrar = request.args.get("nom_empresa")
    practica_a_borrar = request.args.get("nom_de_la_practica")
    controlador_empreses.borrar_practica(nom_de_empresa_per_a_filtrar, practica_a_borrar)
    resp = jsonify(success=True, message="S'ha eliminat la pràctica "+str(practica_a_borrar)+".")
    return resp
