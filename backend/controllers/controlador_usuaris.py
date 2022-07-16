from flask_login import login_required, logout_user, current_user, login_user
from backend.models.usuaris import Usuari
import bcrypt

##############################
########## Usuaris ###########
##############################
def registrar_usuari(nom_de_usuari, contrasenya_de_usuari, rol_de_usuari):
    existing_user = recuperar_dades_del_usuari(nom_de_usuari)
    if len(existing_user) == 0:
        #contrasenya_encriptada = bcrypt.hashpw(contrasenya_de_usuari.encode('utf-8'), bcrypt.gensalt())
        usuari = Usuari(
            nom=nom_de_usuari, 
            contrasenya=contrasenya_de_usuari, 
            rol=rol_de_usuari
            )
        usuari.set_password(contrasenya_de_usuari)
        print(usuari)
        usuari.save()
        login_user(usuari)

def actualitzar_credencials_del_usuari(nom_de_usuari_per_a_filtrar, nom_de_usuari, contrasenya_de_usuari, rol_de_usuari):
    contrasenya_encriptada = bcrypt.hashpw(contrasenya_de_usuari.encode('utf-8'), bcrypt.gensalt())
    Usuari.objects(nom=nom_de_usuari_per_a_filtrar).update(__raw__=
        {"$set": {
            "nom": nom_de_usuari,
            "contrasenya": contrasenya_encriptada,
            "rol": rol_de_usuari
            }
        }
    )

def borrar_usuaris():
    Usuari.objects.delete()

def borrar_usuari(nom_del_usuari):
    Usuari.objects(nom=nom_del_usuari).delete()

def autenticar_usuari(nom_de_usuari, contrasenya_de_usuari):
    usuari = recuperar_dades_del_usuari(nom_de_usuari)
    if usuari and usuari.check_password(password=contrasenya_de_usuari):
        login_user(usuari)

def recuperar_dades_de_usuaris():
    return Usuari.objects()

def recuperar_dades_del_usuari(nom_del_usuari):
    return Usuari.objects(nom=nom_del_usuari)

##########################################################
##########################################################