from __future__ import annotations
from ..domain.models import Acao, Cripto, OutroAtivo, AtivoBase

class AtivoFactory:
    @staticmethod
    def criar(tipo: str, nome: str, quantidade: int, preco: float) -> AtivoBase:
        t = (tipo or "outro").lower()
        if t == "acao":
            return Acao(nome, quantidade, preco)
        if t == "cripto":
            return Cripto(nome, quantidade, preco)
        return OutroAtivo(nome, quantidade, preco)
