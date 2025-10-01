from __future__ import annotations
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from ..data.db import PortfolioDB
from ..domain.models import AtivoBase
from ..creation.factory import AtivoFactory
from ..creation.abstract_factory import AcaoFactory, CriptoFactory, OutroFactory
from ..creation.builder import AtivoBuilder
from ..creation.prototype import AtivoPrototype
from ..implementacao.relatorio import Relatorio, TextoRenderer, JsonRenderer

class PortfolioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Portfólio — AF/Builder/Factory/Monostate/Singleton/Prototype/Bridge")
        self.geometry("980x680")
        self.db = PortfolioDB()

        # Linha 0
        ctk.CTkLabel(self, text="User ID:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.entry_user = ctk.CTkEntry(self, width=100); self.entry_user.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        ctk.CTkLabel(self, text="Padrão de criação:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.var_padrao = ctk.StringVar(value="Builder")
        ctk.CTkOptionMenu(self, values=["Builder","Factory Method","Abstract Factory"], variable=self.var_padrao).grid(row=0, column=3, padx=8, pady=8, sticky="w")

        # Linha 1
        ctk.CTkLabel(self, text="Nome:").grid(row=1, column=0, padx=8, pady=4, sticky="w")
        self.entry_nome = ctk.CTkEntry(self, width=180); self.entry_nome.grid(row=1, column=1, padx=8, pady=4, sticky="w")

        ctk.CTkLabel(self, text="Quantidade:").grid(row=1, column=2, padx=8, pady=4, sticky="w")
        self.entry_qtd = ctk.CTkEntry(self, width=80); self.entry_qtd.grid(row=1, column=3, padx=8, pady=4, sticky="w")

        ctk.CTkLabel(self, text="Preço unitário:").grid(row=1, column=4, padx=8, pady=4, sticky="w")
        self.entry_preco = ctk.CTkEntry(self, width=100); self.entry_preco.grid(row=1, column=5, padx=8, pady=4, sticky="w")

        ctk.CTkLabel(self, text="Tipo:").grid(row=1, column=6, padx=8, pady=4, sticky="w")
        self.tipo_var = ctk.StringVar(value="acao")
        ctk.CTkOptionMenu(self, values=["acao","cripto","outro"], variable=self.tipo_var).grid(row=1, column=7, padx=8, pady=4, sticky="w")

        # Botões
        ctk.CTkButton(self, text="Adicionar (criação)", command=self.adicionar_ativo).grid(row=2, column=0, padx=8, pady=10)
        ctk.CTkButton(self, text="Listar Carteira", command=self.listar_carteira).grid(row=2, column=1, padx=8, pady=10)
        ctk.CTkButton(self, text="Calcular Total", command=self.calcular_total).grid(row=2, column=2, padx=8, pady=10)
        ctk.CTkButton(self, text="Clonar Último (Prototype)", command=self.clonar_ultimo).grid(row=2, column=3, padx=8, pady=10)

        ctk.CTkLabel(self, text="Relatório (Bridge):").grid(row=2, column=4, padx=8, pady=10, sticky="e")
        self.var_formato = ctk.StringVar(value="txt")
        ctk.CTkOptionMenu(self, values=["txt","json"], variable=self.var_formato).grid(row=2, column=5, padx=8, pady=10, sticky="w")
        ctk.CTkButton(self, text="Exportar Relatório", command=self.exportar_relatorio).grid(row=2, column=6, padx=8, pady=10)

        # Tabela
        self.tree = ttk.Treeview(self, columns=("Nome","Quantidade","Preço","Tipo","Total"), show="headings", height=18)
        for col in ("Nome","Quantidade","Preço","Tipo","Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160 if col == "Nome" else 120)
        self.tree.grid(row=3, column=0, columnspan=8, padx=8, pady=12, sticky="nsew")

        self.label_total = ctk.CTkLabel(self, text="Valor total: R$0.00")
        self.label_total.grid(row=4, column=0, columnspan=4, pady=6, sticky="w")

        self.columnconfigure(7, weight=1)
        self.rowconfigure(3, weight=1)

    def _criar_ativo(self, tipo: str, nome: str, qtd: int, preco: float) -> AtivoBase:
        padrao = self.var_padrao.get()
        if padrao == "Builder":
            return (AtivoBuilder()
                    .set_nome(nome)
                    .set_quantidade(qtd)
                    .set_preco(preco)
                    .set_tipo(tipo)
                    .build())
        elif padrao == "Factory Method":
            return AtivoFactory.criar(tipo, nome, qtd, preco)
        else:  # Abstract Factory
            fabrica = {"acao": AcaoFactory(), "cripto": CriptoFactory(), "outro": OutroFactory()}.get(tipo, OutroFactory())
            return fabrica.criar_ativo(nome, qtd, preco)

    def adicionar_ativo(self):
        try:
            user_id = int(self.entry_user.get())
            nome = self.entry_nome.get().strip()
            qtd = int(self.entry_qtd.get())
            preco = float(self.entry_preco.get())
            tipo = self.tipo_var.get()

            ativo = self._criar_ativo(tipo, nome, qtd, preco)
            self.db.adicionar_ativo(user_id, ativo)
            self.listar_carteira()
            messagebox.showinfo("Sucesso", f"{ativo.descricao()} adicionado.")
            self.entry_nome.delete(0,"end"); self.entry_qtd.delete(0,"end"); self.entry_preco.delete(0,"end")
        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos corretamente.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_carteira(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        try:
            user_id = int(self.entry_user.get())
            for (nome, qtd, preco, tipo) in self.db.listar_carteira(user_id):
                total = float(qtd) * float(preco)
                self.tree.insert("", "end", values=(nome, qtd, f"{preco:.2f}", tipo, f"{total:.2f}"))
        except ValueError:
            messagebox.showerror("Erro", "Digite um User ID válido.")

    def calcular_total(self):
        try:
            user_id = int(self.entry_user.get())
            total = self.db.calcular_valor_total(user_id)
            self.label_total.configure(text=f"Valor total: R${total:.2f}")
        except ValueError:
            messagebox.showerror("Erro", "Digite um User ID válido.")

    def clonar_ultimo(self):
        try:
            user_id = int(self.entry_user.get())
            row = self.db.obter_ultimo(user_id)
            if not row:
                messagebox.showwarning("Aviso", "Nenhum ativo para clonar.")
                return
            nome, qtd, preco, _tipo = row
            proto = AtivoPrototype(nome, qtd, preco)
            clone = proto.clone()
            self.db.adicionar_ativo(user_id, clone)
            self.listar_carteira()
            messagebox.showinfo("Prototype", f"Clonado: {clone.descricao()}")
        except ValueError:
            messagebox.showerror("Erro", "Digite um User ID válido.")

    def exportar_relatorio(self):
        try:
            user_id = int(self.entry_user.get())
            itens = self.db.listar_carteira(user_id)
            formato = self.var_formato.get()
            renderer = JsonRenderer() if formato == "json" else TextoRenderer()
            rel = Relatorio(renderer)
            conteudo = rel.gerar(itens)

            ext = "json" if formato == "json" else "txt"
            path = filedialog.asksaveasfilename(defaultextension=f".{ext}", filetypes=[("Text","*.txt"),("JSON","*.json"),("All","*.*")])
            if not path: return
            with open(path, "w", encoding="utf-8") as f:
                f.write(conteudo)
            messagebox.showinfo("Relatório", f"Arquivo salvo em {path}")
        except ValueError:
            messagebox.showerror("Erro", "Digite um User ID válido.")

