import tkinter as tk
from tkinter import messagebox
from data.reservation_repository import ReservationRepository
from data.car_repository import CarRepository
from data.user_repository import UserRepository
from tkcalendar import Calendar


class BookingScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Reserva de Taxis")
        self.geometry = '800x748+300+300'

        # Configuración de la ventana
        master.geometry(self.geometry)
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Lista desplegable para seleccionar usuario
        self.user_label = tk.Label(self.frame, text="Usuario:")
        self.user_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.user_var = tk.StringVar(self.frame)
        self.user_var.set("Seleccione un usuario")

        self.user_options=self.get_users()
        if not self.user_options:
            self.user_options=['No hay usuarios disponibles']
        self.user_dropdown = tk.OptionMenu(self.frame, self.user_var, *self.user_options)
        self.user_dropdown.config(width=30)
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Lista desplegable para seleccionar coche
        self.car_label = tk.Label(self.frame, text="Coche:")
        self.car_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.car_var = tk.StringVar(self.frame)
        self.car_var.set("Seleccione un coche")

        self.car_options=self.get_cars()
        if not self.car_options: #compruebo si hay coches disponibles
            self.car_options = ['No hay coches disponibles']

        self.car_dropdown = tk.OptionMenu(self.frame, self.car_var, *self.car_options)
        self.car_dropdown.config(width=30)
        self.car_dropdown.grid(row=1, column=1, padx=5, pady=5)

        """
        # Campo de texto para la fecha
        self.date_label = tk.Label(self.frame, text="Fecha (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        """
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
        self.user_filter_dropdown = tk.OptionMenu(self.frame, self.user_filter_var, *self.get_users(),
                                                  command=self.update_filtered_reservations_list)
        self.user_filter_dropdown.config(width=30)
        self.user_filter_dropdown.grid(row=8, column=1, padx=5, pady=5)


        # Botón para actualizar la lista de reservas
        self.update_button = tk.Button(self.frame, text="Ver Todas Reservas", command=self.update_reservations_list)
        self.update_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.update_reservations_list()  # Carga inicial de reservas



    def get_users(self):
        # Esta función debería interactuar con UserRepository para obtener una lista de usuarios
        return UserRepository.get_all_users()


    def get_cars(self):
        # Esta función debería interactuar con CarRepository para obtener una lista de coches disponibles
        return CarRepository.get_all_cars()


    def book(self):
        user = self.user_var.get()
        car = self.car_var.get()
        date = self.cal.get_date()
        time = self.time_entry.get()
        origen = self.origin_entry.get()
        destino = self.destination_entry.get()
        if user and car and date and time and origen and destino:
            result = ReservationRepository.add_reservation(user, car, date, time,origen,destino)
            if result:
                messagebox.showinfo("Éxito", "Reserva realizada correctamente")
                self.clear_fields()
                self.update_reservations_list()
            else:
                messagebox.showerror("Error", "No se pudo realizar la reserva")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def clear_fields(self):
        # Limpia todos los campos de entrada
        self.user_var.set('Seleccione usuario')
        self.car_var.set('Seleccione coche')
        self.time_entry.delete(0, tk.END)
        self.origin_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)

    def update_reservations_list(self):
        self.user_filter_var.set('Seleccione usuario')
        reservations = ReservationRepository.get_reservations()  # Asume que existe este método
        self.reservations_listbox.delete(0, tk.END)  # Limpiar la lista actual
        for res in reservations:
            # `res` es una tupla con los datos de la reserva
            # e.g. (1, "('Toyota', 'Auris')", "('carlos',)", '2024-05-12', '13:00', 'Luceros', 'Aeropuerto Alicante')

            display_text = f"{res[0]}: Reserva de {res[1]} para {res[2]} el {res[3]} a las {res[4]} de {res[5]} a {res[6]}"
            self.reservations_listbox.insert(tk.END, display_text)

    def update_filtered_reservations_list(self, _=None):  # _ para manejar el parámetro extra de command
        user_id = self.user_filter_var.get()
        reservations = ReservationRepository.get_filtered_reservations(user_id)
        self.reservations_listbox.delete(0, tk.END)  # Limpiar la lista actual
        for res in reservations:
            display_text = f"{res[0]}: Reserva de {res[1]} para {res[2]} el {res[3]} a las {res[4]} de {res[5]} a {res[6]}"
            self.reservations_listbox.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingScreen(root)
    root.mainloop()
