from urllib.request import Request
from backend.alumnes import controlador_alumnes
from backend.alumnes.model_alumnes import Alumne
from backend.empreses import controlador_empreses
from backend.professors.model_professors import Professor
from backend.empreses.model_empreses import Empresa
from backend.professors import controlador_professors
from ortools.linear_solver import pywraplp
from geopy import Nominatim
import requests
import json

###################################
########## Assignacions ###########
###################################
def insertar_assignacio_manual(
    nom_de_alumne_per_a_filtrar: str,
    nom_de_professor_per_a_filtrar: str,
    cognoms_de_professor_per_a_filtrar: str,
    nom_de_empresa_per_a_filtrar: str,
    assignacio: dict[str, str]
    ) -> str:
    """Assigna cadascuna de les parts a una pràctica.

    Args:
        nom_de_alumne_per_a_filtrar (str): Nom del alumne protagonista de l'assignació.
        nom_de_professor_per_a_filtrar (str): Nom del professor que tutoritza l'alumne.
        cognoms_de_professor_per_a_filtrar (str): Cognom del professor que tutoritza l'alumne.
        nom_de_empresa_per_a_filtrar (str): Nom de l'empresa a la que el alumne va a fer pràctiques.
        assignacio (dict[str, str]): Assignació resultant.

    Returns:
        str: Resultat de l'operació.
    """
    Alumne.objects(nom_i_cognoms=nom_de_alumne_per_a_filtrar).update(__raw__=
        {"$set": {
            "assignacio": assignacio
            }
        }
    )

    professor: Professor = Professor.objects(nom=nom_de_professor_per_a_filtrar, cognoms=cognoms_de_professor_per_a_filtrar).get()
    professor.assignacions.append(assignacio)

    empresa: Empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).get()
    empresa.assignacions.append(assignacio)

    assignacio_insertada: Alumne|None = Alumne.objects(assignacio=assignacio).first()

    if assignacio_insertada is not None:
        return "L'assignació s'ha insertat."
    else:
        return "No s'ha insertat cap assignacio."

def actualitzar_assignacio(
    nom_de_alumne_per_a_filtrar: str, 
    nom_de_empresa_per_a_filtrar: str,
    nom_de_practica_per_a_filtrar: str,
    nom_de_professor_per_a_filtrar: str,
    cognoms_de_professor_per_a_filtrar: str,
    assignacio: dict[str, str]
    ) -> str:
    """Actualitza una assignació donada.

    Args:
        nom_de_alumne_per_a_filtrar (str): Nom d'alumne a actualitzar.
        nom_de_empresa_per_a_filtrar (str): Nom d'empresa a actualitzar.
        nom_de_practica_per_a_filtrar (str): Nom de pràctica a actualitzar.
        nom_de_professor_per_a_filtrar (str): Nom del professor a actualitzar.
        cognoms_de_professor_per_a_filtrar (str): Cognoms del professor a actualitzar.
        assignacio (dict[str, str]): Nova assignació.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: int = Alumne.objects(nom_i_cognoms=nom_de_alumne_per_a_filtrar).update(__raw__=
        {"$set": {
            "assignacio": assignacio
            }
        }
    )

    Professor.objects(
        nom=nom_de_professor_per_a_filtrar,
        cognoms=cognoms_de_professor_per_a_filtrar,
        assignacions={"Alumne": nom_de_alumne_per_a_filtrar, "Practica": nom_de_empresa_per_a_filtrar+"("+nom_de_practica_per_a_filtrar+")", "Professor": nom_de_professor_per_a_filtrar}
    ).update(set__assignacions__S=assignacio)

    Empresa.objects(
        nom=nom_de_empresa_per_a_filtrar,
        assignacions={"Alumne": nom_de_alumne_per_a_filtrar, "Practica": nom_de_empresa_per_a_filtrar+"("+nom_de_practica_per_a_filtrar+")", "Professor": nom_de_professor_per_a_filtrar}
    ).update(set__assignacions__S=assignacio)

    if resultat > 0:
        return "S'ha actualitzat l'assignació."
    else:
        return "No hi ha hagut cap canvi en l'assignació."

def esborrar_assignacio(
    nom_de_professor_per_a_filtrar: str,
    cognoms_de_professor_per_a_filtrar: str,
    nom_de_empresa_per_a_filtrar: str,
    assignacio: dict
    ) -> str:
    """Esborra una assignacio donada.

    Args:
        nom_de_professor_per_a_filtrar (str): Nom del professor del que se li esborra d'una assignacio.
        cognoms_de_professor_per_a_filtrar (str): Cognoms del professor del que se li esborra d'una assignacio.
        nom_de_empresa_per_a_filtrar (str): Nom de l'empresa propietaria de la pràctica.
        assignacio (dict): Assignacio a esborrar.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: int = Alumne.objects(nom_i_cognoms=assignacio["Alumne"]).update(__raw__=
        {"$set": {
            "assignacio": ""
            }
        }
    )

    Professor.objects(
        nom=nom_de_professor_per_a_filtrar,
        cognoms=cognoms_de_professor_per_a_filtrar
    ).update(pull__assignacions__S=assignacio)

    Empresa.objects(
        nom=nom_de_empresa_per_a_filtrar
    ).update(pull__assignacions__S=assignacio)

    if resultat > 0:
        return "S'ha esborrat l'assignació."
    else:
        return "No s'ha esborrat l'assignació."

