import os
from projecte_assignacio.empreses.model_empreses import Empresa
import pandas as pd


###############################
########## Empreses ###########
###############################
def insertar_empresa(
    nom_de_empresa: str, 
    poblacio_de_empresa: str, 
    telefon_de_empresa: int = 0, 
    correu_de_empresa: str = "", 
    persona_de_contacte_en_la_empresa: str = "",
    practiques_de_la_empresa: list[dict] = [],
    assignacions_de_la_empresa: list[dict] = []
    ) -> str:
    """Inserta una empresa en la base de dades.

    Args:
        nom_de_empresa (str): Nom de la empresa.
        poblacio_de_empresa (str): Poble/ciutat de l'empresa.
        telefon_de_empresa (int. optional): Nombre de telefon de l'empresa. Defaults to 0.
        correu_de_empresa (str, optional): Correu de l'empresa. Defaults to "".
        persona_de_contacte_en_la_empresa (str, optional): Persona interna de l'empresa amb contacte amb el cicle. Defaulst to "".
        practiques_de_la_empresa (list[dict], optional): Informació sobre la oferta en pràctiques de l'empresa. Defaults to [].
        assignacions_de_la_empresa (list[dict], optional): Pràctiques assignades de l'empresa. Defaults to [].

    Returns:
        str: Resultat de l'operació.
    """
    empresa_existent: Empresa|None = recuperar_dades_de_la_empresa(nom_de_empresa)

    if empresa_existent is None:
        empresa: Empresa = Empresa(
            nom=nom_de_empresa, 
            poblacio=poblacio_de_empresa, 
            telefon=telefon_de_empresa, 
            correu=correu_de_empresa, 
            persona_de_contacte=persona_de_contacte_en_la_empresa, 
            practiques=practiques_de_la_empresa,
            assignacions=assignacions_de_la_empresa
            )
        empresa.save()
        empresa_insertada: Empresa|None = recuperar_dades_de_la_empresa(nom_de_empresa)

        if empresa_insertada:
            return "L'empresa s'ha insertat amb èxit."
        else:
            return "Ha ocorregut un problema durant la inserció."
    else:
        return "Ja existeix una empresa amb aquest nom."


def actualitzar_empresa(
    nom_de_empresa_per_a_filtrar: str,
    nom_de_empresa: str, 
    poblacio_de_empresa: str, 
    telefon_de_empresa: int = 0, 
    correu_de_empresa: str = "", 
    persona_de_contacte_en_la_empresa: str = "",
    ) -> str:
    """Actualitza les dades d'una empresa donada.

    Args:
        nom_de_empresa_per_a_filtrar (str): Nom de la empresa a actualitzar.
        nom_de_empresa (str): Nou nom de la empresa.
        poblacio_de_empresa (str): Nova població de la empresa.
        telefon_de_empresa (int): Nou telefon de l'empresa.
        correu_de_empresa (str): Nou correu de l'empresa.
        persona_de_contacte_en_la_empresa (str): Nova persona de contacte en l'empresa.

    Returns:
        str: Resultat de l'operació.
    """
    resultat: int = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).update(__raw__=
        {"$set": {
            "nom": nom_de_empresa,
            "poblacio": poblacio_de_empresa,
            "telefon": telefon_de_empresa,
            "correu": correu_de_empresa,
            "persona_de_contacte": persona_de_contacte_en_la_empresa,
            }
        }
    )
    if resultat > 0:
            return "L'empresa ha sigut actualitzada."
    else:
        return "No s'ha canviat res de l'empresa."

def esborrar_empreses() -> str:
    """Esborra totes les empreses.

    Returns:
        str: Resultat de l'operació.
    """
    Empresa.objects.delete()

    empreses: list[Empresa] = recuperar_dades_de_empreses()
    if len(empreses) == 0:
        return "S'ha esborrat amb èxit totes les empreses."
    else:
        return "Ha ocorregut un problema durant el esborrament."

def esborrar_empresa(nom_de_la_empresa: str) -> str:
    """Esborra una empresa donada.

    Args:
        nom_de_la_empresa (str): Nom de la empresa a esborrar.
    
    Returns:
        str: Resultat de l'operació.
    """
    Empresa.objects(nom=nom_de_la_empresa).delete()

    empresa: Empresa = recuperar_dades_de_la_empresa(nom_de_la_empresa)
    if empresa:
        return "Ha ocorregut un problema durant el esborrament."
    else:
        return "S'ha esborrat amb èxit l'empresa."

def insertar_practica(
    nom_de_empresa_per_a_filtrar: str,
    practica_de_la_empresa: dict
    ) -> str:
    """Anyadix una pràctica a la llista de pràctiques ofertada per l'empresa.

    Args:
        nom_de_empresa_per_a_filtrar (str): Nom de l'empresa que oferta la pràctica.
        practica_de_la_empresa (dict): Pràctica a anyadir.

    Returns:
        str: Resultat de l'operació.
    """
    empresa: Empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).get()
    if empresa:
        practica_existeix: Empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar, practiques=practica_de_la_empresa).first()
        if practica_existeix:
            return "La pràctica ja existeix."
        else:
            empresa.practiques.append(practica_de_la_empresa)
            empresa.save()
            return "Pràctica insertada."
    else:
        return "L'empresa no existeix."

