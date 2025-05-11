import streamlit as st
import json
import os
import pandas as pd
import sqlite3

# ========================
# 📋 Função para carregar os dados
# ========================
def get_data():
    conn = sqlite3.connect("livros.db")
    df_livros = pd.read_sql_query("SELECT * FROM livros", conn)
    conn.close()

    conn = sqlite3.connect("clientes.db")
    df_clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()

    conn = sqlite3.connect("vendas.db")
    df_vendas = pd.read_sql_query("SELECT * FROM vendas", conn)
    conn.close()

    df_completo = df_vendas.merge(df_clientes, on="id_cliente").merge(df_livros, on="id_livro")

    return df_livros, df_clientes, df_vendas, df_completo


# ========================
# 📋 Função para adicionar informações à base de dados
# ========================

def adicionar_livro():
    st.subheader("📖 Adicionar Novo Livro")

    if "livro_candidato" not in st.session_state:
        st.session_state.livro_candidato = None

    titulo = st.text_input("Título do Livro")
    autor = st.text_input("Autor do Livro")
    genero = st.text_input("Gênero do Livro")
    preco = st.number_input("Preço do Livro", min_value=0.0, step=0.01)

    if st.button("Verificar Dados do Livro"):
        if titulo and autor and genero and preco > 0:
            st.session_state.livro_candidato = {
                "titulo": titulo,
                "autor": autor,
                "genero": genero,
                "preco": preco
            }
        else:
            st.warning("⚠️ Preencha todos os campos corretamente.")

    if st.session_state.livro_candidato:
        livro = st.session_state.livro_candidato
        st.success(f"""
        📖 **Título:** {livro['titulo']}
        ✍️ **Autor:** {livro['autor']}
        📚 **Gênero:** {livro['genero']}
        💲 **Preço:** R$ {livro['preco']:.2f}
        """)

        confirmar, cancelar = st.columns(2)

        with confirmar:
            if st.button("✅ Confirmar Cadastro"):
                conn = sqlite3.connect("livros.db")
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT COUNT(*) FROM livros WHERE titulo = ? AND autor = ? AND genero = ? AND preco = ?",
                    (livro['titulo'], livro['autor'], livro['genero'], livro['preco'])
                )
                existe = cursor.fetchone()[0]

                if existe:
                    st.warning("⚠️ Livro já cadastrado com essas informações.")
                else:
                    cursor.execute(
                        "INSERT INTO livros (titulo, autor, genero, preco) VALUES (?, ?, ?, ?)",
                        (livro['titulo'], livro['autor'], livro['genero'], livro['preco'])
                    )
                    conn.commit()
                    st.success("✅ Livro cadastrado com sucesso!")

                conn.close()
                global df_livros, df_clientes, df_vendas, df_completo
                df_livros, df_clientes, df_vendas, df_completo = get_data()
                st.session_state.livro_candidato = None  # Limpa para não cadastrar de novo

        with cancelar:
            if st.button("❌ Cancelar Cadastro"):
                st.session_state.livro_candidato = None
                st.warning("Cadastro cancelado.")

def editar_livro():
    st.subheader("✏️ Editar Livro Existente")

    if "livro_edicao" not in st.session_state:
        st.session_state.livro_edicao = None

    conn = sqlite3.connect("livros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, genero, preco FROM livros ORDER BY titulo ASC")
    livros = cursor.fetchall()
    conn.close()

    livro_selecionado = st.selectbox("Selecione o livro para editar:", livros, format_func=lambda x: f"{x[1]} - {x[0]}")

    if livro_selecionado:
        id_livro, titulo_atual, autor_atual, genero_atual, preco_atual = livro_selecionado

        st.info(f"""
        📖 **Título Atual:** {titulo_atual}
        ✍️ **Autor Atual:** {autor_atual}
        📚 **Gênero Atual:** {genero_atual}
        💲 **Preço Atual:** R$ {preco_atual:.2f}
        """)

        novo_titulo = st.text_input("Novo Título", value=titulo_atual)
        novo_autor = st.text_input("Novo Autor", value=autor_atual)
        novo_genero = st.text_input("Novo Gênero", value=genero_atual)
        novo_preco = st.number_input("Novo Preço", min_value=0.0, step=0.01, value=preco_atual)

        if st.button("Verificar Alterações"):
            st.session_state.livro_edicao = {
                "id_livro": id_livro,
                "titulo": novo_titulo,
                "autor": novo_autor,
                "genero": novo_genero,
                "preco": novo_preco
            }

    if st.session_state.livro_edicao:
        livro = st.session_state.livro_edicao
        st.success(f"""
        Você deseja atualizar para:

        📖 **Título:** {livro['titulo']}
        ✍️ **Autor:** {livro['autor']}
        📚 **Gênero:** {livro['genero']}
        💲 **Preço:** R$ {livro['preco']:.2f}
        """)

        confirmar, cancelar = st.columns(2)

        with confirmar:
            if st.button("✅ Confirmar Alteração"):
                conn = sqlite3.connect("livros.db")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE livros SET titulo = ?, autor = ?, genero = ?, preco = ? WHERE id_livro = ?",
                    (livro['titulo'], livro['autor'], livro['genero'], livro['preco'], livro['id_livro'])
                )
                conn.commit()
                conn.close()
                st.success("✅ Livro alterado com sucesso!")
                global df_livros, df_clientes, df_vendas, df_completo
                df_livros, df_clientes, df_vendas, df_completo = get_data()
                st.session_state.livro_edicao = None  # Limpa para não repetir

        with cancelar:
            if st.button("❌ Cancelar Alteração"):
                st.session_state.livro_edicao = None
                st.warning("Alteração cancelada.")

