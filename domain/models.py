from __future__ import annotations
from abc import ABC, abstractmethod

class AtivoBase(ABC):
    def __init__(self, nome: str, quantidade: int, preco: float):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    @property
    @abstractmethod
    def tipo(self) -> str: ...

    def descricao(self) -> str:
        return f"{self.tipo.title()}: {self.nome} - {self.quantidade} x R${self.preco:.2f}"

    def calcular_total(self) -> float:
        return float(self.quantidade) * float(self.preco)


class Acao(AtivoBase):
    @property
    def tipo(self) -> str: return "acao"


class Cripto(AtivoBase):
    @property
    def tipo(self) -> str: return "cripto"


class OutroAtivo(AtivoBase):
    @property
    def tipo(self) -> str: return "outro"
