from model.professors import Professor
import pandas as pd

###############################
######### Professors ##########
###############################
def insertar_professor(
    nom_del_professor,
    cognoms_del_professor,
    titulacions_del_professor,
    hores_alliberades_del_professor,
    hores_restants_del_professor,
    rati_fct_del_professor = "",
    rati_dual_del_professor = "",
    assignacions_del_professor = {}
):
    professor = Professor(
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

def actualitzar_professor(
    nom_de_professor_per_a_filtrar,
    cognoms_de_professor_per_a_filtrar,
    nom_del_professor,
    cognoms_del_professor,
    titulacions_del_professor,
    hores_alliberades_del_professor,
    hores_restants_del_professor
):
    Professor.objects(nom=nom_de_professor_per_a_filtrar, cognoms=cognoms_de_professor_per_a_filtrar).update(__raw__=[
        {"$set": {
            "nom": nom_del_professor,
            "cognoms": cognoms_del_professor,
            "titulacions": titulacions_del_professor,
            "hores_alliberades": hores_alliberades_del_professor,
            "hores_restants": hores_restants_del_professor
            }
        }
    ],)

def borrar_professors():
    Professor.objects.delete()

def borrar_professor(nom_del_professor, cognoms_del_professor):
    Professor.objects(nom=nom_del_professor, cognoms=cognoms_del_professor).delete()

def recuperar_dades_de_professors():
    return Professor.objects()
    
def recuperar_dades_del_professor(nom_del_professor):
    professor = Professor.objects(nom=nom_del_professor)
    return professor;

def importar_professors(nom_del_fitxer):
    df = pd.read_excel(nom_del_fitxer)

    nombre_de_fila = 0

    while nombre_de_fila < len(df):

        professor = {}
        preferencies = {}

        for columna in df:
            if not pd.isnull(df.loc[nombre_de_fila, columna]):
            
                ## Nom del professor.
                if columna == "NOM":
                    professor[columna] = df.loc[nombre_de_fila, columna]

                ## Hores lliures del professor.
                elif columna == "HORES":
                    professor[columna] = df.loc[nombre_de_fila, columna]

                ## Preferències.
                else:
                    preferencies[columna] = df.loc[nombre_de_fila, columna]

            professor["Preferències"] = preferencies

        insertar_professor(
            professor["NOM"],
            professor["NOM"],
            professor["Preferències"],
            professor["HORES"],
            professor["HORES"],
        )
        nombre_de_fila+=1
##########################################################
##########################################################