from curses.ascii import EM
import sys
sys.path.insert(0, "C:\\Users\\david\\Documents\\Proyectos\\Personales\\TFG\\problema_assignacio")
from backend import init_app

import pytest
import random
import uuid
import bcrypt

 
from flask_mongoengine import MongoEngine
from mockupdb import MockupDB, go, Command
from bson.objectid import ObjectId
from json import dumps

from backend.models.usuaris import Usuari
from backend.models.alumnes import Alumne
from backend.models.professors import Professor
from backend.models.empreses import Empresa

@pytest.fixture(scope='module')
def test_client():
    flask_app = init_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def test_mongo():
    random.seed()     
    mongo_server = MockupDB(auto_ismaster=True, verbose=True)
    mongo_server.run()
    yield mongo_server
    mongo_server.stop()


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
        nom_i_cognom="David Fernández Fuster", 
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


# def test_insert(inicialitzacio_de_flask_i_mongo):
#     client, servidor = inicialitzacio_de_flask_i_mongo
#     capçalera = [('Content-Type', 'application/json')]

#     id = str(uuid.uuid4()).encode('utf-8')[:12]
#     obj_id = ObjectId(id)
#     a_insertar = {
#         "_id": obj_id,
#         "nom_de_usuari": "Mikaeru Softo",
#         "contrasenya_de_usuari": "Whoa",
#         "rol_de_usuari": "Alumne"

#     }
#     a_verificar = {
#         "_id": obj_id,
#         "nom_de_usuari": "Mikaeru Softo",
#         "contrasenya_de_usuari": "Whoa",
#         "rol_de_usuari": "Alumne"
#     }

#     future = go(client.post, '/insertar_usuari', data=dumps(a_insertar), headers=capçalera)
#     peticio = servidor.receives(
#         Command({
#             'insert': 'test',
#             'ordered': True,
#             '$db': "test",
#             '$readPreference': {"mode": "primary"},
#             'documents': [
#                 a_verificar
#             ]
#         }, namespace='test')
#     )
#     peticio.ok(cursor={'inserted_id': id})
    
#     # act
#     resposta_http = future()

#     # assert
#     data = resposta_http.get_data(as_text=True)
#     print(data)