import tkinter as tk
root = tk.Tk()
root.title("Тест")
root.geometry("300x200")
tk.Label(root, text="Работает!").pack(expand=True)
root.mainloop()