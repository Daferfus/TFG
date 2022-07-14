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

# @pytest.fixture
# def inicialitzacio_de_flask_i_mongo():
#     random.seed()
#     mongo_server = MockupDB(auto_ismaster=True, verbose=True)
#     mongo_server.run()
#     app = init_app()
#     yield app
#     mongo_server.stop()

# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()


@pytest.fixture(scope='module')
def nou_usuari():
    usuari = Usuari('Mikaeru Softo', bcrypt.hashpw('Machete1@'.encode('utf-8'), bcrypt.gensalt()), 'Alumne')
    return usuari


@pytest.fixture(scope='module')
def test_client():
    flask_app = init_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

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