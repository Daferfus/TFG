########################################################################
## Autor: David Fernández Fuster                                      ##
## Data: 09/09/2022                                                   ## 
## Funció: Comproba que els objectes amb els que treballa l'aplicació ##
##         s'instancien correctament.                                 ##
########################################################################

def test_nou_usuari_amb_fixture(nou_usuari):
    """
    DONAT un model d'Usuari
    QUAN un nou Usuari es creat
    LLAVORS comprobar que els camps nom, contrasenya i rol hajen sigut definits correctament.
    """
    nou_usuari.establir_contrasenya(nou_usuari.contrasenya)

    assert nou_usuari.nom == 'Mikaeru Softo'
    assert nou_usuari.contrasenya != 'Machete1@'
    assert nou_usuari.rol == 'Alumne'
## ()

def test_nou_alumne_amb_fixture(nou_alumne):
    """
    DONAT un model d'Alumne
    QUAN un nou Alumne es creat
    LLAVORS comprobar que els camps nom_i_cognoms, grup, poblacio, mobilitat, tipo_de_practica, 
    preferencies, observacions, aporta_empresa, erasmus, distancies i assignacio 
    hajen sigut definits correctament.
    """
    assert nou_alumne.nom_i_cognoms == "David Fernández Fuster" 
    assert nou_alumne.grup == "DAW"
    assert nou_alumne.poblacio == "Gandía"
    assert nou_alumne.mobilitat == "Sí" 
    assert nou_alumne.tipo_de_practica == "DUAL" 
    assert nou_alumne.preferencies == {"FrontEnd": 5, "BackEnd": 7, "BD": 4} 
    assert nou_alumne.observacions == "Disponible"
    assert nou_alumne.aporta_empresa == True
    assert nou_alumne.erasmus == False 
    assert nou_alumne.distancies == {
        "Punt de Partida": "Gandía", 
        "Punt de Destí": "València", 
        "Distància": 8
    }
    assert nou_alumne.assignacio == {
        "Alumne": "David Fernández Fuster", 
        "Pràctica": "Locatec_(Pràctica 01)", 
        "Professor": "Juan Miguel Alberola Oltra"
    }
## ()

def test_nou_professor_amb_fixture(nou_professor):
    """
    DONAT un model de Professor
    QUAN un nou Professor es creat
    LLAVORS comprobar que els camps nom, cognoms, titulacions, hores_alliberades, hores_restants, 
    rati_fct, rati_dual i assignacions hajen sigut definits correctament.
    """
    assert nou_professor.nom == "Juan Miguel"
    assert nou_professor.cognoms == "Alberola Oltra"
    assert nou_professor.titulacions == {"DAW": "X", "ASIX": "X"}
    assert nou_professor.hores_alliberades == 8 
    assert nou_professor.hores_restants == 5 
    assert nou_professor.rati_fct == "1 hora per alumne"
    assert nou_professor.rati_dual == "3 hores per alumne"
    assert nou_professor.assignacions == [
        {
            "Alumne": "David Fernández Fuster", 
            "Pràctica": "Locatec_(Pràctica 01)", 
            "Professor": "Juan Miguel Alberola Oltra"
        }
    ]
## ()

def test_nova_empresa_amb_fixture(nova_empresa):
    """
    DONAT un model d'Empersa
    QUAN una nova Empresa es creada
    LLAVORS comprobar que els camps nom, poblacio, telefon, correu, 
    persona_de_contacte, practiques i assignacions hajen sigut definits correctament.
    """
    assert nova_empresa.nom == "Locatec" 
    assert nova_empresa.poblacio == "València" 
    assert nova_empresa.telefon == 665517969
    assert nova_empresa.correu == "info@locatec.es" 
    assert nova_empresa.persona_de_contacte == "Salva"
    assert nova_empresa.practiques == [{"Nom": "Pràctica 01"}]
    assert nova_empresa.assignacions == [
        {
            "Alumne": "David Fernández Fuster", 
            "Pràctica": "Locatec_(Pràctica 01)", 
            "Professor": "Juan Miguel Alberola Oltra"
        }
    ]
## ()