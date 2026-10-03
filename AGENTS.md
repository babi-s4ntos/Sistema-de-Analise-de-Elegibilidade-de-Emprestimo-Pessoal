# Diretrizes de Governanca e Contexto para Agentes de IA

## Principios de Desenvolvimento
1. **Type Hints Obrigatorios:** Todo codigo Python deve utilizar anotacoes de tipo explicitas (`int`, `float`, `bool`, `Enum`).
2. **Programacao Defensiva:** Valide tipos de entrada no inicio do metodo lancando `TypeError` se invalido e `ValueError` para valores fora do dominio de negocio.
3. **Padrao AAA nos Testes:** Todos os testes unitarios no Pytest DEVEM seguir explicitamente as secoes `# Arrange`, `# Act` e `# Assert`.
4. **Tecnicas Obrigatorias de Teste:**
   - Aplicar Analise do Valor Limite (BVA) em todas as condicoes numericas.
   - Aplicar Particionamento de Equivalencia (EP) para status de saida.
   - Aplicar Error Guessing para cenarios extremos e entradas malformadas.
5. **Meta de Cobertura:** 100% de cobertura de codigo e ramificacoes (`--cov-branch`). Proibido usar marcadores de exclusao de cobertura.
