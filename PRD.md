# PRD - Sistema de Analise de Elegibilidade de Emprestimo Pessoal

## 1. Visao Geral

O **Analisador de Emprestimo** e um modulo deterministico encarregado de avaliar solicitacoes de credito pessoal para pessoas fisicas com base em idade, renda, valor solicitado, numero de parcelas, pontuacao de credito (score) e restricoes cadastrais.

## 2. Regras de Negocio (RN)

* **RN01 (Maioridade):** O solicitante deve ter no minimo 18 anos completos. Idade negativa ou idade inferior a 18 anos gera excecao de valor (`ValueError`).

* **RN02 (Restricao Cadastral):** Solicitantes com restricao ativa no CPF (`possui_restricao = True`) sao automaticamente **REPROVADOS**.

* **RN03 (Incapacidade Financeira e Score Critico):** Se o score de credito for inferior a 300 OU o comprometimento da renda mensal pela parcela for superior a 50% (`> 0.50`), o emprestimo e **REPROVADO**.

* **RN04 (Aprovacao Direta):** Se o score de credito for maior ou igual a 700 E o comprometimento da renda for menor ou igual a 30% (`<= 0.30`) e nao houver restricao cadastral, o emprestimo e **APROVADO**.

* **RN05 (Analise Manual):** Demais casos validos que nao se enquadram na Aprovacao Direta nem na Reprovacao sao encaminhados para **ANALISE_MANUAL**.

## 3. Tabela de Particionamento de Equivalencia (EP) e Analise de Valor Limite (BVA)

| Variavel                  | Particao Invalida        | Particao Valida | Fronteiras / Limites (BVA)                                                                           |
| :------------------------ | :----------------------- | :-------------- | :--------------------------------------------------------------------------------------------------- |
| **Idade**                 | `< 18` (Gera ValueError) | `>= 18`         | `17` (Erro), `18` (Valido), `19` (Valido)                                                            |
| **Score**                 | `< 0` ou `> 1000`        | `0 a 1000`      | `-1` (Erro), `0`, `299` (Reprovado), `300` (Manual), `699` (Manual), `700` (Aprovado/Manual), `1000` |
| **Comprometimento Renda** | —                        | `0% a 100%`     | `30%` (`0.30`), `30.01%` (`0.3001`), `50%` (`0.50`), `50.01%` (`0.5001`)                             |
| **Parcelas**              | `<= 0` ou `> 120`        | `1 a 120`       | `0` (Erro), `1` (Valido), `120` (Valido), `121` (Erro)                                               |

## 4. Error Guessing

A tecnica de **Error Guessing** foi utilizada para identificar entradas invalidas ou inesperadas que poderiam causar falhas no sistema.

Foram considerados os seguintes cenarios:

* **Idade negativa:** valores menores que zero devem gerar `ValueError`.
* **Idade abaixo da maioridade:** valores entre 0 e 17 anos devem gerar `ValueError`.
* **Renda mensal igual ou inferior a zero:** deve gerar `ValueError`.
* **Valor do emprestimo igual ou inferior a zero:** deve gerar `ValueError`.
* **Numero de parcelas igual a zero ou superior a 120:** deve gerar `ValueError`.
* **Score inferior a 0 ou superior a 1000:** deve gerar `ValueError`.
* **Tipos de dados invalidos:** valores incompatíveis com os tipos esperados, como texto em campos numericos, devem ser rejeitados.
* **Restricao cadastral ativa:** solicitacoes com `possui_restricao = True` devem ser automaticamente classificadas como **REPROVADO**.