def realitzar_assignacio_automatica():
    contador_de_assignacions: int = 0

    alumnes = controlador_alumnes.recuperar_dades_de_alumnes()
    professors = controlador_professors.recuperar_dades_de_professors()
    empreses = controlador_empreses.recuperar_dades_de_empreses()

    
    distancies: list[dict] = calcular_distancia(alumnes, empreses)
    variables: list = definir_variables(alumnes, empreses, professors)
    restriccions: list = definir_restriccions(alumnes, professors, variables[2], variables[3], variables[0], variables[1], variables[4], variables[5])
    funcio = definir_funcio_objectiu(restriccions[0], restriccions[1], alumnes, empreses, distancies, restriccions[2])

    tipo_resultado = funcio[0].Solve()

    for alumne in alumnes:
        sid = alumne["Nom"]
        for v in funcio[2][sid] :
            if v.SolutionValue() > 0:
                # print(v, v.SolutionValue(), funcio[3].GetCoefficient(v))
                parts_de_assignacio = v.split("-")
                parts_de_practica = parts_de_assignacio[1].split("(")  
                assignacio = {"Alumne": parts_de_assignacio[0], "Pràctica": parts_de_assignacio[1], "Professor": ""}
                resultat: int = Alumne.objects(nom_i_cognoms=parts_de_assignacio[0]).update(__raw__=[
                    {"$set": {
                        "assignacio": assignacio
                        }
                    }
                ],)

                empresa: Empresa = Empresa.objects(nom=parts_de_practica[0]).get()
                empresa.assignacions.append(assignacio)

                if resultat > 0:
                    contador_de_assignacions+=1
    if contador_de_assignacions>0:
        return "L'assignació automàtica a ocorregut sense cap problema."
    else:
        return "Ha ocorregut un problema durant l'assignació automàtica."

def calcular_distancia(alumnes: list[Alumne], empreses: list[Empresa]):
    nm = Nominatim(user_agent="assignacio-automatica")
    distancies: dict[dict] = {}

    for alumne in alumnes:
        ciutat_alumne: str = alumne.poblacio
        coordenades_ciutat_alumne = Nominatim.geocode(nm, ciutat_alumne+", València")

        for empresa in empreses:
            ciutat_empresa: str = empresa.poblacio
            coordenades_ciutat_empresa = Nominatim.geocode(nm, ciutat_empresa+", València")
            if (coordenades_ciutat_alumne and coordenades_ciutat_empresa) is not None:
                r: Request = requests.get(f"http://router.project-osrm.org/route/v1/car/{coordenades_ciutat_alumne.longitude},{coordenades_ciutat_alumne.latitude};{coordenades_ciutat_empresa.longitude},{coordenades_ciutat_empresa.latitude}?overview=false""")
                route = json.loads(r.content)["routes"][0]
                distancia = {"Punt de Partida": ciutat_alumne, "Punt de Destí": ciutat_empresa, "Distancia": float(route["distance"]/1000)}
                distancies.update(distancia)
        
        Alumne.objects(nom_i_cognoms=alumne.nom_i_cognoms).update(__raw__=
            {"$set": {
                "distancies": distancies
                }
            }
        )

    return distancies

