import json

def test_esborrar_usuaris_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de esborrat d'usuaris
    LLAVORS comprovar que no quede cap usuari.
    """    
    resposta = test_client.delete('/esborrar_usuaris')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True


def test_registrar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de registre d'usuari
    LLAVORS comprovar que este haja sigut registrat i que no puga tornar-se a registrar.
    """    
    dades = {"nom_de_usuari": 'Mikaeru Softo', "contrasenya_de_usuari": 'Machete1@', "rol_de_usuari": "Alumne"}
    primera_resposta = test_client.post('/registrar_usuari', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta = test_client.post('/registrar_usuari', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "Ja existeix un usuari amb aquest nom."

def test_autenticar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de autenticació d'usuari
    LLAVORS comprovar que estiga autenticat.
    """    
    dades = {"nom_de_usuari": 'Mikaeru Softo', "contrasenya_de_usuari": 'Machete1@'}
    resposta = test_client.post('/autenticar_usuari', data=dades)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True

def test_logout_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de tancar sessió
    LLAVORS comprovar que l'usuari no estiga autenticat.
    """    
    resposta = test_client.get('/logout')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True

def test_recuperar_dades_de_usuaris_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de recuperar dades de tots els usuaris
    LLAVORS el primer usuari te que correspondre al previament insertat.
    """    
    resposta = test_client.get('/recuperar_dades_de_usuaris')
    usuari = json.loads(resposta.get_data(as_text=True))["message"]
    assert usuari[0]["nom"] == "Mikaeru Softo"

def test_actualitzar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'actualitzar usuari
    LLAVORS comprovar que el nom ja no siga el mateix.
    """    
    dades = {'nom_de_usuari': 'Michael Soft', 'contrasenya_de_usuari': 'Machete1@', "rol_de_usuari": "Alumne"}
    primera_resposta = test_client.put('/actualitzar_usuari/Mikaeru Softo', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta = test_client.put('/actualitzar_usuari/Mikaeru Softo', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["success"] == False

def test_esborrar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de esborrat d'usuari
    LLAVORS comprovar que el usuari previament insertat no existisca.
    """    
    resposta = test_client.delete('/esborrar_usuari/Michael Soft')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True

def test_recuperar_dades_del_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de de recerca del usuari anteriorment borrat
    LLAVORS comprovar que no existisca.
    """    
    resposta = test_client.get('/recuperar_dades_del_usuari/Michael Soft')
    usuari = json.loads(resposta.get_data(as_text=True))["message"]
    assert usuari == "No s'ha trovat cap usuari."
