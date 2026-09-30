import tkinter as tk

from view.main_window import MainWindow

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Circuit Schematic Toolbox")
    MainWindow(root)
    root.mainloop()