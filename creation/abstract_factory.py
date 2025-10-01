from __future__ import annotations
from abc import ABC, abstractmethod
from ..domain.models import AtivoBase, Acao, Cripto, OutroAtivo

class AbstractAtivoFactory(ABC):
    @abstractmethod
    def criar_ativo(self, nome: str, quantidade: int, preco: float) -> AtivoBase: ...

class AcaoFactory(AbstractAtivoFactory):
    def criar_ativo(self, nome, quantidade, preco) -> AtivoBase:
        return Acao(nome, quantidade, preco)

class CriptoFactory(AbstractAtivoFactory):
    def criar_ativo(self, nome, quantidade, preco) -> AtivoBase:
        return Cripto(nome, quantidade, preco)

class OutroFactory(AbstractAtivoFactory):
    def criar_ativo(self, nome, quantidade, preco) -> AtivoBase:
        return OutroAtivo(nome, quantidade, preco)
