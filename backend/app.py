import json

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from controller import controlador_alumnes, controlador_professors, controlador_empreses, controlador_usuaris, controlador_assignacions


############################
## Establir Base de Dades ##
############################
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "FP",
}
db = MongoEngine(app)
####################################
####################################

#########
## GET ##
#########
@app.route('/recuperar_dades_de_alumnes', method=['GET'])
def iniciar_recerca_de_alumnes():
    dades_de_alumnes = controlador_alumnes.recuperar_dades_de_alumnes()
    resp = jsonify(success=True, message=dades_de_alumnes)
    return resp

@app.route('/recuperar_dades_del_alumne', method=['GET'])
def iniciar_recerca_del_alumne():
    nom_i_cognom = request.form['nom_i_cognom_del_alumne']
    dades_del_alumne = controlador_alumnes.recuperar_dades_del_alumne(nom_i_cognom)
    resp = jsonify(success=True, message=dades_del_alumne)
    return resp

@app.route('/recuperar_dades_de_professors', method=['GET'])
def iniciar_recerca_de_professors():
    dades_de_professors = controlador_professors.recuperar_dades_de_professors()
    resp = jsonify(success=True, message=dades_de_professors)
    return resp

@app.route('/recuperar_dades_del_professor', method=['GET'])
def iniciar_recerca_del_professor():
    nom = request.form['nom_del_professor']
    cognoms = request.form['cognoms_del_professor'] 
    dades_del_professor = controlador_professors.recuperar_dades_del_professor(nom, cognoms)
    resp = jsonify(success=True, message=dades_del_professor)
    return resp

@app.route('/recuperar_dades_de_empreses', method=['GET'])
def iniciar_recerca_de_empreses():
    dades_de_empreses = controlador_empreses.recuperar_dades_de_empreses()
    resp = jsonify(success=True, message=dades_de_empreses)
    return resp

@app.route('/recuperar_dades_de_la_empresa', method=['GET'])
def iniciar_recerca_de_la_empresa():
    nom = request.form['nom_de_empresa'] 
    dades_de_la_empresa = controlador_empreses.recuperar_dades_de_la_empresa(nom)
    resp = jsonify(success=True, message=dades_de_la_empresa)
    return resp

@app.route('/recuperar_dades_de_usuaris', method=['GET'])
def iniciar_recerca_de_usuaris():
    dades_de_usuaris = controlador_alumnes.recuperar_dades_de_usuaris()
    resp = jsonify(success=True, message=dades_de_usuaris)
    return resp

@app.route('/recuperar_dades_del_usuari', method=['GET'])
def iniciar_recerca_del_usuari():
    nom = request.form['nom_del_usuari'] 
    dades_del_usuari = controlador_usuaris.recuperar_dades_del_usuari(nom)
    resp = jsonify(success=True, message=dades_del_usuari)
    return resp
######################################################################################
######################################################################################


############
### POST ###
############
@app.route('/insertar_alumne', methods=['POST'])
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


@app.route('/insertar_professor', methods=['POST'])
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


@app.route('/insertar_empresa', methods=['POST'])
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


@app.route('/insertar_practica', methods=['POST'])
def recollir_dades_practica():
    nom_de_empresa_per_a_filtrar = request.args.get("nom")
    practiques = json.loads(request.form['practiques_de_la_empresa'])

    controlador_empreses.insertar_practica(
        nom_de_empresa_per_a_filtrar,
        practiques
    )

    resp = jsonify(success=True, message="S'ha anyadit amb èxit una nova oferta de pràctica de l'empresa "+nom_de_empresa_per_a_filtrar+".")
    return resp

@app.route('/insertar_usuari', methods=['POST'])
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


@app.route('/insertar_assignacio_manual', methods=['POST'])
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
######################################################################################
######################################################################################


##################
### Importació ###
##################
@app.route('/importar_alumnes', methods=['POST'])
def recollir_fitxer_alumnes():
    cicle = request.form['cicle']
    f = request.files['fichero']
    nom_de_fitxer = './'+cicle+'.csv';
    f.save(nom_de_fitxer)
    
    controlador_alumnes.importar_alumnes(nom_de_fitxer, cicle)
    resp = jsonify(success=True, message="S'han importat amb èxit els alumnes de "+cicle+".")
    return resp

@app.route('/importar_professors', methods=['POST'])
def recollir_fitxer_professors():
    f = request.files['fichero']
    nom_del_fitxer = './professors.xls'
    f.save(nom_del_fitxer)
    controlador_professors.importar_professors(nom_del_fitxer)
    resp = jsonify(success=True, message="S'han importat amb èxit els professors.")
    return resp

@app.route('/importar_empreses', methods=['POST'])
def recollir_fitxer_empreses():
    f = request.files['fichero']
    nom_del_fitxer = './empreses.xls'
    f.save(nom_del_fitxer)
    controlador_empreses.importar_empreses(nom_del_fitxer)
    resp = jsonify(success=True, message="S'han importat amb èxit les empreses.")
    return resp
######################################################################################
######################################################################################


###########
### PUT ###
###########
@app.route('/actualitzar_alumne', methods=["PUT"])
def recollir_nom_de_alumne():
    nom_de_alumne_per_a_filtrar = request.args.get("nom")
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
        nom_de_alumne_per_a_filtrar,
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


