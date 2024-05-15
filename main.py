import sqlite3
import textwrap

from bd import criar_bd, criar_conexao
from servico import ClienteServico

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tNovo cliente
    [2]\tListar clientes
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.row_factory = sqlite3.Row

        criar_bd(cursor=cursor)

        servico = ClienteServico(cursor=cursor)

        while True:
            opcao = menu()
            if opcao == "1":
                try:
                    servico.criar_cliente()
                    conexao.commit()
                    print("\n=== Cliente criado com sucesso! ===")
                except Exception as e:
                    conexao.rollback()
                    print(f"\n@@@ Erro ao criar cliente: {e} @@@")
            elif opcao == "2":
                try:
                    servico.listar_clientes()
                except Exception as e:
                    print(f"\n@@@ Erro ao listar clientes: {e} @@@")
            elif opcao == "0":
                print("\n=== Saindo... ===")
                break
            else:
                print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

    except sqlite3.Error as e:
        print(f"\n@@@ Erro na conexão com o banco de dados: {e} @@@")
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    main()
