from __future__ import annotations
from abc import ABC, abstractmethod
import json

class Renderer(ABC):
    @abstractmethod
    def render(self, itens) -> str: ...

class TextoRenderer(Renderer):
    def render(self, itens) -> str:
        lines = [f"{n} x{q} R${p:.2f} ({t})" for (n,q,p,t) in itens]
        return "\n".join(lines)

class JsonRenderer(Renderer):
    def render(self, itens) -> str:
        data = [{"nome":n,"quantidade":q,"preco":p,"tipo":t} for (n,q,p,t) in itens]
        return json.dumps(data, ensure_ascii=False, indent=2)

class Relatorio:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
    def gerar(self, itens) -> str:
        return self.renderer.render(itens)
