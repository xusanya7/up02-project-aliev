"""Окно авторизации."""

import tkinter as tk
from tkinter import messagebox
from styles import COLOR_MAIN_BG, COLOR_ACCENT, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
import sqlite3

DB_PATH = "databases/db_variant_15.db"


class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.window = tk.Toplevel(root)
        self.window.title("Вход")
        self.window.geometry("300x200")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.window,
            text="Вход в систему",
            font=font(FONT_SIZE_HEADER, bold=True),
            bg=COLOR_MAIN_BG,
        ).pack(pady=10)

        tk.Label(self.window, text="Логин:", bg=COLOR_MAIN_BG).pack()
        self.login_var = tk.StringVar()
        tk.Entry(self.window, textvariable=self.login_var).pack()

        tk.Label(self.window, text="Пароль:", bg=COLOR_MAIN_BG).pack()
        self.password_var = tk.StringVar()
        tk.Entry(self.window, textvariable=self.password_var, show="*").pack()

        tk.Button(
            self.window,
            text="Войти",
            command=self.do_login,
            bg=COLOR_ACCENT,
            fg="white",
        ).pack(pady=10)

    def do_login(self):
        login = self.login_var.get().strip()
        password = self.password_var.get().strip()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, логин, роль FROM Пользователь "
            "WHERE логин = ? AND пароль = ?",
            (login, password),
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            return

        user = {"id": row[0], "login": row[1], "role": row[2]}
        self.window.destroy()
        self.on_success(user)
