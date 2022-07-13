from backend.model.alumnes import Alumne
from backend.model.professors import Professor
from backend.model.empreses import Empresa
from backend.controller import controlador_alumnes, controlador_empreses, controlador_professors
from geopy import distance
from geopy import Nominatim
import requests
import json

###################################
########## Assignacions ###########
###################################
def insertar_assignacio_manual(
    nom_de_alumne_per_a_filtrar,
    nom_de_professor_per_a_filtrar,
    cognoms_de_professor_per_a_filtrar,
    nom_de_empresa_per_a_filtrar,
    assignacio
    ):
    Alumne.objects(nom=nom_de_alumne_per_a_filtrar).update(__raw__=[
        {"$set": {
            "assignacio": assignacio
            }
        }
    ],)

    professor = Professor.objects(nom=nom_de_professor_per_a_filtrar, cognoms=cognoms_de_professor_per_a_filtrar).get()
    professor.assignacions.append(assignacio)

    empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).get()
    empresa.assignacions.append(assignacio)


def assignacio_automatica():
    alumnes = controlador_alumnes.recuperar_dades_de_alumnes()
    professors = controlador_professors.recuperar_dades_de_professors()
    empreses = controlador_empreses.recuperar_dades_de_empreses()

    definir_variables()

def actualitzar_assignacio(
    nom_de_alumne_per_a_filtrar, 
    nom_de_empresa_per_a_filtrar,
    nom_de_practica_per_a_filtrar,
    nom_de_professor_per_a_filtrar,
    cognoms_de_professor_per_a_filtrar,
    assignacio
    ):
    Alumne.objects(nom=nom_de_alumne_per_a_filtrar).update(__raw__=[
        {"$set": {
            "assignacio": assignacio
            }
        }
    ],)

    Professor.objects(
        nom=nom_de_professor_per_a_filtrar,
        cognoms=cognoms_de_professor_per_a_filtrar,
        assignacions=
        nom_de_alumne_per_a_filtrar+"-"+
        nom_de_practica_per_a_filtrar+"-"+
        nom_de_professor_per_a_filtrar
    ).update(set__assignacions__S=assignacio)

    Empresa.objects(
        nom=nom_de_empresa_per_a_filtrar,
        assignacions=
        nom_de_alumne_per_a_filtrar+"-"+
        nom_de_practica_per_a_filtrar+"-"+
        nom_de_professor_per_a_filtrar
    ).update(set__assignacions__S=assignacio)


def borrar_assignacio(
    nom_de_professor_per_a_filtrar,
    cognoms_de_professor_per_a_filtrar,
    nom_de_empresa_per_a_filtrar,
    assignacio
    ):
    Alumne.objects(nom=assignacio["Alumne"]).update(__raw__=[
        {"$set": {
            "assignacio": ""
            }
        }
    ],)

    Professor.objects(
        nom=nom_de_professor_per_a_filtrar,
        cognoms=cognoms_de_professor_per_a_filtrar
    ).update(pull__assignacions__S=assignacio)

    Empresa.objects(
        nom=nom_de_empresa_per_a_filtrar
    ).update(pull__assignacions__S=assignacio)


def calcular_distancia(alumne):
    nm = Nominatim(user_agent="my-application")
    distancies = []

    ciutat_alumne = alumne["Poblacio"]
    coordenades_ciutat_alumne = Nominatim.geocode(nm, ciutat_alumne+", València")

    empreses = controlador_empreses.recuperar_dades_de_empreses()

    for empresa in empreses:
        ciutat_empresa = empresa["Poblacio"]
        coordenades_ciutat_empresa = Nominatim.geocode(nm, ciutat_empresa+", València")
        r = requests.get(f"http://router.project-osrm.org/route/v1/car/{coordenades_ciutat_alumne.longitude},{coordenades_ciutat_alumne.latitude};{coordenades_ciutat_empresa.longitude},{coordenades_ciutat_empresa.latitude}?overview=false""")
        route = json.loads(r.content)["routes"][0]
        distancia = {"Punt de Partida": ciutat_alumne, "Punt de Destí": ciutat_empresa, "Distancia": float(route["distance"]/1000)}
        distancies.append(distancia)
    
    Alumne.objects(nom=alumne["Nom"]).update(__raw__=[
        {"$set": {
            "distancies": distancies
            }
        }
    ],)