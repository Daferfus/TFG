import json

def test_borrar_usuaris_amb_fixture(test_client):
    assert test_client.get('/borrar_usuaris').status_code == 405
    assert test_client.delete('/borrar_usuaris').status_code == 200
    response = test_client.delete('/borrar_usuaris')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_insertar_usuari_amb_fixture(test_client):
    datos = {'nom_de_usuari': 'Mikaeru Softo', 'contrasenya_de_usuari': 'Machete1@', "rol_de_usuari": "Alumne"}
    assert test_client.get('/insertar_usuari', data=datos).status_code == 405
    assert test_client.post('/insertar_usuari', data=datos).status_code == 200
    response = test_client.post('/insertar_usuari', data={'nom_de_usuari': 'Mikaeru Softo', 'contrasenya_de_usuari': 'Machete1@', "rol_de_usuari": "Alumne"})
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_recuperar_dades_de_usuaris_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_usuaris').status_code == 405
    assert test_client.get('/recuperar_dades_de_usuaris').status_code == 200
    response = test_client.get('/recuperar_dades_de_usuaris')
    usuari = json.loads(response.get_data(as_text=True))["message"]
    assert usuari[0]["nom"] == "Mikaeru Softo"

def test_actualitzar_usuari_amb_fixture(test_client):
    datos = {'nom_de_usuari': 'Michael Soft', 'contrasenya_de_usuari': 'Machete1@', "rol_de_usuari": "Alumne"}
    assert test_client.post('/actualitzar_usuari/Mikaeru Softo', data=datos).status_code == 405
    assert test_client.put('/actualitzar_usuari/Mikaeru Softo', data=datos).status_code == 200
    response = test_client.put('/actualitzar_usuari/Mikaeru Softo', data=datos)
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_borrar_usuari_amb_fixture(test_client):
    assert test_client.get('/borrar_usuari/Michael Soft').status_code == 405
    assert test_client.delete('/borrar_usuari/Michael Soft').status_code == 200
    response = test_client.delete('/borrar_usuari/Michael Soft')
    assert json.loads(response.get_data(as_text=True))["success"] == True

def test_recuperar_dades_del_usuari_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_del_usuari/Michael Soft').status_code == 405
    assert test_client.get('/recuperar_dades_del_usuari/Michael Soft').status_code == 200
    response = test_client.get('/recuperar_dades_del_usuari/Michael Soft')
    usuari = json.loads(response.get_data(as_text=True))["message"]
    assert usuari == []
