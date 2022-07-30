import os
import pandas as pd
from projecte_assignacio.alumnes.model_alumnes import Alumne
import csv


################################
########### Alumnes ############
################################
def insertar_alumne(
    nom_i_cognoms_del_alumne: str,
    grup_del_alumne: str,
    poblacio_del_alumne: str,
    mobilitat_del_alumne: str,
    preferencies_del_alumne: dict[str, int],
    tipo_de_practica_del_alumne: str = "",
    observacions_del_alumne: str = "",
    aporta_empresa_el_alumne: bool = False,
    erasmus_del_alumne: bool = False,
    distancies_del_alumne: list[dict[str, str, float]] = [],
    assignacio_del_alumne: dict[str, str , str] = {}
) -> str:   
    """Inserta un alumne en la base de dades.

    Args:
        nom_i_cognoms_del_alumne (str): Nom i cognoms del alumne
        grup_del_alumne (str): Cicle formatiu al que pertany el alumne.
        poblacio_del_alumne (str): Població del alumne.
        mobilitat_del_alumne (str): Si el alumne té vehicle o no.
        preferencies_del_alumne (dict[str, int]): Preferències de l'alumne cap a cer tipus de pràctiques
        tipo_de_practica_del_alumne (str, optional): Si la pràctica es FCT o DUAL. Defaults to "".
        observacions_del_alumne (str, optional): Detalls que l'alumne vol deixar clars. Defaults to "".
        aporta_empresa_el_alumne (bool, optional): Si l'alumne ha trovat pel seu compte una empresa a la que fer pràctiques. Defaults to False.
        erasmus_del_alumne (bool, optional): Si l'alumne es de erasmus. Defaults to False.
        distancies_del_alumne (list[dict[str, str, float]], optional): Les distàncies de l'alumne cap a totes les empreses. Defaults to [].
        assignacio_del_alumne (dict[str, str , str], optional): A que pràctica i tutor l'alumne està assignat. Defaults to {}.

    Returns:
        str: Resultat de l'operació.
    """
    alumne_existent: Alumne|None = recuperar_dades_del_alumne(nom_i_cognoms_del_alumne)

    if alumne_existent is None:
        alumne: Alumne = Alumne(
            nom_i_cognoms=nom_i_cognoms_del_alumne, 
            grup=grup_del_alumne, 
            poblacio=poblacio_del_alumne, 
            mobilitat=mobilitat_del_alumne, 
            tipo_de_practica=tipo_de_practica_del_alumne, 
            preferencies=preferencies_del_alumne, 
            observacions=observacions_del_alumne, 
            aporta_empresa=aporta_empresa_el_alumne, 
            erasmus=erasmus_del_alumne, 
            distancies=distancies_del_alumne, 
            assignacio=assignacio_del_alumne
        )
        alumne.save()
        alumne_insertat: Alumne|None = recuperar_dades_del_alumne(nom_i_cognoms_del_alumne)

        if alumne_insertat:
            return "L'alumne s'ha insertat amb èxit."
        else:
            return "Ha ocorregut un problema durant la inserció."
    else:
        return "Ja existeix un alumne amb aquest nom i cognoms."

