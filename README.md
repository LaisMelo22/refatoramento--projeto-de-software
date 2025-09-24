# Projeto Orientado a Objetos: Gerenciamento de Portfólio

## Descrição do Projeto
Este módulo é uma funcionalidade de um sistema de **Negociação Automatizada**. Ele permite o **controle e acompanhamento de carteiras de investimento**, incluindo:

- Adição de ativos (ações, criptomoedas e outros tipos)  
- Cálculo do valor total investido  
- Visualização da carteira em uma interface gráfica interativa  

O sistema foi desenvolvido seguindo **conceitos de Programação Orientada a Objetos (POO)** e **padrões de projeto**.

---

## Classes Principais

### 1. `Portfolio`
- Representa a carteira de investimentos de um usuário.  
- **Atributos**:
  - `user_id`: identificador do usuário
  - `ativos`: lista de ativos na carteira
  - `saldo`: saldo disponível do usuário (float)
- **Métodos**:
  - `adicionar_ativo(ativo)`: adiciona um ativo à carteira e ao banco de dados
  - `calcular_valor_total()`: calcula o valor total investido
  - `listar_carteira()`: retorna a lista de ativos

### 2. `AtivoBase` (Classe Abstrata)
- Base para todos os tipos de ativos (Ação, Cripto, Outro)  
- **Métodos abstratos**:
  - `tipo()`: retorna o tipo do ativo
  - `descricao()`: retorna descrição detalhada do ativo

### 3. `Acao`, `Cripto`, `OutroAtivo`
- Herança de `AtivoBase`  
- Implementam polimorfismo no método `descricao()`

### 4. `AtivoFactory` (Factory Method)
- Cria ativos do tipo correto com base em um parâmetro `tipo`

### 5. `AbstractAtivoFactory` (Abstract Factory)
- Cria fábricas de ativos específicas (`AcaoFactory`, `CriptoFactory`)  

### 6. `AtivoBuilder` (Builder)
- Permite criar ativos passo a passo configurando nome, quantidade, preço e tipo

### 7. `AtivoPrototype` (Prototype)
- Permite clonar ativos já existentes usando o método `clone()`

### 8. `PortfolioDB` (Monostate / Borg)
- Classe responsável pela persistência no banco SQLite  
- Todas as instâncias compartilham o mesmo estado (conexão e cursor)  
- Métodos:
  - `adicionar_ativo(user_id, ativo)`
  - `listar_carteira(user_id)`
  - `calcular_valor_total(user_id)`

### 9. `DatabaseConnection` (Singleton)
- Garante que exista apenas **uma conexão única** com o banco de dados

### 10. `PortfolioApp` (GUI)
- Interface desenvolvida com **CustomTkinter**  
- Campos para entrada de `User ID`, `Nome do Ativo`, `Quantidade`, `Preço` e `Tipo`  
- Botões para adicionar ativo, listar carteira e calcular valor total  
- TreeView exibe os ativos e o valor total da carteira

---

## Padrões de Projeto Implementados

| Padrão            | Onde foi usado                                               |
|------------------|-------------------------------------------------------------|
| Abstract Factory  | `AbstractAtivoFactory`, `AcaoFactory`, `CriptoFactory`      |
| Builder           | `AtivoBuilder`                                              |
| Factory Method    | `AtivoFactory`                                              |
| Monostate (Borg)  | `PortfolioDB`                                               |
| Prototype         | `AtivoPrototype`                                           |
| Singleton         | `DatabaseConnection`                                        |
| Implementação     | Integrado em toda a gestão de carteira e GUI               |

---

## Como Rodar
1. Apagar o arquivo `portfolio.db` (para recriar a tabela corretamente com a coluna `tipo`)  
2. Instalar dependências:
   ```bash
   pip install customtkinter
