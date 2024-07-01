# ProjetoCatalogoLivro-API

![Licença](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![FastAPI](https://img.shields.io/badge/fastapi-0.70.0-green.svg) ![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-1.4.0-red.svg)

## 📚 Descrição

ProjetoCatalogoLivro-API é uma API desenvolvida em Python utilizando FastAPI, SQLAlchemy e SQL Server. Esta API oferece autenticação JWT e diferentes níveis de acesso para gerenciamento de um catálogo de livros. Ideal para bibliotecas, livrarias ou qualquer aplicação que necessite de um sistema de catalogação de livros com segurança e controle de acesso.

## 🗂 Índice

- [Instalação](#instalação)
- [Uso](#uso)
- [Recursos](#recursos)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## 🚀 Instalação

Siga os passos abaixo para instalar e configurar o ambiente para rodar o projeto.

```bash
# Clone o repositório
git clone https://github.com/FlavioMartinsJr/ProjetoCatalogoLivro-API.git

# Navegue até o diretório do projeto
cd ProjetoCatalogoLivro-API

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows
venv\Scripts\activate

# No Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente para o SQL Server e JWT
# Crie um arquivo .env e adicione as seguintes variáveis:
# DATABASE_URL=mssql+pyodbc://username:password@hostname:port/dbname?driver=SQL+Server
# SECRET_KEY=sua_secret_key
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

