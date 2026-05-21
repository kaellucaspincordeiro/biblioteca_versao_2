import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_categoria(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # --- Título da Tela ---
    tk.Label(container, text="Cadastro de Categorias", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 20))
    # --- Formulário de Cadastro ---
    tk.Label(container, text="Nome da Categoria:", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=(0, 8))
    ent_nome = tk.Entry(container, width=40)
    ent_nome.grid(row=2, column=0, pady=(0, 12))

    def salvar_categoria():
        nome_categoria = ent_nome.get()
        if nome_categoria.strip():
            bd.db_cadastrar_categoria(nome_categoria)
            messagebox.showinfo("Sucesso", "Categoria cadastrada com sucesso!")
            ent_nome.delete(0, tk.END)
            atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
    

    tk.Button(container, text="Cadastrar Categoria", command=salvar_categoria, bg="green", fg="white").grid(row=3, column=0, pady=(0, 18))

    # --- Lista de Livros ---
    tk.Label(container, text="Categorias Cadastradas:", font=("Arial", 10, "bold")).grid(row=4, column=0)
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")

    container.grid_rowconfigure(5, weight=1)
    container.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "categoria"),
        show="headings",
        yscrollcommand=scroll.set
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("categoria", text="Nome da Categoira")

    tabela.column("id", width=50, anchor="center")
    tabela.column("categoria", width=50, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=7, column=0, pady=10)
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():

        for item in tabela.get_children():
            tabela.delete(item)

        categorias = bd.db_listar_categorias()

        for cat in categorias:           
            tabela.insert("", "end", values=(cat[0],cat[1]))

    atualizar_lista()

    def deletar_categoria():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma categoria para excluir!")
            return

        valores = tabela.item(item_selecionado, "values")
        id_c = valores[0]


        # Abre a mesma tela de cadastro, mas agora enviando o ID para modo edição
        if messagebox.askyesno("Confirmar", "Deseja excluir esta categoria?"):
            bd.db_deletar_categoria(id_c)
            atualizar_lista()

    def atualizar_categoria():
            
            item_selecionado = tabela.selection()
        
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione uma categoria para atualizar!")
                return
            
            valores = tabela.item(item_selecionado, "values")
            id_c = valores[0]
            nome_categoria = valores[1]

            janela_categoria = tk.Toplevel(container)
            janela_categoria.title("Atualizar Categoria")
            janela_categoria.geometry("350x200")
            janela_categoria.grab_set()

            janela_categoria.grid_columnconfigure(0, weight=1)

            tk.Label(janela_categoria, text="Nome da Categoria:").grid(row=0, column=0, pady=5)
            ent_nome = tk.Entry(janela_categoria, width=40)
            ent_nome.grid(row=1, column=0, pady=5)
            ent_nome.insert(0, nome_categoria)

            def salvar_atualizacao():
                 
                nome = ent_nome.get().strip()

                if nome == "":
                    messagebox.showwarning("Aviso", "Preencha todos os campos!")
                    return

                bd.db_atualizar_categoria(id_c, nome)
                messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")

                janela_categoria.destroy()
                atualizar_lista()

            tk.Button(
                janela_categoria,
                text="Salvar Alterações",
                command=salvar_atualizacao,
                bg="blue",
                fg="white"
            ).grid(row=2, column=0, pady=20)

    atualizar_lista()

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_categoria,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=40)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        command=atualizar_categoria,
        bg="blue",
        fg="white",
    ).grid(row=0, column=1, padx=40)
