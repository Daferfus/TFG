import json

from flask import Response

from projecte_assignacio.alumnes.model_alumnes import Alumne

# def test_esborrar_alumnes_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'esborrat d'alumnes
#     LLAVORS comprovar que no quede cap alumne.
#     """  
#     resposta: Response = test_client.delete('/esborrar_alumnes')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_insertar_alumne_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de inserció d'alumne
#     LLAVORS comprovar que este haja sigut insertat i que no puga tornar-se a insertar.
#     """    
#     dades: dict[str, str] = {
#         "nom_i_cognom_del_alumne": "David Fernàndez Fuster",
#         "grup_del_alumne": "DAW",
#         "poblacio_del_alumne": "Gandía",
#         "mobilitat_del_alumne": "Sí",
#         "tipo_de_practica_del_alumne": "DUAL",
#         "preferencies_del_alumne": '{"FrontEnd": 5, "BackEnd": 7, "BD": 4}',
#         "observacions_del_alumne": "Disponible",
#         "aporta_empresa_el_alumne": "True",
#         "erasmus_del_alumne": "False"
#     }
#     primera_resposta: Response = test_client.post('/insertar_alumne', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
#     segona_resposta: Response = test_client.post('/insertar_alumne', data=dades)
#     assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "Ja existeix un alumne amb aquest nom i cognoms."

# def test_recuperar_dades_del_alumne_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de de recerca de l'alumne anteriorment insertat
#     LLAVORS comprovar que existisca.
#     """    
#     resposta: Response = test_client.get('/recuperar_dades_del_alumne/David Fernàndez Fuster')
#     alumne: Alumne|str = json.loads(resposta.get_data(as_text=True))["message"]
#     assert alumne["nom_i_cognoms"] == "David Fernàndez Fuster"

# def test_actualitzar_alumne_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'actualitzar alumne
#     LLAVORS comprovar que el nom ja no siga el mateix.
#     """    
#     dades: dict[str, str] = {
#         "nom_i_cognom_del_alumne": "David Fernández Fuster",
#         "grup_del_alumne": "ASIX",
#         "poblacio_del_alumne": "Gandía",
#         "mobilitat_del_alumne": "Sí",
#         "tipo_de_practica_del_alumne": "DUAL",
#         "preferencies_del_alumne": '{"FrontEnd": 5, "BackEnd": 7, "BD": 4}',
#         "observacions_del_alumne": "Disponible",
#         "aporta_empresa_el_alumne": "True",
#         "erasmus_del_alumne": "False"
#     }
#     primera_resposta: Response = test_client.put('/actualitzar_alumne/David Fernàndez Fuster', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
#     segona_resposta: Response = test_client.put('/actualitzar_alumne/David Fernàndez Fuster', data=dades)
#     assert json.loads(segona_resposta.get_data(as_text=True))["success"] == False

# def test_esborrar_alumne_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'esborrat d'alumne
#     LLAVORS comprovar que l'alumne previament insertat no existisca.
#     """    
#     response = test_client.delete('/esborrar_alumne/David Fernández Fuster')
#     assert json.loads(response.get_data(as_text=True))["success"] == True

# def test_importar_alumnes_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de importar alumnes
#     LLAVORS comprovar que els alumnes estiguen insertats.
#     """    
#     file = "tests\\functional\\fitxers\\DAM.csv"
#     data = {
#         'fichero': (open(file, 'rb'), file),
#         'cicle': "DAM"
#     }
#     resposta: Response = test_client.post('/importar_alumnes', data=data)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_exportar_empreses_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de exportar alumnes
#     LLAVORS comprovar que existisca el fitxer.
#     """    
#     resposta: Response = test_client.get('/exportar_alumnes')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True


# def test_recuperar_dades_de_alumnes_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de recuperar dades de tots els alumnes
#     LLAVORS te que hi haure més de 0 alumnes en la base de dades.
#     """    
#     resposta: Response = test_client.get('/recuperar_dades_de_alumnes')
#     alumnes: list[Alumne] = json.loads(resposta.get_data(as_text=True))["message"]
#     assert len(alumnes) == 15