######################################################################################
##        ##
##  GET   ##
##        ##
######################################################################################
def test_recuperar_dades_de_alumnes_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_alumnes').status_code == 405

def test_recuperar_dades_del_alumne_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_del_alumne/David Fernández Fuster').status_code == 405

def test_recuperar_dades_de_professors_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_professors').status_code == 405

def test_recuperar_dades_del_professor_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_del_professor/Juan Miguel Alberola Oltra').status_code == 405

def test_recuperar_dades_de_empreses_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_empreses').status_code == 405

def test_recuperar_dades_de_la_empresa_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_la_empresa/Locatec').status_code == 405

def test_recuperar_dades_de_usuaris_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_de_usuaris').status_code == 405

def test_recuperar_dades_del_usuari_amb_fixture(test_client):
    assert test_client.post('/recuperar_dades_del_usuari/Miakeru Softo').status_code == 405
######################################################################################
######################################################################################