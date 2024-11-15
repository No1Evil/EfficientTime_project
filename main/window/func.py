import tkinter as tk
from tkinter import messagebox
import sqlite3

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


def laadi_ülesanded(listbox: tk.Listbox):
    """Laadi ülesanded andmebaasist"""
    listbox.delete(0, tk.END)
    for rida in c.execute("SELECT id, ülesanne, staatus FROM ülesanded"):
        ülesanne_tekst = rida[1] + (" ✔" if rida[2] == "tehtud" else "")
        ülesannete_loend.insert(tk.END, ülesanne_tekst)