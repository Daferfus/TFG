import mongomock

def test_iniciar_db(test_mongo):
    client = test_mongo.get_connection()
    assert isinstance(client, mongomock.MongoClient)

def test_cerrar_db(test_mongo):
    try:
        test_mongo.disconnect()
        test_mongo.get_connection()
        assert False
    except Exception:
        assert True