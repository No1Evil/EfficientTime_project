import tkinter as tk
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

    def add_button(self, button_name: str, width: int, command: callable):
        lisa_nupp = tk.Button(self.aken, text=button_name, width=width, command=command)
        lisa_nupp.pack(pady=5)
    def __input__(self):
        self.ülesanne_sisend = tk.Entry(self.aken, width=40)
        self.ülesanne_sisend.pack(pady=10)
    def __listbox__(self):
        self.ülesanne_loend = tk.Listbox(self.aken, width=40, height=15)
        self.ülesanne_loend.pack(pady=10)
    
    def lisa_ülesanne(self):
        ülesanne = self.ülesanne_sisend.get().strip()
        if ülesanne:
            self.database.c.execute(f"INSERT INTO {self.database.table_name} (ülesanne, staatus) VALUES (?, ?)", (ülesanne, "pooleli"))
            self.database.conn.commit()
            self.ülesanne_sisend.delete(0, tk.END)
            self.laadi_ülesanded()
        else:
            messagebox.showwarning("Viga", "Sisesta ülesande tekst")

    def laadi_ülesanded(self):
        self.ülesanne_loend.delete(0, tk.END)
        for row in self.database.c.execute(f"SELECT * FROM {self.database.table_name}"):
            ülesanne_tekst = row[1] + (" ✔" if row[2] == True else "")
            self.ülesanne_loend.insert(tk.END, ülesanne_tekst)
    
    def kustuta_ülesanne(self):
        try:
            valitud_index = self.ülesanne_loend.curselection()[0]
            valitud_ülesanne = self.database.c.execute(f"SELECT id FROM {self.database.table_name}").fetchall()[valitud_index]
            ülesanne_id = valitud_ülesanne[0]
            self.database.c.execute(f"DELETE FROM {self.database.table_name} WHERE id = ?", (ülesanne_id,))
            self.database.conn.commit()
            self.laadi_ülesanded()
        except (tk.TclError, IndexError):
            messagebox.showwarning("Viga", "Vali ülesanne kustutamiseks")

    def märgi_tehtud(self):
        try:
            valitud_ülesanne = self.ülesanne_loend.get(self.ülesanne_loend.curselection())
            ülesanne_tekst = valitud_ülesanne.replace(" ✔", "")
            self.database.c.execute("UPDATE ülesanded SET staatus = TRUE WHERE ülesanne = ?", (ülesanne_tekst,))
            self.database.conn.commit()
            self.laadi_ülesanded()
        except tk.TclError:
            messagebox.showwarning("Viga", "Vali ülesanne, mida märkida tehtuks")