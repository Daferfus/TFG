from backend.models.empreses import Empresa
import pandas as pd


###############################
########## Empreses ###########
###############################
def insertar_empresa(
    nom_de_empresa, 
    poblacio_de_empresa, 
    telefon_de_empresa=0, 
    correu_de_empresa="", 
    persona_de_contacte_en_la_empresa="",
    practiques_de_la_empresa={}
    ):
    empresa = Empresa(
        nom=nom_de_empresa, 
        poblacio=poblacio_de_empresa, 
        telefon=telefon_de_empresa, 
        correu=correu_de_empresa, 
        persona_de_contacte=persona_de_contacte_en_la_empresa, 
        practiques=practiques_de_la_empresa
        )
    empresa.save()


def actualitzar_empresa(
    nom_de_empresa_per_a_filtrar,
    nom_de_empresa, 
    poblacio_de_empresa, 
    telefon_de_empresa=0, 
    correu_de_empresa="", 
    persona_de_contacte_en_la_empresa="",
    ):
    Empresa.objects(nom=nom_de_empresa_per_a_filtrar).update(__raw__=[
        {"$set": {
            "nom": nom_de_empresa,
            "poblacio": poblacio_de_empresa,
            "telefon": telefon_de_empresa,
            "correu": correu_de_empresa,
            "persona_de_contacte": persona_de_contacte_en_la_empresa,
            }
        }
    ],)

def borrar_empreses():
    Empresa.objects.delete()

def borrar_empresa(nom_de_la_empresa):
    Empresa.objects(nom=nom_de_la_empresa).delete()

def insertar_practica(
    nom_de_empresa_per_a_filtrar,
    practica_de_la_empresa
    ):
    empresa = Empresa.objects(nom=nom_de_empresa_per_a_filtrar).get()
    empresa.practiques.append(practica_de_la_empresa)
    empresa.save()

def actualitzar_practica(
    nom_de_empresa_per_a_filtrar,
    practica_a_filtrar,
    practica_de_la_empresa
    ):
    Empresa.objects(nom=nom_de_empresa_per_a_filtrar, practiques=practica_a_filtrar).update(set__practiques__S=practica_de_la_empresa)

def borrar_practica(nom_de_empresa_per_a_filtrar, practica_de_la_empresa):
    Empresa.objects(nom=nom_de_empresa_per_a_filtrar).update(pull__practiques__S=practica_de_la_empresa)

def recuperar_dades_de_empreses():
    return Empresa.objects()
    
def recuperar_dades_de_la_empresa(nom_de_la_empresa):
    empresa = Empresa.objects(nom=nom_de_la_empresa)
    return empresa

def importar_empreses(nom_del_fitxer):
    df = pd.read_excel(nom_del_fitxer)
    empreses = []
    ciutat_empreses = []
    nombre_de_fila = 0

    while nombre_de_fila < len(df):
        empresa = {}
        preferencies = {}
        nombre_de_practiques = 0
        for columna in df:
            ## Nombre de pràctiques que ofereix.
            if columna == "TSMR" or columna == "ASIR" or columna == "DAM" or columna == "DAW":
                if not pd.isnull(df.loc[nombre_de_fila, columna]):
                    preferencies[columna] = df.loc[nombre_de_fila, columna]
                    nombre_de_practiques+=int(df.loc[nombre_de_fila, columna])
                    empresa["Preferencies"] = preferencies
                    empresa["Practiques"] = nombre_de_practiques
            else:
                if not pd.isnull(df.loc[nombre_de_fila, columna]):
                    empresa[columna] = df.loc[nombre_de_fila, columna]

        ## Si ofereix pràctiques s'anyadix al diccionari.
        if empresa["Practiques"] != 0:
            if "Ciutat" in empresa:
                empreses.append(empresa)
                if empresa["Ciutat"] not in ciutat_empreses:
                    ciutat_empreses.append(empresa["Ciutat"])

                insertar_empresa(
                    empresa["Empresa"],
                    empresa["Ciutat"]
                )           
        nombre_de_fila+=1
##########################################################
##########################################################
