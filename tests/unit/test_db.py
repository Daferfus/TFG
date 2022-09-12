###########################################################
## Autor: David Fernández Fuster                         ##
## Data: 09/09/2022                                      ## 
## Funció: Comprova el funcionament de la base de dades. ##
###########################################################
import mongomock

def test_iniciar_db(test_mongo):
    """
    DONAT un client amb base de dades Mongo
    QUAN e s'arreplega la conexió 
    ENTONCES comprobar que apareix com a instanciada.
    """
    client = test_mongo.get_connection()
    assert isinstance(client, mongomock.MongoClient)
## ()

def test_cerrar_db(test_mongo):
    """
    DONAT un client amb base de dades Mongo
    QUAN es desconecta
    ENTONCES comprobar que està desconectada.
    """
    try:
        test_mongo.disconnect()
        test_mongo.get_connection()
        assert False
    except Exception:
        assert True
## ()