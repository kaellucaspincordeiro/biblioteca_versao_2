import tkinter as tk
from Categoria.tela_categoria import montar_tela_categoria
from Editora.tela_editora import montar_tela_editora
from Autor.tela_autor import montar_tela_autor
from Cliente.tela_cliente import montar_tela_cliente
from Livro.tela_livro import montar_tela_livro
from Emprestimo.tela_emprestimo import montar_tela_emprestimo
from Multa.tela_multa import montar_tela_multa
from User.login import montar_login

import backup


def montar_menu_principal():
    # Limpa a tela para voltar ao menu
    for widget in root.winfo_children():
        widget.destroy()

    barra_menu = tk.Menu(root)
    menu_backup = tk.Menu(barra_menu, tearoff=0)
    menu_backup.add_command(label="Realizar Backup", command=lambda: backup.montar_backup(root, montar_menu_principal))
    barra_menu.add_cascade(label="Backup", menu=menu_backup)
    root.config(menu=barra_menu)

    menu_sair = tk.Menu(barra_menu, tearoff=0)
    menu_sair.add_command(label="Sair", command=lambda: montar_login(root, montar_menu_principal))
    barra_menu.add_cascade(label="Logoff", menu=menu_sair)
    root.config(menu=barra_menu)

    root.grid_columnconfigure(0, weight=1)

    tk.Label(root, text="Bem-vindo ao Sistema", font=("Arial", 16)).grid(row=0, column=0, pady=20)

    tk.Button(root, text="Abrir Cadastro de Categorias", 
              command=lambda: montar_tela_categoria(root, montar_menu_principal), 
              width=30, height=2).grid(row=1, column=0, pady=10)

    tk.Button(root, text="Abrir Cadastro das Editoras", 
              command=lambda: montar_tela_editora(root, montar_menu_principal), 
              width=30, height=2).grid(row=2, column=0, pady=10)
    
    tk.Button(root, text="Abrir Cadastro dos Autores", 
              command=lambda: montar_tela_autor(root, montar_menu_principal), 
              width=30, height=2).grid(row=3, column=0, pady=10)

    tk.Button(root, text="Abrir Cadastro dos Clientes", 
              command=lambda: montar_tela_cliente(root, montar_menu_principal), 
              width=30, height=2).grid(row=4, column=0, pady=10)
        
    tk.Button(root, text="Abrir Cadastro dos Livros", 
              command=lambda: montar_tela_livro(root, montar_menu_principal), 
              width=30, height=2).grid(row=5, column=0, pady=10)
             
    tk.Button(root, text="Abrir Cadastro dos Empréstimos", 
              command=lambda: montar_tela_emprestimo(root, montar_menu_principal), 
              width=30, height=2).grid(row=6, column=0, pady=10)
              
    tk.Button(root, text="Abrir Cadastro das Multas", 
              command=lambda: montar_tela_multa(root, montar_menu_principal), 
              width=30, height=2).grid(row=7, column=0, pady=10)
    
    tk.Button(root, text="Sair", 
              command=root.quit,
              fg="red", 
              width=30, height=2).grid(row=8, column=0, pady=10)
    

root = tk.Tk()
root.title("Sistema de Biblioteca Escolar")
root.geometry("670x620")

montar_login(root, montar_menu_principal)

root.mainloop()
