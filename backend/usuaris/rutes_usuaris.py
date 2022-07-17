import json
from flask_login import logout_user, current_user
from flask import Blueprint, request, jsonify
from backend.usuaris import controlador_usuaris
from backend import login_manager
from backend.usuaris.model_usuaris import Usuari

# Blueprint Configuration
usuaris_bp = Blueprint(
    'usuaris_bp', __name__,
)

@usuaris_bp.route('/hello')
def hello():
    return 'Hello, World!'

@usuaris_bp.route('/recuperar_dades_de_usuaris', methods=['GET'])
def iniciar_recerca_de_usuaris():
    dades_de_usuaris: list[Usuari] = controlador_usuaris.recuperar_dades_de_usuaris()
    if dades_de_usuaris is None:
        resposta = jsonify(success=False, message="No s'ha trovat cap usuari.")
        return resposta
    else:
        resposta = jsonify(success=True, message=dades_de_usuaris)
        return resposta

@usuaris_bp.route('/recuperar_dades_del_usuari/<string:usuari>', methods=['GET'])
def iniciar_recerca_del_usuari(usuari: str):
    dades_del_usuari: Usuari = controlador_usuaris.recuperar_dades_del_usuari(usuari)
    if dades_del_usuari is None:
        resposta = jsonify(success=False, message="No s'ha trovat cap usuari.")
        return resposta
    else:
        resposta = jsonify(success=True, message=dades_del_usuari)
        return resposta

@usuaris_bp.route('/registrar_usuari', methods=['POST'])
def recollir_dades_usuari():
    nom: str = request.form['nom_de_usuari'] 
    contrasenya: str = request.form['contrasenya_de_usuari'] 
    rol: str = request.form['rol_de_usuari'] 
 
    resultat: str = controlador_usuaris.registrar_usuari(
        nom, 
        contrasenya, 
        rol
        )
    if resultat == "L'usuari s'ha registrat amb èxit.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(success=False, message=resultat)
        return resposta

@usuaris_bp.route('/autenticar_usuari', methods=['POST'])
def comprovar_dades_del_usuari(): 
    nom: str = request.form['nom_de_usuari'] 
    contrasenya: str = request.form['contrasenya_de_usuari']
    resultat: str = controlador_usuaris.autenticar_usuari(nom, contrasenya)
    
    if resultat == "Usuari autenticat.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(success=False, message=resultat)
        return resposta

@usuaris_bp.route('/logout', methods=['GET'])
def logout():
    """User log-out logic."""
    logout_user()

    if current_user.is_authenticated:
        resposta = jsonify(success=False, message="No s'ha tancat la sessió amb èxit.")
        return resposta
    else:
        resposta = jsonify(success=True, message="S'ha tancat la sessió amb èxit.")
        return resposta

@usuaris_bp.route('/actualitzar_usuari/<string:usuari>', methods=["PUT"])
def recollir_nom_de_usuari(usuari: str):
    nom: str = request.form['nom_de_usuari'] 
    contrasenya: str = request.form['contrasenya_de_usuari'] 
    rol: str = request.form['rol_de_usuari'] 
 
    resultat: str = controlador_usuaris.actualitzar_credencials_del_usuari(
        usuari,
        nom, 
        contrasenya, 
        rol
        )

    if resultat=="L'usuari ha sigut actualitzat.":
        resposta = jsonify(success=True, message=resultat)
    else:
        resposta = jsonify(success=False, message=resultat)
    return resposta

@usuaris_bp.route('/esborrar_usuaris', methods=['DELETE'])
def eliminacio_de_usuaris():
    resultat: str = controlador_usuaris.esborrar_usuaris()

    if resultat == "S'ha esborrat amb èxit tots els usuaris.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(success=False, message=resultat)
        return resposta

@usuaris_bp.route('/esborrar_usuari/<string:usuari>', methods=['DELETE'])
def eliminacio_de_usuari(usuari):
    resultat: str = controlador_usuaris.esborrar_usuari(usuari)
    
    if resultat == "S'ha esborrat amb èxit l'usuari.":
        resposta = jsonify(success=True, message=resultat)
        return resposta
    else:
        resposta = jsonify(succes=False, message=resultat)
        return resposta

@login_manager.user_loader
def load_user(id_de_usuari):
    """Check if user is logged-in on every page load."""
    if id_de_usuari is not None:
        return Usuari.objects(pk=id_de_usuari).first()
    return None


# @login_manager.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash('You must be logged in to view that page.')
#     return redirect(url_for('auth_bp.login'))