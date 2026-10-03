# PRD - Sistema de Analise de Elegibilidade de Emprestimo Pessoal

## 1. Visao Geral
O **Analisador de Emprestimo** e um modulo deterministico encarregado de avaliar solicitacoes de credito pessoal para pessoas fisicas com base em idade, renda, valor solicitado, numero de parcelas, pontuacao de credito (score) e restricoes cadastrais.

## 2. Regras de Negocio (RN)
* **RN01 (Maioridade):** O solicitante deve ter no minimo 18 anos completos. Idade negativa gera excecao de valor (`ValueError`).
* **RN02 (Restricao Cadastral):** Solicitantes com restricao ativa no CPF (`possui_restricao = True`) sao automaticamente **REPROVADOS**.
* **RN03 (Incapacidade Financeira e Score Critico):** Se o score de credito for inferior a 300 OU o comprometimento da renda mensal pela parcela for superior a 50% (`> 0.50`), o emprestimo e **REPROVADO**.
* **RN04 (Aprovação Direta):** Se o score de credito for maior ou igual a 700 E o comprometimento da renda for menor ou igual a 30% (`<= 0.30`) (sem restricoes), o emprestimo e **APROVADO**.
* **RN05 (Analise Manual):** Demais casos validos que nao se enquadram na Aprovacao Direta nem na Reprovacao sao encaminhados para **ANALISE_MANUAL**.

## 3. Tabela de Particionamento de Equivalencia (EP) e Analise de Valor Limite (BVA)

| Variavel | Particao Invalida | Particao Valida | Fronteiras / Limites (BVA) |
| :--- | :--- | :--- | :--- |
| **Idade** | `< 18` (Gera ValueError) | `>= 18` | `17` (Erro), `18` (Valido), `19` (Valido) |
| **Score** | `< 0` ou `> 1000` | `0 a 1000` | `-1` (Erro), `0`, `299` (Reprovado), `300` (Manual), `699` (Manual), `700` (Aprovado/Manual), `1000` |
| **Comprometimento Renda** | `<= 0%` | `0.01% a 100%` | `30%` (`0.30`), `30.01%` (`0.3001`), `50%` (`0.50`), `50.01%` (`0.5001`) |
| **Parcelas** | `<= 0` ou `> 120` | `1 a 120` | `0` (Erro), `1` (Valido), `120` (Valido), `121` (Erro) |
