import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_login(root, abrir_biblioteca):

    for widget in root.winfo_children():
        widget.destroy()

    def verificar_login():

        login = ent_login.get().strip()
        senha = ent_senha.get().strip()

        if login == "" and senha == "":
            conn.close()
            return
    
        conn = bd.conectar()
        cursor = conn.cursor() 
        cursor.execute("SELECT nome_user FROM user WHERE login = ? AND senha = ?", (login, senha))

        usuario_login = cursor.fetchone()
        conn.close()

        if usuario_login:
            messagebox.showinfo("Sucesso", "Logado com sucesso!")
            abrir_biblioteca()
            
        else:
            messagebox.showerror("Erro", "Login ou Senha Incorreta! Digite novamente")
            ent_login.delete(0, tk.END)
            ent_senha.delete(0, tk.END)
            ent_login.focus()

    root.title("Sistema de Biblioteca Escolar")
    root.geometry("670x650")

    root.grid_columnconfigure(0, weight=1)

    frame_login = tk.Frame(root)
    frame_login.grid(row=0, column=0, pady=45)
        
    tk.Label(frame_login, text="Login:", font=("Arial", 10)).grid(row=0, column=0, pady=(0, 15))
    ent_login = tk.Entry(frame_login, width=30)
    ent_login.grid(row=1, column=0, pady= (0, 20))

    tk.Label(frame_login, text="Senha:", font=("Arial", 10)).grid(row=2, column=0, pady=(0, 15))
    ent_senha = tk.Entry(frame_login, width=30, show="*")
    ent_senha.grid(row=3, column=0, pady= (0, 25))
        
    tk.Button(frame_login, command=verificar_login ,text="Entrar", bg="green", fg="#ffffff").grid(row=4, column=0, pady=20)

