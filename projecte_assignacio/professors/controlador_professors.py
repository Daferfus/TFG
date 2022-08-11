from projecte_assignacio.professors.model_professors import Professor
from projecte_assignacio.usuaris import controlador_usuaris
import pandas as pd
import os
###############################
######### Professors ##########
###############################
def insertar_professor(
    nom_de_usuari: str,
    nom_del_professor: str,
    cognoms_del_professor: str,
    titulacions_del_professor: dict,
    hores_alliberades_del_professor: int,
    hores_restants_del_professor: int,
    rati_fct_del_professor: str = "",
    rati_dual_del_professor: str = "",
    assignacions_del_professor: list = []
) -> str:
    """Inserta un professor en la base de dades.

    Args:
        nom_del_professor (str): Nom del professor.
        cognoms_del_professor (str): Cognoms del professor.
        titulacions_del_professor (dict): Cicles formatius dins del perfil del professor.
        hores_alliberades_del_professor (int): Hores totals que el professor te disponibles per a visitar alumnes.
        hores_restants_del_professor (int): Diferència entre les hores alliberades i les invertides per el professor en un alumne.
        rati_fct_del_professor (str, optional): Hores a les que el professor te que dedicar a un alumne (o conjunt d'alumnes) de FCT. Defaults to "".
        rati_dual_del_professor (str, optional): Hores a les que el professor te que dedicar a un alumne (o conjunt d'alumnes) de DUAL. Defaults to "".
        assignacions_del_professor (list, optional): Pràctiques a les que el professor està assignat. Defaults to [].

    Returns:
        str: Resultat de l'operació.
    """
    professor_existent: Professor|None = recuperar_dades_del_professor(nom_de_usuari)

    if professor_existent is None:
        professor: Professor = Professor(
            nom_de_usuari=nom_de_usuari,
            nom=nom_del_professor, 
            cognoms=cognoms_del_professor, 
            titulacions=titulacions_del_professor, 
            hores_alliberades=hores_alliberades_del_professor, 
            hores_restants=hores_restants_del_professor, 
            rati_fct=rati_fct_del_professor, 
            rati_dual=rati_dual_del_professor, 
            assignacions=assignacions_del_professor,
        )
        professor.save()
        professor_insertat: Professor|None = recuperar_dades_del_professor(nom_de_usuari)

        if professor_insertat:
            controlador_usuaris.registrar_usuari(
                nom_de_usuari=nom_de_usuari, 
                contrasenya_de_usuari=nom_de_usuari+"_2022", 
                rol_de_usuari="Professor"
            )
            return "El professor s'ha insertat amb èxit."
        else:
            return "Ha ocorregut un problema durant la inserció."
    else:
        return "Ja existeix un professor amb aquest nom i cognoms."


def actualitzar_professor(
    usuari: str,
    nom_del_professor: str,
    cognoms_del_professor: str,
    titulacions_del_professor: dict,
    hores_alliberades_del_professor: int,
    hores_restants_del_professor: str
) -> str:
    """Actualitza les dades d'un professor donat.

    Args:
        nom_de_professor_per_a_filtrar (str): Nom del professor a actualitzar.
        cognoms_de_professor_per_a_filtrar (str): Cognoms del professor a actualitzar.
        nom_del_professor (str): Nou nom del professor.
        cognoms_del_professor (str): Nous cognoms del professor.
        titulacions_del_professor (dict): Noves titulacions del professor.
        hores_alliberades_del_professor (int): Noves hores alliberades del professor.
        hores_restants_del_professor (str): Noves hores restants del professor.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: int = Professor.objects(nom_de_usuari=usuari).update(__raw__=
            {"$set": {
                "nom": nom_del_professor,
                "cognoms": cognoms_del_professor,
                "titulacions": titulacions_del_professor,
                "hores_alliberades": hores_alliberades_del_professor,
                "hores_restants": hores_restants_del_professor
                }
            }
        )
    if resultat > 0:
            return "El professor ha sigut actualitzat."
    else:
        return "No s'ha canviat res del professor."

def actualitzar_ratis(
    usuari: str,
    rati_fct: str,
    rati_dual: str
) -> str:
    """Actualitza les dades d'un professor donat.

    Args:
        nom_de_professor_per_a_filtrar (str): Nom del professor a actualitzar.
        cognoms_de_professor_per_a_filtrar (str): Cognoms del professor a actualitzar.
        nom_del_professor (str): Nou nom del professor.
        cognoms_del_professor (str): Nous cognoms del professor.
        titulacions_del_professor (dict): Noves titulacions del professor.
        hores_alliberades_del_professor (int): Noves hores alliberades del professor.
        hores_restants_del_professor (str): Noves hores restants del professor.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: int = Professor.objects(nom_de_usuari=usuari).update(__raw__=
            {"$set": {
                "rati_fct": rati_fct,
                "rati_dual": rati_dual                }
            }
        )
    if resultat > 0:
            return "El professor ha sigut actualitzat."
    else:
        return "No s'ha canviat res del professor."


