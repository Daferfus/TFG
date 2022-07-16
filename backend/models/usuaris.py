from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mongoengine as me

class Usuari(UserMixin, me.Document):
    nom = me.StringField(required=True)
    contrasenya = me.StringField(required=True)
    rol = me.StringField(required=True)

    def set_password(self, contrasenya):
        """Create hashed password."""
        self.contrasenya = generate_password_hash(
            contrasenya,
            method='sha256'
        )

    def check_password(self, contrasenya):
        """Check hashed password."""
        return check_password_hash(self.contrasenya, contrasenya)

    def __repr__(self):
        return '<Usuari {}>'.format(self.nom)