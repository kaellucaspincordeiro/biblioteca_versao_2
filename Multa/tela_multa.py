import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

def montar_tela_multa(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(container, text="← Voltar ao Menu", command=funcao_voltar, bg="#ccc").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # --- Título da Tela ---
    tk.Label(container, text="Histórico de Multas", font=("Arial", 14, "bold")).grid(row=1, column=0, pady=(0, 20))

    frame_tabela = tk.Frame(container)
    frame_tabela.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")

    container.grid_rowconfigure(5, weight=1)
    container.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(frame_tabela)
    scroll.grid(row=0, column=1, sticky="ns")

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("id", "emprestimo", "dias_atrasos", "total", "multa"),
        show="headings",
        yscrollcommand=scroll.set
    )
    tabela.grid(row=0, column=0, sticky="nsew")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    scroll.config(command=tabela.yview)

    tabela.heading("id", text="ID")
    tabela.heading("emprestimo", text="Empréstimo")
    tabela.heading("dias_atrasos", text="Dias em Atraso")
    tabela.heading("total", text="Total da Multa")
    tabela.heading("multa", text="Data da Multa")

    tabela.column("id", width=30, anchor="center")
    tabela.column("emprestimo", width=50, anchor="center")
    tabela.column("dias_atrasos", width=30, anchor="center")
    tabela.column("total", width=50, anchor="center")
    tabela.column("multa", width=30, anchor="center")

    def atualizar_lista_multas():
        for item in tabela.get_children():
            tabela.delete(item)

        multas = bd.db_listar_multas()

        for mul in multas:           
            tabela.insert("", "end", values=(mul[0],mul[1],mul[2],mul[3],mul[4]))

    atualizar_lista_multas()