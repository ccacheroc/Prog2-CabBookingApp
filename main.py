import tkinter as tk
#para no tener que poner tk.messagebox, o tk.ttk
from tkinter import messagebox as msb,ttk

import random
import time

from ui.LoginScreen import LoginScreen
def main():
    root = tk.Tk()
    app=LoginScreen(root)
    root.title("Sistema de reserva de taxis")
    root.mainloop()


if __name__ == main():
    main()
