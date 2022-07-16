import json

def test_borrar_alumnes_amb_fixture(test_client):
    assert test_client.get('/borrar_alumnes').status_code == 405
    assert test_client.delete('/borrar_alumnes').status_code == 200
    response = test_client.delete('/borrar_alumnes')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_insertar_alumne_amb_fixture(test_client):
    datos = {
        "nom_i_cognom_del_alumne": "David Fernández Fuster",
        "grup_del_alumne": "DAW",
        "poblacio_del_alumne": "Gandía",
        "mobilitat_del_alumne": "Sí",
        "tipo_de_practica_del_alumne": "DUAL",
        "preferencies_del_alumne": '{"FrontEnd": 5, "BackEnd": 7, "BD": 4}',
        "observacions_del_alumne": "Disponible",
        "aporta_empresa_el_alumne": "True",
        "erasmus_del_alumne": "False"
    }
    assert test_client.get('/insertar_alumne', data=datos).status_code == 405
    assert test_client.post('/insertar_alumne', data=datos).status_code == 200
    response = test_client.post('/insertar_alumne', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True


def test_recuperar_dades_de_alumnes_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_alumnes').status_code == 405
    assert test_client.get('/recuperar_dades_de_alumnes').status_code == 200
    response = test_client.get('/recuperar_dades_de_alumnes')
    alumne = json.loads(response.get_data(as_text=True))["message"]
    assert alumne[0]["nom_i_cognoms"] == "David Fernández Fuster"

def test_actualitzar_alumne_amb_fixture(test_client):
    datos = {
        "nom_i_cognom_del_alumne": "David Fernández Fuster",
        "grup_del_alumne": "ASIX",
        "poblacio_del_alumne": "Gandía",
        "mobilitat_del_alumne": "Sí",
        "tipo_de_practica_del_alumne": "DUAL",
        "preferencies_del_alumne": '{"FrontEnd": 5, "BackEnd": 7, "BD": 4}',
        "observacions_del_alumne": "Disponible",
        "aporta_empresa_el_alumne": "True",
        "erasmus_del_alumne": "False"
    }
    assert test_client.post('/actualitzar_alumne/David Fernández Fuster', data=datos).status_code == 405
    assert test_client.put('/actualitzar_alumne/David Fernández Fuster', data=datos).status_code == 200
    response = test_client.put('/actualitzar_alumne/David Fernández Fuster', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_borrar_alumne_amb_fixture(test_client):
    assert test_client.get('/borrar_alumne/David Fernández Fuster').status_code == 405
    assert test_client.delete('/borrar_alumne/David Fernández Fuster').status_code == 200
    response = test_client.delete('/borrar_alumne/David Fernández Fuster')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_recuperar_dades_del_alumne_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_del_alumne/David Fernández Fuster').status_code == 405
    assert test_client.get('/recuperar_dades_del_alumne/David Fernández Fuster').status_code == 200
    response = test_client.get('/recuperar_dades_del_alumne/David Fernández Fuster')
    alumne = json.loads(response.get_data(as_text=True))["message"]
    assert alumne == []

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