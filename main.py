import tkinter as tk
from tkinter import messagebox as msb
#from tkinter import ttk
import random
import time
import sqlite3

if __name__=='__main__':
    root = tk.Tk()
    root.geometry('500x500+300+300')
    root.title("Login form")
    application= user(root)
    root.mainloop()