def esborrar_professors() -> str:
    """Esborra tots els professors.

    Returns:
        str: Resultat de l'operació.
    """
    Professor.objects.delete()

    professors: list[Professor] = recuperar_dades_de_professors()
    if len(professors) == 0:
        return "S'ha esborrat amb èxit tots els professors."
    else:
        return "Ha ocorregut un problema durant el esborrament."


def esborrar_professor(usuari: str) -> str:
    """Esborra un professor donat.

    Args:
        nom_del_professor (str): Nom del professor a esborrar.
        cognoms_del_professor (str): Cognoms del professor a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    Professor.objects(nom_de_usuari=usuari).delete()

    professor: Professor = recuperar_dades_del_professor(usuari)
    if professor:
        return "Ha ocorregut un problema durant el esborrament."
    else:
        return "S'ha esborrat amb èxit el professor."

def recuperar_dades_de_professors() -> list[Professor]:
    """Retorna una llista de professors.

    Returns:
        list[Professor]: Llista de professors.
    """
    return Professor.objects()
    
def recuperar_dades_del_professor(usuari: str) -> Professor:
    """Retorna un professor donat.

    Args:
        nom_del_professor (str): Nom del professor a retornar.
        cognoms_del_professor (str): Cognoms del professor a retornar.

    Returns:
        Professor: Professor retornat.
    """
    professor = Professor.objects(nom_de_usuari=usuari).first()
    return professor

def importar_professors(nom_del_fitxer: str) -> str:
    """Inserta cada professor trovat en un fitxer.

    Args:
        nom_del_fitxer (str): Ubicació local del ftxer.

    Returns:
        str: Resultat de l'operació.
    """
    df: any = pd.read_excel(nom_del_fitxer)

    nombre_de_fila: int = 0
    contador_de_insertats: int = 0
    quantitat_de_professors_ja_insertats: int = 0

    while nombre_de_fila < len(df):

        professor: dict = {}
        titulacions: dict = {}

        for columna in df:
            if not pd.isnull(df.loc[nombre_de_fila, columna]):
            
                ## Nom del professor.
                if columna == "NOM":
                    professor[columna]: str = df.loc[nombre_de_fila, columna]

                ## Hores lliures del professor.
                elif columna == "HORES":
                    professor[columna]: int = df.loc[nombre_de_fila, columna]

                ## Preferències.
                else:
                    titulacions[columna]: dict = df.loc[nombre_de_fila, columna]

            professor["Titulacions"] = titulacions

        resultat: str = insertar_professor(
            nom_de_usuari=professor["NOM"],
            nom_del_professor=professor["NOM"],
            cognoms_del_professor=professor["NOM"],
            titulacions_del_professor=professor["Titulacions"],
            hores_alliberades_del_professor=professor["HORES"],
            hores_restants_del_professor=professor["HORES"],
        )
        nombre_de_fila+=1
        
        if resultat == "El professor s'ha insertat amb èxit.":
            contador_de_insertats+=1
        elif resultat == "Ja existeix un professor amb aquest nom i cognoms.":
            quantitat_de_professors_ja_insertats+=1
    if contador_de_insertats == 0 and quantitat_de_professors_ja_insertats == 0:
        return "Ha ocorregut un problema durant l'operació."
    else:
        return "S'han insertat " +str(contador_de_insertats)+ " de " +str(len(df))+ " professors." +str(quantitat_de_professors_ja_insertats)+ " ja estaven insertats."


def exportar_professors() -> str:
    """Exporta els professors de la base de dades a un fitxer xlsx.
    """
    professors: list[Professor] = recuperar_dades_de_professors()
    professors_dict: list[dict] = []

    for professor in professors:
        professor_dict: dict = {
            "Nom": professor.nom,
            "Cognoms": professor.cognoms,
            "Titulacions": str(professor.titulacions),
            "Hores Alliberades": professor.hores_alliberades,
            "Hores Restants": professor.hores_restants,
            "Rati FCT": professor.rati_fct,
            "Rati DUAL": professor.rati_dual,
            "Assignacions": professor.assignacions
        }
        professors_dict.append(professor_dict)
    
    dades = pd.DataFrame.from_dict(professors_dict)
    dades.to_excel("professors_ex.xlsx",header=True)

    return os.path.exists("professors_ex.xlsx")
##########################################################
##########################################################