@app.route('/actualitzar_professor', methods=["PUT"])
def recollir_nom_de_professor():
    nom_de_professor_per_a_filtrar = request.args.get("nom")
    cognoms_de_professor_per_a_filtrar = request.args.get("cognoms")
    nom = request.form['nom_del_professor']
    cognoms = request.form['cognoms_del_professor'] 
    titulacions = json.loads(request.form["titulacions_del_professor"]) 
    hores_alliberades = request.form["hores_alliberades_del_professor"] 
    hores_restants = request.form["hores_alliberades_del_professor"]

    controlador_professors.actualitzar_professor(
        nom_de_professor_per_a_filtrar,
        cognoms_de_professor_per_a_filtrar,
        nom,
        cognoms, 
        titulacions, 
        hores_alliberades, 
        hores_restants
        )

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit el professor "+nom+" "+cognoms+".")
    return resp


@app.route('/actualitzar_empresa', methods=["PUT"])
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

@app.route('/actualitzar_practica', methods=["PUT"])
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

@app.route('/actualitzar_usuari', methods=["PUT"])
def recollir_nom_de_usuari():
    nom_de_usuari_per_a_filtrar = request.args.get("nom")
    nom = request.form['nom_de_usuari'] 
    contrasenya = request.form['contrasenya_de_usuari'] 
    rol = request.form['rol_de_usuari'] 
 
    controlador_usuaris.actualitzar_credencials_del_usuari(
        nom_de_usuari_per_a_filtrar,
        nom, 
        contrasenya, 
        rol
        )

    resp = jsonify(success=True, message="S'ha actualitzat amb èxit el usuari "+nom+".")
    return resp

@app.route('/actualitzar_assignacio', methods=['PUT'])
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
######################################################################################
######################################################################################


############
## DELETE ##
############
@app.route('/borrar_alumnes', methods=['DELETE'])
def eliminacio_de_alumnes():
    controlador_alumnes.borrar_alumnes()
    resp = jsonify(success=True, message="S'han eliminat tots els alumnes.")
    return resp

@app.route('/borrar_alumne', methods=['DELETE'])
def eliminacio_de_alumne():
    nom_de_alumne_per_a_filtrar = request.args.get("nom_de_alumne")
    controlador_alumnes.borrar_alumne(nom_de_alumne_per_a_filtrar)
    resp = jsonify(success=True, message="S'ha eliminat el alumne "+nom_de_alumne_per_a_filtrar+".")
    return resp

@app.route('/borrar_professors', methods=['DELETE'])
def eliminacio_de_professors():
    controlador_professors.borrar_professors()
    resp = jsonify(success=True, message="S'han eliminat tots els professors.")
    return resp

@app.route('/borrar_professor', methods=['DELETE'])
def eliminacio_de_professor():
    nom_de_professor_per_a_filtrar = request.args.get("nom_de_professor")
    cognoms_de_professor_per_a_filtrar = request.args.get("cognoms_de_professor")
    controlador_professors.borrar_professor(nom_de_professor_per_a_filtrar, cognoms_de_professor_per_a_filtrar)
    resp = jsonify(success=True, message="S'ha eliminat el professor "+nom_de_professor_per_a_filtrar+" "+cognoms_de_professor_per_a_filtrar+".")
    return resp

@app.route('/borrar_empreses', methods=['DELETE'])
def eliminacio_de_empreses():
    controlador_empreses.borrar_empreses()
    resp = jsonify(success=True, message="S'han eliminat totes les empreses.")
    return resp

@app.route('/borrar_empresa', methods=['DELETE'])
def eliminacio_de_empresa():
    nom_de_empresa_per_a_filtrar = request.args.get("nom_de_empresa")
    controlador_empreses.borrar_empresa(nom_de_empresa_per_a_filtrar)
    resp = jsonify(success=True, message="S'ha eliminat la empresa "+nom_de_empresa_per_a_filtrar+".")
    return resp

@app.route('/borrar_practica', methods=['DELETE'])
def eliminacio_de_practica():
    nom_de_empresa_per_a_filtrar = request.args.get("nom_empresa")
    practica_a_borrar = request.args.get("nom_de_la_practica")
    controlador_empreses.borrar_practica(nom_de_empresa_per_a_filtrar, practica_a_borrar)
    resp = jsonify(success=True, message="S'ha eliminat la pràctica "+str(practica_a_borrar)+".")
    return resp

@app.route('/borrar_usuaris', methods=['DELETE'])
def eliminacio_de_usuaris():
    controlador_usuaris.borrar_usuaris()
    resp = jsonify(success=True, message="S'han eliminat tots els usuaris.")
    return resp

@app.route('/borrar_usuari', methods=['DELETE'])
def eliminacio_de_usuari():
    nom_de_usuari_per_a_filtrar = request.args.get("nom_de_usuari")
    controlador_usuaris.borrar_usuari(nom_de_usuari_per_a_filtrar)
    resp = jsonify(success=True, message="S'ha eliminat el usuari "+nom_de_usuari_per_a_filtrar+".")
    return resp

@app.route('/borrar_assignacio', methods=['DELETE'])
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
######################################################################################
######################################################################################