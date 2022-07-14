from backend.models.alumnes import Alumne
import csv


################################
########### Alumnes ############
################################
def insertar_alumne(
    nom_i_cognom_del_alumne,
    grup_del_alumne,
    poblacio_del_alumne,
    mobilitat_del_alumne,
    preferencies_del_alumne,
    tipo_de_practica_del_alumne="",
    observacions_del_alumne = "",
    aporta_empresa_el_alumne = False,
    erasmus_del_alumne = False,
    distancies_del_alumne = [],
    assignacio_del_alumne = {}
):   

    alumne = Alumne(
        nom_i_cognom=nom_i_cognom_del_alumne, 
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

def actualitzar_alumne(
    nom_de_alumne_per_a_filtrar,
    nom_i_cognom_del_alumne,
    grup_del_alumne,
    poblacio_del_alumne,
    mobilitat_del_alumne,
    preferencies_del_alumne,
    tipo_de_practica_del_alumne="",
    observacions_del_alumne = "",
    aporta_empresa_el_alumne = False,
    erasmus_del_alumne = False
):   

    Alumne.objects(nom_i_cognom=nom_de_alumne_per_a_filtrar).update(__raw__=[
        {"$set": {
            "nom_i_cognom": nom_i_cognom_del_alumne,
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
    ],)

def borrar_alumnes():
    Alumne.objects.delete()

def borrar_alumne(nom_del_alumne):
    Alumne.objects(nom=nom_del_alumne).delete()

def recuperar_dades_de_alumnes():
    alumne = Alumne.objects()
    return alumne;

def recuperar_dades_del_alumne(nom_del_alumne):
    alumne = Alumne.objects(nom=nom_del_alumne)
    return alumne;

def importar_alumnes(nom_deL_fitxer, cicle):
    ## Accedim a dades del fitxer
    with open(nom_deL_fitxer, newline='') as arxiu_csv:

        ## Gastem la funció DictReader per a que agafe la primera fila com a nom de camps.
        dades_de_alumnes = csv.DictReader(arxiu_csv)
        for dades_del_alumne in dades_de_alumnes:

            ## Clavem totes les preferències en un diccionari.
            if cicle == "DAM":
                preferencies = {
                    'Backend': dades_del_alumne["[Desarrollador backend]"], 
                    'Multiplataforma': dades_del_alumne["[Desarrollador software multiplataforma]"],
                    'Videojuegos': dades_del_alumne["[Desarrollador videojuegos]"],
                    'Moviles': dades_del_alumne["[Desarrollador de aplicaciones moviles]"],
                    'Robotica': dades_del_alumne["[Programador de robotica, automocion e informatica industrial]"],
                    'Documentacion': dades_del_alumne["[Tecnico QA y documentacion]"],
                    'ERP': dades_del_alumne["[Consultor ERP]"]
                    }
            elif cicle == "DAW":
                preferencies = {
                    'Backend': dades_del_alumne["[Desarrollador backend]"], 
                    'Multiplataforma': dades_del_alumne["[Desarrollador software multiplataforma]"],
                    'Videojuegos': dades_del_alumne["[Desarrollador videojuegos]"],
                    'Moviles': dades_del_alumne["[Desarrollador de aplicaciones moviles]"],
                    'Robotica': dades_del_alumne["[Programador de robotica, automocion e informatica industrial]"],
                    'Documentacion': dades_del_alumne["[Tecnico QA y documentacion]"],
                    'ERP': dades_del_alumne["[Consultor ERP]"]
                }
            elif cicle == "ASIR":
                preferencies = {
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
                preferencies = {
                    'Microinformatico': dades_del_alumne["[Tecnico de microinformatica]"],
                    'Asesor': dades_del_alumne["[Asesor/vendedor de microinformatica]"],
                    'HelpDesk': dades_del_alumne["[Tecnico de soporte Helpdesk L1]"],
                    'Instalador': dades_del_alumne["[Instalador de redes e infraestructura IT]"]
                }                
            ## Adjuntem el reste de dades i el diccionari de preferències en un altre diccionari
            alumne = { 
                'Nom': dades_del_alumne["Nombre y apellidos"], 
                'Ciutat': dades_del_alumne["Ciudad donde vives"],
                'Cotxe': dades_del_alumne["Podrias utilizar coche"], 
                'Preferències': preferencies 
                }
            insertar_alumne(
                nom_i_cognom_del_alumne = alumne["Nom"], 
                grup_del_alumne = cicle, 
                poblacio_del_alumne = alumne["Ciutat"],
                mobilitat_del_alumne = alumne["Cotxe"],
                preferencies_del_alumne=alumne["Preferències"]
            )
##########################################################
##########################################################