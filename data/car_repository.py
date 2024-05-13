import sqlite3
import os

class CarRepository:
    db_path = os.path.join(os.path.dirname(__file__), 'reservaTaxis.sdb')

    @staticmethod
    def _connect():
        """Establece la conexión con la base de datos."""
        return sqlite3.connect(CarRepository.db_path)

    @staticmethod
    def add_car(matricula, marca, modelo, color):
        """
        Añade un nuevo coche a la base de datos.
        :param matricula: str - Matrícula del coche, única para cada vehículo.
        :param marca: str - Marca del coche.
        :param modelo: str - Modelo del coche.
        :param color: str - Color del coche.
        :return: bool - True si el coche se añadió correctamente, False en caso contrario.
        """
        conn = CarRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO cars (matricula, marca, modelo, color) 
                VALUES (?, ?, ?, ?)
            ''', (matricula, marca, modelo, color))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("Error al añadir el coche:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_cars():
        """
        Recupera todos los coches de la base de datos.
        :return: list of tuples - Lista de coches disponibles.
        """
        conn = CarRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT marca, modelo FROM cars')
            cars = cursor.fetchall()
            return cars
        finally:
            conn.close()

    @staticmethod
    def find_car_by_matricula(matricula):
        """
        Busca un coche por su matrícula.
        :param matricula: str - Matrícula del coche.
        :return: tuple or None - Datos del coche si se encuentra, None si no se encuentra.
        """
        conn = CarRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM cars WHERE matricula = ?', (matricula,))
            car = cursor.fetchone()
            return car
        finally:
            conn.close()

