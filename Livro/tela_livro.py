import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_livro(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(4, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    frame_livro = tk.Frame(container)
    frame_livro.grid(row=1, column=0, pady=(5,5))

    # --- Título da Tela ---
    tk.Label(frame_livro, text="Cadastro dos Livros", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 10))
    # --- Formulário de Cadastro ---
    tk.Label(frame_livro, text="Nome do Livro:", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=(0, 2))
    ent_nome = tk.Entry(frame_livro, width=40)
    ent_nome.grid(row=2, column=0, pady=(0, 5))
    tk.Label(frame_livro, text="Status:", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=(0, 2))
    ent_status = tk.Entry(frame_livro, width=40)
    ent_status.grid(row=4, column=0, pady=(0, 5))

    def obter_editoras():
        conn = bd.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_editora, nome_editora FROM editora")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    tk.Label(frame_livro, text="Editora:", font=("Arial", 10, "bold")).grid(row=5, column=0, pady=(0, 2))

    # Buscamos as categorias do banco
    lista_editoras = obter_editoras() 

    mapeamento_editora = {nomes_editoras: id_editora for id_editora, nomes_editoras in lista_editoras}
   
    combo_editora = ttk.Combobox(frame_livro, values=list(mapeamento_editora.keys()), width=37, state="readonly")
    combo_editora.grid(row=6, column=0, pady=(0, 5))


    def obter_id_editora():
        nome_selecionado = combo_editora.get()

        if nome_selecionado:                
            return mapeamento_editora[nome_selecionado]
        
        return None

    def obter_categorias():
        conn = bd.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria, nome_categoria FROM categoria")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    tk.Label(frame_livro, text="Categoria:", font=("Arial", 10, "bold")).grid(row=7, column=0, pady=(0,2))

    lista_categorias = obter_categorias() 
   
    mapeamento_categoria = {nomes_categorias: id_categoria for id_categoria, nomes_categorias in lista_categorias}

    combo_categoria = ttk.Combobox(frame_livro, values=list(mapeamento_categoria.keys()), width=37, state="readonly")
    combo_categoria.grid(row=8, column=0, pady=(0, 5))


    def obter_id_categoria():
        nome_selecionado = combo_categoria.get()
        if nome_selecionado:
            return mapeamento_categoria[nome_selecionado]
        
        return None

    def obter_autores():
        conn = bd.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_autor, nome_autor FROM autor")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    tk.Label(frame_livro, text="Autor(a):", font=("Arial", 10, "bold")).grid(row=9, column=0, pady=(0,2))

    lista_autores = obter_autores() 
   
    mapeamento_autor = {nomes_autores: id_autor for id_autor, nomes_autores in lista_autores}

    combo_autor = ttk.Combobox(frame_livro, values=list(mapeamento_autor.keys()), width=37, state="readonly")
    combo_autor.grid(row=10, column=0, pady=(0, 6))


    def obter_id_autor():
        nome_selecionado = combo_autor.get()
        if nome_selecionado:
            return mapeamento_autor[nome_selecionado]
        
        return None

    def salvar_livro():
        nome_livro = ent_nome.get()
        status = ent_status.get()
        editora = obter_id_editora()
        categoria = obter_id_categoria()
        autor = obter_id_autor()

        condicao_livro = (nome_livro.strip() 
                            and status.strip() 
                            and editora is not None 
                            and categoria is not None
                            and autor is not None
                           )
        

        if condicao_livro:
            bd.db_cadastrar_livro(nome_livro, status, editora, categoria, autor)
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            ent_nome.delete(0, tk.END)
            ent_status.delete(0, tk.END)
            combo_editora.set("")
            combo_categoria.set("")
            combo_autor.set("")
            atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    tk.Button(frame_livro, text="Cadastrar livro", command=salvar_livro, bg="green", fg="white").grid(row=11, column=0, pady=(4,5))

    # --- Lista de Livros ---
    tk.Label(frame_livro, text="Livros Cadastrados:", font=("Arial", 10, "bold")).grid(row=12, column=0, pady=(4, 5))
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=4, column=0, pady=(0,5), padx=20, sticky="nsew")

    container.grid_rowconfigure(4, weight=1)

    frame_tabela.grid_columnconfigure(0, weight=1)
    frame_tabela.grid_rowconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "livro", "status", "editora", "categoria", "autor"),
        show="headings",
        yscrollcommand=scroll.set,
        height= 4
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("livro", text="Nome do Livro")
    tabela.heading("status", text="Status")
    tabela.heading("editora", text="ID Editora")
    tabela.heading("categoria", text="ID Categoria")
    tabela.heading("autor", text="ID Autor")

    tabela.column("id", width=50, anchor="center")
    tabela.column("livro", width=50, anchor="center")
    tabela.column("status", width=50, anchor="center")
    tabela.column("editora", width=50, anchor="center")
    tabela.column("categoria", width=50, anchor="center")
    tabela.column("autor", width=50, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=5, column=0, pady=(5, 10))
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        livros = bd.db_listar_livros()

        for liv in livros:           
            tabela.insert("", "end", values=(liv[0],liv[1],liv[2],liv[3],liv[4],liv[5]))

    atualizar_lista()

    def deletar_livro():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um livro para excluir!")
            return

        valores = tabela.item(item_selecionado, "values")
        id_liv = valores[0]


        # Abre a mesma tela de cadastro, mas agora enviando o ID para modo edição
        if messagebox.askyesno("Confirmar", "Deseja excluir este livro?"):
            bd.db_deletar_livro(id_liv)
            atualizar_lista()


    def atualizar_livro():

        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um livro para atualizar!")
            return
            
        valores = tabela.item(item_selecionado, "values")
        id_liv = valores[0]
        nome_livro = valores[1]
        status = valores[2]
        editora = valores[3]
        categoria = valores[4]
        autor = valores[5]

        map_editora = {id_editora: nome_editora for nome_editora, id_editora in mapeamento_editora.items()}
        map_categoria = {id_categoria: nome_categoria for nome_categoria, id_categoria in mapeamento_categoria.items()}
        map_autor = {id_autor: nome_autor for nome_autor, id_autor in mapeamento_autor.items()}

        editora = map_editora[int(editora)]
        categoria = map_categoria[int(categoria)]
        autor = map_autor[int(autor)]

        janela_livro = tk.Toplevel(container)
        janela_livro.title("Atualizar Livro")
        janela_livro.geometry("350x500")
        janela_livro.grab_set()
        janela_livro.grid_columnconfigure(0, weight=1)

        tk.Label(janela_livro, text="Nome do Livro:").grid(row=0, column=0, pady=5)
        ent_nome = tk.Entry(janela_livro, width=40)
        ent_nome.grid(row=1, column=0, pady=5)
        ent_nome.insert(0, nome_livro)

        tk.Label(janela_livro, text="Status:").grid(row=2, column=0, pady=5)
        ent_status = tk.Entry(janela_livro, width=40)
        ent_status.grid(row=3, column=0, pady=5)
        ent_status.insert(0, status)

        tk.Label(janela_livro, text="Editora:").grid(row=4, column=0, pady=5)
        combo_editora = ttk.Combobox(
        janela_livro,
        values=list(mapeamento_editora.keys()),
        width=37,
        state="readonly"
        )
        combo_editora.grid(row=5, column=0, pady=5)
        combo_editora.set(editora)

        tk.Label(janela_livro, text="Categoria:").grid(row=6, column=0, pady=5)
        combo_categoria = ttk.Combobox(
        janela_livro,
        values=list(mapeamento_categoria.keys()),
        width=37,
        state="readonly"
        )
        combo_categoria.grid(row=7, column=0, pady=5)
        combo_categoria.set(categoria)
        
        tk.Label(janela_livro, text="Autor:").grid(row=8, column=0, pady=5)
        combo_autor = ttk.Combobox(
        janela_livro,
        values=list(mapeamento_autor.keys()),
        width=37,
        state="readonly"
        )
        combo_autor.grid(row=9, column=0, pady=5)
        combo_autor.set(autor)

        def salvar_atualizacao():
            nome = ent_nome.get().strip()
            status = ent_status.get().strip()
            editora = combo_editora.get()
            categoria = combo_categoria.get()
            autor = combo_autor.get()

            condicao_livro = (nome == ""
                            and status == ""
                            and editora == ""
                            and categoria == "" 
                            and autor == "" 
                            )

            if condicao_livro:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            id_editora = mapeamento_editora[editora]
            id_categoria = mapeamento_categoria[categoria]
            id_autor = mapeamento_autor[autor]

            bd.db_atualizar_livro(
                id_liv,
                nome,
                status,
                id_editora,
                id_categoria,
                id_autor
            )

            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            janela_livro.destroy()
            atualizar_lista()

        tk.Button(
            janela_livro,
            text="Salvar Alterações",
            command=salvar_atualizacao,
            bg="blue",
            fg="white"
        ).grid(row=10, column=0, pady=15)

    atualizar_lista()

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_livro,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        command=atualizar_livro,
        bg="blue",
        fg="white",
    ).grid(row=0, column=1, padx=10)
        