def actualitzar_alumne(
    nom_de_alumne_per_a_filtrar: str,
    nom_i_cognoms_del_alumne: str,
    grup_del_alumne: str,
    poblacio_del_alumne: str,
    mobilitat_del_alumne: str,
    preferencies_del_alumne: dict[str, int],
    tipo_de_practica_del_alumne: str ="",
    observacions_del_alumne: str = "",
    aporta_empresa_el_alumne: bool = False,
    erasmus_del_alumne: bool = False
) -> str:   
    """Actualitza les dades d'un alumne donat.

    Args:
        nom_de_alumne_per_a_filtrar (str): Nom de l'alumne a actualitzar
        nom_i_cognoms_del_alumne (str): Nou nom i cognoms de l'alumne.
        grup_del_alumne (str): Nou cicle formatiu de l'alumne.
        poblacio_del_alumne (str): Nova població de l'alumne.
        mobilitat_del_alumne (str): Nova mobilitat de l'alumne.
        preferencies_del_alumne (dict[str, int]): Noves preferències de l'alumne.
        tipo_de_practica_del_alumne (str, optional): Nou tipus de pràctica de l'alumne. Defaults to "".
        observacions_del_alumne (str, optional): Noves observacions de l'alumne. Defaults to "".
        aporta_empresa_el_alumne (bool, optional): Nova posibilitat de que l'alumne aporte pràctica. Defaults to False.
        erasmus_del_alumne (bool, optional): Nou canvi en la condició de l'estudiant. Defaults to False.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: int = Alumne.objects(nom_i_cognoms=nom_de_alumne_per_a_filtrar).update(__raw__=
        {"$set": {
            "nom_i_cognoms": nom_i_cognoms_del_alumne,
            "grup": grup_del_alumne,
            "poblacio": poblacio_del_alumne,
            "mobilitat": mobilitat_del_alumne,
            "preferencies": preferencies_del_alumne,
            "tipo_de_practica": tipo_de_practica_del_alumne,
            "preferencies": preferencies_del_alumne,
            "observacions": observacions_del_alumne,
            "aporta_empresa": aporta_empresa_el_alumne,
            "erasmus": erasmus_del_alumne
            }
        }
    )
    if resultat > 0:
            return "L'alumne ha sigut actualitzat."
    else:
        return "No s'ha canviat res de l'alumne."


def esborrar_alumnes() -> str:
    """Esborra tots els alumnes.

    Returns:
        str: Resultat de l'operació.
    """
    Alumne.objects.delete()
    alumnes: list[Alumne] = recuperar_dades_de_alumnes()
    if len(alumnes) == 0:
        return "S'ha esborrat amb èxit tots els alumnes."
    else:
        return "Ha ocorregut un problema durant el esborrament."

def esborrar_alumne(nom_del_alumne: str):
    """Esborra un alumne donat.

    Args:
        nom_del_alumne (str): Nom de l'alumne a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    Alumne.objects(nom_i_cognoms=nom_del_alumne).delete()

    alumne: Alumne = recuperar_dades_del_alumne(nom_del_alumne)
    if alumne:
        return "Ha ocorregut un problema durant el esborrament."
    else:
        return "S'ha esborrat amb èxit l'alumne."

def recuperar_dades_de_alumnes() -> list[Alumne]:
    """Retorna una llista d'alumnes.

    Returns:
        list[Alumne]: Llista d'alumnes.
    """
    alumnes: list[Alumne] = Alumne.objects()
    return alumnes;

def recuperar_dades_del_alumne(nom_del_alumne: str) -> Alumne:
    """Retorna un alumne donat.

    Args:
        nom_del_alumne (str): Nom de l'alumne a retornar.

    Returns:
        Alumne: Alumne retornat.
    """
    alumne: Alumne = Alumne.objects(nom_i_cognoms=nom_del_alumne).first()
    return alumne;

