import tkinter as tk
import main_menu_class

root = tk.Tk()
root.geometry('1366x768')
root.title('Cítim potkana')
root.resizable(False, False)

menu = main_menu_class.MainMenu(root)

root.mainloop()