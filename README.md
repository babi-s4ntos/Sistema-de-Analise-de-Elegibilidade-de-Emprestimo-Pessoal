# Sistema de Analise de Elegibilidade de Emprestimo Pessoal (QTS - AT1)

Projeto pratico individual para a disciplina de Qualidade e Teste de Software (QTS), focado em engenharia de testes unitarios, medicao de cobertura de codigo e governanca de IA.

## Requisitos
- Python 3.12+
- Gerenciador de pacotes `uv`

## Instalacao e Execucao

### 1. Instalar dependencias
```bash
uv sync
```

### 2. Executar a suite de testes unitarios
```bash
uv run pytest -v
```

### 3. Executar medicao de cobertura de codigo e branches (100%)
```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```
