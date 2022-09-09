###########################################################################
## Autor: David Fernández Fuster                                         ##
## Data: 23/08/2022                                                      ## 
## Funció: Conté les rutes que desencandenen accions sobre les empreses. ##
###########################################################################

################
## Llibreries ##
################
import json
import os
import pandas as pd
from munch import DefaultMunch
from urllib.request import Request


#############
##  Flask  ##
#############
from flask import current_app as app, Blueprint, Response, make_response, request, flash, redirect, url_for, render_template, jsonify
from flask_login import current_user


##############
##  Mòduls  ##
##############
from projecte_assignacio.empreses.formulari_empreses import EmpresesForm
from projecte_assignacio.empreses.formulari_practiques import PractiquesForm
from projecte_assignacio.empreses.model_empreses import Empresa
from projecte_assignacio.usuaris.model_usuaris import Usuari


############################
## Configuració Blueprint ##
############################
empreses_bp = Blueprint(
    'empreses_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


###################################
## Funcions de Retorn de Pàgines ##
###################################
@empreses_bp.route('/perfil_empresa', methods=["GET"])
def mostrar_perfil() -> str:
    """Mostra la pàgina de perfil de l'empresa.

    Returns:
        str: Pàgina de perfil de l'empresa.
    """    
    empresa: Empresa|None = Empresa.objects(nom_de_usuari=current_user.nom).first()

    form = EmpresesForm(
            nom=empresa.nom,
            poblacio=empresa.poblacio,
            telefon=empresa.telefon,
            correu=empresa.correu,
            nom_de_persona_de_contacte=empresa.persona_de_contacte,
            volen_practica=empresa.volen_practica
        )
    
    if form.validate_on_submit():
        pass
    ## if
    
    return render_template(
        'perfil_empresa.jinja2',
        title="Perfil",
        nom_de_usuari=current_user.nom,
        form=form,
        template="perfil_empresa-template"
    )
## ()


@empreses_bp.route('/llistat_empreses', methods=['GET'])
@empreses_bp.route('/llistat_empreses/pagina/<int:pagina>')
def llistat(pagina=1) -> str:
    """Mostra una pàgina on s'enllista les empreses de forma paginada.

    Args:
        pagina (int, optional): Nombre de pàgina del llistat d'empreses. Defaults to 1.
        
    Returns:
        str: Llista d'empreses en la pàgina indicada.
    """    
    dades_de_empreses: list[Empresa]|None = Empresa.objects.paginate(page=pagina, per_page=5)
    return render_template(
        'llistat_empreses.jinja2',
        title="Llistat d'Empreses",
        form = EmpresesForm(),
        empreses=dades_de_empreses,
        template="llistat_empreses-template"
    )
## ()

@empreses_bp.route('/anyadir_empresa/<string:nombre_de_empresa>', methods=["GET"])
def anyadir_empresa(nombre_de_empresa: str):
    """Mostra el formulari d'inserció d'empresa.

    Returns:
        str: Pàgina amb el formulari d'inserció d'empresa.
    """
    form = EmpresesForm()
    
    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_empresa.jinja2',
        title="Anyadir Empresa",
        accio="crear",
        nombre_de_empresa=nombre_de_empresa,
        form=form,
        template="formulari_empresa-template"
    )
## ()

@empreses_bp.route('/editar_empresa/<string:usuari>', methods=["GET"])
def editar_empresa(usuari: str):
    """Mostra el formulari d'edició d'empresa.

    Args:
        usuari (str): Nom d'usuari de l'empresa a editar.

    Returns:
        str: Pàgina amb el formulari d'edició d'empresa.
    """
    empresa: Empresa = Empresa.objects(nom_de_usuari=usuari).first()
    
    form = EmpresesForm(
            nom=empresa.nom,
            poblacio=empresa.poblacio,
            telefon=empresa.telefon,
            correu=empresa.correu,
            nom_de_persona_de_contacte=empresa.persona_de_contacte
        )
    
    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_empresa.jinja2',
        title="Editar Alumne",
        accio="editar",
        nom_de_usuari=usuari,
        form=form,
        template="formulari_empresa-template"
    )
## ()

@empreses_bp.route('/practiques', methods=["GET"])
def practiques() -> str:
    """Mostra una pàgina on s'enllista les pràctiques de la empresa en sessió.

    Returns:
        str: Llista de pràcticques en la pàgina indicada.
    """    
    empresa: Empresa = Empresa.objects(nom_de_usuari=current_user.nom).first()

    return render_template(
        'practiques_empresa.jinja2',
        title="Pràctiques",
        nom_de_usuari=current_user.nom,
        practiques_de_empresa=empresa.practiques,
        template="practiques_empresa-template"
    )
