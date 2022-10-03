###############################################################################
## Autor: David Fernández Fuster                                             ##
## Data: 11/08/2022                                                          ## 
## Funció: Prova les rutes que desencandenen accions sobre les assignacions. ##
###############################################################################

################
## Llibreries ##
################
import json
import pytest

#############
##  Flask  ##
#############
from flask import Response

######################################
##  Parche per als Tests de Celery  ##
######################################
from unittest.mock import patch

###########
##  Ruta ##
###########
import sys
sys.path.insert(0, "C:\\Users\\david\\Documents\\Proyectos\\Personales\\TFG\\projecte_assignacio")


#######################
##  Funció de Celery ##
#######################
from projecte_assignacio.assignacions.rutes_assignacions import assignar

#############
##  Tests  ##
#############
def test_importar_alumnes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de importar alumnes
    LLAVORS comprovar que els alumnes estiguen inserits.
    """    
    fitxer: str = "tests\\functional\\fitxers\\DAW.csv"
    data = {
        'fichero': (open(fitxer, 'rb'), fitxer),
        'cicle': "DAW"
    }
    resposta: Response = test_client.post('/importar_alumnes', data=data)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_importar_professors_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'importar professors
    LLAVORS comprovar que els professor estiguen inserits.
    """    
    fitxer: str = "tests\\functional\\fitxers\\Dades_empreses-professors-21-22.xlsx"
    data = {
        'fichero': (open(fitxer, 'rb'), fitxer)
    }
    resposta: Response = test_client.post('/importar_professors', data=data)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_importar_empreses_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'importar empreses
    LLAVORS comprovar que les empreses estiguen inserides.
    """    
    fitxer: str = "tests\\functional\\fitxers\\Empreses-Adaptat.xlsx"
    data = {
        'fichero': (open(fitxer, 'rb'), fitxer)
    }
    resposta: Response = test_client.post('/importar_empreses', data=data)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_inserir_assignacio_manual_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició d'inserir assignació de forma manual
    LLAVORS comprovar que l'alumne tinga la seua pràctica assignada.
    """    
    dades: dict[str, str] = {
        "assignacio": '{"Alumne": "alumno01", "Practica": "AEOL(Pràctica 01)", "Professor": "professor01"}'
    }
    resposta: Response = test_client.post('/insertar_assignacio_manual/alumno01/professor01/professor01/AEOL', data=dades)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

def test_actualitzar_assignacio_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de d'actualitzar assignació
    LLAVORS comprovar que l'alumne tinga la seua pràctica actualitzada.
    """    
    dades: dict[str, str] = {
        "assignacio": '{"Alumne": "alumno02", "Practica": "AEOL(Pràctica 01)", "Professor": "professor01"}'
    }
    resposta: Response = test_client.put('/actualitzar_assignacio/alumno01/professor01/professor01/AEOL/Pràctica01', data=dades)
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()
    
def test_esborrar_assignacio_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de d'esborrar assignació
    LLAVORS comprovar que l'alumne ja no estiga assignat a cap pràctica.
    """    
    resposta: Response = test_client.delete('/esborrar_assignacio/alumno02/professor01/professor01/AEOL/Pràctica01')
    assert json.loads(resposta.get_data(as_text=True))["success"] == True
## ()

@patch.object(assignar, 'delay')
@pytest.mark.use_fixtures
def test_realitzar_assignacio_automatica_amb_fixture(mock_delay, test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN s'haja executat la petició de realitzar assignació automàtica
    LLAVORS comprovar que els alumnes s'hagen assignat.
    """    
    resposta: Response = test_client.post('/realitzar_assignacio_automatica')
    #assert json.loads(resposta.get_data(as_text=True))["success"] == True
    assert resposta.status_code == 202
## ()
##############################################################
##############################################################