#########################################################
## Autor: David Fernández Fuster                       ##
## Data: 09/09/2022                                    ## 
## Funció: Comprova el funcionament del client Flask.  ##
#########################################################

def test_acces_valid_a_rutes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN es mana una petició valida a la ruta /prova
    LLAVORS comprovar que la resposta es valida.
    """
    response = test_client.get('/prova')
    assert response.data == b'Hola M\xc3\xb3n!'

def test_acces_invalid_a_rutes_amb_fixture(test_client):
    """
    DONADA una aplicació Flask configurada per a fer proves
    QUAN es mana una petició invalida a la ruta /prova
    LLAVORS comprovar que retorne el còdic 405.
    """
    response = test_client.post('/prova')
    assert response.status_code == 405