## ()

@empreses_bp.route('/anyadir_practica', methods=["GET"])
def anyadir_practica() -> str:
    """Mostra el formulari d'inserció de pràctica.

    Returns:
        str: Pàgina amb el formulari d'inserció de pràctica.
    """
    form = PractiquesForm()

    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'practica_empresa.jinja2',
        title="Anyadir Pràctica",
        accio="crear",
        nom_de_usuari=current_user.nom,
        form=form,
        template="practica_empresa-template"
    )
## ()

@empreses_bp.route('/editar_practica/<int:nombre_de_practica>')
def editar_practica(nombre_de_practica: int):
    """Mostra el formulari d'edició de pràctica.

    Args:
        usuari (str): Nom d'usuari de l'empresa a editar.

    Returns:
        str: Pàgina amb el formulari d'edició de pràctica.
    """
    empresa: Empresa = Empresa.objects(nom_de_usuari=current_user.nom).first()
    practica = empresa.practiques[nombre_de_practica]

    form = PractiquesForm(
            nom=practica["Nom"],
            titulacio=practica["Titulacio"],
            descripcio=practica["Descripcio"],
            tecnologies_i_frameworks=practica["Tecnologies i Frameworks"]
        )

    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'practica_empresa.jinja2',
        title="Editar Pràctica",
        accio="editar",
        nombre_de_practica =nombre_de_practica,
        nom_de_usuari=current_user.nom,
        form=form,
        template="practica_empresa-template"
    )
## ()
##############################################################
##############################################################

######################################
## Funcions de Retorn d'Informació  ##
######################################
@empreses_bp.route('/empreses', methods=['GET'])
def obtindre_dades_de_empreses() -> Response:
    """Retorna una llista d'empreses.

    Returns:
        Response: Llista d'empreses.
    """
    empreses: list[Empresa]|None = Empresa.objects()
    
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if empreses is None:
        resposta: Response = make_response(
            jsonify(
                success=True, 
                message="No s'ha trovat cap professor."
            ), 
            200, 
            headers
        )
        return resposta
    else:
        resposta: Response = make_response(
            jsonify(
                success=True, 
                message=empreses
            ), 
            200, 
            headers
        )
        return resposta
    ## if
## ()

@empreses_bp.route('/empresa/<string:usuari>', methods=['GET'])
def obtindre_dades_de_la_empresa(usuari: str) -> Response:
    """Retorna una empresa donada.

    Args:
        usuari (str): nom d'usuari de la empresa a retornar.

    Returns:
        Response: Dades de l'empresa.
    """    
    empresa: Empresa = Empresa.objects(nom_de_usuari=usuari).first()
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if empresa is None:
        resposta: Response =  make_response(
            jsonify(
            success=False, 
            message=empresa
            ),
            200,
            headers
        )
        return resposta
    else:
        resposta: Response = make_response(
            jsonify(
            success=True, 
            message=empresa
            ),
            200,
            headers
        )
        return resposta
    ## if
## ()
##############################################################
##############################################################

