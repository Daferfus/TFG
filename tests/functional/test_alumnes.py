##########################################################################
## Autor: David Fernández Fuster                                        ##
## Data: 13/08/2022                                                     ## 
## Funció: Conté les rutes que desencandenen accions sobre els alumnes. ##
##########################################################################

################
## Llibreries ##
################
import json

#############
##  Flask  ##
#############
from flask import Response

##############
##  Mòduls  ##
##############
from projecte_assignacio.alumnes.model_alumnes import Alumne


#############
##  Tests  ##
#############
def test_esborrar_alumnes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'esborrat d'alumnes
    LLAVORS comprovar que no quede cap alumne.
    """  
    resposta: Response = test_client.delete('/esborrar_alumnes')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_inserir_alumne_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de inserció d'alumne
    LLAVORS comprovar que este haja sigut insertat i que no puga tornar-se a inserir.
    """    
    dades: dict[str, str] = {
        "nom_i_cognoms": "David Fernàndez Fuster",
        "grup": "DAW",
        "ciutat_de_residencia": "Gandía",
        "disponibilitat_de_cotxe": "Sí",
        "tipo_de_practica": "DUAL",
        "preferencies_del_alumne": '{"FrontEnd": 5, "BackEnd": 7, "BD": 4}',
        "accedeix_a_fct": 'Sí',
        "observacions": "Disponible",
        "aporta_empresa": "True",
        "es_erasmus": "False"
    }
    primera_resposta: Response = test_client.post('/insertar_alumne', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta: Response = test_client.post('/insertar_alumne', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "Ja existeix un alumne amb aquest usuari."
## ()

def test_obtindre_dades_del_alumne_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de de recerca de l'alumne anteriorment inserit
    LLAVORS comprovar que existisca.
    """    
    resposta: Response = test_client.get('/alumne/David Fernàndez Fuster')
    alumne: Alumne|str = json.loads(resposta.get_data(as_text=True))["message"]
    assert alumne["nom_i_cognoms"] == "David Fernàndez Fuster"
## ()

def test_actualitzar_alumne_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat amb éxit la petició d'actualitzar alumne
    LLAVORS comprovar que la petició fracase si és fa sobre un inexistent.
    """    
    dades: dict[str, str] = {
        "nom_i_cognoms": "David Fernández Fuster",
        "grup": "ASIR",
        "ciutat_de_residencia": "Gandía",
        "disponibilitat_de_cotxe": "Sí",
        "tipo_de_practica": "DUAL",
        "preferencies": '{"FrontEnd": 5, "BackEnd": 7, "BD": 4}',
        "accedeix_a_fct": "No",
        "observacions": "Disponible",
        "aporta_empresa": "True",
        "es_erasmus": "False"
    }
    primera_resposta: Response = test_client.post('/actualitzar_alumne/ASIR/David Fernàndez Fuster', data=dades)
    assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
    segona_resposta: Response = test_client.post('/actualitzar_alumne/ASIR/David Fernández Fuster', data=dades)
    assert json.loads(segona_resposta.get_data(as_text=True))["success"] == False
## ()

def test_esborrar_alumne_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'esborrat d'alumne
    LLAVORS comprovar que l'alumne previament inserit no existisca.
    """    
    resposta: Response = test_client.post('/esborrar_alumne/David Fernàndez Fuster')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_importar_alumnes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'importar alumnes
    LLAVORS comprovar que els alumnes estiguen inserits.
    """    
    fitxer = "tests\\functional\\fitxers\\DAM.csv"
    data = {
        'fichero': (open(fitxer, 'rb'), fitxer),
        'cicle': "DAM"
    }
    resposta: Response = test_client.post('/importar_alumnes', data=data)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_exportar_empreses_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'exportar alumnes
    LLAVORS comprovar que existisca el fitxer.
    """    
    resposta: Response = test_client.get('/exportar_alumnes')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_obtindre_dades_de_alumnes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de recuperar dades de tots els alumnes
    LLAVORS ha d'hi haure 15 alumnes en la base de dades.
    """    
    resposta: Response = test_client.get('/alumnes')
    alumnes: list[Alumne] = json.loads(resposta.get_data(as_text=True))["message"]
    assert len(alumnes) == 15
## ()
##############################################################
##############################################################