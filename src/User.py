import tkinter as tk
from tkinter import messagebox as msb
#from tkinter import ttk
import random
import time
import sqlite3
class User:
    def __init__(self, window):
        self.window = window
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.new_username  = tk.StringVar()
        self.new_password = tk.StringVar()
        self.set_widgets()

    def set_widgets(self):
        pass