#######################################
## Funcions de Modificació de Dades  ##
#######################################
@empreses_bp.route('/insertar_empresa/<int:nombre_de_empresa>', methods=['POST'])
def insertar_empresa(nombre_de_empresa: int) -> Response:
    """Crida a la funció per a insertar una empresa.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom: str = request.form['nom'] 
    poblacio: str = request.form['poblacio'] 
    telefon: int = request.form['telefon'] 
    correu: str = request.form['correu'] 
    persona_de_contacte: str = request.form['nom_de_persona_de_contacte']
    
    resposta: Response = obtindre_dades_de_la_empresa("empresa"+str(nombre_de_empresa))
    empresa_existent: Empresa|None = json.loads(resposta.get_data(as_text=True))["message"]

    if empresa_existent is None:
        empresa: Empresa = Empresa(
            nom_de_usuari="empresa"+str(nombre_de_empresa),
            nom=nom, 
            poblacio=poblacio, 
            telefon=telefon, 
            correu=correu, 
            persona_de_contacte=persona_de_contacte, 
            practiques=[],
            assignacions=[]
        )
        empresa.save()
        empresa_insertada: Empresa|None = obtindre_dades_de_la_empresa("empresa"+str(nombre_de_empresa))

        if empresa_insertada:
            dades: dict[str, str] = {
                "nom": empresa.nom_de_usuari,
                "contrasenya": empresa.nom_de_usuari+"_2022",
                "rol": "Empresa"
            }
            app.post('/registrar', data=dades)
            resposta: Response = jsonify(
                success=True, 
                message="L'empresa s'ha insertat amb èxit."
            )
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if app.config["DEBUG"]:
                return resposta
            else:
                return redirect(url_for('usuaris_bp.home'))
        else:
            resposta: Response = jsonify(
                success=False, 
                message="Ha ocorregut un problema durant la inserció."
            )
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if app.config["DEBUG"]:
                return resposta
            else:
                return redirect(url_for('empreses_bp.anyadir_empresa'))
        ## if
    else:
        resposta: Response = jsonify(
                success=False, 
                message="Ja existeix una empresa amb aquest usuari."
            )
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
                return resposta
        else:
            return redirect(url_for('empreses_bp.anyadir_empresa'))
        ## if
    ## if
## ()

@empreses_bp.route('/importar_empreses', methods=['POST'])
def importar_empreses() -> Response:
    """Inserta cada empresa trovada en un fitxer.

    Args:
        nom_del_fitxer (str): Ubicació local del fitxer.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    f: Request = request.files['fichero']
    nom_del_fitxer: str = './projecte_assignacio/empreses/static/file/empreses.xls'
    f.save(nom_del_fitxer)
    
    df = pd.read_excel(nom_del_fitxer)
    empreses: list[dict] = []
    ciutat_empreses: list[dict] = []
    nombre_de_fila: int = 0

    contador_de_insertats: int = 0
    quantitat_de_empreses_ja_insertats: int = 0

    while nombre_de_fila < len(df):
        empresa: dict = {}
        empresa["VolenPractica"]: str = "No"
        empresa["Ciutat"]: str = ""
        preferencies: dict = {}
        nombre_de_practiques: int = 0
        for columna in df:
            ## Nombre de pràctiques que ofereix.
            if columna == "TSMR" or columna == "ASIR" or columna == "DAM" or columna == "DAW":
                if not pd.isnull(df.loc[nombre_de_fila, columna]):
                    preferencies[columna]: int = df.loc[nombre_de_fila, columna]
                    nombre_de_practiques+=int(df.loc[nombre_de_fila, columna])
                    empresa["Preferencies"]: dict = preferencies
                    empresa["Practiques"]: int = nombre_de_practiques
                    if nombre_de_practiques > 0:
                        empresa["VolenPractica"]: str = "Sí"
            else:
                if not pd.isnull(df.loc[nombre_de_fila, columna]):
                    empresa[columna]: str = df.loc[nombre_de_fila, columna]
        ## for

        ## Si ofereix pràctiques s'anyadix al diccionari.
        practiques: list = list()
        practica: dict = dict()
        if empresa["Practiques"] != 0:
            if "Ciutat" in empresa:
                empreses.append(empresa)
                if empresa["Ciutat"] not in ciutat_empreses:
                    ciutat_empreses.append(empresa["Ciutat"])

                contador_practiques:int = 0
                for x, y in empresa["Preferencies"].items():
                    while(y>0):
                        contador_practiques+=1
                        
                        practica["Nom"] = "Pràctica"+str(contador_practiques)
                        practica["Titulacio"] = x
                        practica["Descripcio"] = ""
                        practica["Tecnologies i Frameworks"] = list()
                        practiques.append(practica)
                        y-=1
                    ## while
                ## for
            ## if
        empresa: Empresa = Empresa(
            nom_de_usuari="empresa"+str(nombre_de_fila),
            nom=empresa["Empresa"], 
            poblacio=empresa["Ciutat"], 
            telefon=0, 
            correu="", 
            persona_de_contacte="", 
            volen_practica=empresa["VolenPractica"],
            practiques=practiques,
            assignacions=[]
        )
        empresa.save()

                    
        usuari: Usuari = Usuari(
            nom="empresa"+str(nombre_de_fila), 
            contrasenya="empresa"+str(nombre_de_fila)+"_2022", 
            rol="Empresa"
        )
        
        usuari.establir_contrasenya("empresa"+str(nombre_de_fila)+"_2022")
        resultat = usuari.save()
                    
        if len(resultat) > 0:
            contador_de_insertats+=1
        else:
            quantitat_de_empreses_ja_insertats+=1
        ## if
        
        nombre_de_fila+=1
    ## while

    if contador_de_insertats == 0 and quantitat_de_empreses_ja_insertats == 0:
        resposta: Response = jsonify(sucess=False, message="Ha ocorregut un problema durant l'operació.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message="S'han insertat " +str(contador_de_insertats)+ " de " +str(len(df))+ " empreses." +str(quantitat_de_empreses_ja_insertats)+ " ja estaven insertades.")
        return resposta
    ## if
## ()

@empreses_bp.route('/exportar_empreses', methods=['GET'])
def exportar_empreses() -> Response:
    """Exporta les empreses de la base de dades a un fitxer xlsx.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resposta: Response = obtindre_dades_de_empreses()
    empreses: list[Empresa]|None = DefaultMunch.fromDict(json.loads(resposta.get_data(as_text=True))["message"])

    empreses_dict: list[dict] = []

    for empresa in empreses:
        empresa_dict: dict = {
            "Nom": empresa.nom,
            "Població": empresa.poblacio,
            "Telefon": empresa.telefon,
            "Correu": empresa.correu,
            "Persona de Contacte": empresa.persona_de_contacte,
            "Pràctiques": str(empresa.practiques),
            "Assignacions": empresa.assignacions
        }
        empreses_dict.append(empresa_dict)
    
    dades = pd.DataFrame.from_dict(empreses_dict)
    dades.to_excel("empreses_ex.xlsx",header=True)

    if os.path.exists("empreses_ex.xlsx"):
        resposta: Response = jsonify(success=True, message="S'han exportat amb èxit les dades de les empreses.")
        return resposta
    else:
        resposta: Response = jsonify(success=False, message="Hi ha hagut un problema durant l'exportació.")
    return resposta
    ## if
## ()

@empreses_bp.route('/actualitzar_empresa/<string:usuari>', methods=["POST"])
def actualitzar_empresa(usuari: str) -> Response:
    """Actualitza les dades d'una empresa donada.

    Args:
        nom_de_empresa_per_a_filtrar (str): Nom de la empresa a actualitzar.
        nom_de_empresa (str): Nou nom de la empresa.
        poblacio_de_empresa (str): Nova població de la empresa.
        telefon_de_empresa (int): Nou telefon de l'empresa.
        correu_de_empresa (str): Nou correu de l'empresa.
        persona_de_contacte_en_la_empresa (str): Nova persona de contacte en l'empresa.

    Returns:
        str: Resultat de l'operació.
    """
    nom: str = request.form['nom'] 
    poblacio: str = request.form['poblacio'] 
    telefon: int = request.form['telefon'] 
    correu: str = request.form['correu'] 
    persona_de_contacte: str = request.form['nom_de_persona_de_contacte']

    resultat: int = Empresa.objects(nom_de_usuari=usuari).update(__raw__=
        {"$set": {
            "nom": nom,
            "poblacio": poblacio,
            "telefon": telefon,
            "correu": correu,
            "persona_de_contacte": persona_de_contacte,
            }
        }
    )

    if resultat > 0:
        resposta: Response = jsonify(success=True, message="L'empresa ha sigut actualitzada.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
    else:
        resposta: Response = jsonify(success=False, message="No s'ha canviat res de l'empresa.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('empreses_bp.perfil'))
    ## if
## ()


@empreses_bp.route('/esborrar_empreses', methods=['DELETE'])
def esborrar_empreses() -> Response:
    """Esborra totes les empreses.

    Returns:
        str: Resultat de l'operació.
    """
    Empresa.objects.delete()

    empreses: list[Empresa] = obtindre_dades_de_empreses()
    if len(json.loads(empreses.get_data(as_text=True))["message"]) == 0:
        resposta: Response = jsonify(
            success=True, 
            message="S'ha esborrat amb èxit totes les empreses."
            )
        return resposta
    else:
        resposta: Response = jsonify(
            success=False, 
            message="Ha ocorregut un problema durant el esborrament."
            )
        return resposta
    ## if
## ()

@empreses_bp.route('/esborrar_empresa/<string:usuari>', methods=['POST'])
def esborrar_empresa(usuari: str):
    """Esborra una empresa donada.

    Args:
        nom_del_professor (str): Nom del professor a esborrar.
        cognoms_del_professor (str): Cognoms del professor a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    Empresa.objects(nom_de_usuari=usuari).delete()

    empresa: Empresa = Empresa.objects(nom_de_usuari=usuari).first()
    if empresa:
        resposta: Response = jsonify(success=False, message="Ha ocorregut un problema durant el esborrament.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
        ## if
    else:
        resposta: Response = jsonify(success=True, message="S'ha esborrat amb èxit l'empresa.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('empreses_bp.llistat'))
        ## if
    ## if
## ()
@empreses_bp.route('/insertar_practica/<string:usuari>', methods=['POST'])
def insertar_practica(usuari: str) -> Response:
    """Anyadix una pràctica a la llista de pràctiques ofertada per l'empresa.

    Args:
        nom_de_empresa_per_a_filtrar (str): Nom de l'empresa que oferta la pràctica.
        practica_de_la_empresa (dict): Pràctica a anyadir.

    Returns:
        str: Resultat de l'operació.
    """
    practiques: dict = {
        "Nom": request.form['nom'],
        "Titulacio": request.form["titulacio"],
        "Descripcio": request.form["descripcio"],
        "Tecnologies i Frameworks": request.form["tecnologies_i_frameworks"]
    }

    empresa: Empresa = Empresa.objects(nom_de_usuari=usuari).get()
    if empresa:
        practica_existeix: Empresa = Empresa.objects(nom_de_usuari=usuari, practiques=practiques).first()
        if practica_existeix:
            resposta: Response = jsonify(success=False, message="La pràctica ja existeix.")
            if app.config["DEBUG"]:
                return resposta
            else:
                flash(json.loads(resposta.get_data(as_text=True))["message"])
                return redirect(url_for('empreses_bp.afegir_practica'))
        else:
            empresa.practiques.append(practiques)
            empresa.save()
            resposta: Response = jsonify(success=True, message="Pràctica insertada.")
            if app.config["DEBUG"]:
                return resposta
            else:
                flash(json.loads(resposta.get_data(as_text=True))["message"])
                return redirect(url_for('empreses_bp.practiques'))
    else:
        resposta: Response = jsonify(success=False, message="L'empresa no existeix.")
        if app.config["DEBUG"]:
                return resposta
        else:
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            return redirect(url_for('mostrar_pagina_de_inici'))

@empreses_bp.route('/actualitzar_practica/<string:usuari>/<int:nombre_de_practica>', methods=["POST"])
def actualitzar_practica(usuari: str, nombre_de_practica: int) -> Response:
    """Actualitza una pràctica donada.

    Args:
        nom_de_empresa_per_a_filtrar (str): Empresa de la que es vol actualitzar la pràctica.
        practica_a_filtrar (dict): Pràctica a actualitzar.
        practica_de_la_empresa (dict): Nova informació de la pràctica.

    Returns:
        str: Resultat de l'operació.
    """
    practica_actualitzada: dict = {
        "Nom": request.form['nom'],
        "Titulacio": request.form['titulacio'],
        "Descripcio": request.form['descripcio'],
        "Tecnologies i Frameworks": request.form['tecnologies_i_frameworks'],
    }
    practica_a_actualitzar: int = nombre_de_practica
    empresa: Empresa = Empresa.objects(nom_de_usuari=usuari).first()
    empresa.practiques[practica_a_actualitzar] = practica_actualitzada
    empresa.save()

    practica_existeix: Empresa = Empresa.objects(nom_de_usuari=usuari, practiques=practica_actualitzada).first()

    if practica_existeix:
        resposta: Response = jsonify(success=True, message="La pràctica ha sigut actualitzada.")
        flash("La pràctica ha sigut actualitzada.")
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
    else:
        resposta: Response = jsonify(success=False, message="No s'ha canviat res de la pràctica.")
        flash("No s'ha canviat res de la pràctica.")
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('empreses_bp.editar_practica'))

@empreses_bp.route('/esborrar_practica/<string:usuari>/<int:nombre_de_practica>', methods=['POST'])
def esborrar_practica(usuari: str, nombre_de_practica: int) -> Response:
    """Esborra una pràctica donada.

    Args:
        nom_de_empresa_per_a_filtrar (str): Empresa de la que es vol esborrar la pràctica.
        practica_de_la_empresa (dict): Pràctica a esborrar.

    Returns:
        str: Resultat de l'operació.
    """
    empresa: Empresa = Empresa.objects(nom_de_usuari=usuari).first()
    resultat = empresa.practiques.pop(nombre_de_practica)
    empresa.save()
    if resultat:
        resposta: Response = jsonify(success=True, message="La pràctica ha sigut esborrada.")
        flash(resultat)
        if app.config["DEBUG"]:
            return resposta
        else:        
            return redirect(url_for('empreses_bp.practiques'))
    else:
        resposta: Response = jsonify(success=False, message="No s'ha trovat la pràctica a esborrar.")
        flash(resultat)
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('empreses_bp.practiques'))
