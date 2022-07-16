import json

def test_borrar_empreses_amb_fixture(test_client):
    assert test_client.get('/borrar_empreses').status_code == 405
    assert test_client.delete('/borrar_empreses').status_code == 200
    response = test_client.delete('/borrar_empreses')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_insertar_empresa_amb_fixture(test_client):
    datos = {
        "nom_de_empresa": "Locatec", 
        "poblacio_de_empresa": "València", 
        "telefon_de_empresa": 665517969, 
        "correu_de_empresa": "info@locatec.es", 
        "persona_de_contacte_en_la_empresa": "Salva"
    }
    assert test_client.get('/insertar_empresa', data=datos).status_code == 405
    assert test_client.post('/insertar_empresa', data=datos).status_code == 200
    response = test_client.post('/insertar_empresa', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True


def test_recuperar_dades_de_empreses_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_empreses').status_code == 405
    assert test_client.get('/recuperar_dades_de_empreses').status_code == 200
    response = test_client.get('/recuperar_dades_de_empreses')
    empresa = json.loads(response.get_data(as_text=True))["message"]
    assert empresa[0]["nom"] == "Locatec"

def test_actualitzar_empresa_amb_fixture(test_client):
    datos = {
        "nom_de_empresa": "Locatec", 
        "poblacio_de_empresa": "València", 
        "telefon_de_empresa": 665517969, 
        "correu_de_empresa": "info@locatec.es", 
        "persona_de_contacte_en_la_empresa": "Salva"
    }
    assert test_client.post('/actualitzar_empresa/Locatec', data=datos).status_code == 405
    assert test_client.put('/actualitzar_empresa/Locatec', data=datos).status_code == 200
    response = test_client.put('/actualitzar_empresa/Locatec', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_borrar_empresa_amb_fixture(test_client):
    assert test_client.get('/borrar_empresa/Locatec').status_code == 405
    assert test_client.delete('/borrar_empresa/Locatec').status_code == 200
    response = test_client.delete('/borrar_empresa/Locatec')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_recuperar_dades_de_la_empresa_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_la_empresa/Locatec').status_code == 405
    assert test_client.get('/recuperar_dades_de_la_empresa/Locatec').status_code == 200
    response = test_client.get('/recuperar_dades_de_la_empresa/Locatec')
    empresa = json.loads(response.get_data(as_text=True))["message"]
    assert empresa == []

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