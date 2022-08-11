import json
from flask import Response


# def test_importar_alumnes_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de importar alumnes
#     LLAVORS comprovar que els alumnes estiguen insertats.
#     """    
#     file = "tests\\functional\\fitxers\\DAW.csv"
#     data = {
#         'fichero': (open(file, 'rb'), file),
#         'cicle': "DAW"
#     }
#     resposta: Response = test_client.post('/importar_alumnes', data=data)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_importar_professors_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de importar professors
#     LLAVORS comprovar que els professor estiguen insertats.
#     """    
#     file = "tests\\functional\\fitxers\\Dades_empreses-professors-21-22.xlsx"
#     data = {
#         'fichero': (open(file, 'rb'), file)
#     }
#     resposta: Response = test_client.post('/importar_professors', data=data)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_importar_empreses_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de importar empreses
#     LLAVORS comprovar que les empreses estiguen insertades.
#     """    
#     file = "tests\\functional\\fitxers\\Empreses-Adaptat.xlsx"
#     data = {
#         'fichero': (open(file, 'rb'), file)
#     }
#     resposta: Response = test_client.post('/importar_empreses', data=data)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True


# def test_insertar_practica_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de inserció de pràctica
#     LLAVORS comprovar que esta haja sigut insertada i que no puga tornar-se a insertar.
#     """    
#     dades: dict = {
#         "practiques_de_la_empresa": '{"id": 1, "nom": "Practica01","tutor": "Juanma"}'
#     }
#     primera_resposta: Response = test_client.post('/insertar_practica/AEOL', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
#     segona_resposta: Response = test_client.post('/insertar_practica/AEOL', data=dades)
#     assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "La pràctica ja existeix."

# def test_insertar_assignacio_manual_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de insertar assignació de forma manual
#     LLAVORS comprovar que l'alumne tinga la seua pràctica assignada.
#     """    
#     dades: dict[str, str] = {
#         "assignacio": '{"Alumne": "alumno01", "Practica": "AEOL(Pràctica 01)", "Professor": "professor01"}'
#     }
#     resposta: Response = test_client.post('/insertar_assignacio_manual/alumno01/professor01/professor01/AEOL', data=dades)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_actualitzar_assignacio_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de d'actualitzar assignació
#     LLAVORS comprovar que l'alumne tinga la seua pràctica actualitzada.
#     """    
#     dades: dict[str, str] = {
#         "assignacio": '{"Alumne": "alumno02", "Practica": "AEOL(Pràctica 01)", "Professor": "professor01"}'
#     }
#     resposta: Response = test_client.put('/actualitzar_assignacio/alumno01/professor01/professor01/AEOL/Pràctica01', data=dades)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

    
# def test_esborrar_assignacio_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de d'esborrar assignació
#     LLAVORS comprovar que l'alumne ja no estiga assignat a cap pràctica.
#     """    
#     resposta: Response = test_client.delete('/esborrar_assignacio/alumno02/professor01/professor01/AEOL/Pràctica01')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True


# def test_realitzar_assignacio_automatica_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de realitzar assignació automàtica
#     LLAVORS comprovar que els alumnes s'hajen assignat.
#     """    
#     resposta: Response = test_client.post('/realitzar_assignacio_automatica')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True