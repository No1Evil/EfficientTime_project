from tkinter import *
from tkinter import ttk

root = Tk()
root.title("My GUI App")
frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Hello, World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=5, row=0)
root.mainloop()