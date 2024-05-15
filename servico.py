from sqlite3 import Cursor
from dominio import Cliente, PessoaFisica, PessoaJuridica

class ClienteServico:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def filtrar_cliente(self, documento: str) -> int:
        if len(documento) == 11:
            self.cursor.execute("SELECT COUNT(*) AS total FROM pessoa_fisica WHERE cpf=?;", (documento,))
        elif len(documento) == 14:
            self.cursor.execute("SELECT COUNT(*) AS total FROM pessoa_juridica WHERE cnpj=?;", (documento,))
        else:
            raise ValueError("Documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).")
        return self.cursor.fetchone()["total"]

    def _criar_cliente_pessoa_fisica(self, documento: str) -> PessoaFisica:
        nome = input("Informe o nome completo: ").strip()
        renda_mensal = float(input("Informe sua renda mensal: ").strip())
        email = input("Informe seu email: ").strip()
        telefone = input("Informe seu telefone: ").strip()

        return PessoaFisica(
            nome=nome, cpf=documento, renda_mensal=renda_mensal, email=email, telefone=telefone, status="ativo"
        )

    def _criar_cliente_pessoa_juridica(self, documento: str) -> PessoaJuridica:
        nome = input("Informe o nome fantasia: ").strip()
        faturamento_anual = float(input("Informe seu faturamento anual: ").strip())
        email = input("Informe seu email: ").strip()
        telefone = input("Informe seu telefone: ").strip()

        return PessoaJuridica(
            nome_fantasia=nome,
            cnpj=documento,
            faturamento_anual=faturamento_anual,
            email=email,
            telefone=telefone,
            status="ativo",
        )

    def _criar_cliente(self, cliente: Cliente) -> int:
        self.cursor.execute(
            "INSERT INTO cliente (email, telefone, status) VALUES (?,?,?);",
            (cliente.email, cliente.telefone, cliente.status),
        )
        return self.cursor.lastrowid

    def criar_cliente(self) -> None:
        documento = input("Informe o documento (CPF/CNPJ): ").strip()
        try:
            existe_cliente = self.filtrar_cliente(documento)
        except ValueError as e:
            print(f"\n@@@ {e} @@@")
            return

        if existe_cliente:
            print("\n@@@ Já existe cliente com esse documento (CPF/CNPJ)! @@@")
            return

        if len(documento) == 11:
            cliente = self._criar_cliente_pessoa_fisica(documento=documento)
            cliente_id = self._criar_cliente(cliente=cliente)
            self.cursor.execute(
                "INSERT INTO pessoa_fisica (cliente_id, nome, cpf, renda_mensal) VALUES (?,?,?,?)",
                (cliente_id, cliente.nome, cliente.cpf, cliente.renda_mensal),
            )
        elif len(documento) == 14:
            cliente = self._criar_cliente_pessoa_juridica(documento=documento)
            cliente_id = self._criar_cliente(cliente=cliente)
            self.cursor.execute(
                "INSERT INTO pessoa_juridica (cliente_id, nome_fantasia, cnpj, faturamento_anual) VALUES (?,?,?,?)",
                (cliente_id, cliente.nome_fantasia, cliente.cnpj, cliente.faturamento_anual),
            )

        print("\n=== Cliente criado com sucesso! ===")

    def listar_clientes(self) -> None:
        self.cursor.execute("SELECT * FROM pessoa_fisica pf INNER JOIN cliente c ON c.id = pf.cliente_id;")
        clientes = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM pessoa_juridica pj INNER JOIN cliente c ON c.id = pj.cliente_id;")
        clientes += self.cursor.fetchall()

        if not clientes:
            print("\n@@@ Não existem clientes cadastrados! @@@")
            return

        for cliente in clientes:
            print(self._apresentar_dados(dados_cliente=dict(cliente)))

    def _apresentar_dados(self, dados_cliente: dict[str, str | int]) -> str:
        if "cpf" in dados_cliente:
            return PessoaFisica.converter_objeto_bd(objeto_db=dados_cliente)
        return PessoaJuridica.converter_objeto_bd(objeto_db=dados_cliente)
