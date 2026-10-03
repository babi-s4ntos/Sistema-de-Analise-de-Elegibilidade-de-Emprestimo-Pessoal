# Relatorio de Transparencia e Uso de IA (AI_USAGE.md)

## Ferramenta Utilizada
- **Ferramenta:** Claude 3.5 Sonnet / ChatGPT / GitHub Copilot

## Como a IA foi Empregada
1. **Geracao Inicial de Esboco:** Criacao da estrutura inicial do `PRD.md` e mapeamento das tabelas BVA/EP.
2. **Refatoracao de Testes Parametrizados:** Auxilio na construcao dos decorators `@pytest.mark.parametrize` para cenarios de fronteira.

## Processo de Auditoria e Validacao
- **Auditoria Manual do Codigo (SUT):** Revisao de todos os encadeamentos condicionais `if/elif` para garantir determinismo e ausencia de efeitos colaterais.
- **Validacao de Testes e BVA:** Verificacao manual se as fronteiras numericas (`299`, `300`, `699`, `700`, `0.30`, `0.50`) refletiam exatamente as regras do PRD.
- **Execucao do Pytest-cov:** Execucao local de `uv run pytest --cov=app --cov-branch` garantindo que 100% das linhas e branches foram exercitadas sem falsos positivos.
