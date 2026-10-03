# Sistema de Análise de Elegibilidade de Empréstimo Pessoal

Projeto prático individual desenvolvido para a disciplina de **Qualidade e Teste de Software (QTS)** — AT1: Engenharia de Testes Unitários, Cobertura de Código e Governança de IA.

O sistema implementa regras de negócio determinísticas para analisar a **elegibilidade de um cliente para um empréstimo pessoal**, considerando critérios como idade, renda, score de crédito, comprometimento de renda e histórico de inadimplência.

O projeto foi desenvolvido em **Python 3.12+**, utilizando **uv** para gerenciamento de dependências e **Pytest** para a implementação da suíte de testes.

---

## 🎯 Objetivo do Projeto

O objetivo é desenvolver um sistema simples de análise de crédito que permita aplicar, de forma prática, conceitos de Engenharia de Testes de Software, incluindo:

* Desenvolvimento de regras de negócio;
* Testes unitários;
* Testes de caixa preta;
* Testes de caixa branca;
* Particionamento de Equivalência (EP);
* Análise do Valor Limite (BVA);
* Error Guessing;
* Testes parametrizados;
* Padrão AAA — Arrange, Act, Assert;
* Cobertura de código;
* Cobertura de ramificações (branches);
* Tratamento defensivo de entradas inválidas;
* Type Hints;
* Governança e transparência no uso de Inteligência Artificial.

---

# 📋 Domínio do Sistema

O sistema pertence ao domínio de **análise de elegibilidade para empréstimo pessoal**.

A partir dos dados fornecidos pelo cliente, o sistema verifica se ele atende aos critérios definidos nas regras de negócio.

### Dados analisados

O sistema considera informações como:

| Informação               | Descrição                                    |
| ------------------------ | -------------------------------------------- |
| Idade                    | Idade do solicitante                         |
| Renda mensal             | Renda mensal comprovada                      |
| Score de crédito         | Pontuação de crédito do cliente              |
| Comprometimento de renda | Percentual da renda já comprometida          |
| Inadimplência            | Indica se existem registros de inadimplência |

O resultado da análise é determinístico: para uma mesma entrada, o sistema deve produzir sempre o mesmo resultado.

---

# 📖 Especificação das Regras

As regras de negócio completas estão documentadas no arquivo:

```text
PRD.md
```

As regras são utilizadas como base para a implementação do sistema e para a criação dos casos de teste.

Exemplos de critérios avaliados:

* idade mínima e máxima permitida;
* renda mínima;
* score mínimo;
* limite de comprometimento de renda;
* existência de inadimplência;
* validação de valores inválidos ou inesperados.

> Os valores exatos dos limites utilizados pelo sistema estão definidos no `PRD.md`, que representa a fonte de verdade das regras de negócio.

---

# 🧪 Estratégia de Testes

A suíte de testes foi desenvolvida utilizando **Pytest** e organizada para cobrir diferentes técnicas de Engenharia de Testes.

Os testes estão localizados no diretório:

```text
tests/
```

## Padrão AAA

Os testes seguem o padrão:

### Arrange

Preparação dos dados e condições necessárias para o teste.

### Act

Execução da função ou regra que está sendo testada.

### Assert

Verificação do resultado esperado.

Exemplo conceitual:

```python
def test_cliente_elegivel():
    # Arrange
    cliente = Cliente(
        idade=30,
        renda=5000,
        score=750,
        comprometimento=20,
        inadimplente=False
    )

    # Act
    resultado = analisar_elegibilidade(cliente)

    # Assert
    assert resultado.elegivel is True
```

---

# 🔬 Técnicas de Teste Aplicadas

## 1. Particionamento de Equivalência — EP

O Particionamento de Equivalência divide as entradas em grupos que devem apresentar comportamento semelhante.

Exemplo para idade:

| Partição         | Exemplo | Resultado esperado |
| ---------------- | ------: | ------------------ |
| Abaixo do limite |      17 | Inválido           |
| Dentro da faixa  |      30 | Válido             |
| Acima do limite  |      70 | Conforme regra     |
| Valor inválido   |      -1 | Erro               |

