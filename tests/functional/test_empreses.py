import json

from flask import Response

from projecte_assignacio.empreses.model_empreses import Empresa

# def test_esborrar_empreses_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de esborrat d'empreses
#     LLAVORS comprovar que no quede cap empresa.
#     """  
#     resposta: Response = test_client.delete('/esborrar_empreses')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_insertar_empresa_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de inserció d'empresa
#     LLAVORS comprovar que esta haja sigut insertada i que no puga tornar-se a insertar.
#     """    
#     dades: dict = {
#         "nom_de_empresa": "Mahico Soluciones", 
#         "poblacio_de_empresa": "València", 
#         "telefon_de_empresa": 665517969, 
#         "correu_de_empresa": "info@locatec.es", 
#         "persona_de_contacte_en_la_empresa": "Salva"
#     }
#     primera_resposta: Response = test_client.post('/insertar_empresa', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
#     segona_resposta: Response = test_client.post('/insertar_empresa', data=dades)
#     assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "Ja existeix una empresa amb aquest nom."

# def test_recuperar_dades_de_la_empresa_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de de recerca de l'empresa anteriorment insertada
#     LLAVORS comprovar que existisca.
#     """    
#     resposta: Response = test_client.get('/recuperar_dades_de_la_empresa/Mahico Soluciones')
#     empresa: Empresa|str = json.loads(resposta.get_data(as_text=True))["message"]
#     assert empresa["nom"] == "Mahico Soluciones"

# def test_actualitzar_empresa_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'actualitzar empresa
#     LLAVORS comprovar que el nom ja no siga el mateix.
#     """    
#     dades: dict = {
#         "nom_de_empresa": "Locatec", 
#         "poblacio_de_empresa": "València", 
#         "telefon_de_empresa": 665517969, 
#         "correu_de_empresa": "info@locatec.es", 
#         "persona_de_contacte_en_la_empresa": "Salva"
#     }
#     primera_resposta: Response = test_client.put('/actualitzar_empresa/Mahico Soluciones', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
#     segona_resposta: Response = test_client.put('/actualitzar_empresa/Mahico Soluciones', data=dades)
#     assert json.loads(segona_resposta.get_data(as_text=True))["success"] == False

# def test_insertar_practica_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de inserció de pràctica
#     LLAVORS comprovar que esta haja sigut insertada i que no puga tornar-se a insertar.
#     """    
#     dades: dict = {
#         "practiques_de_la_empresa": '{"id": 1, "nom": "Practica01","tutor": "Juanma"}'
#     }
#     primera_resposta: Response = test_client.post('/insertar_practica/Locatec', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True
#     segona_resposta: Response = test_client.post('/insertar_practica/Locatec', data=dades)
#     assert json.loads(segona_resposta.get_data(as_text=True))["message"] == "La pràctica ja existeix."

# def test_actualitzar_practica_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'actualitzar pràctica
#     LLAVORS comprovar que el nom ja no siga el mateix.
#     """    
#     dades: list[dict] = {
#         "practica_de_la_empresa": '{"id": 1, "nom": "Pràctica01", "tutor": "Juan Miguel Alberola Oltra"}'
#     }
#     primera_resposta: Response = test_client.put('/actualitzar_practica/Locatec/{"id": 1, "nom": "Practica01", "tutor": "Juanma"}', data=dades)
#     assert json.loads(primera_resposta.get_data(as_text=True))["success"] == True

# def test_esborrar_practica_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'esborrat de pràctica
#     LLAVORS comprovar que la pràctica previament insertada no existisca.
#     """    
#     resposta: Response = test_client.delete('/esborrar_practica/Locatec/{"id": 1, "nom": "Pràctica01", "tutor": "Juan Miguel Alberola Oltra"}')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_esborrar_empresa_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició d'esborrat d'empresa
#     LLAVORS comprovar que l'empresa previament insertada no existisca.
#     """    
#     resposta: Response = test_client.delete('/esborrar_empresa/Locatec')
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
#     resposta = test_client.post('/importar_empreses', data=data)
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_exportar_empreses_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de exportar empreses
#     LLAVORS comprovar que existisca el fitxer.
#     """    
#     resposta = test_client.get('/exportar_empreses')
#     assert json.loads(resposta.get_data(as_text=True))["success"] == True

# def test_recuperar_dades_de_empreses_amb_fixture(test_client):
#     """
#     DONADA una aplicació Flask configurada per a fer proves
#     QUAN s'haja executat la petició de recuperar dades de totes les empreses
#     LLAVORS te que hi haure més de 0 empreses en la base de dades.
#     """    
#     resposta: Response = test_client.get('/recuperar_dades_de_empreses')
#     empreses: list[Empresa] = json.loads(resposta.get_data(as_text=True))["message"]
#     assert len(empreses) == 51