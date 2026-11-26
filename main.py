from funcoes import (
    createTables,
    listarProdutos,
    insertComprador, 
    insertVendedor, 
    insertProduto, 
    insertCompra, 
    updateComprador,
    deleteCompra
)

while True:
    print()
    print("--###### MENU CASSANDRA ########--")
    print("--## 1 - Inserir Comprador    ##--")
    print("--## 2 - Inserir Vendedor     ##--")
    print("--## 3 - Inserir Produto      ##--")
    print("--## 4 - Inserir Compra       ##--")
    print("--## 5 - Update Comprador     ##--")
    print("--## 6 - Pesquisar Produto    ##--")
    print("--## 7 - Deletar Compra       ##--")
    print("--## 8 - Criar tabelas        ##--")
    print("--##############################--\n")
    
    menuKey = input("Digite a opção desejada (para sair, digite 'sair'): ").strip()

    if menuKey == '1':
        insertComprador()
    elif menuKey == '2':
        insertVendedor()
    elif menuKey == '3':
        insertProduto()
    elif menuKey == '4':
        insertCompra()
    elif menuKey == '5':
        updateComprador()
    elif menuKey == '6':
        listarProdutos()
    elif menuKey == '7':
        deleteCompra()
    elif menuKey == '8':
        createTables()
    elif menuKey == 'sair':
        break
    else:
        print()
        print("--### Opção inválida! ###--")