# portfolio-padroes-v2
Aplicativo desktop (CustomTkinter + SQLite) demonstrando **Abstract Factory, Builder, Factory Method, Monostate (Borg), Prototype, Singleton, Implementação (Bridge)**.

## Instalar e executar
```bash
pip install -e .
portfolio-padroes-v2
# ou
python -m portfolio_padroes_v2.main
```

## Onde está cada padrão
- **Singleton**: `data/db.py` → `DatabaseConnection`
- **Monostate (Borg)**: `data/db.py` → `PortfolioDB`
- **Factory Method**: `creation/factory.py` → `AtivoFactory.criar(...)`
- **Abstract Factory**: `creation/abstract_factory.py` → `AcaoFactory`, `CriptoFactory`, `OutroFactory`
- **Builder**: `creation/builder.py` → `AtivoBuilder`
- **Prototype**: `creation/prototype.py` → `AtivoPrototype` (botão “Clonar Último”)
- **Implementação (Bridge)**: `implementacao/relatorio.py` → `Relatorio` + `TextoRenderer`/`JsonRenderer` (botão “Exportar Relatório`)
