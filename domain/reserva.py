# domain/reserva.py
from data.reservation_repository import ReservationRepository

class Reserva:
    def __init__(self, id_usuario, id_coche, fecha, hora, origen, destino, id_reserva=None,username=None, marca_coche=None, modelo_coche=None):
        self._id_reserva = id_reserva
        self._id_usuario = id_usuario
        self._id_coche = id_coche
        self._fecha = fecha
        self._hora = hora
        self._origen = origen
        self._destino = destino
        self._duracion_reserva=2 #se podría calcular en función de distancia entre origen y destino del viaje
        self.username = username
        self.marca_coche = marca_coche
        self.modelo_coche = modelo_coche
    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_coche(self):
        return self._id_coche

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        self._fecha = value

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, value):
        self._hora = value

    @property
    def origen(self):
        return self._origen

    @origen.setter
    def origen(self, value):
        self._origen = value

    @property
    def destino(self):
        return self._destino

    @destino.setter
    def destino(self, value):
        self._destino = value

    def __str__(self):
        cad=f"RESERVA {self._id_reserva}\n"
        cad=cad+f"ID usuario: {self._id_usuario}\n"
        cad=cad+f"ID coche: {self._id_coche}\n"
        cad=cad+f"Fecha: {self._fecha}\n"
        cad=cad+f"Hora: {self._hora}\n"
        cad=cad+f"Origen: {self._origen}\n"
        cad=cad+f"Destino: {self._destino}\n"
        cad=cad+f"Duración reserva: {self._duracion_reserva}\n"

        return cad
    def save(self):
        if self._id_reserva:
            return ReservationRepository.update_reservation(self._id_reserva, self.id_usuario, self.id_coche, self.fecha, self.hora, self.origen, self.destino)
        else:
            return ReservationRepository.add_reservation(self.id_usuario, self.id_coche, self.fecha, self.hora, self.origen, self.destino)

    @classmethod
    def get_all(cls):
        reservations_data = ReservationRepository.get_all_reservations()
        print(reservations_data)
        return [cls(id_user, id_car,fecha, hora, origen, destino,id_res,username,marca,modelo) for id_res, id_car, id_user, marca, modelo, username, fecha, hora, origen, destino in reservations_data]

    @classmethod
    def get_filtered(cls, user_id):
        reservations_data = ReservationRepository.get_filtered_reservations(user_id)
        print(reservations_data)
        return [cls(id_user, id_car,fecha, hora, origen, destino,id_res,username,marca,modelo) for id_res, id_car, id_user, marca, modelo, username, fecha, hora, origen, destino in reservations_data]
