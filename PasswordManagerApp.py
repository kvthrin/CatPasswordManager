import tkinter as tk
import os
import json
from tkinter import messagebox
from tkinter import simpledialog


def init_ui(master):
    label_title = tk.Label(text="CAT (PASSWORD) MANAGER", font=("Arial", 20))
    label_title.configure(background='#FFC0CB')
    label_title.pack(pady=20)

    if os.path.isfile('passwords.json'):
        label_start = tk.Label(text="Forgot your cats' name? Check on it now", font=("Arial", 20))
        label_start.configure(background='#FFC0CB')
        label_start.pack()
    else:
        label_new = tk.Label(text="Never forget your cats names now \n Enter a secure Password:", font=("Arial", 20))
        label_new.configure(background='#FFC0CB')
        entry_box = tk.Entry(width=20, font=("Arial", 20))
        button_create = tk.Button(master, text="Create Database", font=("Arial", 20),command= lambda : createDatabase(entry_box.get()))
        label_new.pack(pady=5)
        entry_box.pack()
        button_create.pack(pady = 10)


def createDatabase(password):
    data = {'password': password}  # Example data to write to JSON file
    database = open('passwords.json', 'x')
    json.dump(data, database)

class PasswordManagerUI:
    def __init__(self, master):
        self.label_title = None
        self.frame = None
        self.master = master
        self.master.title("Password Manager")

        init_ui(master)


def main():
    # create initial window
    window = tk.Tk()
    app = PasswordManagerUI(window)
    window.geometry("900x600")
    window.maxsize(900, 600)
    window.minsize(900, 600)
    window.config(background="#FFC0CB")
    window.mainloop()


if __name__ == "__main__":
    main()
