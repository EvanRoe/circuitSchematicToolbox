import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Circuit Schematic Toolbox")

main = ttk.Frame(root)
main.pack(fill="both", expand=True)

canvas = tk.Canvas(main, width=600, height=600, bg="white")
canvas.pack(side="left", fill="both", expand=True)

side = ttk.Frame(main, width=220)
side.pack(side="right", fill="y")
side.pack_propagate(False)

root.mainloop()
