import sqlite3
import os

class UserRepository:
    #db_path = './reservaTaxis.sdb'  # Asegúrate de cambiar esto por la ruta real a tu base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'reservaTaxis.sdb')
    @staticmethod
    def _connect():
        """Establece la conexión con la base de datos."""
        return sqlite3.connect(UserRepository.db_path)

    @staticmethod
    def add_user(username, password):
        """Añade un nuevo usuario a la base de datos."""
        conn = UserRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def find_user(username, password):
        """Busca un usuario en la base de datos y verifica si la contraseña es correcta."""
        conn = UserRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            return user is not None
        finally:
            conn.close()

    @staticmethod
    def get_all_users():
        """
        Recupera todos los usuarios de la base de datos.
        :return: list of tuples - Cada tupla contiene los detalles de un usuario (id_user, username, password).
        """
        conn = UserRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT username FROM users')
            users = cursor.fetchall()
            return users
        finally:
            conn.close()
