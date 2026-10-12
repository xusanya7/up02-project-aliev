import tkinter as tk

root = tk.Tk()
root.title("Тест окна")
root.geometry("400x300")
tk.Label(root, text="Если видишь это — tkinter работает!",
         font=("Arial", 16)).pack(expand=True)

root.mainloop()