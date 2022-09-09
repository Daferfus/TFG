from urllib.request import Request
from projecte_assignacio.alumnes import rutes_alumnes
from projecte_assignacio.alumnes.model_alumnes import Alumne
from projecte_assignacio.empreses import rutes_empreses
from projecte_assignacio.professors.model_professors import Professor
from projecte_assignacio.empreses.model_empreses import Empresa
from projecte_assignacio.professors import rutes_professors
from ortools.linear_solver import pywraplp
from geopy import Nominatim
import requests
import json

###################################
########## Assignacions ###########
###################################
def calcular_distancia(alumnes: list[Alumne], empreses: list[Empresa]):
    nm = Nominatim(user_agent="assignacio-automatica")
    distancies: list = []

    print("Calculem distàncies.")
    for alumne in alumnes:
        distancies_alumne: list = []
        ciutat_alumne: str = alumne.poblacio
        coordenades_ciutat_alumne = Nominatim.geocode(nm, ciutat_alumne+", València")

        for empresa in empreses:
            ciutat_empresa: str = empresa.poblacio
            coordenades_ciutat_empresa = Nominatim.geocode(nm, ciutat_empresa+", València")
            if (coordenades_ciutat_alumne and coordenades_ciutat_empresa) is not None:
                r: Request = requests.get(f"http://router.project-osrm.org/route/v1/car/{coordenades_ciutat_alumne.longitude},{coordenades_ciutat_alumne.latitude};{coordenades_ciutat_empresa.longitude},{coordenades_ciutat_empresa.latitude}?overview=false""")
                route = json.loads(r.content)["routes"][0]
                distancia = {"Punt de Partida": ciutat_alumne, "Punt de Destí": ciutat_empresa, "Distancia": float(route["distance"]/1000)}
                distancies_alumne.append(distancia)
        
        Alumne.objects(nom_i_cognoms=alumne.nom_i_cognoms).update(__raw__=
            {"$set": {
                "distancies": distancies_alumne
                }
            }
        )
        distancies.append(distancies_alumne)
    return distancies

def definir_variables(alumnes: list[Alumne], empreses: list[Empresa], professors: list[Professor]):
    print("Definim Variables.")
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
    print("Definim Restriccions.")
    # Restricció de capacitat del alumne.
    for alumne in alumnes:
        sid = alumne.nom_i_cognoms
        c = solver.Constraint(1, 1)
        for v in variable_alumnes[sid] :
            c.SetCoefficient(v, 1)

    # Restricció de capacitat del professor.
    for professor in professors:
        variables = professor.nom
        c = solver.Constraint(0, float(professor.hores_alliberades))
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
    
    print("Acabem de definir restriccions.")
    return [solver, variable_practiques_alumne, variable_alumnes]

def definir_funcio_objectiu(solver, variable_practiques_alumne, alumnes: list[Alumne], empreses: list[Empresa], distancies, variable_alumnes):
    print("Definim Funció Objectiu.")
    objective = solver.Objective()
    objective.SetMinimization()

    nombre_de_alumne: int = 0
    for alumne in alumnes:
        nombre_de_practica: int = 0
        sid = alumne.nom_i_cognoms
        print(distancies[0][nombre_de_alumne])
        for key, val in distancies[0][nombre_de_alumne].items():
            print(key)
            if key=="Distancia":
                print(float(val))
                #print(variable_alumnes[sid])
                objective.SetCoefficient(variable_alumnes[sid][nombre_de_practica], float(val))
                nombre_de_practica+=1
            # if        # for
        nombre_de_alumne+=1
    # for
    return [solver, objective, variable_alumnes]