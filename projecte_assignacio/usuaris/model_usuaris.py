##########################################
## Autor: David Fernández Fuster        ##
## Data: 12/08/2022                     ## 
## Funció: Defineix i valida un usuari. ##
##########################################

###########
## Flask ##
###########
from flask_login import UserMixin

########################
## Xifrat/Verificació ##
##  de Contrasenyes   ##
########################
from werkzeug.security import generate_password_hash, check_password_hash

###################
## Base de Dades ##
###################
from flask_mongoengine import MongoEngine
db = MongoEngine()

class Usuari(UserMixin, db.Document):
    nom: str = db.StringField(required=True)
    contrasenya: str = db.StringField(required=True)
    rol: str = db.StringField(required=True)
    distancies: list[dict] = db.ListField(required=False)

    def establir_contrasenya(self, contrasenya: str):
        """Crea una contrasenya xifrada.

        Args:
            contrasenya (str): Contrasenya sense xifrar del usuari.
        """
        self.contrasenya = generate_password_hash(
            contrasenya,
            method='sha256'
        )
    ## ()

    def validar_contraseya(self, contrasenya: str) -> bool:
        """Verifica que la contrasenya pasada siga la mateixa que la xifrada.

        Args:
            contrasenya (str): Contrasenya a verificar.

        Returns:
            bool: Si la contrasenya es igual a la xifrada.
        """
        return check_password_hash(self.contrasenya, contrasenya)
    ## ()

    def __repr__(self) -> str:
        """Retorna el usuari actual.

        Returns:
            str: Usuari actual.
        """
        return '<Usuari {}>'.format(self.nom)
    ## ()
## class
##############################################################
##############################################################