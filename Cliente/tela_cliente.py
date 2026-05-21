import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_cliente(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    frame_cliente = tk.Frame(container)
    frame_cliente.grid(row=1, column=0, pady=10)

    # --- Título da Tela ---
    tk.Label(frame_cliente, text="Cadastro de Clientes", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 15))
    # --- Formulário de Cadastro ---
    tk.Label(frame_cliente, text="Nome do Cliente:", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=(0, 5))
    ent_nome = tk.Entry(frame_cliente, width=40)
    ent_nome.grid(row=2, column=0, pady=(0, 10))
    tk.Label(frame_cliente, text="Telefone:", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=(0, 5))
    ent_telefone = tk.Entry(frame_cliente, width=40)
    ent_telefone.grid(row=4, column=0, pady=(0, 10))
    tk.Label(frame_cliente, text="Endereço:", font=("Arial", 10, "bold")).grid(row=5, column=0, pady=(0, 5))
    ent_endereco = tk.Entry(frame_cliente, width=40)
    ent_endereco.grid(row=6, column=0, pady=(0, 10))
    tk.Label(frame_cliente, text="CPF:", font=("Arial", 10, "bold")).grid(row=7, column=0, pady=(0, 5))
    ent_cpf = tk.Entry(frame_cliente, width=40)
    ent_cpf.grid(row=8, column=0, pady=(0, 10))

    def salvar_cliente():
        nome_cliente = ent_nome.get()
        telefone = ent_telefone.get()
        endereco = ent_endereco.get()
        cpf = ent_cpf.get()

        condicao_cliente = (nome_cliente.strip() 
                            and telefone.strip() 
                            and endereco.strip() 
                            and cpf.strip()
                           )
        

        if condicao_cliente:
            bd.db_cadastrar_cliente(nome_cliente, telefone, endereco, cpf)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            ent_nome.delete(0, tk.END)
            ent_telefone.delete(0, tk.END)
            ent_endereco.delete(0, tk.END)
            ent_cpf.delete(0, tk.END)
            atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    tk.Button(frame_cliente, text="Cadastrar cliente", command=salvar_cliente, bg="green", fg="white").grid(row=9, column=0, pady=(0, 15))

    # --- Lista de Livros ---
    tk.Label(frame_cliente, text="Clientes Cadastrados:", font=("Arial", 10, "bold")).grid(row=10, column=0, pady=(0, 10))
    
    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")

    container.grid_rowconfigure(5, weight=1)
    container.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "cliente", "telefone", "endereço", "cpf"),
        show="headings",
        yscrollcommand=scroll.set
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("cliente", text="Nome do Cliente")
    tabela.heading("telefone", text="Telefone")
    tabela.heading("endereço", text="Endereço")
    tabela.heading("cpf", text="CPF")

    tabela.column("id", width=30, anchor="center")
    tabela.column("cliente", width=30, anchor="center")
    tabela.column("telefone", width=30, anchor="center")
    tabela.column("endereço", width=30, anchor="center")
    tabela.column("cpf", width=30, anchor="center")

    frame_botoes = tk.Frame(container)
    frame_botoes.grid(row=7, column=0, pady=10)
    frame_botoes.grid_columnconfigure(0, minsize=150)
    frame_botoes.grid_columnconfigure(1, minsize=150)

    def atualizar_lista():
        for item in tabela.get_children():
            tabela.delete(item)

        clientes = bd.db_listar_clientes()

        for cli in clientes:           
            tabela.insert("", "end", values=(cli[0],cli[1],cli[2],cli[3],cli[4]))

    atualizar_lista()
        
    def deletar_cliente():
        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return

        valores = tabela.item(item_selecionado, "values")
        id_cli = valores[0]


        # Abre a mesma tela de cadastro, mas agora enviando o ID para modo edição
        if messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
            bd.db_deletar_cliente(id_cli)
            atualizar_lista()

    def atualizar_cliente():

        item_selecionado = tabela.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma cliente para atualizar!")
            return
            
        valores = tabela.item(item_selecionado, "values")
        id_cli = valores[0]
        nome_cliente = valores[1]
        telefone = valores[2]
        endereco = valores[3]
        cpf = valores[4]

        janela_cliente = tk.Toplevel(container)
        janela_cliente.title("Atualizar Cliente")
        janela_cliente.geometry("350x430")
        janela_cliente.grab_set()

        janela_cliente.grid_columnconfigure(0, weight=1)

        tk.Label(janela_cliente, text="Nome da Cliente:").grid(row=0, column=0, pady=5)
        ent_nome = tk.Entry(janela_cliente, width=40)
        ent_nome.grid(row=1, column=0, pady=5)
        ent_nome.insert(0, nome_cliente)

        tk.Label(janela_cliente, text="Telefone:").grid(row=2, column=0, pady=5)
        ent_telefone = tk.Entry(janela_cliente, width=40)
        ent_telefone.grid(row=3, column=0, pady=5)
        ent_telefone.insert(0, telefone)

        tk.Label(janela_cliente, text="Endereço:").grid(row=4, column=0, pady=5)
        ent_endereco = tk.Entry(janela_cliente, width=40)
        ent_endereco.grid(row=5, column=0, pady=5)
        ent_endereco.insert(0, endereco)

        tk.Label(janela_cliente, text="CPF:").grid(row=6, column=0, pady=5)
        ent_cpf = tk.Entry(janela_cliente, width=40)
        ent_cpf.grid(row=7, column=0, pady=5)
        ent_cpf.insert(0, cpf)

        def salvar_atualizacao():
                 
                nome = ent_nome.get().strip()
                telefone = ent_telefone.get().strip()
                endereco = ent_endereco.get().strip()
                cpf = ent_cpf.get().strip()

                condicao_cliente = (nome == ""
                                    and telefone == ""
                                    and endereco == ""
                                    and cpf == ""
                                    )

                if condicao_cliente:
                    messagebox.showwarning("Aviso", "Preencha todos os campos!")
                    return

                bd.db_atualizar_cliente(id_cli, nome, telefone, endereco, cpf)
                messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")

                janela_cliente.destroy()
                atualizar_lista()

        tk.Button(
            janela_cliente,
            text="Salvar Alterações",
            command=salvar_atualizacao,
            bg="blue",
            fg="white"
        ).grid(row=8, column=0, pady=20)

    atualizar_lista()

    tk.Button(
        frame_botoes,
        text="Excluir",
        command=deletar_cliente,
        bg="red",
        fg="white",
    ).grid(row=0, column=0, padx=40)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        command=atualizar_cliente,
        bg="blue",
        fg="white",
    ).grid(row=0, column=1, padx=40)