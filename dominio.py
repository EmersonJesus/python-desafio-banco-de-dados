from dataclasses import dataclass
from typing import Self, Dict, Any

@dataclass
class Cliente:
    email: str
    telefone: str
    status: str

    def __str__(self) -> str:
        texto = ""
        for campo, valor in self.__dict__.items():
            campo = campo.replace("_", " ").capitalize()
            texto += f"{campo}: {valor}\n"
        return texto


@dataclass
class PessoaFisica(Cliente):
    nome: str
    cpf: str
    renda_mensal: float

    @classmethod
    def converter_objeto_bd(cls, objeto_db: Dict[str, Any]) -> Self:
        return cls(
            email=objeto_db["email"],
            telefone=objeto_db["telefone"],
            status=objeto_db["status"],
            nome=objeto_db["nome"],
            cpf=objeto_db["cpf"],
            renda_mensal=objeto_db["renda_mensal"],
        )

    def __str__(self) -> str:
        return super().__str__() + f"Nome: {self.nome}\nCPF: {self.cpf}\nRenda mensal: {self.renda_mensal}\n"


@dataclass
class PessoaJuridica(Cliente):
    nome_fantasia: str
    cnpj: str
    faturamento_anual: float

    @classmethod
    def converter_objeto_bd(cls, objeto_db: Dict[str, Any]) -> Self:
        return cls(
            email=objeto_db["email"],
            telefone=objeto_db["telefone"],
            status=objeto_db["status"],
            nome_fantasia=objeto_db["nome_fantasia"],
            cnpj=objeto_db["cnpj"],
            faturamento_anual=objeto_db["faturamento_anual"],
        )

    def __str__(self) -> str:
        return super().__str__() + f"Nome fantasia: {self.nome_fantasia}\nCNPJ: {self.cnpj}\nFaturamento anual: {self.faturamento_anual}\n"
