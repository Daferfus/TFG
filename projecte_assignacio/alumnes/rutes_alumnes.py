import json
from urllib.request import Request
from flask import Blueprint, Response, flash, redirect, render_template, request, make_response, jsonify, url_for
from flask_login import current_user
from projecte_assignacio.alumnes import controlador_alumnes
from projecte_assignacio.alumnes.model_alumnes import Alumne
from .formulari_alumnes import AlumnesForm

# Blueprint Configuration
alumnes_bp = Blueprint(
    'alumnes_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@alumnes_bp.route('/perfil', methods=["GET", "POST"])
def perfil():
    alumne: Alumne = controlador_alumnes.recuperar_dades_del_alumne(current_user.nom)
    if(alumne.grup == "DAM"):
        form = AlumnesForm(
            nom_i_cognoms=alumne.nom_i_cognoms,
            ciutat_de_residencia=alumne.poblacio,
            disponibilitat_de_cotxe=alumne.mobilitat.encode("windows-1252").decode("utf-8"),
            preferencies_dam={
                'desenvolupador_backend': alumne.preferencies["Backend"],
                'desenvolupador_software_multiplataforma': alumne.preferencies["Multiplataforma"],
                'desenvolupador_de_videojocs': alumne.preferencies["Videojuegos"],
                'desenvolupador_de_aplicacions_mobils': alumne.preferencies["Moviles"],
                'robotica_automocio_i_informatica_tradicional': alumne.preferencies["Robotica"],
                'tecnic_qa_i_documentacio': alumne.preferencies["Documentacion"],
                'consultor_erp': alumne.preferencies["ERP"],
                },
            observacions=alumne.observacions
        )
    elif(alumne.grup == "DAW"):
        form = AlumnesForm(
            nom_i_cognoms=alumne.nom_i_cognoms,
            ciutat_de_residencia=alumne.poblacio,
            disponibilitat_de_cotxe=alumne.mobilitat.encode("windows-1252").decode("utf-8"),
            preferencies_daw={
                'desenvolupador_backend': alumne.preferencies["Backend"],
                'desenvolupador_frontend': alumne.preferencies["Frontend"],
                'desenvolupador_fullstack': alumne.preferencies["Fullstack"],
                'dissenyador': alumne.preferencies["Disenyador"],
                'tecnic_qa_i_documentacio': alumne.preferencies["Documentacion"],
                'devops': alumne.preferencies["Devops"],
                'desenvolupador_de_aplicacions_mobils': alumne.preferencies["Moviles"],
                },
            observacions=alumne.observacions
        )
    elif(alumne.grup == "TSMR"):
        form = AlumnesForm(
            nom_i_cognoms=alumne.nom_i_cognoms,
            ciutat_de_residencia=alumne.poblacio,
            disponibilitat_de_cotxe=alumne.mobilitat.encode("windows-1252").decode("utf-8"),
            preferencies_tsmr={
                'tecnic_de_microinformatica': alumne.preferencies["Tecnico"],
                'asesor_de_microinformatica': alumne.preferencies["Asesor"],
                'tecnic_de_soport_helpdesk_l1': alumne.preferencies["HelpDesk"],
                'instalador_de_xarxes_i_infraestructura_it': alumne.preferencies["Instalador"],
                },
            observacions=alumne.observacions
        )
    elif(alumne.grup == "ASIR"):
        form = AlumnesForm(
            nom_i_cognoms=alumne.nom_i_cognoms,
            ciutat_de_residencia=alumne.poblacio,
            disponibilitat_de_cotxe=alumne.mobilitat.encode("windows-1252").decode("utf-8"),
            preferencies_asir={
                'administrador_de_base_de_dades': alumne.preferencies["BD"],
                'administrador_de_xarxes': alumne.preferencies["Redes"],
                'ciberseguretat': alumne.preferencies["Ciberseguridad"],
                'administrador_de_sistemes': alumne.preferencies["Sistemas"],
                'consultor_tic': alumne.preferencies["Consultor"],
                'tecnic_de_hardware': alumne.preferencies["Hardware"],
                'tecnic_de_soport_helpdesk_l2': alumne.preferencies["HelpDesk"],
                'auditor_tic': alumne.preferencies["Auditor"],
                'tecnic_de_monitoritzacio_de_xarxes': alumne.preferencies["Monitorizador"],
                },
            observacions=alumne.observacions
        )
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'perfil_alumne.jinja2',
        title="Perfil",
        nom_de_usuari=current_user.nom,
        cicle=alumne.grup,
        form=form,
        template="perfil_alumne-template"
    )

