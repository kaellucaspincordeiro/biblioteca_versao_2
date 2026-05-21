import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_emprestimo(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(4, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    frame_emprestimo = tk.Frame(container)
    frame_emprestimo.grid(row=1, column=0, pady=(5,5))

    # --- Título da Tela ---
    tk.Label(frame_emprestimo, text="Cadastro dos Empréstimos", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 10))
    # --- Formulário de Cadastro ---
    tk.Label(frame_emprestimo, text="Nome do Empréstimo:", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=(0, 2))
    ent_nome = tk.Entry(frame_emprestimo, width=40)
    ent_nome.grid(row=2, column=0, pady=(0,5))

    def obter_clientes():
        conn = bd.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nome_cliente FROM cliente")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    tk.Label(frame_emprestimo, text="Cliente:", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=(0,2))

    # Buscamos as categorias do banco
    lista_clientes = obter_clientes() 

    mapeamento_cliente = {nomes_clientes: id_cliente for id_cliente, nomes_clientes in lista_clientes}
   
    combo_cliente = ttk.Combobox(frame_emprestimo, values=list(mapeamento_cliente.keys()), width=37, state="readonly")
    combo_cliente.grid(row=4, column=0, pady=(0,5))


    def obter_id_cliente():
        nome_selecionado = combo_cliente.get()

        if nome_selecionado:                
            return mapeamento_cliente[nome_selecionado]
        
        return None
    
    def obter_livros():
        conn = bd.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_livro, nome_livro FROM livro")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    tk.Label(frame_emprestimo, text="Livro:", font=("Arial", 10, "bold")).grid(row=5, column=0, pady=(0,2))

    # Buscamos as categorias do banco
    lista_livros = obter_livros() 

    mapeamento_livro = {nomes_livros: id_livro for id_livro, nomes_livros in lista_livros}
   
    combo_livro = ttk.Combobox(frame_emprestimo, values=list(mapeamento_livro.keys()), width=37, state="readonly")
    combo_livro.grid(row=6, column=0, pady=(0,5))


    def obter_id_livro():
        nome_selecionado = combo_livro.get()

        if nome_selecionado:                
            return mapeamento_livro[nome_selecionado]
        
        return None

    tk.Label(frame_emprestimo, text="Data do Empréstimo:", font=("Arial", 10, "bold")).grid(row=7, column=0, pady=(5, 2))
    ent_emprestimo = tk.Entry(frame_emprestimo, width=40)
    ent_emprestimo.grid(row=8, column=0, pady=(0,5))

    tk.Label(frame_emprestimo, text="Data da Devolução:", font=("Arial", 10, "bold")).grid(row=9, column=0, pady=(5, 2))
    ent_devolucao = tk.Entry(frame_emprestimo, width=40)
    ent_devolucao.grid(row=10, column=0, pady=(0,5))

    def salvar_emprestimo():
        nome_emprestimo = ent_nome.get()
        cliente = obter_id_cliente()
        livro = obter_id_livro()
        data_emprestimo = ent_emprestimo.get()
        data_devolucao = ent_devolucao.get()

        def verificar_livro():
            if livro == "disponível":
                messagebox.showinfo("Informar", "Livro disponível")
            else:
                messagebox.showwarning("Atenção", "O livro está emprestado")


        def validar_emprestimo():

            if data_devolucao < data_emprestimo:
                messagebox.showwarning("Atenção", "O empréstimo não será realizado!")

            else:
                messagebox.showinfo("Informar", "O empréstimo será realizado!")

                condicao_emprestimo = (nome_emprestimo.strip() 
                                       and cliente is not None 
                                       and livro is not None
                                       and data_emprestimo.strip() 
                                       and data_devolucao.strip()
                                      )
        
                if condicao_emprestimo:
                    bd.db_cadastrar_emprestimo(nome_emprestimo, cliente, livro, data_emprestimo, data_devolucao)
                    messagebox.showinfo("Sucesso", "Empréstimo cadastrado com sucesso!")
                    ent_nome.delete(0, tk.END)
                    combo_cliente.set("")
                    combo_livro.set("")
                    ent_emprestimo.delete(0, tk.END)
                    ent_devolucao.delete(0, tk.END)
                    atualizar_lista()
                else:
                    messagebox.showwarning("Aviso", "Preencha todos os campos!")
        validar_emprestimo()
        verificar_livro()

    tk.Button(frame_emprestimo, text="Cadastrar empréstimo", command=salvar_emprestimo, bg="green", fg="white").grid(row=11, column=0, pady=(4,5))

    # --- Lista de Livros ---
    tk.Label(frame_emprestimo, text="Empréstimos Cadastrados:", font=("Arial", 10, "bold")).grid(row=12, column=0, pady=(4, 5))
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=4, column=0, pady=(0,5), padx=20, sticky="nsew")

    container.grid_rowconfigure(4, weight=1)

    frame_tabela.grid_columnconfigure(0, weight=1)
    frame_tabela.grid_rowconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "nome", "cliente", "livro", "emprestimo", "devolucao"),
        show="headings",
        yscrollcommand=scroll.set,
        height= 4
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome do Empréstimo")
    tabela.heading("cliente", text="ID Cliente")
    tabela.heading("livro", text="ID Livro")
    tabela.heading("emprestimo", text="Data do Empréstimo")
    tabela.heading("devolucao", text="Data da Devolução")

    tabela.column("id", width=30, anchor="center")
    tabela.column("nome", width=30, anchor="center")
    tabela.column("cliente", width=30, anchor="center")
    tabela.column("livro", width=30, anchor="center")
    tabela.column("emprestimo", width=30, anchor="center")
    tabela.column("devolucao", width=30, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=5, column=0, pady=(5, 10))
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        emprestimos = bd.db_listar_emprestimos()

        for emp in emprestimos:           
            tabela.insert("", "end", values=(emp[0],emp[1],emp[2],emp[3],emp[4],emp[5]))

    atualizar_lista()

    def deletar_emprestimo():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para excluir!")
            return

        valores = tabela.item(item_selecionado, "values")
        id_emp = valores[0]


        # Abre a mesma tela de cadastro, mas agora enviando o ID para modo edição
        if messagebox.askyesno("Confirmar", "Deseja excluir este empréstimo?"):
            bd.db_deletar_emprestimo(id_emp)
            atualizar_lista()

    def atualizar_emprestimo():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um emprestimo para atualizar!")
            return
            
        valores = tabela.item(item_selecionado, "values")
        id_emp = valores[0]
        nome_emprestimo = valores[1]
        cliente = valores[2]
        livro = valores[3]
        emprestimo = valores[4]
        devolucao = valores[5]

        map_cliente = {id_cliente: nome_cliente for nome_cliente, id_cliente in mapeamento_cliente.items()}
        map_livro = {id_livro: nome_livro for nome_livro, id_livro in mapeamento_livro.items()}

        cliente = map_cliente[int(cliente)]
        livro = map_livro[int(livro)]

        janela_emprestimo = tk.Toplevel(container)
        janela_emprestimo.title("Atualizar Emprestimo")
        janela_emprestimo.geometry("350x500")
        janela_emprestimo.grab_set()
        janela_emprestimo.grid_columnconfigure(0, weight=1)

        tk.Label(janela_emprestimo, text="Nome do Empréstimo:").grid(row=0, column=0, pady=5)
        ent_nome = tk.Entry(janela_emprestimo, width=40)
        ent_nome.grid(row=1, column=0, pady=5)
        ent_nome.insert(0, nome_emprestimo)

        tk.Label(janela_emprestimo, text="Cliente:").grid(row=2, column=0, pady=5)
        combo_cliente = ttk.Combobox(
        janela_emprestimo,
        values=list(mapeamento_cliente.keys()),
        width=37,
        state="readonly"
        )
        combo_cliente.grid(row=3, column=0, pady=5)
        combo_cliente.set(cliente)

        tk.Label(janela_emprestimo, text="Livro:").grid(row=4, column=0, pady=5)
        combo_livro = ttk.Combobox(
        janela_emprestimo,
        values=list(mapeamento_livro.keys()),
        width=37,
        state="readonly"
        )
        combo_livro.grid(row=5, column=0, pady=5)
        combo_livro.set(livro)

        tk.Label(janela_emprestimo, text="Data do Empréstimo:").grid(row=6, column=0, pady=5)
        ent_emprestimo = tk.Entry(janela_emprestimo, width=40)
        ent_emprestimo.grid(row=7, column=0, pady=5)
        ent_emprestimo.insert(0, emprestimo)

        tk.Label(janela_emprestimo, text="Data da Devolução:").grid(row=8, column=0, pady=5)
        ent_devolucao = tk.Entry(janela_emprestimo, width=40)
        ent_devolucao.grid(row=9, column=0, pady=5)
        ent_devolucao.insert(0, devolucao)

        def salvar_atualizacao():
            nome = ent_nome.get().strip()
            cliente = combo_cliente.get()
            livro = combo_livro.get()
            emprestimo = ent_emprestimo.get().strip()
            devolucao = ent_devolucao.get().strip()

            condicao_emprestimo = (nome == ""
                                   and cliente == ""
                                   and livro == ""
                                   and emprestimo == "" 
                                   and devolucao == "" 
                                  )

            if condicao_emprestimo:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            id_cliente = mapeamento_cliente[cliente]
            id_livro = mapeamento_livro[livro]

            bd.db_atualizar_emprestimo(
                id_emp,
                nome,
                id_cliente,
                id_livro,
                emprestimo,
                devolucao
            )

            messagebox.showinfo("Sucesso", "Empréstimo atualizado com sucesso!")
            janela_emprestimo.destroy()
            atualizar_lista()

        tk.Button(
            janela_emprestimo,
            text="Salvar Alterações",
            command=salvar_atualizacao,
            bg="blue",
            fg="white"
        ).grid(row=10, column=0, pady=15)

    atualizar_lista()

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_emprestimo,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        command=atualizar_emprestimo,
        bg="blue",
        fg="white",
    ).grid(row=0, column=1, padx=10)