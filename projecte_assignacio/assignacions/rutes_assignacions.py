import json
from munch import DefaultMunch
from flask import (
    current_app as app,
    Blueprint, 
    Response, 
    jsonify, 
    request, 
    render_template, 
    flash, 
    redirect, 
    url_for, 
    session,
    g
)

from flask_login import current_user
from projecte_assignacio.assignacions.formulari_assignacions import AssignacionsForm

from projecte_assignacio.usuaris.model_usuaris import Usuari

from .. import celery
from projecte_assignacio.assignacions import model_de_optimitzacio
from projecte_assignacio.alumnes import rutes_alumnes
from projecte_assignacio.empreses import rutes_empreses
from projecte_assignacio.professors import rutes_professors
from projecte_assignacio.alumnes.model_alumnes import Alumne
from projecte_assignacio.empreses.model_empreses import Empresa
from projecte_assignacio.professors.model_professors import Professor
from projecte_assignacio import r
# Blueprint Configuration
assignacions_bp = Blueprint(
    'assignacions_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@assignacions_bp.route('/assignacio')
@assignacions_bp.route('/assignacio/pagina/<int:pagina>')
@assignacions_bp.route('/assignacio/filtro/<string:filtro>')
@assignacions_bp.route('/assignacio/filtro/<string:filtro>/pagina/<int:pagina>')
def mostrar_panel_de_assignacio(pagina=1, filtro=""):
    alumnes: list[Alumne]|None = Alumne.objects(nom_i_cognoms__icontains=filtro).paginate(page=pagina, per_page=5)
    form = AssignacionsForm(filtrar_assignacions=filtro)
    return render_template(
        'assignacio.jinja2',
        title="Panel d'Assignació",
        alumnes=alumnes,
        form=form,
        description="Resolució d'un problema d'assignació d'alumne i professors a pràctiques d'empresa."
    )

@assignacions_bp.route('/afegir_assignacio', methods=["GET"])
def afegir_assignacio():
    """Mostra el formulari d'assignació.

    Returns:
        str: Pàgina amb el formulari d'assignacio.
    """
    resposta_alumnes: Response = rutes_alumnes.obtindre_dades_de_alumnes()
    alumnes: list[Alumne]|None = DefaultMunch.fromDict(json.loads(resposta_alumnes.get_data(as_text=True))["message"])

    resposta_professors: Response = rutes_professors.obtindre_dades_de_professors()
    professors: list[Professor]|None = DefaultMunch.fromDict(json.loads(resposta_professors.get_data(as_text=True))["message"])

    empreses: list[Empresa]|None = Empresa.objects()
    
    form = AssignacionsForm()
    form.alumne.choices = [(alumne.nom_i_cognoms, alumne.nom_i_cognoms) for alumne in alumnes]
    form.professor.choices = [(professor.nom, professor.nom) for professor in professors]
    form.empresa.choices = [(empresa.nom + "("+practica["Nom"]+")", empresa.nom+ "("+practica["Nom"]+")") for empresa in empreses for practica in empresa.practiques]

    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_assignacio.jinja2',
        title="Assignar",
        accio="crear",
        form=form,
        template="formulari_assignacio-template"
    )
## ()
@assignacions_bp.route('/editar_assignacio/<string:alumne>', methods=["GET"])
@assignacions_bp.route('/editar_assignacio/<string:professor>/<string:alumne>/<string:practica>', methods=["GET"])
def editar_assignacio(professor: str = "", alumne: str = "", practica: str = ""):
    """Mostra el formulari d'edició d'assignació.

    Args:
        usuari (str): Nom d'usuari de l'assignació a editar.

    Returns:
        str: Pàgina amb el formulari d'edició d'assignacio.
    """
    form = AssignacionsForm()
    resposta_alumnes: Response = rutes_alumnes.obtindre_dades_de_alumnes()
    alumnes: list[Alumne]|None = DefaultMunch.fromDict(json.loads(resposta_alumnes.get_data(as_text=True))["message"])

    resposta_professors: Response = rutes_professors.obtindre_dades_de_professors()
    professors: list[Professor]|None = DefaultMunch.fromDict(json.loads(resposta_professors.get_data(as_text=True))["message"])

    empreses: list[Empresa]|None = Empresa.objects()
    
    form = AssignacionsForm()
    form.alumne.choices = [(alumne.nom_i_cognoms, alumne.nom_i_cognoms) for alumne in alumnes]
    form.professor.choices = [(professor.nom, professor.nom) for professor in professors]
    form.empresa.choices = [(empresa.nom + "("+practica["Nom"]+")", empresa.nom+ "("+practica["Nom"]+")") for empresa in empreses for practica in empresa.practiques]
    
    form.alumne.data = alumne
    form.professor.data = professor
    form.empresa.data = practica

    if form.validate_on_submit():
        pass
    ## if

    return render_template(
        'formulari_assignacio.jinja2',
        title="Editar Assignació",
        accio="editar",
        form=form,
        template="formulari_assignacio-template"
    )
