from __future__ import annotations
import sqlite3
from typing import List, Tuple
from ..domain.models import AtivoBase

class DatabaseConnection:
    _instance = None
    def __new__(cls, db_name: str = "portfolio.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(db_name, check_same_thread=False)
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

class PortfolioDB:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.db = DatabaseConnection()
        self._criar_tabela()

    def _criar_tabela(self):
        self.db.cursor.execute(
            """CREATE TABLE IF NOT EXISTS portfolio(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
                preco REAL NOT NULL CHECK (preco >= 0),
                tipo TEXT NOT NULL
            )"""
        )
        self.db.conn.commit()

    def adicionar_ativo(self, user_id: int, ativo: AtivoBase):
        self.db.cursor.execute(
            "INSERT INTO portfolio (user_id, nome, quantidade, preco, tipo) VALUES (?,?,?,?,?)",
            (user_id, ativo.nome, ativo.quantidade, ativo.preco, ativo.tipo),
        )
        self.db.conn.commit()

    def listar_carteira(self, user_id: int) -> List[Tuple[str,int,float,str]]:
        self.db.cursor.execute("SELECT nome, quantidade, preco, tipo FROM portfolio WHERE user_id = ?", (user_id,))
        return self.db.cursor.fetchall()

    def calcular_valor_total(self, user_id: int) -> float:
        self.db.cursor.execute("SELECT quantidade, preco FROM portfolio WHERE user_id = ?", (user_id,))
        return sum(q*p for (q,p) in self.db.cursor.fetchall())

    def obter_ultimo(self, user_id: int):
        self.db.cursor.execute(
            "SELECT nome, quantidade, preco, tipo FROM portfolio WHERE user_id=? ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        return self.db.cursor.fetchone()