def actualitzar_practica(
    nom_de_empresa_per_a_filtrar: str,
    practica_a_filtrar: dict,
    practica_de_la_empresa: dict
    ) -> str:
    """Actualitza una pràctica donada.

    Args:
        nom_de_empresa_per_a_filtrar (str): Empresa de la que es vol actualitzar la pràctica.
        practica_a_filtrar (dict): Pràctica a actualitzar.
        practica_de_la_empresa (dict): Nova informació de la pràctica.

    Returns:
        str: Resultat de l'operació.
    """
    empresa: Empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).first()
    empresa.practiques[practica_a_filtrar["id"]-1] = practica_de_la_empresa
    empresa.save()

    practica_existeix: Empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar, practiques=practica_de_la_empresa).first()

    if practica_existeix:
        return "La pràctica ha sigut actualitzada."
    else:
        return "No s'ha canviat res de la pràctica."

def esborrar_practica(nom_de_empresa_per_a_filtrar: str, practica_de_la_empresa: dict) -> str:
    """Esborra una pràctica donada.

    Args:
        nom_de_empresa_per_a_filtrar (str): Empresa de la que es vol esborrar la pràctica.
        practica_de_la_empresa (dict): Pràctica a esborrar.

    Returns:
        str: Resultat de l'operació.
    """
    empresa: Empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).first()
    resultat = empresa.practiques.pop(practica_de_la_empresa["id"]-1)
    if resultat:
        return "La pràctica ha sigut esborrada."
    else:
        return "No s'ha trovat la pràctica a esborrar."

def recuperar_dades_de_empreses() -> list[Empresa]:
    """Retorna una llista d'empreses.

    Returns:
        list[Empresa]: Llista d'empreses.
    """
    return Empresa.objects()
    
def recuperar_dades_de_la_empresa(nom_de_la_empresa: str) -> Empresa:
    """Retorna una empresa donada.

    Args:
        nom_de_la_empresa (str): Nom de l'empresa a retornar.

    Returns:
        Empresa: Empresa retornada.
    """
    empresa: Empresa = Empresa.objects(nom=nom_de_la_empresa).first()
    return empresa

def importar_empreses(nom_del_fitxer: str) -> str:
    """Inserta cada empresa trovada en un fitxer.

    Args:
        nom_del_fitxer (str): Ubicació local del fitxer.

    Returns:
        str: Resultat de l'operació.
    """
    df = pd.read_excel(nom_del_fitxer)
    empreses: list[dict] = []
    ciutat_empreses: list[dict] = []
    nombre_de_fila: int = 0

    contador_de_insertats: int = 0
    quantitat_de_empreses_ja_insertats: int = 0

    while nombre_de_fila < len(df):
        empresa: dict = {}
        preferencies: dict = {}
        nombre_de_practiques: int = 0
        for columna in df:
            ## Nombre de pràctiques que ofereix.
            if columna == "TSMR" or columna == "ASIR" or columna == "DAM" or columna == "DAW":
                if not pd.isnull(df.loc[nombre_de_fila, columna]):
                    preferencies[columna]: int = df.loc[nombre_de_fila, columna]
                    nombre_de_practiques+=int(df.loc[nombre_de_fila, columna])
                    empresa["Preferencies"]: dict = preferencies
                    empresa["Practiques"]: int = nombre_de_practiques
            else:
                if not pd.isnull(df.loc[nombre_de_fila, columna]):
                    empresa[columna]: str = df.loc[nombre_de_fila, columna]

        ## Si ofereix pràctiques s'anyadix al diccionari.
        if empresa["Practiques"] != 0:
            if "Ciutat" in empresa:
                empreses.append(empresa)
                if empresa["Ciutat"] not in ciutat_empreses:
                    ciutat_empreses.append(empresa["Ciutat"])

                resultat: str = insertar_empresa(
                    empresa["Empresa"],
                    empresa["Ciutat"]
                )           
        nombre_de_fila+=1
        if resultat == "L'empresa s'ha insertat amb èxit.":
            contador_de_insertats+=1
        elif resultat == "Ja existeix una empresa amb aquest nom.":
            quantitat_de_empreses_ja_insertats+=1
    if contador_de_insertats == 0 and quantitat_de_empreses_ja_insertats == 0:
        return "Ha ocorregut un problema durant l'operació."
    else:
        return "S'han insertat " +str(contador_de_insertats)+ " de " +str(len(df))+ " empreses." +str(quantitat_de_empreses_ja_insertats)+ " ja estaven insertades."

def exportar_empreses() -> str:
    """Exporta les empreses de la base de dades a un fitxer xlsx.
    """
    empreses: list[Empresa] = recuperar_dades_de_empreses()
    empreses_dict: list[dict] = []

    for empresa in empreses:
        empresa_dict: dict = {
            "Nom": empresa.nom,
            "Població": empresa.poblacio,
            "Telefon": empresa.telefon,
            "Correu": empresa.correu,
            "Persona de Contacte": empresa.persona_de_contacte,
            "Pràctiques": str(empresa.practiques),
            "Assignacions": empresa.assignacions
        }
        empreses_dict.append(empresa_dict)
    
    dades = pd.DataFrame.from_dict(empreses_dict)
    dades.to_excel("empreses_ex.xlsx",header=True)

    return os.path.exists("empreses_ex.xlsx")
##########################################################
##########################################################
