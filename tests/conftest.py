from curses.ascii import EM
from shelve import DbfilenameShelf
import sys
sys.path.insert(0, "C:\\Users\\david\\Documents\\Proyectos\\Personales\\TFG\\projecte_assignacio")
from projecte_assignacio import init_app

import pytest
import random
import uuid
import bcrypt
from flask import Flask

 
from flask_mongoengine import MongoEngine
# from mockupdb import MockupDB, go, Command
# from bson.objectid import ObjectId
from json import dumps

from projecte_assignacio.usuaris.model_usuaris import Usuari
from projecte_assignacio.alumnes.model_alumnes import Alumne
from projecte_assignacio.professors.model_professors import Professor
from projecte_assignacio.empreses.model_empreses import Empresa

@pytest.fixture(scope='module')
def test_client():
    flask_app = init_app('config.DevConfig')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def test_mongo():
    db = MongoEngine()
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')
    db.init_app(app)
    return db

@pytest.fixture(scope='module')
def nou_usuari():
    usuari = Usuari(
        nom='Mikaeru Softo', 
        contrasenya=bcrypt.hashpw('Machete1@'.encode('utf-8'), bcrypt.gensalt()), 
        rol='Alumne'
        )
    return usuari

@pytest.fixture(scope='module')
def nou_alumne():
    alumne = Alumne(
        nom_i_cognoms="David Fernández Fuster", 
        grup="DAW", 
        poblacio="Gandía", 
        mobilitat="Sí", 
        tipo_de_practica="DUAL", 
        preferencies={"FrontEnd": 5, "BackEnd": 7, "BD": 4}, 
        observacions="Disponible", 
        aporta_empresa=True, 
        erasmus=False, 
        distancies={"Punt de Partida": "Gandía", "Punt de Destí": "València", "Distància": 8}, 
        assignacio={"Alumne": "David Fernández Fuster", "Pràctica": "Locatec_(Pràctica 01)", "Professor": "Juan Miguel Alberola Oltra"}
        )
    return alumne

@pytest.fixture(scope='module')
def nou_professor():
    professor = Professor(
        nom="Juan Miguel", 
        cognoms="Alberola Oltra", 
        titulacions={"DAW": "X", "ASIX": "X"}, 
        hores_alliberades=8, 
        hores_restants=5, 
        rati_fct="1 hora per alumne", 
        rati_dual="3 hores per alumne", 
        assignacions=[{"Alumne": "David Fernández Fuster", "Pràctica": "Locatec_(Pràctica 01)", "Professor": "Juan Miguel Alberola Oltra"}]
    )
    return professor


@pytest.fixture(scope='module')
def nova_empresa():
    empresa = Empresa(
        nom="Locatec", 
        poblacio="València", 
        telefon=665517969, 
        correu="info@locatec.es", 
        persona_de_contacte="Salva", 
        practiques=[{"Nom": "Pràctica 01"}],
        assignacions=[{"Alumne": "David Fernández Fuster", "Pràctica": "Locatec_(Pràctica 01)", "Professor": "Juan Miguel Alberola Oltra"}]
    )
    return empresa