A técnica reduz a necessidade de testar todas as possibilidades existentes, concentrando os testes em classes representativas.

---

## 2. Análise do Valor Limite — BVA

A Análise do Valor Limite verifica valores próximos às fronteiras das regras.

Para uma regra com limite mínimo, são considerados cenários como:

```text
limite - 1
limite
limite + 1
```

Exemplo:

```text
Idade mínima permitida = 18

17 → inválido
18 → válido
19 → válido
```

Os testes de BVA são aplicados principalmente nas regras que possuem limites numéricos.

---

## 3. Error Guessing

Também foram considerados cenários de entradas inesperadas que podem causar falhas na aplicação.

Exemplos:

* valores negativos;
* idade impossível;
* renda negativa;
* score fora da faixa esperada;
* comprometimento de renda inválido;
* tipos incorretos;
* valores vazios;
* dados ausentes;
* valores extremos.

Esses testes têm o objetivo de verificar o comportamento defensivo da aplicação.

---

# 🧩 Testes Parametrizados

Para evitar repetição de código e permitir a execução de diversos cenários utilizando a mesma estrutura, foram utilizados testes parametrizados com:

```python
@pytest.mark.parametrize
```

Exemplo:

```python
@pytest.mark.parametrize(
    "idade, esperado",
    [
        (17, False),
        (18, True),
        (19, True),
    ],
)
def test_idade(idade, esperado):
    # Arrange
    ...

    # Act
    resultado = ...

    # Assert
    assert resultado == esperado
```

Essa abordagem permite representar diferentes casos de teste de forma organizada e facilita a manutenção da suíte.

---

# 🏷️ Marcação dos Testes

Os testes unitários são identificados utilizando a marcação:

```python
@pytest.mark.unit
```

Isso permite executar especificamente os testes unitários do projeto.

Exemplo:

```bash
uv run pytest -m unit
```

---

# 🧱 Implementação do Domínio

A implementação das regras de negócio está localizada no diretório:

```text
app/
```

O código foi desenvolvido utilizando:

* Python 3.12+;
* Type Hints;
* funções e estruturas de domínio;
* validação de entradas;
* tratamento defensivo de exceções;
* regras determinísticas;
* separação entre código de produção e testes.

---

# 📊 Cobertura de Código

A cobertura é realizada utilizando:

```text
pytest-cov
```

A medição considera tanto:

* cobertura de linhas;
* cobertura de ramificações (branches).

O comando utilizado é:

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

A meta da atividade é:

```text
100% de cobertura de código
100% de cobertura de branches
```

A opção:

```text
--cov-branch
```

é importante porque verifica não apenas se uma linha foi executada, mas também se os diferentes caminhos condicionais da aplicação foram exercitados pelos testes.

---

# 🚀 Instalação

## Requisitos

Antes de executar o projeto, é necessário possuir:

* Python 3.12 ou superior;
* uv;
* Git.

---

## 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entrar no diretório:

```bash
cd nome-do-repositorio
```

---

## 2. Instalar as dependências

O projeto utiliza o `uv` para gerenciamento do ambiente e das dependências.

Execute:

```bash
uv sync
```

---

# ▶️ Execução dos Testes

Para executar toda a suíte de testes:

```bash
uv run pytest -v
```

O comando apresenta individualmente os testes executados e seus respectivos resultados.

Um resultado esperado é semelhante a:

```text
======================== test session starts ========================

collected XX items

tests/test_... PASSED
tests/test_... PASSED
tests/test_... PASSED

========================= XX passed ================================
```

---

# 📈 Execução com Cobertura

Para executar os testes juntamente com a medição de cobertura:

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

O relatório deve apresentar:

```text
TOTAL    100%    100%
```

representando a cobertura das linhas e das ramificações do código de produção.

---

# 🗂️ Estrutura do Projeto

A estrutura esperada do projeto é:

