import json

def test_borrar_professors_amb_fixture(test_client):
    assert test_client.get('/borrar_professors').status_code == 405
    assert test_client.delete('/borrar_professors').status_code == 200
    response = test_client.delete('/borrar_professors')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_insertar_professor_amb_fixture(test_client):
    datos = {
        "nom_del_professor": "Juan Miguel", 
        "cognoms_del_professor": "Alberola Oltra", 
        "titulacions_del_professor": '{"DAW": "X", "ASIX": "X"}', 
        "hores_alliberades_del_professor": 8, 
        "hores_restants_del_professor": 5
    }
    assert test_client.get('/insertar_professor', data=datos).status_code == 405
    assert test_client.post('/insertar_professor', data=datos).status_code == 200
    response = test_client.post('/insertar_professor', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True


def test_recuperar_dades_de_professors_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_professors').status_code == 405
    assert test_client.get('/recuperar_dades_de_professors').status_code == 200
    response = test_client.get('/recuperar_dades_de_professors')
    professor = json.loads(response.get_data(as_text=True))["message"]
    assert professor[0]["nom"] == "Juan Miguel"

def test_actualitzar_professor_amb_fixture(test_client):
    datos = {
        "nom_del_professor": "Juan Miguel", 
        "cognoms_del_professor": "Alberola Oltra", 
        "titulacions_del_professor": '{"DAW": "X", "ASIX": "X"}', 
        "hores_alliberades_del_professor": 8, 
        "hores_restants_del_professor": 8
    }
    assert test_client.post('/actualitzar_professor/Juan Miguel/Alberola Oltra', data=datos).status_code == 405
    assert test_client.put('/actualitzar_professor/Juan Miguel/Alberola Oltra', data=datos).status_code == 200
    response = test_client.put('/actualitzar_professor/Juan Miguel/Alberola Oltra', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_borrar_professor_amb_fixture(test_client):
    assert test_client.get('/borrar_professor/Juan Miguel/Alberola Oltra').status_code == 405
    assert test_client.delete('/borrar_professor/Juan Miguel/Alberola Oltra').status_code == 200
    response = test_client.delete('/borrar_professor/Juan Miguel/Alberola Oltra')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_recuperar_dades_del_professor_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_del_professor/Juan Miguel/Alberola Oltra').status_code == 405
    assert test_client.get('/recuperar_dades_del_professor/Juan Miguel/Alberola Oltra').status_code == 200
    response = test_client.get('/recuperar_dades_del_professor/Juan Miguel/Alberola Oltra')
    professor = json.loads(response.get_data(as_text=True))["message"]
    assert professor == []

# def test_importar_alumnes_amb_fixture(test_client):
#     assert test_client.get('/importar_alumnes').status_code == 405
#     assert test_client.post('/importar_alumnes').status_code == 200
#     response = test_client.post('/importar_alumnes')
#     usuari = json.loads(response.get_data(as_text=True))["message"]
#     assert usuari == []

# @alumnes_bp.route('/importar_alumnes', methods=['POST'])
# def recollir_fitxer_alumnes():
#     cicle = request.form['cicle']
#     f = request.files['fichero']
#     nom_de_fitxer = './'+cicle+'.csv';
#     f.save(nom_de_fitxer)
    
#     controlador_alumnes.importar_alumnes(nom_de_fitxer, cicle)
#     resp = jsonify(success=True, message="S'han importat amb èxit els alumnes de "+cicle+".")
#     return resp