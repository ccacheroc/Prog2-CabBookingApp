import sqlite3
import os

class ReservationRepository:
    db_path = os.path.join(os.path.dirname(__file__), 'reservaTaxis.sdb')

    @staticmethod
    def _connect():
        """Establece la conexión con la base de datos."""
        return sqlite3.connect(ReservationRepository.db_path)

    @staticmethod
    def add_reservation(user_id, car_id, date, time,origen,destino):
        """
        Añade una nueva reserva a la base de datos.
        :param user_id: int - ID del usuario que realiza la reserva.
        :param car_id: int - ID del coche reservado.
        :param date: str - Fecha de la reserva.
        :param time: str - Hora de la reserva.
        :return: bool - True si la reserva se añadió correctamente, False en caso contrario.
        """
        conn = ReservationRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO reservations (id_user, id_car, fecha, hora,origen,destino) 
                VALUES (?, ?, ?, ?,?,?)
            ''', (user_id, car_id, date, time,origen,destino))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("Error al añadir la reserva:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def get_reservations():
        """
        Recupera todas las reservas de la base de datos.
        :return: list of tuples - Lista de reservas.
        """
        conn = ReservationRepository._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM reservations')
            reservations = cursor.fetchall()
            return reservations
        finally:
            conn.close()


    @staticmethod
    def get_filtered_reservations(user_id=None, car_id=None):
        conn = ReservationRepository._connect()
        cursor = conn.cursor()
        query = 'SELECT * FROM reservations'
        params = []
        conditions = []

        if user_id:
            conditions.append('id_user = ?')
            params.append(user_id)
        if car_id:
            conditions.append('id_car = ?')
            params.append(car_id)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        conn.close()
        return results
