import tkinter as tk
from tkinter import messagebox
from Database.IDatabase import Database

# Default window settings
class window_settings:
    def _add_button(self, button_name: str, width: int, command: callable, pady=5):
        lisa_nupp = tk.Button(self.aken, text=button_name, width=width, command=command)
        lisa_nupp.pack(pady=pady)

    # Add inputs
    def _add_inputs(self):
        # Ülesanne sisend - input for the tasks
        self.ülesanne_sisend = tk.Entry(self.aken, width=40)
        self.ülesanne_sisend.pack(pady=10)

    # Add listbox
    def _add_listbox(self):
        self.ülesanne_loend = tk.Listbox(self.aken, width=40, height=15)
        self.ülesanne_loend.pack(pady=10)

# Main window of TO-DO application
class Window(window_settings):
    def __init__(self, title: str, database: Database):
        self.aken = tk.Tk()
        self.aken.title(title)
        self.database = database
        self._add_inputs()
        self._add_button("Lisa ülesanne", 20, self.lisa_ülesanne)
        self._add_button("Kustuta ülesanne", 20, self.kustuta_ülesanne)
        self._add_button("Märgi tehtuks", 20, self.märgi_tehtud)
        self._add_listbox()
        self.__laadi_ülesanded()
        self.__start()
    
    def __start(self):
        self.aken.mainloop()

    # Add new task
    def lisa_ülesanne(self):
        ülesanne = self.ülesanne_sisend.get().strip()
        if ülesanne:
            self.database.insert(ülesanne, False)
            self.__clear_input()
            self.__laadi_ülesanded()
        else:
            messagebox.showwarning("Viga", "Sisesta ülesande tekst")

    # Remove the task
    def kustuta_ülesanne(self):
        valitud_ülesanne = self.__get_selected_task_id()
        self.database.delete_data(valitud_ülesanne)
        self.__laadi_ülesanded()
    
    # Tick the task as done
    def märgi_tehtud(self):
        valitud_ülesanne = self.__get_selected_task_id()
        if valitud_ülesanne is None:
            return
        status = bool(self.database.get_status_value(valitud_ülesanne))
        self.database.update_status(valitud_ülesanne, not status)
        self.__laadi_ülesanded()

    # Load the tasks
    def __laadi_ülesanded(self):
        self.__clear_listbox()
        for row in self.database.select_all():
            ülesanne_tekst = row[1]
            if row[2]:
                ülesanne_tekst += "[✔]"
            self.ülesanne_loend.insert(tk.END, ülesanne_tekst)

    def __clear_listbox(self):
        self.ülesanne_loend.delete(0, tk.END)

    def __clear_input(self):
        self.ülesanne_sisend.delete(0, tk.END)

    def __get_selected_task_id(self):
        try:
            index = self.ülesanne_loend.curselection()[0] + 1
            return index
        except (tk.TclError, IndexError):
            messagebox.showwarning("Viga", "Vali ülesanne")
            return None