def test_acces_valid_a_rutes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN es mana una petició valida a la ruta /hello
    LLAVORS comprovar que la resposta es valida.
    """
    response = test_client.get('/hello')
    assert response.data == b'Hello, World!'

def test_acces_invalid_a_rutes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN es mana una petició invalida a la ruta /hello
    LLAVORS comprovar que retorne el còdic 405.
    """
    response = test_client.post('/hello')
    assert response.status_code == 405