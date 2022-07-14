def test_nou_usuari_amb_fixture(nou_usuari):
    """
    DONAT un model d'Usuari
    QUAN un nou Usuari es creat
    ENTONCES comprobar que els camps nom, contrasenya i rol hajen sigut definits correctament
    """

    assert nou_usuari.nom == 'Mikaeru Softo'
    assert nou_usuari.contrasenya != 'Machete1@'
    assert nou_usuari.rol == 'Alumne'