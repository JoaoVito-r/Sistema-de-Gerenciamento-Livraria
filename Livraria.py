import streamlit as st

# Lista para armazenar os livros
livros = []

# Função para adicionar um livro
def adicionar_livro(nome, autor, ano):
    livro = {"nome": nome, "autor": autor, "ano": ano}
    livros.append(livro)

# Função para listar livros
def listar_livros():
    if not livros:
        st.info("Nenhum livro cadastrado.")
    else:
        for idx, livro in enumerate(livros, start=1):
            st.write(f"**{idx}.** {livro['nome']} - {livro['autor']} ({livro['ano']})")

# Função para remover livro
def remover_livro(indice):
    if 0 <= indice < len(livros):
        livros.pop(indice)
        st.success("Livro removido com sucesso!")
    else:
        st.error("Índice inválido.")

# Título da aplicação
st.title("📚 Sistema de Gerenciamento de Livraria")

# Menu de navegação
opcao = st.sidebar.selectbox("Menu", ["Adicionar Livro", "Listar Livros", "Remover Livro"])

# Tela de adicionar livro
if opcao == "Adicionar Livro":
    st.header("Adicionar um novo livro")
    nome = st.text_input("Nome do Livro")
    autor = st.text_input("Autor do Livro")
    ano = st.number_input("Ano de Publicação", min_value=0, max_value=2100, step=1)

    if st.button("Adicionar"):
        if nome and autor and ano:
            adicionar_livro(nome, autor, ano)
            st.success("Livro adicionado com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos.")

# Tela de listar livros
elif opcao == "Listar Livros":
    st.header("Lista de Livros Cadastrados")
    listar_livros()

# Tela de remover livro
elif opcao == "Remover Livro":
    st.header("Remover um Livro")
    listar_livros()
    indice = st.number_input("Digite o número do livro a remover", min_value=1, step=1)

    if st.button("Remover"):
        remover_livro(indice - 1)
