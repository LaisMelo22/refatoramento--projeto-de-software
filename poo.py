import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import copy


# SINGLETON para conexão DB

class DatabaseConnection:
    _instance = None

    def __new__(cls, db_name="portfolio.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(db_name)
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance


# MONOSTATE (Borg)

class PortfolioDB:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.db = DatabaseConnection()
        self._criar_tabela()

    def _criar_tabela(self):
        self.db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            tipo TEXT NOT NULL
        )
        """)
        self.db.conn.commit()

    def adicionar_ativo(self, user_id, ativo):
        self.db.cursor.execute(
            "INSERT INTO portfolio (user_id, nome, quantidade, preco, tipo) VALUES (?, ?, ?, ?, ?)",
            (user_id, ativo.nome, ativo.quantidade, ativo.preco, ativo.tipo)
        )
        self.db.conn.commit()

    def listar_carteira(self, user_id):
        self.db.cursor.execute("SELECT nome, quantidade, preco, tipo FROM portfolio WHERE user_id = ?", (user_id,))
        return self.db.cursor.fetchall()

    def calcular_valor_total(self, user_id):
        self.db.cursor.execute("SELECT quantidade, preco FROM portfolio WHERE user_id = ?", (user_id,))
        ativos = self.db.cursor.fetchall()
        return sum(qtd * preco for qtd, preco in ativos)


# CLASSES DE ATIVO

class AtivoBase(ABC):
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    @property
    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def descricao(self):
        pass

    def calcular_total(self):
        return self.quantidade * self.preco

# HERANÇA + POLIMORFISMO
class Acao(AtivoBase):
    @property
    def tipo(self): return "acao"

    def descricao(self):
        return f"Ação: {self.nome} - {self.quantidade} x R${self.preco:.2f}"

class Cripto(AtivoBase):
    @property
    def tipo(self): return "cripto"

    def descricao(self):
        return f"Criptomoeda: {self.nome.upper()} - {self.quantidade} x R${self.preco:.2f}"

class OutroAtivo(AtivoBase):
    @property
    def tipo(self): return "outro"

    def descricao(self):
        return f"Ativo Genérico: {self.nome} - {self.quantidade} x R${self.preco:.2f}"


# FACTORY METHOD

class AtivoFactory:
    @staticmethod
    def criar(tipo, nome, quantidade, preco):
        if tipo == "acao":
            return Acao(nome, quantidade, preco)
        elif tipo == "cripto":
            return Cripto(nome, quantidade, preco)
        else:
            return OutroAtivo(nome, quantidade, preco)


# ABSTRACT FACTORY

class AbstractAtivoFactory(ABC):
    @abstractmethod
    def criar_ativo(self, nome, quantidade, preco): pass

class AcaoFactory(AbstractAtivoFactory):
    def criar_ativo(self, nome, quantidade, preco):
        return Acao(nome, quantidade, preco)

class CriptoFactory(AbstractAtivoFactory):
    def criar_ativo(self, nome, quantidade, preco):
        return Cripto(nome, quantidade, preco)


# BUILDER

class AtivoBuilder:
    def __init__(self):
        self._nome = None
        self._quantidade = 0
        self._preco = 0.0
        self._tipo = "outro"

    def set_nome(self, nome): self._nome = nome; return self
    def set_quantidade(self, qtd): self._quantidade = qtd; return self
    def set_preco(self, preco): self._preco = preco; return self
    def set_tipo(self, tipo): self._tipo = tipo; return self

    def build(self):
        return AtivoFactory.criar(self._tipo, self._nome, self._quantidade, self._preco)


# PROTOTYPE

class AtivoPrototype(AtivoBase):
    @property
    def tipo(self): return "prototype"

    def descricao(self): return f"Clone de {self.nome} ({self.quantidade} x R${self.preco:.2f})"

    def clone(self):
        return copy.deepcopy(self)


# CLASSE Portfolio (objeto do usuário)

class Portfolio:
    def __init__(self, user_id):
        self.user_id = user_id
        self.ativos = []
        self.saldo = 0.0
        self.db = PortfolioDB()

    def adicionar_ativo(self, ativo):
        self.ativos.append(ativo)
        self.db.adicionar_ativo(self.user_id, ativo)

    def calcular_valor_total(self):
        return self.db.calcular_valor_total(self.user_id)

    def listar_carteira(self):
        return self.db.listar_carteira(self.user_id)

# INTERFACE
class PortfolioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Portfólio - Padrões de Projeto")
        self.geometry("850x600")

        # User ID
        ctk.CTkLabel(self, text="User ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_user = ctk.CTkEntry(self, width=100)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Nome ativo
        ctk.CTkLabel(self, text="Nome do ativo:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_nome = ctk.CTkEntry(self, width=200)
        self.entry_nome.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Quantidade
        ctk.CTkLabel(self, text="Quantidade:").grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.entry_qtd = ctk.CTkEntry(self, width=100)
        self.entry_qtd.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Preço
        ctk.CTkLabel(self, text="Preço unitário:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_preco = ctk.CTkEntry(self, width=100)
        self.entry_preco.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Tipo
        ctk.CTkLabel(self, text="Tipo:").grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.tipo_var = ctk.StringVar(value="acao")
        self.tipo_menu = ctk.CTkOptionMenu(self, values=["acao", "cripto", "outro"], variable=self.tipo_var)
        self.tipo_menu.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        # Botões
        ctk.CTkButton(self, text="Adicionar Ativo", command=self.adicionar_ativo).grid(row=3, column=0, padx=10, pady=15)
        ctk.CTkButton(self, text="Listar Carteira", command=self.listar_carteira).grid(row=3, column=1, padx=10, pady=15)
        ctk.CTkButton(self, text="Calcular Total", command=self.calcular_total).grid(row=3, column=2, padx=10, pady=15)

        # TreeView
        self.tree = ttk.Treeview(
            self,
            columns=("Nome", "Quantidade", "Preço", "Tipo", "Total"),
            show="headings",
            height=15
        )
        for col in ("Nome", "Quantidade", "Preço", "Tipo", "Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=15, sticky="nsew")

        # Label total
        self.label_total = ctk.CTkLabel(self, text="Valor total: R$0.00", font=("Arial", 16))
        self.label_total.grid(row=5, column=0, columnspan=4, pady=10)

        self.user_portfolio = None

    def adicionar_ativo(self):
        try:
            user_id = int(self.entry_user.get())
            nome = self.entry_nome.get()
            qtd = int(self.entry_qtd.get())
            preco = float(self.entry_preco.get())
            tipo = self.tipo_var.get()

            if not self.user_portfolio or self.user_portfolio.user_id != user_id:
                self.user_portfolio = Portfolio(user_id)

            # Builder Pattern
            ativo = AtivoBuilder().set_nome(nome).set_quantidade(qtd).set_preco(preco).set_tipo(tipo).build()
            self.user_portfolio.adicionar_ativo(ativo)

            self.listar_carteira()
            messagebox.showinfo("Sucesso", f"Ativo {nome} adicionado!")

            self.entry_nome.delete(0, "end")
            self.entry_qtd.delete(0, "end")
            self.entry_preco.delete(0, "end")

        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

    def listar_carteira(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            user_id = int(self.entry_user.get())
            ativos = PortfolioDB().listar_carteira(user_id)

            for nome, qtd, preco, tipo in ativos:
                total = qtd * preco
                self.tree.insert("", "end", values=(nome, qtd, f"{preco:.2f}", tipo, f"{total:.2f}"))

        except ValueError:
            messagebox.showerror("Erro", "Digite um User ID válido!")

    def calcular_total(self):
        try:
            user_id = int(self.entry_user.get())
            total = PortfolioDB().calcular_valor_total(user_id)
            self.label_total.configure(text=f"Valor total: R${total:.2f}")
        except ValueError:
            messagebox.showerror("Erro", "Digite um User ID válido!")


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = PortfolioApp()
    app.mainloop()
