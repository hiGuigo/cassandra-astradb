import uuid
from decimal import Decimal
from conexao import session

#CREATE TABLES
def createTables():
    session.execute("""
        CREATE TABLE IF NOT EXISTS comprador (
            email       TEXT PRIMARY KEY,
            nome        TEXT,
            favoritos   LIST<TEXT>
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS vendedor (
            email   TEXT PRIMARY KEY,
            nome    TEXT
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id              UUID PRIMARY KEY,
            nome            TEXT,
            preco           DECIMAL,
            vendedor_email  TEXT
        )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id               UUID PRIMARY KEY,
            comprador_email  TEXT,
            produto_id       UUID,
            pagamento        TEXT
        )
    """)

    print("Tabelas criadas com sucesso.")

#SELECT
def listarProdutos(pesquisar=True):
    print("\n#### PESQUISAR PRODUTOS ####")

    if pesquisar:
        nome = input("Digite o nome do produto (Enter para listar todos): ").strip()
    else:
        nome = ""

    if nome:
        stmt = session.prepare("""
            SELECT id, nome, preco, vendedor_email
            FROM produtos
            WHERE nome = ?
            ALLOW FILTERING
        """)
        produtos = session.execute(stmt, (nome,)).all()
    else:
        produtos = session.execute("""
            SELECT id, nome, preco, vendedor_email
            FROM produtos
        """).all()

    if not produtos:
        print("Nenhum produto encontrado.")
        return []

    for i, produto in enumerate(produtos):
        print(f"\nProduto nº {i}")
        print(f"ID: {produto.id}")
        print(f"Nome: {produto.nome}")
        print(f"Preço: R$ {produto.preco}")
        print(f"Vendedor: {produto.vendedor_email}")

    return produtos

#INSERT
def insertComprador():
    print("\n#### INSERT COMPRADOR ####")

    nome = input("Digite o nome do comprador: ").strip()
    email = input("Digite o e-mail do comprador: ").strip()

    stmt = session.prepare("""
        INSERT INTO comprador (email, nome, favoritos)
        VALUES (?, ?, ?)
        IF NOT EXISTS
    """)

    resultado = session.execute(stmt, (email, nome, []))

    if resultado.was_applied:
        print("Comprador inserido:", nome)
    else:
        print("Já existe um comprador com esse e-mail.")


def insertVendedor():
    print("\n#### INSERT VENDEDOR ####")

    nome = input("Digite o nome do vendedor: ").strip()
    email = input("Digite o e-mail do vendedor: ").strip()

    stmt = session.prepare("""
        INSERT INTO vendedor (email, nome)
        VALUES (?, ?)
        IF NOT EXISTS
    """)

    resultado = session.execute(stmt, (email, nome))

    if resultado.was_applied:
        print("Vendedor inserido:", nome)
    else:
        print("Já existe um vendedor com esse e-mail.")


def insertProduto():
    print("\n#### INSERT PRODUTO ####")

    nome = input("Digite o nome do produto: ").strip()
    preco = Decimal(input("Digite o preço do produto: ").strip().replace(",", "."))
    vendedor = input("Digite o e-mail do vendedor").strip()

    vendedor_existente = session.execute(
        "SELECT email FROM vendedor WHERE email = %s",
        (vendedor,)
    ).one()

    if not vendedor_existente:
        print("Vendedor não encontrado.")
        return

    produto_id = uuid.uuid4()

    stmt = session.prepare("""
        INSERT INTO produtos (
            id, nome, preco, vendedor_email
        )
        VALUES (?, ?, ?, ?)
    """)

    session.execute(
        stmt,
        (produto_id, nome, preco, vendedor)
    )

    print("Produto inserido:", nome)
    print("ID do produto:", produto_id)


def insertCompra():
    print("\n#### INSERT COMPRA ####")

    comprador = input("Digite o e-mail do comprador: ").strip()
    produto = uuid.UUID(input("Digite o id do produto: ").strip())
    pagamento = input("Digite a forma de pagamento (PIX/CARTÃO): ").strip()

    comprador_existente = session.execute(
        "SELECT email FROM comprador WHERE email = %s",
        (comprador,)
    ).one()

    if not comprador_existente:
        print("Comprador não encontrado.")
        return

    produto_existente = session.execute(
        "SELECT id FROM produtos WHERE id = %s",
        (produto,)
    ).one()

    if not produto_existente:
        print("Produto não encontrado.")
        return

    if pagamento not in ["PIX", "CARTÃO"]:
        print("Forma de pagamento inválida.")
        return

    compra_id = uuid.uuid4()

    stmt = session.prepare("""
        INSERT INTO compras (
            id, comprador_email, produto_id, pagamento
        )
        VALUES (?, ?, ?, ?)
    """)

    session.execute(
        stmt,
        (compra_id, comprador, produto, pagamento)
    )

    print("Compra inserida com sucesso!")

