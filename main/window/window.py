import tkinter as tk
from tkinter import messagebox
from Database.sqlite import *

class Window:
    def __init__(self, title: str, database: Database_sqlite):
        self.aken = tk.Tk()
        self.aken.title(title)
        self.database = database
        self.__input__()
        self.add_button("Lisa ülesanne", 20, self.lisa_ülesanne)
        self.add_button("Kustuta ülesanne", 20, self.kustuta_ülesanne)
        self.add_button("Märgi tehtuks", 20, self.märgi_tehtud)
        self.__listbox__()
        self.laadi_ülesanded()
        self.aken.mainloop()

    # Add button
    def add_button(self, button_name: str, width: int, command: callable, pady=5):
        lisa_nupp = tk.Button(self.aken, text=button_name, width=width, command=command)
        lisa_nupp.pack(pady=pady)

    # Add inputs
    def __input__(self):
        # Ülesanne sisend - input for the tasks
        self.ülesanne_sisend = tk.Entry(self.aken, width=40)
        self.ülesanne_sisend.pack(pady=10)

    # Add listbox
    def __listbox__(self):
        self.ülesanne_loend = tk.Listbox(self.aken, width=40, height=15)
        self.ülesanne_loend.pack(pady=10)

    # Add new task
    def lisa_ülesanne(self):
        ülesanne = self.ülesanne_sisend.get().strip()
        if ülesanne:
            self.database.insert("ülesanne", "staatus", ülesanne, False)
            self.clear_input()
            self.laadi_ülesanded()
        else:
            messagebox.showwarning("Viga", "Sisesta ülesande tekst")

    # Load the tasks
    def laadi_ülesanded(self):
        self.clear_listbox()
        for row in self.database.select_all():
            ülesanne_tekst = row[1]
            if row[2]:
                ülesanne_tekst += "[✔]"
            self.ülesanne_loend.insert(tk.END, ülesanne_tekst)

    # Remove the task
    def kustuta_ülesanne(self):
        valitud_ülesanne = self.get_cursor_taskId_by_id()
        self.database.delete(valitud_ülesanne)
        self.laadi_ülesanded()

    def clear_listbox(self):
        self.ülesanne_loend.delete(0, tk.END)

    def clear_input(self):
        self.ülesanne_sisend.delete(0, tk.END)

    # Tick the task as done
    def märgi_tehtud(self):
        valitud_ülesanne = self.get_cursor_taskId_by_id()
        staatus = bool(self.database.get_value("staatus", valitud_ülesanne))
        self.database.update_value("staatus", "id", staatus, valitud_ülesanne)
        self.laadi_ülesanded()

    def get_cursor_taskId_by_id(self):
        try:
            index = self.ülesanne_loend.curselection()[0]
            valitud_ülesanne = self.database.select("id").fetchall()[index][0]
            return valitud_ülesanne
        except (tk.TclError, IndexError):
            messagebox.showwarning("Viga", "Vali ülesanne")
            return None