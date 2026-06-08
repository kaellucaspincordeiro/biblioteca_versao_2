import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd
from datetime import datetime, timedelta

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

    def salvar_emprestimo():
        nome_emprestimo = ent_nome.get()
        cliente = obter_id_cliente()
        livro = obter_id_livro()
        data_emprestimo = ent_emprestimo.get()

        condicao_emprestimo = (nome_emprestimo.strip() 
                               and cliente is not None 
                               and livro is not None
                               and data_emprestimo.strip()
                              )
            
        if not condicao_emprestimo:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        status_livro = bd.status_emprestado_livro(livro)

        if status_livro != "Disponível":
            messagebox.showinfo("Atenção", "O Livro está emprestado e não pode realizar um empréstimo!")
            return
        
        data_emp = datetime.strptime(data_emprestimo, "%d/%m/%Y")

        status_cliente = bd.procurar_status_cliente(cliente)

        if status_cliente == "Aluno":
            dias = 7

        elif status_cliente == "Professor":
            dias = 30

        else:
            messagebox.showerror("Erro", "Opção do status desse cliente é inválido!")
            return
        
        data_dev = data_emp + timedelta(days=dias)
        data_devolucao = data_dev.strftime("%d/%m/%Y")

        status = "Emprestado"
        
        bd.db_cadastrar_emprestimo(nome_emprestimo, cliente, livro, data_emprestimo, data_devolucao, status)
        bd.atualizar_status_livro(livro, "Emprestado")

        messagebox.showinfo("Sucesso", f"Empréstimo cadastrado com sucesso! A devolução deste livro ficou para {data_devolucao}")

        ent_nome.delete(0, tk.END)
        combo_cliente.set("")
        combo_livro.set("")
        ent_emprestimo.delete(0, tk.END)

        atualizar_lista()

    def devolver_livro():

        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um livro para a devolução!")
            return
            
        valores = tabela.item(item_selecionado[0], "values")
        id_emprestimo = valores[0]

        emprestimo = bd.buscar_id_emprestimo(id_emprestimo)

        if emprestimo is None:
            messagebox.showerror("Erro", "Empréstimo não encontrado!")
            return
        
        id_emprestimo, id_livro, data_devolucao, status = emprestimo

        if status == "Devolvido":
            messagebox.showwarning("Aviso", "Este empréstimo foi devolvido!")
            return
        
        bd.status_emprestado_para_devolvido(id_emprestimo)

        previsao = datetime.strptime(data_devolucao, "%d/%m/%Y")
        data_hoje = datetime.now()

        dias_atrasos = max(0, (data_hoje - previsao).days)
        total_multa = dias_atrasos * 2.0
        data_multa = data_hoje.strftime("%d/%m/%Y")

        if dias_atrasos > 0:
            total_multa = dias_atrasos * 2.0
            data_multa = data_hoje.strftime("%d/%m/%Y")

            existe_multa = bd.buscar_multa(id_emprestimo)

            if not existe_multa:

                bd.db_cadastrar_multa(id_emprestimo, dias_atrasos, total_multa, data_multa)

            messagebox.showwarning("Livro Devolvido", f"Você devolveu com prazo atrasado de {dias_atrasos} dias. Multa R$ {total_multa:.2f}")
        else:
            messagebox.showinfo("Livro Devolvido", "Você devolveu dentro do prazo")

        bd.atualizar_status_emprestimo(id_emprestimo, "Devolvido")
        bd.atualizar_status_livro(id_livro, "Disponível")

        atualizar_lista()
    
    tk.Button(frame_emprestimo, text="Cadastrar empréstimo", command=salvar_emprestimo, bg="green", fg="white").grid(row=9, column=0, pady=(4,5))

    # --- Lista de Livros ---
    tk.Label(frame_emprestimo, text="Empréstimos Cadastrados:", font=("Arial", 10, "bold")).grid(row=10, column=0, pady=(4, 5))
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=4, column=0, pady=(0,5), padx=20, sticky="nsew")

    container.grid_rowconfigure(4, weight=1)

    frame_tabela.grid_columnconfigure(0, weight=1)
    frame_tabela.grid_rowconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "nome", "cliente", "livro", "emprestimo", "devolucao", "status"),
        show="headings",
        yscrollcommand=scroll.set,
        height= 4
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome do Empréstimo")
    tabela.heading("cliente", text="Cliente")
    tabela.heading("livro", text="Livro")
    tabela.heading("emprestimo", text="Data do Empréstimo")
    tabela.heading("devolucao", text="Data da Devolução")
    tabela.heading("status", text="Status do Empréstimo")

    tabela.column("id", width=30, anchor="center")
    tabela.column("nome", width=30, anchor="center")
    tabela.column("cliente", width=30, anchor="center")
    tabela.column("livro", width=30, anchor="center")
    tabela.column("emprestimo", width=30, anchor="center")
    tabela.column("devolucao", width=30, anchor="center")
    tabela.column("status", width=30, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=5, column=0, pady=(5, 10))
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        emprestimos = bd.db_listar_emprestimos()

        for emp in emprestimos:           
            tabela.insert("", "end", values=(emp[0],emp[1],emp[2],emp[3],emp[4],emp[5],emp[6]))

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

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_emprestimo,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_botoes, 
        text="Devolver Livro", 
        command=devolver_livro, 
        bg="lightblue", 
        fg="#000000"
    ).grid(row=0, column=1, padx=10)
