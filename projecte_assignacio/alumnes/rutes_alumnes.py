##########################################################################
## Autor: David Fernández Fuster                                        ##
## Data: 13/08/2022                                                     ## 
## Funció: Conté les rutes que desencandenen accions sobre els alumnes. ##
##########################################################################

################
## Llibreries ##
################
import os
import pandas as pd
import csv
import json
from munch import DefaultMunch
from urllib.request import Request

#############
##  Flask  ##
#############
from flask import current_app as app, Blueprint, Response, flash, redirect, render_template, request, make_response, jsonify, send_file, url_for
from flask_login import current_user


##############
##  Mòduls  ##
##############
from projecte_assignacio.alumnes.model_alumnes import Alumne
from ..usuaris.model_usuaris import Usuari
from .formulari_alumnes import AlumnesForm



############################
## Configuració Blueprint ##
############################
alumnes_bp = Blueprint(
    'alumnes_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

###################################
## Funcions de Retorn de Pàgines ##
###################################
@alumnes_bp.route('/perfil_alumne', methods=["GET"])
def mostrar_perfil() -> str:
    """Mostra la pàgina de perfil de l'alumne que ha iniciat la sessió.

    Returns:
        str: Pàgina de perfil de l'alumne que ha iniciat la sessió.
    """    
    alumne: Alumne = Alumne.objects(nom_de_usuari=current_user.nom).first()
    if(alumne.grup == "DAM"):
        form = AlumnesForm(
            nom_i_cognoms=alumne.nom_i_cognoms,
            ciutat_de_residencia=alumne.poblacio,
            disponibilitat_de_cotxe=alumne.mobilitat,
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
            disponibilitat_de_cotxe=alumne.mobilitat,
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
            disponibilitat_de_cotxe=alumne.mobilitat,
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
            disponibilitat_de_cotxe=alumne.mobilitat,
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
    ## if
    
    if form.validate_on_submit():
        pass
    ## if
    
    return render_template(
        'perfil_alumne.jinja2',
        title="Perfil",
        nom_de_usuari=current_user.nom,
        cicle=alumne.grup,
        form=form,
        template="perfil_alumne-template"
    )
## ()

@alumnes_bp.route('/llistat_alumnes', methods=['GET'])
@alumnes_bp.route('/llistat_alumnes/pagina/<int:pagina>')
@alumnes_bp.route('/llistat_alumnes/filtro/<string:filtro>')
@alumnes_bp.route('/llistat_alumnes/filtro/<string:filtro>/pagina/<int:pagina>')
def llistat(pagina=1, filtro="") -> str:
    """Mostra una pàgina on s'enllista els alumnes de formma paginada.

    Args:
        pagina (int, optional): Nombre de pàgina del llistat d'alumnes. Defaults to 1.
        filtro (str, optional): Text amb el que es filtra els alumnes. Defaults to ALL.
        
    Returns:
        str: Llista d'alumnes en la pàgina indicada.
    """    
    dades_de_alumnes: list[Alumne]|None = Alumne.objects(nom_i_cognoms__icontains=filtro).paginate(page=pagina, per_page=5)
    form = AlumnesForm(filtrar_alumne=filtro)
    return render_template(
        'llistat_alumnes.jinja2',
        title="Llistat d'Alumnes",
        form = form,
        alumnes=dades_de_alumnes,
        template="llistat_alumnes-template"
    )
## ()

@alumnes_bp.route('/afegir_alumne')
def afegir_alumne() -> str:
    """Mostra el formulari d'inserció d'alumne.

    Returns:
        str: Pàgina amb el formulari d'inserció d'alumne.
    """
    form = AlumnesForm()
    
    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_alumne.jinja2',
        title="Anyadir Alumne",
        accio="crear",
        form=form,
        template="formulari_alumne-template"
    )
## ()

@alumnes_bp.route('/editar_alumne/<string:usuari>')
def editar_alumne(usuari: str) -> str:
    """Mostra el formulari d'edició d'alumne.

    Args:
        usuari (str): Nom d'usuari de l'alumne a editar.

    Returns:
        str: Pàgina amb el formulari d'edició d'alumne.
    """
    alumne: Alumne = Alumne.objects(nom_de_usuari=usuari).first()

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
        pass
    ## if

    return render_template(
        'formulari_alumne.jinja2',
        title="Editar Alumne",
        accio="editar",
        cicle=alumne.grup,
        nom_de_usuari=usuari,
        form=form,
        template="formulari_alumne-template"
    )
## ()
##############################################################
##############################################################

######################################
## Funcions de Retorn d'Informació  ##
######################################
@alumnes_bp.route('/alumnes', methods=['GET'])
def obtindre_dades_de_alumnes() -> Response:
    """Retorna una llista d'alumnes.

    Returns:
        Response: Llista d'alumnes.
    """
    alumnes: list[Alumne]|None = Alumne.objects()
    
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if alumnes is None:
        resposta: Response = make_response(
            jsonify(
                success=True, 
                message="No s'ha trovat cap alumne."
            ), 
            200, 
            headers
        )
        return resposta
    else:
        resposta: Response = make_response(
            jsonify(
                success=True, 
                message=alumnes
            ), 
            200, 
            headers
        )
        return resposta
    ## if
## ()

@alumnes_bp.route('/alumne/<string:usuari>', methods=['GET'])
def obtindre_dades_del_alumne(usuari: str) -> Response:
    """Retorna un alumne donat.

    Args:
        nom_del_alumne (str): Nom de l'alumne a retornar.

    Returns:
        Response: Dades de l'alumne.
    """    
    alumne: Alumne = Alumne.objects(nom_de_usuari=usuari).first()
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if alumne is None:
        resposta: Response =  make_response(
            jsonify(
            success=False, 
            message=alumne
            ),
            200,
            headers
        )
        return resposta
    else:
        resposta: Response = make_response(
            jsonify(
            success=True, 
            message=alumne
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
@alumnes_bp.route('/insertar_alumne', methods=['POST'])
def insertar_alumne() -> Response:
    """Inserta un alumne en la base de dades.

    Args:
        nom_i_cognoms_del_alumne (str): Nom i cognoms del alumne
        grup_del_alumne (str): Cicle formatiu al que pertany el alumne.
        poblacio_del_alumne (str): Població del alumne.
        mobilitat_del_alumne (str): Si el alumne té vehicle o no.
        preferencies_del_alumne (dict[str, int]): Preferències de l'alumne cap a cer tipus de pràctiques
        tipo_de_practica_del_alumne (str, optional): Si la pràctica es FCT o DUAL. Defaults to "".
        observacions_del_alumne (str, optional): Detalls que l'alumne vol deixar clars. Defaults to "".
        aporta_empresa_el_alumne (bool, optional): Si l'alumne ha trovat pel seu compte una empresa a la que fer pràctiques. Defaults to False.
        erasmus_del_alumne (bool, optional): Si l'alumne es de erasmus. Defaults to False.
        distancies_del_alumne (list[dict[str, str, float]], optional): Les distàncies de l'alumne cap a totes les empreses. Defaults to [].
        assignacio_del_alumne (dict[str, str , str], optional): A que pràctica i tutor l'alumne està assignat. Defaults to {}.

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
    
    resposta: Response = obtindre_dades_del_alumne(nom_i_cognoms)
    alumne_existent: Alumne|None = json.loads(resposta.get_data(as_text=True))["message"]

    if alumne_existent is None:
        alumne: Alumne = Alumne(
            nom_de_usuari=nom_i_cognoms,
            nom_i_cognoms=nom_i_cognoms, 
            grup=grup, 
            poblacio=poblacio, 
            mobilitat=mobilitat, 
            tipo_de_practica=tipo_de_practica, 
            preferencies=preferencies, 
            accedeix_a_fct=accedeix_a_fct,
            observacions=observacions, 
            aporta_empresa=aporta_empresa, 
            erasmus=es_erasmus, 
            distancies=[], 
            assignacio={}
        )
        alumne.save()
        resposta: Response = obtindre_dades_del_alumne(nom_i_cognoms)
        alumne_insertat: Alumne|None = json.loads(resposta.get_data(as_text=True))["message"]

        if alumne_insertat:
            dades: dict[str, str] = {
                "nom": alumne.nom_de_usuari,
                "contrasenya": alumne.grup+"_"+alumne.nom_de_usuari+"_2022",
                "rol": "Alumne"
            }

            app.post('/registrar', data=dades)
            #rutes_usuaris.registrar_usuari(nom=alumne.nom_de_usuari, contrasenya=alumne.grup+"_"+alumne.nom_de_usuari+"_2022", rol="Alumne")
            resposta: Response = jsonify(
                success=True, 
                message="L'alumne s'ha insertat amb èxit."
            )
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if app.config["DEBUG"]:
                return resposta
            else:
                return redirect(url_for('alumnes_bp.llistat'))
        else:
            resposta: Response = jsonify(
                success=False, 
                message="Ha ocorregut un problema durant la inserció."
            )
            flash(json.loads(resposta.get_data(as_text=True))["message"])
            if app.config["DEBUG"]:
                return resposta
            else:
                return redirect(url_for('alumnes_bp.afegir_alumne'))
        ## if
    else:
        resposta: Response = jsonify(
                success=False, 
                message="Ja existeix un alumne amb aquest usuari."
            )
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
                return resposta
        else:
            return redirect(url_for('alumnes_bp.afegir_alumne'))
        ## if
    ## if
## ()

@alumnes_bp.route('/importar_alumnes', methods=['POST'])
def importar_alumnes() -> Response:
    """Inserta cada alumne trovat en un fitxer.

    Args:
        nom_del_fitxer (str): Ubicació local del fitxer.
        cicle (str): Cicle formatiu del que es vol importar els alumnes.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    cicle: str = request.form['cicle']
    f: Request = request.files['fichero']
    nom_de_fitxer: str = './projecte_assignacio/alumnes/static/files/'+cicle+'.csv';
    f.save(nom_de_fitxer)
    
    contador_de_insertats: int = 0
    quantitat_de_alumnes_ja_insertats: int = 0
    ## Accedim a dades del fitxer
    with open(nom_de_fitxer, newline='') as arxiu_csv:

        ## Gastem la funció DictReader per a que agafe la primera fila com a nom de camps.
        dades_de_alumnes = csv.DictReader(arxiu_csv)
        for dades_del_alumne in dades_de_alumnes:

            ## Clavem totes les preferències en un diccionari.
            if cicle == "DAM":
                preferencies: dict[str, int] = {
                    'Backend': dades_del_alumne["[Desarrollador backend]"], 
                    'Multiplataforma': dades_del_alumne["[Desarrollador software multiplataforma]"],
                    'Videojuegos': dades_del_alumne["[Desarrollador videojuegos]"],
                    'Moviles': dades_del_alumne["[Desarrollador de aplicaciones moviles]"],
                    'Robotica': dades_del_alumne["[Programador de robotica, automocion e informatica industrial]"],
                    'Documentacion': dades_del_alumne["[Tecnico QA y documentacion]"],
                    'ERP': dades_del_alumne["[Consultor ERP]"]
                    }
            elif cicle == "DAW":
                preferencies: dict[str, int] = {
                    'Backend': dades_del_alumne["[Desarrollador backend]"], 
                    'Frontend': dades_del_alumne["[Desarrollador frontend]"],
                    'Fullstack': dades_del_alumne["[Desarrollador fullstack]"],
                    'Disenyador': dades_del_alumne["[Disenyador]"],
                    'Documentacion': dades_del_alumne["[Tecnico QA y documentacion]"],
                    'Devops': dades_del_alumne["[Devops]"],
                    'Moviles': dades_del_alumne["[Desarrollador de aplicaciones moviles]"]
                }
            elif cicle == "ASIR":
                preferencies: dict[str, int] = {
                    'Sistemas': dades_del_alumne["[Administrador de sistemas]"],
                    'BD': dades_del_alumne["[Administrador de bases de datos]"],
                    'Redes': dades_del_alumne["[Administrador de redes]"],
                    'Ciberseguridad': dades_del_alumne["[Ciberseguridad]"],
                    'Consultor': dades_del_alumne["[Consultor TIC]"],
                    'Hardware': dades_del_alumne["[Tecnico de hardware]"],
                    'HelpDesk': dades_del_alumne["[Tecnico de soporte HelpDesk L2]"],
                    'Auditor': dades_del_alumne["[Auditor TIC]"],
                    'Monitorizador': dades_del_alumne["[Tecnico de monitorizacion de sistemas]"]
                }
            elif cicle == "TSMR":
                preferencies: dict[str, int] = {
                    'Tecnico': dades_del_alumne["[Tecnico de microinformatica]"],
                    'Asesor': dades_del_alumne["[Asesor/vendedor de microinformatica]"],
                    'HelpDesk': dades_del_alumne["[Tecnico de soporte Helpdesk L1]"],
                    'Instalador': dades_del_alumne["[Instalador de redes e infraestructura IT]"]
                }                
            ## Adjuntem el reste de dades i el diccionari de preferències en un altre diccionari
            alumne: Alumne = Alumne(
                nom_de_usuari=dades_del_alumne["Nombre y apellidos"],
                nom_i_cognoms=dades_del_alumne["Nombre y apellidos"], 
                grup=cicle, 
                poblacio=dades_del_alumne["Ciudad donde vives"], 
                mobilitat=dades_del_alumne["Podrias utilizar coche"], 
                tipo_de_practica='', 
                preferencies=preferencies, 
                accedeix_a_fct='',
                observacions='', 
                aporta_empresa='', 
                erasmus='', 
                distancies=[], 
                assignacio={}
            )
            alumne.save()
            usuari: Usuari = Usuari(
                nom=dades_del_alumne["Nombre y apellidos"], 
                contrasenya=cicle+"_"+dades_del_alumne["Nombre y apellidos"]+"_2022", 
                rol="Alumne"
            )
            usuari.establir_contrasenya(cicle+"_"+dades_del_alumne["Nombre y apellidos"]+"_2022")
            resultat = usuari.save()
            if len(resultat) > 0:
                contador_de_insertats+=1
            else:
                quantitat_de_alumnes_ja_insertats+=1
    if contador_de_insertats == 0 and quantitat_de_alumnes_ja_insertats == 0:
        resposta: Response = jsonify(sucess=False, message="Ha ocorregut un problema durant l'operació.")
        return resposta
    else:
        resposta: Response = jsonify(success=True, message="S'han insertat " +str(contador_de_insertats)+ " de 15 alumnes." +str(quantitat_de_alumnes_ja_insertats)+ " ja estaven insertades.")
        return resposta
    ## if
## ()

@alumnes_bp.route('/exportar_alumnes', methods=['GET'])
def exportar_alumnes() -> Response:
    """Exporta els alumnes de la base de dades a un fitxer xlsx.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    resposta: Response = obtindre_dades_de_alumnes()
    alumnes: list[Alumne]|None = DefaultMunch.fromDict(json.loads(resposta.get_data(as_text=True))["message"])

    alumnes_dict: list[dict] = []
    
    for alumne in alumnes:
        alumne_dict: dict = {
            "Nom": alumne.nom_i_cognoms,
            "Grup": alumne.grup,
            "Població": alumne.poblacio,
            "Mobilitat": alumne.mobilitat,
            "Preferencies": str(alumne.preferencies),
            "Tipo de Pràctica": alumne.tipo_de_practica,
            "Observacions": alumne.observacions,
            "Aporta Empresa": alumne.aporta_empresa,
            "Erasmus": alumne.erasmus,
            "Distàncies": alumne.distancies,
            "Assignacions": alumne.assignacio
        }
        alumnes_dict.append(alumne_dict)

    dades = pd.DataFrame.from_dict(alumnes_dict)
    dades.to_excel("./projecte_assignacio/alumnes/static/files/alumnes_ex.xlsx",header=True)

    if os.path.exists("./projecte_assignacio/alumnes/static/files/alumnes_ex.xlsx"):
        resposta: Response = jsonify(success=True, message="S'han exportat amb èxit les dades dels alumnes.")
        if app.config["DEBUG"]:
            return resposta
        else:
            return send_file(".\\alumnes\\static\\files\\alumnes_ex.xlsx", as_attachment=True, attachment_filename="alumnes_ex.xlsx")
    else:
        resposta: Response = jsonify(success=False, message="Hi ha hagut un problema durant l'exportació.")
    return resposta
    ## if
## ()

@alumnes_bp.route('/actualitzar_alumne/<string:grup>/<string:usuari>', methods=["POST"])
def actualitzar_alumne(grup: str, usuari: str) -> Response:
    """Actualitza les dades d'un alumne donat.

    Args:
        nom_de_alumne_per_a_filtrar (str): Nom de l'alumne a actualitzar
        nom_i_cognoms_del_alumne (str): Nou nom i cognoms de l'alumne.
        grup_del_alumne (str): Nou cicle formatiu de l'alumne.
        poblacio_del_alumne (str): Nova població de l'alumne.
        mobilitat_del_alumne (str): Nova mobilitat de l'alumne.
        preferencies_del_alumne (dict[str, int]): Noves preferències de l'alumne.
        tipo_de_practica_del_alumne (str, optional): Nou tipus de pràctica de l'alumne. Defaults to "".
        observacions_del_alumne (str, optional): Noves observacions de l'alumne. Defaults to "".
        aporta_empresa_el_alumne (bool, optional): Nova posibilitat de que l'alumne aporte pràctica. Defaults to False.
        erasmus_del_alumne (bool, optional): Nou canvi en la condició de l'estudiant. Defaults to False.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    nom_i_cognoms: str = request.form['nom_i_cognoms']
    poblacio: str = request.form['ciutat_de_residencia']
    mobilitat: str = request.form['disponibilitat_de_cotxe']
    tipo_de_practica: str = ""
    accedeix_a_fct: str = ""
    aporta_empresa: str = ""
    erasmus: str = ""
    
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


    resultat: int = Alumne.objects(nom_de_usuari=usuari).update(__raw__=
        {"$set": {
            "nom_i_cognoms": nom_i_cognoms,
            "grup": grup,
            "poblacio": poblacio,
            "mobilitat": mobilitat,
            "preferencies": preferencies,
            "tipo_de_practica": tipo_de_practica,
            "preferencies": preferencies,
            "accedeix_a_fct": accedeix_a_fct,
            "observacions": observacions,
            "aporta_empresa": aporta_empresa,
            "erasmus": erasmus
            }
        }
    )
    if resultat > 0:
        resposta: Response = jsonify(success=True, message="L'alumne ha sigut actualitzat.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
    else:
        resposta: Response = jsonify(success=False, message="No s'ha canviat res de l'alumne.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('alumnes_bp.perfil'))
    ## if
## ()

@alumnes_bp.route('/esborrar_alumnes', methods=['DELETE'])
def esborrar_alumnes() -> Response:
    """Esborra tots els alumnes.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    Alumne.objects.delete()
    alumnes: list[Alumne] = obtindre_dades_de_alumnes()
    if len(json.loads(alumnes.get_data(as_text=True))["message"]) == 0:
        resposta: Response = jsonify(
            success=True, 
            message="S'ha esborrat amb èxit tots els alumnes."
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

@alumnes_bp.route('/esborrar_alumne/<string:usuari>', methods=['POST'])
def esborrar_alumne(usuari: str) -> Response:
    """Esborra un alumne donat.

    Args:
        nom_del_alumne (str): Nom de l'alumne a esborrar.
    
    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    Alumne.objects(nom_de_usuari=usuari).delete()

    alumne: Alumne = Alumne.objects(nom_de_usuari=usuari).first()
    if alumne:
        resposta: Response = jsonify(success=False, message="Ha ocorregut un problema durant el esborrament.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('mostrar_pagina_de_inici'))
        ## if
    else:
        resposta: Response = jsonify(success=True, message="S'ha esborrat amb èxit l'alumne.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('alumnes_bp.llistat'))
        ## if
    ## if
## ()
##############################################################
##############################################################