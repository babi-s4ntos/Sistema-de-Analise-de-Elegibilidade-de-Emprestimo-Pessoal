from enum import Enum
from dataclasses import dataclass


class StatusEmprestimo(str, Enum):
    APROVADO = "APROVADO"
    ANALISE_MANUAL = "ANALISE_MANUAL"
    REPROVADO = "REPROVADO"


@dataclass
class SolicitacaoEmprestimo:
    idade: int
    renda_mensal: float
    valor_emprestimo: float
    num_parcelas: int
    score_credito: int
    possui_restricao: bool


class AnalisadorEmprestimo:
    """Classe responsavel por avaliar a elegibilidade de emprestimos com regras deterministicas."""

    @staticmethod
    def avaliar(solicitacao: SolicitacaoEmprestimo) -> StatusEmprestimo:
        # 1. Tratamento Defensivo - Validacao de Tipos
        if not isinstance(solicitacao.idade, int) or isinstance(solicitacao.idade, bool):
            raise TypeError("A idade deve ser um numero inteiro.")
        if not isinstance(solicitacao.score_credito, int) or isinstance(solicitacao.score_credito, bool):
            raise TypeError("O score de credito deve ser um numero inteiro.")
        if not isinstance(solicitacao.renda_mensal, (int, float)) or isinstance(solicitacao.renda_mensal, bool):
            raise TypeError("A renda mensal deve ser numerica.")
        if not isinstance(solicitacao.valor_emprestimo, (int, float)) or isinstance(solicitacao.valor_emprestimo, bool):
            raise TypeError("O valor do emprestimo deve ser numerico.")
        if not isinstance(solicitacao.num_parcelas, int) or isinstance(solicitacao.num_parcelas, bool):
            raise TypeError("O numero de parcelas deve ser um numero inteiro.")
        if not isinstance(solicitacao.possui_restricao, bool):
            raise TypeError("A restricao cadastral deve ser um valor booleano.")

        # 2. Tratamento Defensivo - Validacao de Dominio/Valores
        if solicitacao.idade < 0:
            raise ValueError("Idade nao pode ser negativa.")
        if solicitacao.idade < 18:
            raise ValueError("Solicitante deve ser maior de idade (18+ anos).")
        if solicitacao.renda_mensal <= 0:
            raise ValueError("A renda mensal deve ser maior que zero.")
        if solicitacao.valor_emprestimo <= 0:
            raise ValueError("O valor do emprestimo deve ser maior que zero.")
        if solicitacao.num_parcelas <= 0 or solicitacao.num_parcelas > 120:
            raise ValueError("O numero de parcelas deve estar entre 1 e 120.")
        if solicitacao.score_credito < 0 or solicitacao.score_credito > 1000:
            raise ValueError("O score de credito deve estar entre 0 e 1000.")

        # 3. Regra RN02: Restricao cadastral reprova imediatamente
        if solicitacao.possui_restricao:
            return StatusEmprestimo.REPROVADO

        valor_parcela = solicitacao.valor_emprestimo / solicitacao.num_parcelas
        comprometimento_renda = valor_parcela / solicitacao.renda_mensal

        # 4. Regra RN03: Score muito baixo (< 300) ou comprometimento alto (> 50%)
        if solicitacao.score_credito < 300 or comprometimento_renda > 0.50:
            return StatusEmprestimo.REPROVADO

        # 5. Regra RN04: Aprovacao Direta (Score >= 700 e Comprometimento <= 30%)
        if solicitacao.score_credito >= 700 and comprometimento_renda <= 0.30:
            return StatusEmprestimo.APROVADO

        # 6. Regra RN05: Demais casos entram em analise manual
        return StatusEmprestimo.ANALISE_MANUAL
