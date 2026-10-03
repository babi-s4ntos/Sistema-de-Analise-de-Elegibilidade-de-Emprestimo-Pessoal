import pytest
from app.loan_approval import AnalisadorEmprestimo, SolicitacaoEmprestimo, StatusEmprestimo


@pytest.mark.unit
class TestAnalisadorEmprestimoEPandBVA:
    """Suite de testes unitarios com padroes AAA, EP, BVA e Error Guessing."""

    # --- 1. TESTES PARAMETRIZADOS DE SUCESSO E FRONTEIRA (BVA / EP) ---
    @pytest.mark.parametrize(
        "score, renda, valor, parcelas, restricao, status_esperado, descricao",
        [
            # EP: Aprovacao Direta
            (700, 10000.0, 30000.0, 10, False, StatusEmprestimo.APROVADO, "BVA: Score exato 700 e DTI 30%"),
            (850, 5000.0, 10000.0, 10, False, StatusEmprestimo.APROVADO, "EP: Score alto e DTI 20%"),
            
            # EP & BVA: Analise Manual (Fronteiras de Score e DTI)
            (699, 10000.0, 30000.0, 10, False, StatusEmprestimo.ANALISE_MANUAL, "BVA: Score 699 (Abaixo de 700)"),
            (700, 10000.0, 31000.0, 10, False, StatusEmprestimo.ANALISE_MANUAL, "BVA: DTI 31% (Acima de 30%)"),
            (300, 10000.0, 50000.0, 10, False, StatusEmprestimo.ANALISE_MANUAL, "BVA: Score limite minimo 300 e DTI 50%"),
            
            # EP & BVA: Reprovacao
            (299, 10000.0, 10000.0, 10, False, StatusEmprestimo.REPROVADO, "BVA: Score 299 (Score critico)"),
            (800, 10000.0, 51000.0, 10, False, StatusEmprestimo.REPROVADO, "BVA: DTI 51% (Acima de 50%)"),
            (800, 10000.0, 10000.0, 10, True, StatusEmprestimo.REPROVADO, "EP: Possui restricao cadastral"),
        ],
    )
    def test_avaliar_status_solicitacao(
        self, score, renda, valor, parcelas, restricao, status_esperado, descricao
    ):
        # Arrange
        solicitacao = SolicitacaoEmprestimo(
            idade=25,
            renda_mensal=renda,
            valor_emprestimo=valor,
            num_parcelas=parcelas,
            score_credito=score,
            possui_restricao=restricao,
        )

        # Act
        resultado = AnalisadorEmprestimo.avaliar(solicitacao)

        # Assert
        assert resultado == status_esperado, f"Falha no cenario: {descricao}"

    # --- 2. ERROR GUESSING & FRONTEIRAS DE IDADE ---
    @pytest.mark.parametrize(
        "idade, mensagem_erro",
        [
            (17, "Solicitante deve ser maior de idade (18+ anos)."),  # BVA Limite inferior invalido
            (-1, "Idade nao pode ser negativa."),                      # Error Guessing: valor negativo
        ],
    )
    def test_validacao_idade_invalida(self, idade, mensagem_erro):
        # Arrange
        solicitacao = SolicitacaoEmprestimo(
            idade=idade,
            renda_mensal=5000.0,
            valor_emprestimo=10000.0,
            num_parcelas=10,
            score_credito=750,
            possui_restricao=False,
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            AnalisadorEmprestimo.avaliar(solicitacao)
        assert mensagem_erro in str(exc_info.value)

    # --- 3. ERROR GUESSING & FRONTEIRAS DE VALORES E PARCELAS ---
    @pytest.mark.parametrize(
        "renda, valor, parcelas, score, mensagem_erro",
        [
            (0.0, 10000.0, 10, 700, "A renda mensal deve ser maior que zero."),
            (5000.0, 0.0, 10, 700, "O valor do emprestimo deve ser maior que zero."),
            (5000.0, 10000.0, 0, 700, "O numero de parcelas deve estar entre 1 e 120."),
            (5000.0, 10000.0, 121, 700, "O numero de parcelas deve estar entre 1 e 120."),
            (5000.0, 10000.0, 10, -1, "O score de credito deve estar entre 0 e 1000."),
            (5000.0, 10000.0, 10, 1001, "O score de credito deve estar entre 0 e 1000."),
        ],
    )
    def test_validacao_valores_fora_do_limite(
        self, renda, valor, parcelas, score, mensagem_erro
    ):
        # Arrange
        solicitacao = SolicitacaoEmprestimo(
            idade=30,
            renda_mensal=renda,
            valor_emprestimo=valor,
            num_parcelas=parcelas,
            score_credito=score,
            possui_restricao=False,
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            AnalisadorEmprestimo.avaliar(solicitacao)
        assert mensagem_erro in str(exc_info.value)

    # --- 4. TRATAMENTO DEFENSIVO - ERROS DE TIPO (TypeError) ---
    @pytest.mark.parametrize(
        "solicitacao_invalida",
        [
            SolicitacaoEmprestimo("30", 5000.0, 10000.0, 10, 700, False),  # Idade str
            SolicitacaoEmprestimo(30, "5000", 10000.0, 10, 700, False),    # Renda str
            SolicitacaoEmprestimo(30, 5000.0, "10000", 10, 700, False),    # Valor str
            SolicitacaoEmprestimo(30, 5000.0, 10000.0, "10", 700, False),   # Parcelas str
            SolicitacaoEmprestimo(30, 5000.0, 10000.0, 10, "700", False),   # Score str
            SolicitacaoEmprestimo(30, 5000.0, 10000.0, 10, 700, "False"),   # Restricao str
            SolicitacaoEmprestimo(True, 5000.0, 10000.0, 10, 700, False),   # Idade bool
        ],
    )
    def test_validacao_tipos_invalidos(self, solicitacao_invalida):
        # Act & Assert
        with pytest.raises(TypeError):
            AnalisadorEmprestimo.avaliar(solicitacao_invalida)
