# ui/bookingscreen.py
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

import domain.usuario
from domain.usuario import Usuario
from domain.coche import Coche
from domain.reserva import Reserva

class BookingScreen:
    def __init__(self, master,user):
        self.master = master
        self.user=user
        self.master.title(f"Reserva de Taxis ({user.username})")
        self.geometry = '800x748+300+300'

        # Configuración de la ventana
        master.geometry(self.geometry)
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Mapeos de usuarios y coches: la clave es la cdena que aparece en el desplegable
        self.user_map = {user.username: user for user in Usuario.get_all()}
        #for key,user in self.user_map.items():
           # print(key,user)
        print(self.user_map)
        self.car_map = {f"{car.marca} {car.modelo}": car for car in Coche.get_all()}
        #for key, car in self.car_map.items():
            #print(key, car)
        # Lista desplegable para seleccionar usuario
        self.user_label = tk.Label(self.frame, text="Usuario:")
        self.user_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.user_var = tk.StringVar(self.frame)
        self.user_var.set("Seleccione un usuario")
        self.user_dropdown = self.create_option_menu(self.user_var, list(self.user_map.keys()), 30)
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Lista desplegable para seleccionar coche
        self.car_label = tk.Label(self.frame, text="Coche:")
        self.car_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.car_var = tk.StringVar(self.frame)
        self.car_var.set("Seleccione un coche")
        self.car_dropdown = self.create_option_menu(self.car_var, list(self.car_map.keys()), 30)
        self.car_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Widget de calendario para la fecha
        self.date_label = tk.Label(self.frame, text="Fecha de reserva:")
        self.date_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cal = Calendar(self.frame, selectmode='day')
        self.cal.grid(row=2, column=1, padx=5, pady=5)

        # Campo de texto para la hora
        self.time_label = tk.Label(self.frame, text="Hora (HH:MM):")
        self.time_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.time_entry = tk.Entry(self.frame)
        self.time_entry.grid(row=3, column=1, padx=5, pady=5)

        # Campo de texto para el origen del viaje
        self.origin_label = tk.Label(self.frame, text="Origen:")
        self.origin_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.origin_entry = tk.Entry(self.frame)
        self.origin_entry.grid(row=4, column=1, padx=5, pady=5)

        # Campo de texto para el destino del viaje
        self.destination_label = tk.Label(self.frame, text="Destino:")
        self.destination_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.destination_entry = tk.Entry(self.frame)
        self.destination_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botón para realizar la reserva
        self.book_button = tk.Button(self.frame, text="Reservar", command=self.book)
        self.book_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Widget para visualizar reservas
        self.reservations_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.reservations_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Sección de filtros
        self.filter_label = tk.Label(self.frame, text="Filtrar por usuario:")
        self.filter_label.grid(row=8, column=0, padx=5, pady=5)

        # Filtrar por usuario
        self.user_filter_var = tk.StringVar(self.frame)
        self.user_filter_var.set("Seleccione un usuario")
        self.user_filter_dropdown = self.create_option_menu(self.user_filter_var, list(self.user_map.keys()), 30,
                                                            self.update_filtered_reservations_list)
        self.user_filter_dropdown.grid(row=8, column=1, padx=5, pady=5)

        # Botón para actualizar la lista de reservas
        self.update_button = tk.Button(self.frame, text="Ver Todas Reservas", command=self.update_reservations_list)
        self.update_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.update_reservations_list()  # Carga inicial de reservas

    def create_option_menu(self, var, options, width, command=None):
        print("Lista de cadenas de opción: ",options)
        menu = tk.OptionMenu(self.frame, var, *options, command=command)
        menu.config(width=width)
        return menu

    def book(self):
        username = self.user_var.get()

        car_desc = self.car_var.get()

        date = self.cal.get_date()
        time = self.time_entry.get()
        origen = self.origin_entry.get()
        destino = self.destination_entry.get()

        if username and car_desc and date and time and origen and destino:
            userid=self.user_map.get(username).iduser
            carid=self.car_map.get(car_desc).idcar
            if userid and carid:
                reservation = Reserva(userid, carid, date, time, origen, destino)
                print(reservation)
                if reservation.save():
                    messagebox.showinfo("Éxito", "Reserva realizada correctamente")
                    self.clear_fields()
                    self.update_reservations_list()
                else:
                    messagebox.showerror("Error", "No se pudo realizar la reserva")
            else:
                messagebox.showerror("Error", "Error al obtener los datos del usuario o del coche")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def clear_fields(self):
        self.user_var.set("Seleccione un usuario")
        self.car_var.set("Seleccione un coche")
        self.time_entry.delete(0, tk.END)
        self.origin_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)

    def update_reservations_list(self):
        self.user_filter_var.set("Seleccione un usuario")
        reservations = Reserva.get_all()
        self.reservations_listbox.delete(0, tk.END)
        for res in reservations:
            display_text = f"{res.id_reserva}: Reserva de {res.marca_coche}-{res.modelo_coche} para {res.username} el {res.fecha} a las {res.hora} de {res.origen} a {res.destino}"
            self.reservations_listbox.insert(tk.END, display_text)

    def update_filtered_reservations_list(self, _=None):
        username = self.user_filter_var.get()
        if username in self.user_map:
            user_id = self.user_map[username].iduser
            reservations = Reserva.get_filtered(user_id)
            self.reservations_listbox.delete(0, tk.END)
            for res in reservations:
                display_text = f"{res.id_reserva}: Reserva de {res.marca_coche}-{res.modelo_coche} para {res.username} el {res.fecha} a las {res.hora} de {res.origen} a {res.destino}"
                self.reservations_listbox.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    user=Usuario('cris','cris')
    app = BookingScreen(root,user)
    root.mainloop()
