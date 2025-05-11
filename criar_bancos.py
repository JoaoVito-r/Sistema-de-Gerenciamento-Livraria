import sqlite3
import random
import json

# ========================
# 📚 CRIAR LIVROS.DB
# ========================

# Conectar ao banco livros.db
conn = sqlite3.connect("livros.db")
cursor = conn.cursor()

# Criar a tabela livros
cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT UNIQUE,
    autor TEXT,
    genero TEXT,
    preco REAL
)
""")

# Carregar livros do JSON
with open('livros.json', 'r', encoding='utf-8') as f:
    livros = json.load(f)

# Inserir livros
cursor.executemany("INSERT OR IGNORE INTO livros (titulo, autor, genero, preco) VALUES (?, ?, ?, ?)", livros)

conn.commit()
conn.close()

# ========================
# 👥 CRIAR CLIENTES.DB
# ========================

# Conectar ao banco clientes.db
conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

# Criar a tabela clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    email TEXT,
    telefone TEXT
)
""")

# Carregar clientes do JSON
with open('clientes.json', 'r', encoding='utf-8') as f:
    clientes = json.load(f)

# Inserir clientes
cursor.executemany("INSERT OR IGNORE INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", clientes)

conn.commit()
conn.close()

# ========================
# 📊 CRIAR VENDAS.DB
# ========================

# Conectar ao banco vendas.db
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()

# Criar a tabela vendas
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_livro INTEGER,
    quantidade INTEGER,
    FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY(id_livro) REFERENCES livros(id_livro)
)
""")
conn.commit()
conn.close()

# ========================
# 🎲 GERAR VENDAS ALEATÓRIAS
# ========================

# Carregar IDs de clientes e livros
conn_livros = sqlite3.connect("livros.db")
cursor_livros = conn_livros.cursor()
cursor_livros.execute("SELECT id_livro FROM livros")
livros_ids = [row[0] for row in cursor_livros.fetchall()]
conn_livros.close()

conn_clientes = sqlite3.connect("clientes.db")
cursor_clientes = conn_clientes.cursor()
cursor_clientes.execute("SELECT id_cliente FROM clientes")
clientes_ids = [row[0] for row in cursor_clientes.fetchall()]
conn_clientes.close()

# Criar lista de vendas
vendas = []
for _ in range(50):  # Gerar 50 vendas aleatórias
    id_cliente = random.choice(clientes_ids)
    id_livro = random.choice(livros_ids)
    quantidade = random.randint(1, 5)
    vendas.append((id_cliente, id_livro, quantidade))

# Inserir vendas
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()
cursor.executemany("INSERT INTO vendas (id_cliente, id_livro, quantidade) VALUES (?, ?, ?)", vendas)

conn.commit()
conn.close()

print("📚 Bancos de dados criados e populados com sucesso!")
