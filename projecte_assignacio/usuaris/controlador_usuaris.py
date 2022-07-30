from flask_login import login_user
from projecte_assignacio.usuaris.model_usuaris import Usuari

##############################
########## Usuaris ###########
##############################
def registrar_usuari(nom_de_usuari: str, contrasenya_de_usuari: str, rol_de_usuari: str) -> str:
    """Inserta un usuari en la base de dades de no existir.

    Args:
        nom_de_usuari (str): el nom del usuari.
        contrasenya_de_usuari (str): contrasenya no xifrada del usuari.
        rol_de_usuari (str): rol que tindrà l'usuari en l'aplicació (alumne, professor, empresa o coordinador)

    Returns:
        str: Resultat de l'operació.
    """
    usuari_existent: Usuari = recuperar_dades_del_usuari(nom_de_usuari)

    if usuari_existent is None:

        usuari: Usuari = Usuari(
            nom=nom_de_usuari, 
            contrasenya=contrasenya_de_usuari, 
            rol=rol_de_usuari
            )
        usuari.establir_contrasenya(contrasenya_de_usuari)
        usuari.save()
        login_user(usuari)

        usuari_insertat: Usuari = recuperar_dades_del_usuari(nom_de_usuari)

        if usuari_insertat:
            return "L'usuari s'ha registrat amb èxit."
        else:
            return "Ha ocorregut un problema durant el registre."
    else:
        return "Ja existeix un usuari amb aquest nom."

def actualitzar_credencials_del_usuari(
    nom_de_usuari_per_a_filtrar: str, 
    nom_de_usuari: str, 
    contrasenya_de_usuari: str, 
    rol_de_usuari: str
    ) -> str:
    """Actualitza les dades d'un usuari donat.

    Args:
        nom_de_usuari_per_a_filtrar (str): nom antic del usuari, per a temes de recerca (a substituir per id).
        nom_de_usuari (str): nou nom del usuari.
        contrasenya_de_usuari (str): nova contrasenya del usuari.
        rol_de_usuari (str): nou rol del usuari.

    Returns:
        str: Resultat de l'operació.
    """
    usuari_existent: Usuari = Usuari.objects(nom=nom_de_usuari_per_a_filtrar) 
    if usuari_existent:
        usuari: Usuari = usuari_existent.get(nom=nom_de_usuari_per_a_filtrar)
        usuari.nom = nom_de_usuari
        usuari.establir_contrasenya(contrasenya_de_usuari)
        usuari.rol = rol_de_usuari
        usuari.save()
        
        usuari_actualitzat: Usuari = Usuari.objects(nom=nom_de_usuari, rol=rol_de_usuari).first()
        if usuari_actualitzat and usuari.validar_contraseya(contrasenya=contrasenya_de_usuari):
            return "L'usuari ha sigut actualitzat."
    else:
        return "L'usuari no existeix."

def esborrar_usuaris() -> str:
    """Esborra tots els usuaris.

    Returns:
        str: Resultat de l'operació.
    """
    Usuari.objects.delete()

    usuaris: list[Usuari] = recuperar_dades_de_usuaris()
    if len(usuaris) == 0:
        return "S'ha esborrat amb èxit tots els usuaris."
    else:
        return "Ha ocorregut un problema durant el esborrament."

def esborrar_usuari(nom_del_usuari: str) -> str:
    """Esborra un usuari donat.

    Args:
        nom_del_usuari (str): Nom del usuari a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    Usuari.objects(nom=nom_del_usuari).delete()
    usuari: Usuari = recuperar_dades_del_usuari(nom_del_usuari)
    if usuari:
        return "Ha ocorregut un problema durant el esborrament."
    else:
        return "S'ha esborrat amb èxit l'usuari."

def autenticar_usuari(nom_de_usuari: str, contrasenya_de_usuari: str) -> str:
    """Autentica un usuari.

    Args:
        nom_de_usuari (str): Nom del usuari a autenticar.
        contrasenya_de_usuari (str): Contrasenya del usuari a autenticar.
       
    Returns:
        str: Resultat de l'operació.
    """
    usuari: Usuari = recuperar_dades_del_usuari(nom_de_usuari)
    if usuari and usuari.validar_contraseya(contrasenya=contrasenya_de_usuari):
        login_user(usuari)
        return "Usuari autenticat."
    else:
        return "Les credencials no son valides."

def recuperar_dades_de_usuaris() -> list[Usuari]:
    """Retorna una llista d'usuaris.

    Returns:
        list[Usuari]: Llista d'usuaris.
    """
    return Usuari.objects()

def recuperar_dades_del_usuari(nom_del_usuari: str) -> list[Usuari]:
    """Retorna un usuari donat.

    Args:
        nom_del_usuari (str): Nom del usuari a retornar.

    Returns:
        Usuari: Usuari retornat.
    """
    return Usuari.objects(nom=nom_del_usuari).first()

##########################################################
##########################################################