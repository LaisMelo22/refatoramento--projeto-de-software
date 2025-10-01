from __future__ import annotations
import copy
from ..domain.models import OutroAtivo

class AtivoPrototype(OutroAtivo):
    @property
    def tipo(self): return "prototype"
    def clone(self):
        return copy.deepcopy(self)