def importar_alumnes(nom_deL_fitxer: str, cicle: str):
    """Inserta cada alumne trovat en un fitxer.

    Args:
        nom_del_fitxer (str): Ubicació local del fitxer.
        cicle (str): Cicle formatiu del que es vol importar els alumnes.

    Returns:
        str: Resultat de l'operació.
    """

    contador_de_insertats: int = 0
    quantitat_de_alumnes_ja_insertats: int = 0
    ## Accedim a dades del fitxer
    with open(nom_deL_fitxer, newline='') as arxiu_csv:

        ## Gastem la funció DictReader per a que agafe la primera fila com a nom de camps.
        dades_de_alumnes = csv.DictReader(arxiu_csv)
        for dades_del_alumne in dades_de_alumnes:

            ## Clavem totes les preferències en un diccionari.
            if cicle == "DAM":
                preferencies: dict[str, int] = {
                    'Backend': dades_del_alumne["[Desarrollador backend]"], 
                    'Multiplataforma': dades_del_alumne["[Desarrollador software multiplataforma]"],
                    'Videojuegos': dades_del_alumne["[Desarrollador videojuegos]"],
                    'Moviles': dades_del_alumne["[Desarrollador de aplicaciones moviles]"],
                    'Robotica': dades_del_alumne["[Programador de robotica, automocion e informatica industrial]"],
                    'Documentacion': dades_del_alumne["[Tecnico QA y documentacion]"],
                    'ERP': dades_del_alumne["[Consultor ERP]"]
                    }
            elif cicle == "DAW":
                preferencies: dict[str, int] = {
                    'Backend': dades_del_alumne["[Desarrollador backend]"], 
                    'Multiplataforma': dades_del_alumne["[Desarrollador software multiplataforma]"],
                    'Videojuegos': dades_del_alumne["[Desarrollador videojuegos]"],
                    'Moviles': dades_del_alumne["[Desarrollador de aplicaciones moviles]"],
                    'Robotica': dades_del_alumne["[Programador de robotica, automocion e informatica industrial]"],
                    'Documentacion': dades_del_alumne["[Tecnico QA y documentacion]"],
                    'ERP': dades_del_alumne["[Consultor ERP]"]
                }
            elif cicle == "ASIR":
                preferencies: dict[str, int] = {
                    'Sistemas': dades_del_alumne["[Administrador de sistemas]"],
                    'BD': dades_del_alumne["[Administrador de bases de datos]"],
                    'Redes': dades_del_alumne["[Administrador de redes]"],
                    'Ciberseguridad': dades_del_alumne["[Ciberseguridad]"],
                    'Consultor': dades_del_alumne["[Consultor TIC]"],
                    'Hardware': dades_del_alumne["[Tecnico de hardware]"],
                    'HelpDesk': dades_del_alumne["[Tecnico de soporte HelpDesk L2]"],
                    'Auditor': dades_del_alumne["[Auditor TIC]"],
                    'Monitorizador': dades_del_alumne["[Tecnico de monitorizacion de sistemas]"]
                }
            elif cicle == "TSMR":
                preferencies: dict[str, int] = {
                    'Microinformatico': dades_del_alumne["[Tecnico de microinformatica]"],
                    'Asesor': dades_del_alumne["[Asesor/vendedor de microinformatica]"],
                    'HelpDesk': dades_del_alumne["[Tecnico de soporte Helpdesk L1]"],
                    'Instalador': dades_del_alumne["[Instalador de redes e infraestructura IT]"]
                }                
            ## Adjuntem el reste de dades i el diccionari de preferències en un altre diccionari
            alumne: dict[str, str|dict[str,int]] = { 
                'Nom': dades_del_alumne["Nombre y apellidos"], 
                'Ciutat': dades_del_alumne["Ciudad donde vives"],
                'Cotxe': dades_del_alumne["Podrias utilizar coche"], 
                'Preferències': preferencies 
                }
            resultat: str = insertar_alumne(
                nom_i_cognoms_del_alumne = alumne["Nom"], 
                grup_del_alumne = cicle, 
                poblacio_del_alumne = alumne["Ciutat"],
                mobilitat_del_alumne = alumne["Cotxe"],
                preferencies_del_alumne=alumne["Preferències"]
            )
            if resultat == "L'alumne s'ha insertat amb èxit.":
                contador_de_insertats+=1
            elif resultat == "Ja existeix un alumne amb aquest nom i cognoms.":
                quantitat_de_alumnes_ja_insertats+=1
    if contador_de_insertats == 0 and quantitat_de_alumnes_ja_insertats == 0:
        return "Ha ocorregut un problema durant l'operació."
    else:
        return "S'han insertat " +str(contador_de_insertats)+ " de 15 alumnes." +str(quantitat_de_alumnes_ja_insertats)+ " ja estaven insertades."


def exportar_alumnes() -> str:
    """Exporta els alumnes de la base de dades a un fitxer xlsx.
    """
    alumnes: list[Alumne] = recuperar_dades_de_alumnes()
    alumnes_dict: list[dict] = []

    for alumne in alumnes:
        alumne_dict: dict = {
            "Nom": alumne.nom_i_cognoms,
            "Grup": alumne.grup,
            "Població": alumne.poblacio,
            "Mobilitat": alumne.mobilitat,
            "Preferencies": str(alumne.preferencies),
            "Tipo de Pràctica": alumne.tipo_de_practica,
            "Observacions": alumne.observacions,
            "Aporta Empresa": alumne.aporta_empresa,
            "Erasmus": alumne.erasmus,
            "Distàncies": alumne.distancies,
            "Assignacions": alumne.assignacio
        }
        alumnes_dict.append(alumne_dict)
    
    dades = pd.DataFrame.from_dict(alumnes_dict)
    dades.to_excel("alumnes_ex.xlsx",header=True)

    return os.path.exists("alumnes_ex.xlsx")
##########################################################
##########################################################