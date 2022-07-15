from flask import Blueprint, render_template
from flask import current_app as app

import json
from flask import request, make_response, jsonify
from backend.controllers import controlador_alumnes, controlador_professors, controlador_empreses, controlador_usuaris, controlador_assignacions

# Blueprint Configuration
assignacions_bp = Blueprint(
    'assignacions_bp', __name__,
)

@assignacions_bp.route('/insertar_assignacio_manual', methods=['POST'])
def recollir_dades_assignacio():
    nom_de_alumne_per_a_filtrar = request.args.get("nom_de_alumne")
    nom_de_professor_per_a_filtrar = request.args.get("nom_de_professor")
    cognoms_de_professor_per_a_filtrar = request.args.get("cognoms_de_professor")
    nom_de_empresa_per_a_filtrar = request.args.get("nom_de_empresa")

    alumne = request.form['alumne']
    practica = request.form['practica']
    professor = request.form['professor']

    assignacio = {"Alumne": alumne, "Practica": nom_de_alumne_per_a_filtrar+"_"+practica, "Professor": professor}
    controlador_assignacions.insertar_assignacio_manual(
        nom_de_alumne_per_a_filtrar,
        nom_de_professor_per_a_filtrar,
        cognoms_de_professor_per_a_filtrar,
        nom_de_empresa_per_a_filtrar,
        assignacio
    )

    resp = jsonify(success=True, message="S'ha anyadit amb èxit l'assignació "+alumne+"-"+practica+"-"+professor+".")
    return resp


@assignacions_bp.route('/actualitzar_assignacio', methods=['PUT'])
def actualitzar_assignacio():
    nom_de_alumne_per_a_filtrar = request.args.get("nom_de_alumne")
    nom_de_empresa_per_a_filtrar = request.args.get("nom_de_empresa")
    nom_de_practica_per_a_filtrar = request.args.get("nom_de_practica")
    nom_de_professor_per_a_filtrar = request.args.get("nom_de_professor")
    cognoms_de_professor_per_a_filtrar = request.args.get("cognoms_de_professor")

    alumne = request.form['alumne']
    practica = request.form['practica']
    professor = request.form['professor']

    assignacio = {"Alumne": alumne, "Practica": alumne+"_"+practica, "Professor": professor}
    controlador_assignacions.insertar_assignacio_manual(
        nom_de_alumne_per_a_filtrar,
        nom_de_empresa_per_a_filtrar,
        nom_de_practica_per_a_filtrar,
        nom_de_professor_per_a_filtrar,
        cognoms_de_professor_per_a_filtrar,
        assignacio
    )

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit l'assignació "+alumne+"-"+practica+"-"+professor+".")
    return resp

@assignacions_bp.route('/borrar_assignacio', methods=['DELETE'])
def eliminacio_de_assignacio():
    nom_de_alumne_per_a_filtrar = request.args.get("nom_de_alumne")
    nom_de_empresa_per_a_filtrar = request.args.get("nom_de_empresa")
    nom_de_practica_per_a_filtrar = request.args.get("nom_de_practica")
    nom_de_professor_per_a_filtrar = request.args.get("nom_de_professor")
    cognoms_de_professor_per_a_filtrar = request.args.get("cognoms_de_professor")

    assignacio = {
        "Alumne": nom_de_alumne_per_a_filtrar, 
        "Practica": nom_de_empresa_per_a_filtrar+"_"+nom_de_practica_per_a_filtrar, 
        "Professor": nom_de_professor_per_a_filtrar+" "+cognoms_de_professor_per_a_filtrar}
    controlador_assignacions.borrar_assignacio(
        nom_de_professor_per_a_filtrar, 
        cognoms_de_professor_per_a_filtrar, 
        nom_de_empresa_per_a_filtrar,
        assignacio
    )
    resp = jsonify(success=True, message="S'ha eliminat l'assignació "+str(assignacio)+".")
    return resp