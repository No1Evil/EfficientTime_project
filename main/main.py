import tkinter as tk
from tkinter import messagebox
import sqlite3

# Loo või ühenda andmebaasiga
conn = sqlite3.connect("ülesanded.db")
c = conn.cursor()

# Loo tabel, kui see veel ei eksisteeri
c.execute('''CREATE TABLE IF NOT EXISTS ülesanded (
                id INTEGER PRIMARY KEY,
                ülesanne TEXT NOT NULL,
                staatus TEXT NOT NULL
            )''')
conn.commit()

# Funktsioonid
def laadi_ülesanded():
    """Laadi ülesanded andmebaasist"""
    ülesannete_loend.delete(0, tk.END)
    for rida in c.execute("SELECT id, ülesanne, staatus FROM ülesanded"):
        ülesanne_tekst = rida[1] + (" ✔" if rida[2] == "tehtud" else "")
        ülesannete_loend.insert(tk.END, ülesanne_tekst)

def lisa_ülesanne():
    """Lisa uus ülesanne"""
    ülesanne = ülesanne_sisend.get().strip()
    if ülesanne:
        c.execute("INSERT INTO ülesanded (ülesanne, staatus) VALUES (?, ?)", (ülesanne, "pooleli"))
        conn.commit()
        ülesanne_sisend.delete(0, tk.END)
        laadi_ülesanded()
    else:
        messagebox.showwarning("Viga", "Sisesta ülesande tekst")

def kustuta_ülesanne():
    """Kustuta valitud ülesanne"""
    try:
        valitud_ülesanne = ülesannete_loend.get(ülesannete_loend.curselection())
        ülesanne_tekst = valitud_ülesanne.replace(" ✔", "")
        c.execute("DELETE FROM ülesanded WHERE ülesanne = ?", (ülesanne_tekst,))
        conn.commit()
        laadi_ülesanded()
    except tk.TclError:
        messagebox.showwarning("Viga", "Vali ülesanne kustutamiseks")

def märgi_tehtud():
    """Märgi ülesanne tehtuks"""
    try:
        valitud_ülesanne = ülesannete_loend.get(ülesannete_loend.curselection())
        ülesanne_tekst = valitud_ülesanne.replace(" ✔", "")
        c.execute("UPDATE ülesanded SET staatus = 'tehtud' WHERE ülesanne = ?", (ülesanne_tekst,))
        conn.commit()
        laadi_ülesanded()
    except tk.TclError:
        messagebox.showwarning("Viga", "Vali ülesanne, mida märkida tehtuks")

# Liides
aken = tk.Tk()
aken.title("Ülesannete nimekiri")

# Sisestusväli uue ülesande jaoks
ülesanne_sisend = tk.Entry(aken, width=40)
ülesanne_sisend.pack(pady=10)

# Nupud
lisa_nupp = tk.Button(aken, text="Lisa ülesanne", width=20, command=lisa_ülesanne)
lisa_nupp.pack(pady=5)

kustuta_nupp = tk.Button(aken, text="Kustuta ülesanne", width=20, command=kustuta_ülesanne)
kustuta_nupp.pack(pady=5)

tehtud_nupp = tk.Button(aken, text="Märgi tehtuks", width=20, command=märgi_tehtud)
tehtud_nupp.pack(pady=5)

# Ülesannete loend
ülesannete_loend = tk.Listbox(aken, width=50, height=15)
ülesannete_loend.pack(pady=10)

# Laadi ülesanded käivitamisel
laadi_ülesanded()

# Käivita rakendus
aken.mainloop()

# Sulge andmebaasi ühendus
conn.close()
