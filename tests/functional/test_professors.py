import json
import io
from flask import Response
from backend.professors.model_professors import Professor

def test_esborrar_professors_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de esborrat de professors
    LLAVORS comprovar que no quede cap professor.
    """    
    resposta: Response = test_client.delete('/esborrar_professors')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True

def test_insertar_professor_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de inserció de professor
    LLAVORS comprovar que este haja sigut insertat i que no puga tornar-se a insertar.
    """    
    dades: dict = {
        "nom_del_professor": "Juan Maria", 
        "cognoms_del_professor": "Alberola Oltra", 
        "titulacions_del_professor": '{"DAW": "X", "ASIX": "X"}', 
        "hores_alliberades_del_professor": 8, 
        "hores_restants_del_professor": 5
    }
    primera_resposta: Response = test_client.post('/insertar_professor', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta: Response = test_client.post('/insertar_professor', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "Ja existeix un professor amb aquest nom i cognoms."

def test_recuperar_dades_del_professor_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de de recerca del professor anteriorment insertat
    LLAVORS comprovar que existisca.
    """    
    resposta = test_client.get('/recuperar_dades_del_professor/Juan Maria/Alberola Oltra')
    professor: Professor|str = json.loads(resposta.get_data(as_text=True))["message"]
    assert professor["nom"] == "Juan Maria"

def test_actualitzar_professor_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'actualitzar professor
    LLAVORS comprovar que el nom ja no siga el mateix.
    """    
    dades: dict = {
        "nom_del_professor": "Juan Miguel", 
        "cognoms_del_professor": "Alberola Oltra", 
        "titulacions_del_professor": '{"DAW": "X", "ASIX": "X"}', 
        "hores_alliberades_del_professor": 8, 
        "hores_restants_del_professor": 8
    }
    primera_resposta: Response = test_client.put('/actualitzar_professor/Juan Maria/Alberola Oltra', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta: Response = test_client.put('/actualitzar_professor/Juan Maria/Alberola Oltra', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["success"] == False

def test_esborrar_professor_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de esborrat de professor
    LLAVORS comprovar que el professor previament insertat no existisca.
    """    
    resposta: Response = test_client.delete('/esborrar_professor/Juan Miguel/Alberola Oltra')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True


def test_importar_professors_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de importar professors
    LLAVORS comprovar que els professor estiguen insertats.
    """    
    file = "tests\\functional\\fitxers\\Dades_empreses-professors-21-22.xlsx"
    data = {
        'fichero': (open(file, 'rb'), file)
    }
    resposta = test_client.post('/importar_professors', data=data)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True

def test_exportar_professors_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de exportar professors
    LLAVORS comprovar que existisca el fitxer.
    """    
    resposta = test_client.get('/exportar_professors')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True

def test_recuperar_dades_de_professors_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de recuperar dades de tots els professors
    LLAVORS te que hi haure més de 0 professors en la base de dades.
    """    
    resposta: Response = test_client.get('/recuperar_dades_de_professors')
    professors: list[Professor] = json.loads(resposta.get_data(as_text=True))["message"]
    assert len(professors) == 44