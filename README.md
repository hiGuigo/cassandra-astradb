## *Projeto desenvolvido utilizando Python, MongoDB e AstraDB*

### Especificações
- python 3.12
- AstraDB (Apache Cassandra)

### Manual do usuário
1. Criar uma conta gratuita em https://astra.datastax.com.
2. Criar um banco de dados no AstraDB.
3. Criar o keyspace `mercadolivre` no banco.
4. Gerar um token de aplicação e baixar o **Secure Connect Bundle**.
5. Gerar o arquivo *.env*: `cp .env.example .env`
6. Preencher no arquivo *.env* as variáveis `ASTRA_SCB_PATH` (caminho do bundle) e `ASTRA_DB_TOKEN` (token gerado).
7. Criar e ativar o ambiente virtual: `python3 -m venv .venv` -> `source .venv/bin/activate`
8. Instalar as bibliotecas necessárias: `pip install -r requirements.txt`
9. Iniciar a aplicação: `cd src` -> `python3 main.py`
10. Selecionar a opção `8` no menu para criar as tabelas e começar a usar o sistema.
