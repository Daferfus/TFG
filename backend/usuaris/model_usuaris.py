from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mongoengine as me

class Usuari(UserMixin, me.Document):
    nom: str = me.StringField(required=True)
    contrasenya: str = me.StringField(required=True)
    rol: str = me.StringField(required=True)

    def establir_contrasenya(self, contrasenya: str):
        """Crea una contrasenya xifrada.

        Args:
            contrasenya (str): Contrasenya sense xifrar del usuari.
        """
        self.contrasenya = generate_password_hash(
            contrasenya,
            method='sha256'
        )

    def validar_contraseya(self, contrasenya: str) -> bool:
        """Verifica que la contrasenya pasada siga la mateixa que la xifrada.

        Args:
            contrasenya (str): Contrasenya a verificar.

        Returns:
            bool: Si la contrasenya es igual a la xifrada.
        """
        return check_password_hash(self.contrasenya, contrasenya)

    def __repr__(self) -> str:
        """Retorna el usuari actual.

        Returns:
            str: Usuari actual.
        """
        return '<Usuari {}>'.format(self.nom)