def definir_variables(alumnes: list[Alumne], empreses: list[Empresa], professors: list[Professor]):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    solver.SetTimeLimit(10000)

    practiques: list = [];

    variable_alumnes: dict = {}
    variable_professors: dict = {}
    variable_practiques_alumne: dict = {}
    variable_practiques_professor: dict = {}
    variable_empreses: dict = {}


    ## Definim Variables
    ## Alumnes (Y_ki)
    for alumne in alumnes:
        contador: int = 0;
        for empresa in empreses:
            nombre_de_practiques: int = len(empresa.practiques)
            while nombre_de_practiques > 0:
                contador+=1;
                variable_buleana = solver.BoolVar(alumne.nom_i_cognoms+"-"+empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")")
                practiques.append(empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")")
                llistat_practiques: list = variable_alumnes.setdefault(alumne.nom_i_cognoms, list())
                llistat_practiques.append(variable_buleana)
                variable_alumnes[alumne.nom_i_cognoms]: dict[list] = llistat_practiques
                llistat_practiques = variable_practiques_alumne.setdefault(empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")", list())
                llistat_practiques.append(variable_buleana)
                variable_practiques_alumne[len(empresa.practiques)] = llistat_practiques
                nombre_de_practiques-=1

    ## Professors (X_ji)
    for professor in professors:
        for empresa in empreses:
            nombre_de_practiques: int = len(empresa.practiques)
            while nombre_de_practiques > 0:
                variable_buleana = solver.BoolVar(professor.nom+"-"+empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")")
                llistat_practiques: list = variable_professors.setdefault(professor.nom, list())
                llistat_practiques.append(variable_buleana)
                variable_professors[professor.nom]: list = llistat_practiques
                llistat_practiques: list = variable_practiques_professor.setdefault(empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")", list())
                llistat_practiques.append(variable_buleana)
                variable_practiques_professor[len(empresa.practiques)]: list = llistat_practiques
                nombre_de_practiques-=1

    return [variable_alumnes, variable_professors, practiques, solver, variable_practiques_alumne, variable_practiques_professor]

def definir_restriccions(alumnes: list[Alumne], professors: list[Professor], practiques, solver, variable_alumnes, variable_professors, variable_practiques_alumne, variable_practiques_professor):
    # Restricció de capacitat del alumne.
    for alumne in alumnes:
        sid = alumne.nom_i_cognoms
        c = solver.Constraint(1, 1)
        for v in variable_alumnes[sid] :
            c.SetCoefficient(v, 1)

    # Restricció de capacitat del professor.
    for professor in professors:
        variables = professor.nom
        c = solver.Constraint(0, professor.hores_alliberades)
        for v in variable_professors[variables]:
            c.SetCoefficient(v, 1)

    # Restricció de alumnes i professors per pràctica.
    for practica in practiques:
        pracal = practica
        prapro = practica
        practica_alumne = solver.Constraint(0, 1)
        practica_professor = solver.Constraint(0, 1)

        for v_alumne in variable_practiques_alumne[pracal]:
            practica_alumne.SetCoefficient(v_alumne, 1)
        for v_professor in variable_practiques_professor[prapro]:
            practica_professor.SetCoefficient(v_professor, 1)
    
    return [solver, variable_practiques_alumne, variable_alumnes]

def definir_funcio_objectiu(solver, variable_practiques_alumne, alumnes: list[Alumne], empreses: list[Empresa], distancies, variable_alumnes):
    objective = solver.Objective()
    objective.SetMinimization()
    quantitat = len(variable_practiques_alumne)

    for alumne in alumnes:

        sid = alumne.nom_i_cognoms
        punt_partida = alumne.poblacio
        distancia_alumne_practica = []
        for empresa in empreses:
            nom_empresa = empresa.nom
            punt_desti = empresa.poblacio
            nombre_de_practiques = len(empresa.practiques)

            # Recopilem les distàncies.
            for ciutats, distancia in distancies.items():
                if punt_partida in ciutats and punt_desti in ciutats:
                    while nombre_de_practiques > 0:
                        distancia_alumne_practica.append(float(distancia));
                        nombre_de_practiques = nombre_de_practiques - 1
                    # while
                # if
            # for
        # for


        #  Minimització de Distàncies.
        contador = 0
        for v in variable_alumnes[sid]:
            objective.SetCoefficient(v, distancia_alumne_practica[contador])
            contador+=1
            # if
        # for
    # for
    return [solver, objective, variable_alumnes]