## ()

@assignacions_bp.route('/inserir_assignacio', methods=['POST'])
def inserir_assignacio() -> Response:
    """Crida a la funció per a assignar a cascuna de les parts a una pràctica.

    Args:
        alumne (str): Alumne protagonista de l'assignació.
        nom_de_professor (str): Nom del professor que farà el seguiment de l'alumne.
        cognoms_de_professor (str): Cognoms del professor encarregat de fer el seguiment de l'alumne.
        empresa (str): Empresa en la que el alumne farà la practica.
        practica (str): Pràctica a la que s'assigna l'alumne.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    alumne: str = request.form['alumne'];
    professor: str = request.form['professor'];
    practica: str = request.form['empresa'];
    assignacio: dict[str, str] = {
        "alumne": alumne,
        "professor": professor,
        "practica": practica
    }
    Alumne.objects(nom_i_cognoms=alumne).update(__raw__=
        {"$set": {
            "assignacio": assignacio
            }
        }
    )

    professor: Professor = Professor.objects(nom=professor, cognoms=professor).get()
    professor.assignacions.append(assignacio)
    professor.save()
    
    parts_de_practica = practica.split("(") 

    empresa: Empresa = Empresa.objects(nom=parts_de_practica[0]).get()
    empresa.assignacions.append(assignacio)
    empresa.save()

    assignacio_insertada: Alumne|None = Alumne.objects(assignacio=assignacio).first()
    if assignacio_insertada is not None:
        resposta: Response = jsonify(success=True, message="L'assignació s'ha inserit.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('assignacions_bp.mostrar_panel_de_assignacio'))
    else:
        resposta: Response = jsonify(success=False, message="No s'ha inserit cap assignacio.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('assignacions_bp.afegir_assignacio'))

@assignacions_bp.route('/actualitzar_assignacio', methods=['POST'])
def actualitzar_assignacio() -> Response:
    """Crida a la funció per a actualitzar una assignació donada.

    Args:
        alumne (str): Alumne al que se li vol actualitzar l'assignació.
        nom_de_professor (str): Nom del professor encarregat de fer un seguiment de la pràctica.
        cognoms_de_professor (str): Cognoms del professor encarregat de fer un seguiment de la pràctica.
        empresa (str): Empresa que oferta la pràctica.
        practica (str): Pràctica a la que s'assigna.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    alumne: str = request.form['alumne']
    professor: str = request.form['professor']
    practica: str = request.form['empresa']
    empresa: str = practica.split("(")[0]
    assignacio: dict[str, str] = {
        "Alumne": alumne,
        "Professor": professor,
        "Pràctica": practica
    }
    resultat: int = Alumne.objects(nom_i_cognoms=alumne).update(__raw__=
        {"$set": {
            "assignacio": assignacio
            }
        }
    )

    professor: Professor = Professor.objects(nom=professor).get()
    professor.assignacions.append(assignacio)
    professor.save()

    empresa: Empresa = Empresa.objects(nom=empresa).get()
    empresa.assignacions.append(assignacio)
    empresa.save()
    
    if resultat > 0:
        resposta: Response = jsonify(success=True, message="S'ha actualitzat l'assignació.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('assignacions_bp.mostrar_panel_de_assignacio'))
    else:
        resposta: Response = jsonify(success=False, message="No hi ha hagut cap canvi en l'assignació.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('assignacions_bp.editar_assignacio'))

@assignacions_bp.route('/esborrar_assignacio/<string:alumne>/<string:professor>/<string:practica>', methods=['POST'])
def esborrar_assignacio(alumne: str, professor: str, practica:str) -> Response:
    """Crida a la funció per a esborrar un assignació.

    Args:
        alumne (str): Alumne al que se li vol esborrar l'assignació.
        nom_de_professor (str): Nom del professor al que se li vol esborrar l'assignació.
        cognoms_de_professor (str): Cognoms del professor al que se li vol esborrar l'assignació.
        empresa (str): Empresa a la que se li vol esborrar l'assignació.
        practica (str): Pràctica a la que s'assigna el reste de parts.

    Returns:
        Response: Informació sobre el resultat de l'operació.
    """
    parts_de_practica = practica.split("(") 
    assignacio = {"alumne": alumne, "professor": professor, "practica": practica}
    resultat: int = Alumne.objects(nom_i_cognoms=alumne).update(__raw__=
        {"$set": {
            "assignacio": ""
            }
        }
    )

    Professor.objects(
        nom=professor,
        cognoms=professor
    ).update(pull__assignacions__S=assignacio)

    Empresa.objects(
        nom=parts_de_practica[0]
    ).update(pull__assignacions__S=assignacio)

    if resultat == "S'ha esborrat l'assignació.":
        resposta: Response = jsonify(success=True, message="S'ha esborrat l'assignació.")
        flash(json.loads(resposta.get_data(as_text=True))["message"])
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('assignacions_bp.mostrar_panel_de_assignacio'))
    else:
        resposta: Response = jsonify(success=True, message="No s'ha esborrat l'assignació.")
        if app.config["DEBUG"]:
            return resposta
        else:
            return redirect(url_for('assignacions_bp.mostrar_panel_de_assignacio'))


@assignacions_bp.route('/realitzar_assignacio_automatica', methods=['POST'])
def assignar_automaticament() -> Response:
    """Crida a la funció que assigna automàticament d'alumnes i professors a pràctiques d'empresa.

    Returns:
        Response: Informació sobre el resultat de la petició.
    """
    distancies = session.get('distancies')
    tasca_de_assignacio = assignar.delay(distancies)
    flash("L'assignació automàtica s'està executant en segó plà."
    +"Quan acabi se t'avisarà a través d'una notificació com aquesta.")
    return jsonify({}), 202, {'Location': url_for('assignacions_bp.taskstatus',
                                                  task_id=tasca_de_assignacio.id)}

@assignacions_bp.route('/status/<task_id>')
def taskstatus(task_id):
    task = assignar.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        print("Fase 1")
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        if task.info.get('status', '') == 'Assignacions Realitzades':
            session['distancies'] = current_user.distancies
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
            
    else:
        # something went wrong in the background job
        print("Error")
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@celery.task(bind=True)
def assignar(self, distancies):
    contador_de_assignacions: int = 0

    self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 100,
                                'status': "Recopil·lant alumnes"})
    alumnes: list[Alumne]|None = Alumne.objects()
    self.update_state(state='PROGRESS',
                            meta={'current': 15, 'total': 100,
                                'status': "Recopil·lant professors"})
    professors: list[Professor]|None = Professor.objects()
    self.update_state(state='PROGRESS',
                          meta={'current': 30, 'total': 100,
                                'status': "Recopil·lant empreses"})
    empreses: list[Empresa]|None = Empresa.objects()
    
    self.update_state(state='PROGRESS',
                          meta={'current': 35, 'total': 100,
                                'status': "Calculant distàncies alumne-pràctica"})

    redis = r    
    #if not redis.exists("Distancies"):
    distancies: list[dict] = model_de_optimitzacio.calcular_distancia(self, redis, alumnes, empreses)
    ## if

    self.update_state(state='PROGRESS',
                          meta={'current': 70, 'total': 100,
                                'status': "Comprovant les distintes prosibil·litats"})
    variables: list = model_de_optimitzacio.definir_variables(alumnes, empreses, professors)
    restriccions: list = model_de_optimitzacio.definir_restriccions(alumnes, professors, variables[2], variables[3], variables[0], variables[1], variables[4], variables[5])

    self.update_state(state='PROGRESS',
                          meta={'current': 85, 'total': 100,
                                'status': "Buscant assignacions més óptimes"})
    funcio = model_de_optimitzacio.definir_funcio_objectiu(restriccions[0], alumnes, professors, restriccions[2], restriccions[3])

    tipo_resultado = funcio[0].Solve()


    self.update_state(state='PROGRESS',
                          meta={'current': 95, 'total': 100,
                                'status': "Guardant assignacions més óptimes"})
                                
    for alumne in alumnes:
        #if alumne.aporta_empresa == "No" and alumne.accedeix_a_fct == "Sí":
            sid = alumne.nom_i_cognoms
            for v in funcio[2][sid] :
                if v.SolutionValue() > 0:
                    print(v, v.SolutionValue(), funcio[1].GetCoefficient(v))
                    parts_de_assignacio = str(v).split("-")
                    parts_de_practica = parts_de_assignacio[1].split("(")  
                    assignacio = {"Alumne": parts_de_assignacio[0], "Pràctica": parts_de_assignacio[1]}
                    resultat: int = Alumne.objects(nom_de_usuari=alumne.nom_de_usuari).update(__raw__=
                        {"$set": {
                            "assignacio": assignacio
                            }
                        }
                    ,)

                    # empresa: Empresa = Empresa.objects(nom=parts_de_practica[0]).get()
                    # empresa.assignacions.append(assignacio)

                    if resultat > 0:
                        contador_de_assignacions+=1
    if contador_de_assignacions>0:
        return {'current': 100, 'total': 100, 'status': "Assignacions Realitzades"}
    else:
        return "Ha ocorregut un problema durant l'assignació automàtica."
        