def excluir_livro():
    st.subheader("🗑️ Excluir Livro")

    if "livro_exclusao" not in st.session_state:
        st.session_state.livro_exclusao = None

    conn = sqlite3.connect("livros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, genero, preco FROM livros ORDER BY titulo ASC")
    livros = cursor.fetchall()
    conn.close()

    livro_selecionado = st.selectbox("Selecione o livro para excluir:", livros, format_func=lambda x: f"{x[1]} - {x[0]}")

    if livro_selecionado:
        id_livro, titulo, autor, genero, preco = livro_selecionado

        st.warning(f"""
        Você selecionou para excluir:

        📖 **Título:** {titulo}
        ✍️ **Autor:** {autor}
        📚 **Gênero:** {genero}
        💲 **Preço:** R$ {preco:.2f}
        """)

        if st.button("Verificar Exclusão"):
            st.session_state.livro_exclusao = id_livro

    if st.session_state.livro_exclusao:
        confirmar, cancelar = st.columns(2)

        with confirmar:
            if st.button("✅ Confirmar Exclusão"):
                conn = sqlite3.connect("livros.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM livros WHERE id_livro = ?", (st.session_state.livro_exclusao,))
                conn.commit()
                conn.close()
                st.success("✅ Livro excluído com sucesso!")
                global df_livros, df_clientes, df_vendas, df_completo
                df_livros, df_clientes, df_vendas, df_completo = get_data()
                st.session_state.livro_exclusao = None

        with cancelar:
            if st.button("❌ Cancelar Exclusão"):
                st.session_state.livro_exclusao = None
                st.warning("Exclusão cancelada.")


# ========================
# 📋 Carregar os dados
# ========================
df_livros, df_clientes, df_vendas, df_completo = get_data()

# ========================
# 📋 Menu de navegação
# ========================
st.sidebar.title("📚 Sistema de Gerenciamento de Livraria")
aba = st.sidebar.radio(
    "Escolha uma opção:",
    ["📖 Consultar Livros", "👥 Consultar Clientes", "📊 Consultar Vendas", "📈 Estatísticas Livraria", "🛠️ Gerenciar Cadastros"]
)

# ========================
# 📋 Conteúdo das abas
# ========================

if aba == "📖 Consultar Livros":
    st.header("📖 Consulta de Livros")
    st.dataframe(df_livros)

elif aba == "👥 Consultar Clientes":
    st.header("👥 Consulta de Clientes")
    st.dataframe(df_clientes)

elif aba == "📊 Consultar Vendas":
    st.header("📊 Consulta de Vendas")
    st.dataframe(df_vendas)

elif aba == "📈 Estatísticas Livraria":
    st.header("📈 Estatísticas")
    st.bar_chart(df_completo.groupby("genero")["quantidade"].sum())

elif aba == "🛠️ Gerenciar Cadastros":
    st.header("🛠️ Gerenciar Cadastros")

    tipo = st.selectbox("Escolha o que deseja gerenciar:", ["Livro", "Cliente", "Venda"])
    acao = st.selectbox("Escolha a ação:", ["Adicionar", "Editar", "Excluir"])

    if tipo == "Livro":
        if acao == "Adicionar":
            adicionar_livro()
        elif acao == "Editar":
            editar_livro()
        elif acao == "Excluir":
            excluir_livro()


