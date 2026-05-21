categoria = """
            CREATE TABLE IF NOT EXISTS categoria (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome_categoria VARCHAR(100) NOT NULL
            )
            """

editora = """
          CREATE TABLE IF NOT EXISTS editora (
                id_editora INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome_editora VARCHAR(100) NOT NULL
          )
          """

autor = """
        CREATE TABLE IF NOT EXISTS autor (
            id_autor INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome_autor VARCHAR(100) NOT NULL
        )
        """

cliente = """
          CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome_cliente VARCHAR(100) NOT NULL,
                telefone VARCHAR(50),
                endereco VARCHAR(50) NOT NULL,
                cpf VARCHAR(50) NOT NULL
          )
          """

emprestimo = """
             CREATE TABLE IF NOT EXISTS emprestimo (
                id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome_emprestimo VARCHAR(100) NOT NULL,
                id_cliente INTEGER,
                id_livro INTEGER,
                data_emprestimo VARCHAR(50),
                data_devolucao VARCHAR(50),
                CONSTRAINT fk_emprestimo_cliente FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
                CONSTRAINT fk_emprestimo_cliente FOREIGN KEY (id_livro) REFERENCES livro (id_livro)    
             )
             """

livro = """
        CREATE TABLE IF NOT EXISTS livro (
            id_livro INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome_livro VARCHAR(100) NOT NULL,
            status VARCHAR(50) NOT NULL,
            id_editora INTEGER,
            id_categoria INTEGER,
            id_autor INTEGER,
            CONSTRAINT fk_livro_editora FOREIGN KEY (id_editora) REFERENCES editora (id_editora),
            CONSTRAINT fk_livro_categoria FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),    
            CONSTRAINT fk_livro_autor FOREIGN KEY (id_autor) REFERENCES autor (id_autor)    
        )
        """

multa = """
        CREATE TABLE IF NOT EXISTS multas (
            id_multa INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome_multa VARCHAR(100) NOT NULL,
            id_emprestimo INTEGER,
            CONSTRAINT fk_multa_emprestimo FOREIGN KEY (id_emprestimo) REFERENCES emprestimo (id_emprestimo) 
        )
        """

user = """
       CREATE TABLE IF NOT EXISTS user (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(100) NOT NULL, 
            nome_user VARCHAR(100) NOT NULL,
            senha VARCHAR(100) NOT NULL
       )
       """

