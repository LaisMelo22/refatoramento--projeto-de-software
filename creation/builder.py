from __future__ import annotations
from ..domain.models import AtivoBase
from .factory import AtivoFactory

class AtivoBuilder:
    def __init__(self):
        self._nome: str | None = None
        self._quantidade: int = 0
        self._preco: float = 0.0
        self._tipo: str = "outro"

    def set_nome(self, nome: str): self._nome = nome; return self
    def set_quantidade(self, qtd: int): self._quantidade = int(qtd); return self
    def set_preco(self, preco: float): self._preco = float(preco); return self
    def set_tipo(self, tipo: str): self._tipo = tipo; return self

    def build(self) -> AtivoBase:
        if not self._nome: raise ValueError("Nome do ativo não pode ser vazio.")
        if self._quantidade <= 0: raise ValueError("Quantidade deve ser positiva.")
        if self._preco <= 0: raise ValueError("Preço deve ser positivo.")
        return AtivoFactory.criar(self._tipo, self._nome, self._quantidade, self._preco)
