## *Projeto desenvolvido para execução no VS Code (Linux)*

### Especificações
- Python 3.12
- Astra DB (Apache Cassandra)

### Manual do usuário
1. Criar uma conta gratuita em https://astra.datastax.com
2. Criar um banco de dados Astra DB.
3. Criar o keyspace `mercadolivre` no banco.
4. Gerar um token de aplicação e baixar o **Secure Connect Bundle**.
5. Gerar o arquivo *.env*: `cp .env.example .env`
6. Preencher no arquivo *.env* as variáveis `ASTRA_SCB_PATH` (caminho do bundle) e `ASTRA_DB_TOKEN` (token gerado).
7. Criar e ativar o ambiente virtual: `python3 -m venv .venv` -> `source .venv/bin/activate`
8. Instalar as bibliotecas necessárias: `pip install cassandra-driver python-dotenv`
9. Executar o arquivo *menu.py*: `python3 menu.py`
10. Selecionar a opção `8` no menu para criar as tabelas e começar a usar o sistema.
