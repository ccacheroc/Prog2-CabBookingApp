# domain/coche.py
from data.car_repository import CarRepository

class Coche:
    def __init__(self, marca, modelo, color, matricula,id_car=None):
        self._idcar = id_car
        self._marca = marca
        self._modelo = modelo
        self._color = color
        self._matricula = matricula

    @property
    def idcar(self):
        return self._idcar
    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, value):
        self._marca = value

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, value):
        self._modelo = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, value):
        self._matricula = value

    def __str__(self):
        cad=f"COCHE {self._idcar}\n"
        cad=cad+f"Marca: {self._marca}\n"
        cad=cad+f"Modelo: {self._modelo}\n"
        cad=cad+f"Color: {self._color}\n"
        cad=cad+f"Matrícula: {self._matricula}\n"
        return cad

    def save(self):
        if self._id_car:
            return CarRepository.update_car(self._id_car, self.marca, self.modelo, self.color, self.matricula)
        else:
            return CarRepository.add_car(self.marca, self.modelo, self.color, self.matricula)

    @classmethod
    def get_all(cls):
        cars_data = CarRepository.get_all_cars()
        print(cars_data)
        return [cls(marca,modelo,color,matricula,car_id) for car_id,matricula,marca,modelo,color in cars_data]