#UPDATE
def updateComprador():
    print("\n#### UPDATE COMPRADOR ####")

    email = input("Digite o e-mail do comprador: ").strip()

    comprador = session.execute(
        "SELECT * FROM comprador WHERE email = %s",
        (email,)
    ).one()

    if not comprador:
        print("Este e-mail não está vinculado a nenhum comprador.")
        return

    print("\nDados do comprador:")
    print("------")
    print(f"Nome: {comprador.nome}")
    print(f"E-mail: {comprador.email}")
    print("Favoritos:")

    favoritos = comprador.favoritos or []

    for i, favorito_id in enumerate(favoritos):
        produto = session.execute(
            "SELECT id, nome, preco FROM produtos WHERE id = %s",
            (uuid.UUID(favorito_id),)
        ).one()

        if produto:
            print("-----")
            print(f"Produto nº {i}")
            print(f"Nome: {produto.nome}")
            print(f"Preço: R$ {produto.preco}")

    print("------")

    print("\n- Alteração dos dados do comprador -")

    nome_final = comprador.nome
    email_final = comprador.email
    favoritos_final = list(favoritos)

    nome_alt = input("Mudar nome (Enter para manter): ").strip()

    if nome_alt:
        nome_final = nome_alt

    email_alt = input("Mudar e-mail (Enter para manter): ").strip()

    if email_alt:
        email_existente = session.execute(
            "SELECT email FROM comprador WHERE email = %s",
            (email_alt,)
        ).one()

        if email_existente:
            print(f"O e-mail '{email_alt}' já está em uso.")
        else:
            email_final = email_alt

    adicionar_favorito = input(
        "Deseja adicionar um novo favorito? (S/N): "
    ).strip().upper()

    while adicionar_favorito != 'N':
        if adicionar_favorito != 'S':
            print("--### Opção inválida! ###--")

        else:
            produtos = listarProdutos(pesquisar=False)

            if not produtos:
                print("Nenhum produto disponível.")
            else:
                print("\nProdutos disponíveis:")

                for i, produto in enumerate(produtos):
                    print(f"{i} - {produto.nome} | R$ {produto.preco}")

                escolha = input(
                    "Escolha o número do produto: "
                ).strip()

                if not escolha.isdigit():
                    print("Digite um número válido.")

                else:
                    indice = int(escolha)

                    if 0 <= indice < len(produtos):
                        produto_escolhido = produtos[indice]
                        produto_id = str(produto_escolhido.id)

                        if produto_id in favoritos_final:
                            print("Esse produto já está nos favoritos.")
                        else:
                            favoritos_final.append(produto_id)
                            print("Produto adicionado aos favoritos.")

                    else:
                        print("Número de produto inválido.")

        adicionar_favorito = input(
            "\nDeseja adicionar outro favorito? (S/N): "
        ).strip().upper()

    if (
        nome_final == comprador.nome
        and email_final == comprador.email
        and favoritos_final == favoritos
    ):
        print("\nNenhuma alteração realizada.")
        return

    try:
        if email_final != comprador.email:

            stmt = session.prepare("""
                INSERT INTO comprador (email, nome, favoritos)
                VALUES (?, ?, ?)
                IF NOT EXISTS
            """)

            resultado = session.execute(
                stmt,
                (email_final, nome_final, favoritos_final)
            )

            if not resultado.was_applied:
                print("Não foi possível alterar o e-mail.")
                print("O novo e-mail já está cadastrado.")
                return

            session.execute(
                "DELETE FROM comprador WHERE email = %s",
                (comprador.email,)
            )
        else:
            stmt = session.prepare("""
                UPDATE comprador
                SET nome = ?, favoritos = ?
                WHERE email = ?
            """)

            session.execute(
                stmt,
                (nome_final, favoritos_final, comprador.email)
            )
            
        print("\nComprador alterado com sucesso.")
    except Exception as erro:
        print("\nNão foi possível alterar o comprador.")
        print(erro)

#DELETE
def deleteCompra():
    print("\n#### DELETAR COMPRA ####")

    compras = session.execute("""
        SELECT id, comprador_email, produto_id, pagamento
        FROM compras
    """).all()

    if not compras:
        print("Nenhuma compra cadastrada.")
        return

    print("\nCompras registradas:")
    print("------------------------------")

    for i, compra in enumerate(compras):
        print(f"Compra nº {i}")
        print(f"ID: {compra.id}")
        print(f"Comprador: {compra.comprador_email}")
        print(f"Produto ID: {compra.produto_id}")
        print(f"Pagamento: {compra.pagamento}")
        print("------------------------------")

    escolha = input(
        "Digite o número da compra que deseja excluir: "
    ).strip()

    if not escolha.isdigit():
        print("Digite um número válido.")
        return

    indice = int(escolha)

    if not 0 <= indice < len(compras):
        print("Número de compra inválido.")
        return

    compra_escolhida = compras[indice]

    confirmacao = input(
        "Deseja realmente excluir esta compra? (S/N): "
    ).strip().upper()

    if confirmacao != "S":
        print("Exclusão cancelada.")
        return

    try:
        stmt = session.prepare("""
            DELETE FROM compras
            WHERE id = ?
        """)

        session.execute(stmt, (compra_escolhida.id,))

        print("Compra excluída com sucesso.")

    except Exception as erro:
        print("Não foi possível excluir a compra.")
        print(erro)