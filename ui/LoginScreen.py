import tkinter as tk
from tkinter import messagebox
from domain.usuario import Usuario
from ui.BookingScreen import BookingScreen


class LoginScreen:
    def __init__(self, master): #aquí creo todos los widgets

        self.master = master
        self.master.title("Identificación")
        self.geometry='500x500+300+300'

        # Configuración de la ventana
        master.geometry(self.geometry)
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Campo de texto para el nombre de usuario
        self.username_label = tk.Label(self.frame, text="Usuario:")
        self.username_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Campo de texto para la contraseña
        self.password_label = tk.Label(self.frame, text="Contraseña:")
        self.password_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botón para añadir nuevo usuario
        self.add_user_button = tk.Button(self.frame, text="Añadir usuario", command=self.add_user)
        self.add_user_button.grid(row=2, column=0, padx=5, pady=5)

        # Botón para iniciar sesión
        self.login_button = tk.Button(self.frame, text="Iniciar sesión", command=self.login)
        self.login_button.grid(row=2, column=1, padx=5, pady=5)

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            user = Usuario(username, password)
            result = user.save()
            if result:
                messagebox.showinfo("Éxito", "Usuario añadido correctamente")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

            else:
                messagebox.showerror("Error", "No se pudo añadir al usuario")

        else:
            messagebox.showwarning("Advertencia", "Usuario y contraseña no pueden estar vacíos")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user=Usuario.authenticate(username,password) #método de clase

        if user:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.open_booking_screen(user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def open_booking_screen(self,user):

        # Cierra la ventana actual
        self.master.withdraw()  # Cierra la ventana de login

        # Abre la nueva ventana de reservas
        new_root = tk.Toplevel(self.master)  # Crea una nueva ventana raíz
        app = BookingScreen(new_root,user)  # Crea una instancia de la pantalla de reservas
        new_root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Maneja el cierre de la nueva ventana

    def on_closing(self):
        self.master.destroy()  # Destruye la ventana principal cuando se cierra la ventana de reservas


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