```text
.
├── app/
│   ├── __init__.py
│   └── ...
│
├── tests/
│   ├── __init__.py
│   └── test_*.py
│
├── PRD.md
├── AI_USAGE.md
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

### `app/`

Contém a implementação das regras de negócio do sistema.

### `tests/`

Contém a suíte de testes unitários.

### `PRD.md`

Contém a especificação dos requisitos e regras de negócio.

### `AGENTS.md`

Contém as regras de contexto utilizadas para orientar o desenvolvimento e o uso de IA.

### `AI_USAGE.md`

Documenta a utilização de ferramentas de Inteligência Artificial no desenvolvimento do projeto.

### `pyproject.toml`

Contém as configurações do projeto e suas dependências.

### `uv.lock`

Registra as versões das dependências utilizadas pelo projeto.

---

# 🤖 Governança e Uso de Inteligência Artificial

A utilização de Inteligência Artificial no desenvolvimento do projeto é documentada no arquivo:

```text
AI_USAGE.md
```

O objetivo da documentação é garantir transparência sobre:

* ferramenta de IA utilizada;
* finalidade da utilização;
* partes do projeto nas quais a IA auxiliou;
* validação do código gerado;
* revisão humana;
* execução dos testes;
* correções realizadas após a análise.

A IA é utilizada como ferramenta de apoio ao desenvolvimento, enquanto a validação das regras de negócio e dos resultados dos testes permanece sob responsabilidade do desenvolvedor.

---

# 🔐 Regras de Contexto

As regras utilizadas para orientar ferramentas de IA durante o desenvolvimento estão documentadas em:

```text
AGENTS.md
```

Essas regras estabelecem critérios relacionados a:

* arquitetura;
* estilo do código;
* utilização de Type Hints;
* testes;
* validação;
* segurança;
* tratamento de erros;
* manutenção da separação entre código de produção e testes.

---

# 🧾 Auditoria do Código

Após a implementação das regras e dos testes, o código deve ser validado por meio da execução da suíte completa.

A auditoria considera:

1. Execução dos testes unitários;
2. Verificação dos casos de sucesso;
3. Verificação dos casos de falha;
4. Verificação dos valores limites;
5. Verificação de entradas inválidas;
6. Verificação das ramificações;
7. Análise do relatório de cobertura;
8. Revisão manual das regras de negócio.

Com isso, o resultado da cobertura não é utilizado isoladamente como evidência de qualidade: os casos de teste também são relacionados às regras especificadas no `PRD.md`.

---

# ✅ Checklist da AT1

| Requisito                            | Implementação |
| ------------------------------------ | ------------- |
| Python 3.12+                         | ✅             |
| Gerenciamento com uv                 | ✅             |
| `pyproject.toml`                     | ✅             |
| Regras de negócio                    | ✅             |
| Type Hints                           | ✅             |
| Tratamento defensivo                 | ✅             |
| `PRD.md`                             | ✅             |
| Arquivo de regras de contexto        | ✅             |
| `AI_USAGE.md`                        | ✅             |
| Pytest                               | ✅             |
| Testes unitários                     | ✅             |
| Padrão AAA                           | ✅             |
| Particionamento de Equivalência (EP) | ✅             |
| Análise do Valor Limite (BVA)        | ✅             |
| Error Guessing                       | ✅             |
| `pytest.mark.parametrize`            | ✅             |
| `pytest.mark.unit`                   | ✅             |
| Cobertura de linhas                  | ✅             |
| Cobertura de branches                | ✅             |
| `--cov-branch`                       | ✅             |
| Meta de cobertura de 100%            | ✅             |
| Execução `pytest -v`                 | ✅             |
| Execução com `pytest-cov`            | ✅             |

# 👩‍💻 Autoria

**Bárbara Vitória Ferreira dos Santos**

**Disciplina:** Qualidade e Teste de Software — QTS

**Atividade:** AT1 — Engenharia de Testes Unitários, Cobertura de Código e Governança de IA

**Curso:** Desenvolvimento de Software Multiplataforma — DSM

---

## 📌 Resumo dos comandos

### Instalar dependências

```bash
uv sync
```

### Executar testes

```bash
uv run pytest -v
```

### Executar testes com cobertura

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

### Executar somente testes unitários

```bash
uv run pytest -m unit
```

---

**Projeto desenvolvido para fins acadêmicos na disciplina de Qualidade e Teste de Software (QTS).**
