import json
from flask import Response
from projecte_assignacio.usuaris.model_usuaris import Usuari

def test_esborrar_usuaris_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de esborrat d'usuaris
    LLAVORS comprovar que no quede cap usuari.
    """    
    resposta: Response = test_client.delete('/esborrar_usuaris')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True


def test_registrar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de registre d'usuari
    LLAVORS comprovar que este haja sigut registrat i que no puga tornar-se a registrar.
    """    
    dades: dict = {
        "nom": 'Mikaeru Softo', 
        "contrasenya": 'Machete1@', 
        "rol": "Alumne"
    }
    primera_resposta: Response = test_client.post('/registrar', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta: Response = test_client.post('/registrar', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "Ja existeix un usuari amb aquest nom."


def test_autenticar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de autenticació d'usuari
    LLAVORS comprovar que estiga autenticat.
    """    
    dades: dict = {
        "nom": 'Mikaeru Softo', 
        "contrasenya": 'Machete1@'
        }
    resposta: Response = test_client.post('/autenticar', data=dades)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True


def test_logout_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de tancar sessió
    LLAVORS comprovar que l'usuari no estiga autenticat.
    """    
    resposta: Response = test_client.get('/tancar_sessio')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True


def test_obtindre_dades_de_usuaris_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de recuperar dades de tots els usuaris
    LLAVORS el primer usuari te que correspondre al previament insertat.
    """    
    resposta: Response = test_client.get('/usuaris')
    usuari: list[Usuari] = json.loads(resposta.get_data(as_text=True))["message"]
    assert usuari[0]["nom"] == "Mikaeru Softo"


def test_actualitzar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'actualitzar usuari
    LLAVORS comprovar que el nom ja no siga el mateix.
    """    
    dades: dict = {'nom': 'Michael Soft', 'contrasenya': 'Machete1@', "rol": "Alumne"}
    primera_resposta: Response = test_client.put('/actualitzar_usuari/Mikaeru Softo', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta: Response = test_client.put('/actualitzar_usuari/Mikaeru Softo', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["success"] == False


def test_esborrar_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de esborrat d'usuari
    LLAVORS comprovar que el usuari previament insertat no existisca.
    """    
    resposta: Response = test_client.delete('/esborrar_usuari/Michael Soft')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True


def test_obtindre_dades_del_usuari_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de de recerca del usuari anteriorment borrat
    LLAVORS comprovar que no existisca.
    """    
    resposta: Response = test_client.get('/usuari/Michael Soft')
    usuari: Usuari|None = json.loads(resposta.get_data(as_text=True))["message"]
    assert usuari is None