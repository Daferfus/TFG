###################################################################
## Autor: David Fernández Fuster                                 ##
## Data: 09/09/2022                                              ## 
## Funció: Funcions amb les dades base per a executar tests.     ##
###################################################################
from flask import Flask
from flask_mongoengine import MongoEngine

import pytest

#############################################
## Ruta sobre la que s'executen els tests. ##
#############################################
import sys
sys.path.insert(0, "C:\\Users\\david\\Projectes\\Personales\\TFG\\projecte_assignacio")

from projecte_assignacio import init_app
from projecte_assignacio.usuaris.model_usuaris import Usuari
from projecte_assignacio.alumnes.model_alumnes import Alumne
from projecte_assignacio.professors.model_professors import Professor
from projecte_assignacio.empreses.model_empreses import Empresa
#############################################
#############################################

@pytest.fixture(scope='module')
def test_client():
    """Inicialitza el client Flask per al seu testeig.

    Yields:
        Flask Client: Client Flask inicialitzat.
    """
    flask_app: Flask = init_app('config.DevConfig')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
## ()


@pytest.fixture(scope='module')
def test_mongo() -> object:
    """Inicialitza el client Flask amb una base de dades no persistent per al seu testeig.

    Returns:
        object: Client Flask amb la base de dades inicialitzada.
    """
    db: object = MongoEngine()
    app: Flask = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')
    db.init_app(app)
    return db
## ()

        
@pytest.fixture(scope='module')
def nou_usuari() -> Usuari:
    """Instancia un objecte Usuari per a provar les seues funcionalitats. 

    Returns:
        Usuari: Objecte de tipus Usuari.
    """
    usuari: Usuari = Usuari(
        nom='Mikaeru Softo', 
        contrasenya='Machete1@', 
        rol='Alumne'
    )## Usuari()
    return usuari
## ()

@pytest.fixture(scope='module')
def nou_alumne() -> Alumne:
    """Instancia un objecte Alumne per a provar les seues funcionalitats. 

    Returns:
        Alumne: Objecte de tipus Alumne.
    """
    alumne: Alumne = Alumne(
        nom_i_cognoms="David Fernández Fuster", 
        grup="DAW", 
        poblacio="Gandía", 
        mobilitat="Sí", 
        tipo_de_practica="DUAL", 
        preferencies={"FrontEnd": 5, "BackEnd": 7, "BD": 4}, 
        observacions="Disponible", 
        aporta_empresa=True, 
        erasmus=False, 
        distancies={
            "Punt de Partida": "Gandía", 
            "Punt de Destí": "València", 
            "Distància": 8
        }, 
        assignacio={
            "Alumne": "David Fernández Fuster", 
            "Pràctica": "Locatec_(Pràctica 01)", 
            "Professor": "Juan Miguel Alberola Oltra"
        }
    )## Alumne()
    return alumne
## ()

@pytest.fixture(scope='module')
def nou_professor() -> Professor:
    """Instancia un objecte Professor per a provar les seues funcionalitats. 

    Returns:
        Professor: Objecte de tipus Professor.
    """
    professor: Professor = Professor(
        nom="Juan Miguel", 
        cognoms="Alberola Oltra", 
        titulacions={"DAW": "X", "ASIX": "X"}, 
        hores_alliberades=8, 
        hores_restants=5, 
        rati_fct="1 hora per alumne", 
        rati_dual="3 hores per alumne", 
        assignacions=[
            {
                "Alumne": "David Fernández Fuster", 
                "Pràctica": "Locatec_(Pràctica 01)", 
                "Professor": "Juan Miguel Alberola Oltra"
            }
        ]
    )## Professor()
    return professor
## ()

@pytest.fixture(scope='module')
def nova_empresa() -> Empresa:
    """Instancia un objecte Empresa per a provar les seues funcionalitats. 

    Returns:
        Alumne: Objecte de tipus Empresa.
    """
    empresa: Empresa = Empresa(
        nom="Locatec", 
        poblacio="València", 
        telefon=665517969, 
        correu="info@locatec.es", 
        persona_de_contacte="Salva", 
        practiques=[{"Nom": "Pràctica 01"}],
        assignacions=[
            {
                "Alumne": "David Fernández Fuster", 
                "Pràctica": "Locatec_(Pràctica 01)", 
                "Professor": "Juan Miguel Alberola Oltra"
            }
        ]
    )## Empresa()
    return empresa
## ()