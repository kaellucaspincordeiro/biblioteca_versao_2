import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_multa(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # --- Título da Tela ---
    tk.Label(container, text="Cadastro das Multas", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 20))
    # --- Formulário de Cadastro ---
    tk.Label(container, text="Nome da Multa:", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=(0, 8))
    ent_nome = tk.Entry(container, width=40)
    ent_nome.grid(row=2, column=0, pady=(0, 12))

    def obter_emprestimos():
        conn = bd.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_emprestimo, nome_emprestimo FROM emprestimo")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    tk.Label(container, text="Empréstimo:", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=(0, 2))

    # Buscamos as categorias do banco
    lista_emprestimos = obter_emprestimos() 

    mapeamento_emprestimo = {nomes_emprestimos: id_emprestimo for id_emprestimo, nomes_emprestimos in lista_emprestimos}
   
    combo_emprestimo = ttk.Combobox(container, values=list(mapeamento_emprestimo.keys()), width=37, state="readonly")
    combo_emprestimo.grid(row=4, column=0, pady=(0, 5))


    def obter_id_emprestimo():
        nome_selecionado = combo_emprestimo.get()

        if nome_selecionado:                
            return mapeamento_emprestimo[nome_selecionado]
        
        return None

    def salvar_multa():
        nome_multa = ent_nome.get()
        emprestimo = obter_id_emprestimo()

        condicao_multa = (nome_multa.strip() 
                          and emprestimo is not None 
                         )
        

        if condicao_multa:
            bd.db_cadastrar_multa(nome_multa, emprestimo)
            messagebox.showinfo("Sucesso", "Multa cadastrada com sucesso!")
            ent_nome.delete(0, tk.END)
            combo_emprestimo.set("")
            atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    tk.Button(container, text="Cadastrar multa", command=salvar_multa, bg="green", fg="white").grid(row=5, column=0, pady=(0, 18))

    # --- Lista de Livros ---
    tk.Label(container, text="Multas Cadastradas:", font=("Arial", 10, "bold")).grid(row=6, column=0)
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=7, column=0, pady=10, padx=20, sticky="nsew")

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "nome", "emprestimo"),
        show="headings",
        yscrollcommand=scroll.set
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    scroll.config(command=tabela.yview)

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome da Multa")
    tabela.heading("emprestimo", text="Nome do Empréstimo")

    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=50, anchor="center")
    tabela.column("emprestimo", width=50, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=8, column=0, pady=10)
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)
        
        multas = bd.db_listar_multas()

        for mul in multas:            
            tabela.insert("", "end", values=(mul[0],mul[1],mul[2]))

    atualizar_lista()

    def deletar_multa():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma multa para excluir!")
            return

        valores = tabela.item(item_selecionado, "values")
        id_mul = valores[0]


        # Abre a mesma tela de cadastro, mas agora enviando o ID para modo edição
        if messagebox.askyesno("Confirmar", "Deseja excluir esta multa?"):
            bd.db_deletar_multa(id_mul)
            atualizar_lista()

    def atualizar_multa():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um(a) autor(a) para atualizar!")
            return
            
        valores = tabela.item(item_selecionado, "values")
        id_mul = valores[0]
        nome_multa = valores[1]
        emprestimo = valores[2]

        janela_multa = tk.Toplevel(container)
        janela_multa.title("Atualizar Autor(a)")
        janela_multa.geometry("350x200")
        janela_multa.grab_set()

        janela_multa.grid_columnconfigure(0, weight=1)

        tk.Label(janela_multa, text="Nome da Multa:").grid(row=0, column=0, pady=5)
        ent_nome = tk.Entry(janela_multa, width=40)
        ent_nome.grid(row=1, column=0, pady=5)
        ent_nome.insert(0, nome_multa)

        tk.Label(janela_multa, text="Empréstimo:").grid(row=2, column=0, pady=5)
        combo_emprestimo = ttk.Combobox(
        janela_multa,
        values=list(mapeamento_emprestimo.keys()),
        width=37,
        state="readonly"
        )
        combo_emprestimo.grid(row=3, column=0, pady=5)
        combo_emprestimo.set(emprestimo)

        def salvar_atualizacao():
                 
            nome = ent_nome.get().strip()
            emprestimo = combo_emprestimo.get()

            if nome == "" and emprestimo == "":
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            id_emprestimo = mapeamento_emprestimo[emprestimo]

            bd.db_atualizar_multas(id_mul, nome, id_emprestimo)
            messagebox.showinfo("Sucesso", "Autor(a) atualizado(a) com sucesso!")

            janela_multa.destroy()
            atualizar_lista()

        tk.Button(
            janela_multa,
            text="Salvar Alterações",
            command=salvar_atualizacao,
            bg="blue",
            fg="white"
        ).grid(row=4, column=0, pady=20)

    atualizar_lista()

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_multa,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=40)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        command=atualizar_multa,
        bg="blue",
        fg="white",
    ).grid(row=0, column=1, padx=40)