import sqlite3
import script_banco

def conectar():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute(script_banco.categoria)
    cursor.execute(script_banco.editora)
    cursor.execute(script_banco.autor)
    cursor.execute(script_banco.cliente)
    cursor.execute(script_banco.livro)
    cursor.execute(script_banco.emprestimo)
    cursor.execute(script_banco.multa)
    cursor.execute(script_banco.user)
    conn.commit()
    return conn

def db_cadastrar_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categoria (nome_categoria) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def db_listar_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categoria")
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_categoria(id_categoria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categoria WHERE id_categoria = ?", (id_categoria,))
    conn.commit()
    conn.close()

def db_atualizar_categoria(id_categoria, nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE categoria SET nome_categoria = ? WHERE id_categoria = ?", (nome, id_categoria))
    conn.commit()
    conn.close()

def db_cadastrar_editora(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO editora (nome_editora) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def db_listar_editoras():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM editora")
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_editora(id_editora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM editora WHERE id_categoria = ?", (id_editora,))
    conn.commit()
    conn.close()

def db_atualizar_editora(id_editora, nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE editora SET nome_editora = ? WHERE id_editora = ?", (nome, id_editora))
    conn.commit()
    conn.close() 

def db_cadastrar_autor(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO autor (nome_autor) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def db_listar_autores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM autor")
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_autor(id_autor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM autor WHERE id_autor = ?", (id_autor,))
    conn.commit()
    conn.close()

def db_atualizar_autor(id_autor, nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE autor SET nome_autor = ? WHERE id_autor = ?", (nome, id_autor))
    conn.commit()
    conn.close() 

def db_cadastrar_cliente(nome, telefone, endereco, cpf, status_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cliente (nome_cliente, telefone, endereco, cpf, status) VALUES (?, ?, ?, ?, ?)", (nome, telefone, endereco, cpf, status_cliente))
    conn.commit()
    conn.close()

def db_listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
    conn.commit()
    conn.close()

def db_atualizar_cliente(id_cliente, nome, telefone, endereco, cpf, status_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE cliente SET nome_cliente = ?, telefone = ?, endereco = ?, cpf = ?, status = ? WHERE id_cliente = ?", (nome, telefone, endereco, cpf, status_cliente, id_cliente))
    conn.commit()
    conn.close()  

def db_cadastrar_livro(nome, status, id_editora, id_categoria, id_autor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livro (nome_livro, status, id_editora, id_categoria, id_autor) VALUES (?, ?, ?, ?, ?)", (nome, status, id_editora, id_categoria, id_autor))
    conn.commit()
    conn.close()

def db_listar_livros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT livro.id_livro,
                          livro.nome_livro,
                          livro.status,
                          editora.nome_editora,
                          categoria.nome_categoria,
                          autor.nome_autor
                   FROM livro
                   INNER JOIN editora ON livro.id_editora = editora.id_editora
                   INNER JOIN categoria ON livro.id_categoria = categoria.id_categoria
                   INNER JOIN autor ON livro.id_autor = autor.id_autor
                  """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_livro(id_livro):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livro WHERE id_livro = ?", (id_livro,))
    conn.commit()
    conn.close()

def db_atualizar_livro(id_livro, nome, status, editora, categoria, autor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE livro SET nome_livro = ?, status = ?, id_editora = ?, id_categoria = ?, id_autor = ? WHERE id_livro = ?", (nome, status, editora, categoria, autor, id_livro))
    conn.commit()
    conn.close()

def db_cadastrar_emprestimo(nome, id_cliente, id_livro, data_emprestimo, data_devolucao, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emprestimo (nome_emprestimo, id_cliente, id_livro, data_emprestimo, data_devolucao, status) VALUES (?, ?, ?, ?, ?, ?)", (nome, id_cliente, id_livro, data_emprestimo, data_devolucao, status))
    conn.commit()
    conn.close()

def db_listar_emprestimos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT emprestimo.id_emprestimo,
                          emprestimo.nome_emprestimo,
                          cliente.nome_cliente,
                          livro.nome_livro,
                          emprestimo.data_emprestimo,
                          emprestimo.data_devolucao,
                          emprestimo.status
                   FROM emprestimo
                   INNER JOIN cliente ON emprestimo.id_cliente = cliente.id_cliente
                   INNER JOIN livro ON emprestimo.id_livro = livro.id_livro
                  """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_emprestimo(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM emprestimo WHERE id_emprestimo = ?", (id_emprestimo,))
    conn.commit()
    conn.close()

def db_cadastrar_multa(id_emprestimo, dias_atrasos, total_multa, data_multa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO multa (id_emprestimo, dias_atrasos, total_multa, data_multa) VALUES (?, ?, ?, ?)", (id_emprestimo, dias_atrasos, total_multa, data_multa))
    conn.commit()
    conn.close()

def db_listar_multas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT multa.id_multa,
                          emprestimo.nome_emprestimo,
                          multa.dias_atrasos,
                          multa.total_multa,
                          multa.data_multa
                   FROM multa
                   INNER JOIN emprestimo ON multa.id_emprestimo = multa.id_emprestimo
                  """)
    dados = cursor.fetchall()
    conn.close()
    return dados


# Manipulação para o Sistema da Biblioteca
def buscar_livro(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_livro FROM emprestimo WHERE id_emprestimo = ?", (id_emprestimo,))

    dados = cursor.fetchone()
    conn.close()

    if dados:    
        return dados[0]
    return None

def status_emprestado_livro(id_livro):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM livro WHERE id_livro = ?", (id_livro,))

    dados = cursor.fetchone()
    conn.close()

    if dados:    
        return dados[0]
    return None

def atualizar_status_livro(id_livro, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE livro SET status = ? WHERE id_livro = ?""", (status, id_livro))

    conn.commit()
    conn.close()

def realizar_emprestimo(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE emprestimo SET status = "Emprestado" WHERE id_emprestimo = ?""", (id_emprestimo,))

    conn.commit()
    conn.close()

def atualizar_status_emprestimo(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE emprestimo SET status = "Devolvido" WHERE id_emprestimo = ?""", (id_emprestimo,))
    conn.commit()
    conn.close()

def procurar_status_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM cliente WHERE id_cliente = ?", (id_cliente,))

    dados = cursor.fetchone()
    conn.close()

    if dados:    
        return dados[0]
    return None

def buscar_id_emprestimo(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT id_emprestimo, 
                             id_livro, 
                             data_devolucao,
                             status 
                      FROM emprestimo WHERE id_emprestimo = ?""",(id_emprestimo,))
    dado = cursor.fetchone()
    conn.close()

    return dado

def buscar_multa(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT id_multa 
                      FROM multa WHERE id_emprestimo = ?""",(id_emprestimo,))
    mu = cursor.fetchone()
    conn.close()

    return mu
