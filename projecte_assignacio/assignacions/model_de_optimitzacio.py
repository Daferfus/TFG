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
from flask import session, g

###################################
########## Assignacions ###########
###################################
def calcular_distancia(self, redis, alumnes: list[Alumne], empreses: list[Empresa]):
    nm = Nominatim(user_agent="assignacio-automatica")
    distancies: dict = {}

    progres = 35
    print("Calculem distàncies.")
    for alumne in alumnes:
        #if alumne.aporta_empresa == "No" and alumne.accedeix_a_fct == "Sí":
            progres+=1
            distancies_alumne: list = []
            ciutat_alumne: str = alumne.poblacio
            coordenades_ciutat_alumne = Nominatim.geocode(nm, ciutat_alumne+", València")
            self.update_state(state='PROGRESS',
                                meta={'current': progres, 'total': 100,
                                        'status': "Calculant distàncies alumne-pràctica"})
            for empresa in empreses:
                # perfil: bool = False;
                # for practica in empresa.practiques:
                #     if practica["Titulacio"] == alumne.grup:
                #         perfil = True
                # if perfil:
                    ciutat_empresa: str = empresa.poblacio
                    coordenades_ciutat_empresa = Nominatim.geocode(nm, ciutat_empresa+", València")
                    if (coordenades_ciutat_alumne and coordenades_ciutat_empresa) is not None:
                        transport = "";
                        if alumne.mobilitat == "Sí":
                            transport = "car"
                        else:
                            transport = "foot"
                        r: Request = requests.get(f"http://router.project-osrm.org/route/v1/{transport}/{coordenades_ciutat_alumne.longitude},{coordenades_ciutat_alumne.latitude};{coordenades_ciutat_empresa.longitude},{coordenades_ciutat_empresa.latitude}?overview=false""")
                        route = json.loads(r.content)["routes"][0]
                        distancia = {"Punt de Partida": ciutat_alumne, "Punt de Destí": ciutat_empresa, "Nombre de Pràctiques": len(empresa.practiques), "Distancia": float(route["distance"]/1000)}
                        distancies_alumne.append(distancia)

                        redis.hset("Distancies", str((ciutat_alumne+"-"+ciutat_empresa)), float(route["distance"]/1000))
                        distancies = redis.hgetall("Distancies")
                # else:
                #     print(alumne.nom_i_cognoms)
            Alumne.objects(nom_i_cognoms=alumne.nom_i_cognoms).update(__raw__=
                {"$set": {
                    "distancies": distancies_alumne
                    }
                }
            )
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
        #if alumne.aporta_empresa == "No" and alumne.accedeix_a_fct == "Sí":
            for empresa in empreses:
                nombre_de_practiques: int = len(empresa.practiques)
                contador: int = 0;
                while nombre_de_practiques > 0:
                    #if empresa.practiques[contador]["Titulacio"] == alumne.grup:
                        variable_buleana = solver.BoolVar(alumne.nom_i_cognoms+"-"+empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")")
                        practiques.append(empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")")
                        llistat_practiques: list = variable_alumnes.setdefault(alumne.nom_i_cognoms, list())
                        llistat_practiques.append(variable_buleana)
                        variable_alumnes[alumne.nom_i_cognoms]: dict[list] = llistat_practiques
                        llistat_practiques = variable_practiques_alumne.setdefault(empresa.nom+"(Pràctica "+str(nombre_de_practiques)+")", list())
                        llistat_practiques.append(variable_buleana)
                        variable_practiques_alumne[len(empresa.practiques)] = llistat_practiques
                    #else:
                        #print(empresa.practiques[contador]["Titulacio"])
                        #print(alumne.grup)
                        contador+=1;
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
        #if alumne.aporta_empresa == "No" and alumne.accedeix_a_fct == "Sí":
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
    return [solver, variable_practiques_alumne, variable_alumnes, variable_professors]

def definir_funcio_objectiu(solver, alumnes: list[Alumne], professors: list[Professor], variable_alumnes, variable_professors):
    print("Definim Funció Objectiu.")
    objective = solver.Objective()
    objective.SetMinimization()

    for alumne in alumnes:
        #if alumne.aporta_empresa == "No" and alumne.accedeix_a_fct == "Sí":
            sid = alumne.nom_i_cognoms
            contador_practica = 0
            for distancia in alumne.distancies:
                nombre_de_practiques = distancia["Nombre de Pràctiques"]
                while(nombre_de_practiques > 0):
                    objective.SetCoefficient(variable_alumnes[sid][contador_practica], float(distancia["Distancia"]))
                    nombre_de_practiques-=1  
                    contador_practica+=1
                # while         
            # for
        # if
    # for
    # for professor in professors:
    #     sid = professor.nom
    #     contador_practica = 0
    #     for v in variable_professors[sid]:
    #         objective.SetCoefficient(v, 34)
    return [solver, objective, variable_alumnes, variable_professors]