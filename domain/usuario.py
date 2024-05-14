# domain/usuario.py
from data.user_repository import UserRepository

class Usuario:
    def __init__(self, username, password, email=None, tfno=None, id_usuario=None):
        self._username = username
        self._password = password
        self._email = email
        self._tfno = tfno
        self._iduser = id_usuario

    @property
    def iduser(self):
        return self._iduser
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def tfno(self):
        return self._tfno

    @tfno.setter
    def tfno(self, value):
        self._tfno = value
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def get_name(self):
        return self.username
    def save(self):
        """

        :return: true si se ha añadido con éxito, false en caso contrario
        """
        return UserRepository.add_user(self.username, self.password)

    def __str__(self):
        cad=f"USUARIO {self._iduser}\n"
        cad=cad+f"Username: {self._username}\n"
        cad=cad+f"Password: {self._password}\n"
        cad=cad+f"Email: {self._email}\n"
        cad=cad+f"Teléfono: {self._tfno}\n"
        return cad

    @classmethod
    def authenticate(cls, username, password):
        user_data = UserRepository.find_user(username, password)
        if user_data:
            print(user_data)
            return cls(user_data[1], user_data[2],user_data[0])
        return None

    @classmethod
    def get_all(cls):
        users_data = UserRepository.get_all_users()
        print(users_data)
        return [cls(username, password,email,tfno, idbd) for idbd,username, password, email, tfno in users_data]

# Otros métodos de negocio, como eliminación, actualización, etc., también pueden ser agregados aquí.
