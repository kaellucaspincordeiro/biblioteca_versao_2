import sqlite3
import tkinter as tk
from tkinter import messagebox 

def realizar_backup(db_origem, db_destino):

    conn_origem = None
    conn_destino = None

    try:
        conn_origem = sqlite3.connect(db_origem)
        conn_destino = sqlite3.connect(db_destino)
 
        # Executa o backup
        with conn_destino:
            conn_origem.backup(conn_destino)
        messagebox.showinfo("Sucesso", "Backup concluído com sucesso")
 
    except sqlite3.Error:
        messagebox.showerror("Erro", "Erro ao realizar backup")
    finally:
        if conn_origem:
            conn_origem.close()
        if conn_destino:
            conn_destino.close()

def montar_backup(root, abrir_backup):

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Sistema de Biblioteca Escolar")
    root.geometry("670x650")

    root.grid_columnconfigure(0, weight=1)

    frame_backup = tk.Frame(root)
    frame_backup.grid(row=0, column=0, pady=45)

    tk.Button(
        root,
        text="← Voltar ao Menu",
        command=abrir_backup,
        bg="#ccc"
    ).grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
    tk.Label(frame_backup, text="Nome da Origem:", font=("Arial", 10)).grid(row=1, column=0, pady=(0, 15))
    ent_origem = tk.Entry(frame_backup, width=30)
    ent_origem.grid(row=2, column=0, pady= (0, 20))

    tk.Label(frame_backup, text="Nome do Destino:", font=("Arial", 10)).grid(row=3, column=0, pady=(0, 15))
    ent_destino = tk.Entry(frame_backup, width=30)
    ent_destino.grid(row=4, column=0, pady= (0, 25))

    def verificar_backup():

        origem = ent_origem.get()
        destino = ent_destino.get()

        if origem == "":
            messagebox.showwarning("Aviso", "Informe um nome do banco da origem!")
            return
        
        if destino == "":
            messagebox.showwarning("Aviso", "Informe um nome do banco do destino!")
            return
        
        realizar_backup(origem, destino)

    tk.Button(frame_backup, command=verificar_backup ,text="Realizar Backup", bg="lightblue", fg="#000000").grid(row=5, column=0, pady=20)