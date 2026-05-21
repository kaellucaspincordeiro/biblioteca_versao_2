import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_autor(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)


    # --- Título da Tela ---
    tk.Label(container, text="Cadastro dos Autores", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 20))
    # --- Formulário de Cadastro ---
    tk.Label(container, text="Nome do(a) Autor(a):", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=(0, 8))
    ent_nome = tk.Entry(container, width=40)
    ent_nome.grid(row=2, column=0, pady=(0, 12))

    def salvar_autor():
        nome_autor = ent_nome.get()
        if nome_autor.strip():
            bd.db_cadastrar_autor(nome_autor)
            messagebox.showinfo("Sucesso", "Autor(a) cadastrado(a) com sucesso!")
            ent_nome.delete(0, tk.END)
            atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    tk.Button(container, text="Cadastrar Autores", command=salvar_autor, bg="green", fg="white").grid(row=3, column=0, pady=(0, 18))

    # --- Lista de Livros ---
    tk.Label(container, text="Autores Cadastrados:", font=("Arial", 10, "bold")).grid(row=4, column=0)
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")

    container.grid_rowconfigure(5, weight=1)
    container.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "autor"),
        show="headings",
        yscrollcommand=scroll.set
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("autor", text="Nome do Autor")

    tabela.column("id", width=50, anchor="center")
    tabela.column("autor", width=50, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=7, column=0, pady=10)
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():
        # Limpa a lista atual para recarregar
        for item in tabela.get_children():
            tabela.delete(item)
        
        autores = bd.db_listar_autores()

        for aut in autores:            
            tabela.insert("", "end", values=(aut[0],aut[1]))

    atualizar_lista()

    def deletar_autor():

        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um(a) autor(a) para excluir!")
            return

        valores = tabela.item(item_selecionado, "values")
        id_aut = valores[0]


        # Abre a mesma tela de cadastro, mas agora enviando o ID para modo edição
        if messagebox.askyesno("Confirmar", "Deseja excluir este(a) autor(a)?"):
            bd.db_deletar_autor(id_aut)
            atualizar_lista()

    def atualizar_autor():

        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um(a) autor(a) para atualizar!")
            return
            
        valores = tabela.item(item_selecionado, "values")
        id_aut = valores[0]
        nome_autor = valores[1]

        janela_autor = tk.Toplevel(container)
        janela_autor.title("Atualizar Autor(a)")
        janela_autor.geometry("350x200")
        janela_autor.grab_set()

        janela_autor.grid_columnconfigure(0, weight=1)

        tk.Label(janela_autor, text="Nome do(a) Autor(a):").grid(row=0, column=0, pady=5)
        ent_nome = tk.Entry(janela_autor, width=40)
        ent_nome.grid(row=1, column=0, pady=5)
        ent_nome.insert(0, nome_autor)

        def salvar_atualizacao():
                 
            nome = ent_nome.get().strip()

            if nome == "":
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            bd.db_atualizar_categoria(id_aut, nome)
            messagebox.showinfo("Sucesso", "Autor(a) atualizado(a) com sucesso!")

            janela_autor.destroy()
            atualizar_lista()

        tk.Button(
            janela_autor,
            text="Salvar Alterações",
            command=salvar_atualizacao,
            bg="blue",
            fg="white"
        ).grid(row=2, column=0, pady=20)

    atualizar_lista()

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_autor,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=40)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        command=atualizar_autor,
        bg="blue",
        fg="white",
    ).grid(row=0, column=1, padx=40)