@alumnes_bp.route('/llistat_alumnes', methods=['GET'])
def llistat():
    dades_de_alumnes: list[Alumne]|None = controlador_alumnes.recuperar_dades_de_alumnes()
    return render_template(
        'llistat_alumnes.jinja2',
        title="Llistat d'Alumnes",
        alumnes=dades_de_alumnes,
        template="llistat_alumnes-template"
    )


@alumnes_bp.route('/anyadir_alumne')
def anyadir_alumne():
    form = AlumnesForm()
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'formulari_alumne.jinja2',
        title="Anyadir Alumne",
        accio="crear",
        form=form,
        template="formulari_alumne-template"
    )

@alumnes_bp.route('/editar_alumne/<string:usuari>')
def editar_alumne(usuari: str):
    alumne: Alumne = controlador_alumnes.recuperar_dades_del_alumne(usuari)
    print(alumne.erasmus)
    form = AlumnesForm(
            nom_i_cognoms=alumne.nom_i_cognoms,
            grup=alumne.grup,
            ciutat_de_residencia=alumne.poblacio,
            disponibilitat_de_cotxe=alumne.mobilitat,
            tipo_de_practica=alumne.tipo_de_practica,
            accedeix_a_fct=alumne.accedeix_a_fct,
            observacions=alumne.observacions,
            aporta_empresa=alumne.aporta_empresa,
            es_erasmus=alumne.erasmus
        )
    if form.validate_on_submit():
        print("woah");
    return render_template(
        'formulari_alumne.jinja2',
        title="Editar Alumne",
        accio="editar",
        cicle=alumne.grup,
        nom_de_usuari=usuari,
        form=form,
        template="formulari_alumne-template"
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
    nom_i_cognoms: str = request.form['nom_i_cognoms']
    grup: str = request.form['grup']
    poblacio: str = request.form['ciutat_de_residencia']
    mobilitat: str = request.form['disponibilitat_de_cotxe']
    if 'preferencies_del_alumne' in request.form:
        preferencies: dict = json.loads(request.form['preferencies_del_alumne'])
    else:
        preferencies: dict = dict()
    tipo_de_practica: str = request.form['tipo_de_practica']
    accedeix_a_fct: str = request.form['accedeix_a_fct']
    observacions: str = request.form['observacions']
    aporta_empresa: bool = request.form['aporta_empresa']
    es_erasmus: bool = request.form['es_erasmus']
    
    resultat: str = controlador_alumnes.insertar_alumne(
        nom_i_cognoms,
        nom_i_cognoms, 
        grup, 
        poblacio, 
        mobilitat, 
        preferencies, 
        tipo_de_practica, 
        accedeix_a_fct,
        observacions, 
        aporta_empresa, 
        es_erasmus
        )
    if resultat == "L'alumne s'ha insertat amb èxit.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.anyadir_alumne'))
        #return resposta

@alumnes_bp.route('/importar_alumnes', methods=['POST'])
def recollir_fitxer_alumnes() -> Response:
    """Crida a la funció per a importar alumnes a partir d'un arxiu.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    cicle: str = request.form['cicle']
    f: Request = request.files['fichero']
    nom_de_fitxer: str = './projecte_assignacio/alumnes/static/files/'+cicle+'.csv';
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

@alumnes_bp.route('/actualitzar_alumne/<string:grup>/<string:usuari>', methods=["POST"])
def recollir_nom_de_alumne(grup: str, usuari: str) -> Response:
    """Crida a la funció per a actualitzar un alumne donat.

    Args:
        alumne (str): Nom de l'alumne a actualitzar.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    print(request.form)
    nom_i_cognom: str = request.form['nom_i_cognoms']
    poblacio: str = request.form['ciutat_de_residencia']
    mobilitat: str = request.form['disponibilitat_de_cotxe']

    if(grup=="DAM" and 'preferencies_dam-desenvolupador_backend' in request.form):
        preferencies: dict = {
            "Backend": request.form['preferencies_dam-desenvolupador_backend'],
            "Multiplataforma": request.form['preferencies_dam-desenvolupador_software_multiplataforma'],
            "Videojuegos": request.form['preferencies_dam-desenvolupador_de_videojocs'],
            "Moviles": request.form['preferencies_dam-desenvolupador_de_aplicacions_mobils'],
            "Robotica": request.form['preferencies_dam-robotica_automocio_i_informatica_tradicional'],
            "Documentacion": request.form['preferencies_dam-tecnic_qa_i_documentacio'],
            "ERP": request.form['preferencies_dam-consultor_erp']
        }
    elif(grup=="DAW" and 'preferencies_daw-desenvolupador_backend' in request.form):
        preferencies: dict = {
            'Backend': request.form['preferencies_daw-desenvolupador_backend'],
            'Frontend': request.form['preferencies_daw-desenvolupador_frontend'],
            'Fullstack': request.form['preferencies_daw-desenvolupador_fullstack'],
            'Disenyador': request.form['preferencies_daw-dissenyador'],
            'Documentacion': request.form['preferencies_daw-tecnic_qa_i_documentacio'],
            'Devops': request.form['preferencies_daw-devops'],
            'Moviles': request.form['preferencies_daw-desenvolupador_de_aplicacions_mobils'],
        },
    elif(grup=="TSMR" and 'preferencies_tsmr-tecnic_de_microinformatica' in request.form):
        preferencies: dict = {
            'Tecnico': request.form['preferencies_tsmr-tecnic_de_microinformatica'],
            'Asesor': request.form['preferencies_tsmr-asesor_de_microinformatica'],
            'HelpDesk': request.form['preferencies_tsmr-tecnic_de_soport_helpdesk_l1'],
            'Instalador': request.form['preferencies_tsmr-instalador_de_xarxes_i_infraestructura_it'],
        }
    elif(grup=="ASIR" and 'preferencies_asir-administrador_de_xarxes' in request.form):
        preferencies: dict = {
            'BD': request.form['preferencies_asir-administrador_de_base_de_dades'],
            'Redes': request.form['preferencies_asir-administrador_de_xarxes'],
            'Ciberseguridad': request.form['preferencies_asir-ciberseguretat'],
            'Sistemas': request.form['preferencies_asir-administrador_de_sistemes'],
            'Consultor': request.form['preferencies_asir-consultor_tic'],
            'Hardware': request.form['preferencies_asir-tecnic_de_hardware'],
            'HelpDesk': request.form['preferencies_asir-tecnic_de_soport_helpdesk_l2'],
            'Auditor': request.form['preferencies_asir-auditor_tic'],
            'Monitorizador': request.form['preferencies_asir-tecnic_de_monitoritzacio_de_xarxes'],
        }
    else:
        preferencies: dict = {'BD': 1}
        tipo_de_practica: str = request.form['tipo_de_practica']
        accedeix_a_fct: str = request.form['accedeix_a_fct']
        aporta_empresa: str = request.form['aporta_empresa']
        erasmus: bool = request.form['es_erasmus']
    
    observacions: str = request.form['observacions']


    resultat: str = controlador_alumnes.actualitzar_alumne(
        usuari,
        nom_i_cognom, 
        grup, 
        poblacio, 
        mobilitat, 
        preferencies,
        tipo_de_practica,
        accedeix_a_fct,
        observacions, 
        aporta_empresa, 
        erasmus
        )

    if resultat=="L'alumne ha sigut actualitzat.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('alumnes_bp.perfil'))
        #return resposta


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

@alumnes_bp.route('/esborrar_alumne/<string:usuari>', methods=['POST'])
def eliminacio_de_alumne(usuari: str) -> Response:
    """Crida a la funció per a esborrar un alumne donat.

    Args:
        alumne (str): Nom de l'alummne a esborrar.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resultat: str = controlador_alumnes.esborrar_alumne(usuari)
    if resultat == "S'ha esborrat amb èxit l'alumne.":
        resposta: Response = jsonify(success=True, message=resultat)
        flash(resultat)
        return redirect(url_for('usuaris_bp.home'))
        #return resposta
    else:
        resposta: Response = jsonify(success=False, message=resultat)
        flash(resultat)
        return redirect(url_for('alumnes_bp.llistat'))
        return resposta