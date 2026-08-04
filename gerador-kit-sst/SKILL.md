---
name: gerador-kit-sst
description: Orquestra e elabora o Kit de Documentos de Segurança e Saúde do Trabalho (PGR, LTCAT, AEP/AET, LI, LP) de forma à prova de erros, blindado esteticamente e com profundo rigor técnico de engenharia.
---

# Gerador do Kit SST (PGR, LTCAT, AEP/AET, LI e LP)

Esta skill orquestra a criação, aprimoramento e formatação do kit completo de laudos e programas ocupacionais (SST). Seu objetivo é garantir que o agente sempre aja de forma autônoma, técnica e previsível (à prova de erros), produzindo relatórios de padrão sênior.

---

## 1. Protocolo de Triagem Obrigatório (Pré-Codificação)

Sempre que o usuário invocar a geração ou melhoria de um documento do Kit SST, **NÃO inicie a criação de códigos ou scripts imediatamente**. Você deve primeiro fazer as seguintes perguntas ao usuário (Protocolo de Triagem):

1. **Qual documento** do Kit SST vamos elaborar ou atualizar?
2. **Onde estão os dados fonte?**
3. **Qual Padrão de Cores** de formatação devo utilizar? (Normatiza ou Deni? *(Se o usuário não souber, assuma Normatiza)*).

*Aguarde as respostas antes de iniciar qualquer plano de implementação.*

---

## 2. BLINDAGEM ESTÉTICA: Regras Rigorosas de Formatação do Word

O código Python (`python-docx`) DEVE garantir que os documentos tenham uma estética impecável e idêntica entre os laudos, seguindo estas regras MANDATÓRIAS que substituem e unificam qualquer outra orientação prévia:

1. **Primeira Página em Branco (Capa do Canva)**
   - O documento DEVE conter uma primeira página completamente em branco (apenas com um `doc.add_page_break()` logo no início).
   - O cabeçalho desta primeira página DEVE estar desvinculado (`different_first_page_header_footer = True`), para que o usuário possa colar uma capa inteira do Canva depois, sem afetar o layout.

2. **Caixas de Destaque (Metodologia, Conclusão, Jurisprudência)**
   - **Tabelas sem bordas (fundo colorido)** devem possuir:
     - **Alinhamento Vertical**: Células com alinhamento vertical no centro (`w:vAlign = center`).
     - **Alinhamento Horizontal**: O texto final (conclusões e resultados) DEVE ser alinhado à ESQUERDA (não justificado).
     - **Espaçamento de Parágrafo**: Rigorosamente 3pt superior (`space_before = Pt(3)`) e 3pt inferior (`space_after = Pt(3)`).
     - **Entrelinhas**: Tabulação Simples (`line_spacing = 1.0`).
     - *Essas regras garantem que o texto fique visualmente centralizado no meio do destaque colorido.*

3. **Tabelas Técnicas**
   - **Espaçamento e Centralização**: Todos os parágrafos dentro de tabelas devem ter 3pt superior, 3pt inferior e entrelinhas simples (1.0). Alinhamento vertical das células DEVE ser centro (`vAlign = center`).
   - **Uniformidade de Colunas**: Se uma coluna for detectada como tendo apenas "textos curtos" (ex: Sim, Não, valores curtos), TODA a coluna deve ser centralizada. Do contrário, alinhe à esquerda.

4. **Regras Gerais de Supressão de Erros Estéticos**
   - **Nunca use Markdown Literal no Word**: É proibido passar `*` ou `**` em variáveis esperando que fiquem em negrito no Word.
   - **Cabeçalhos Híbridos Nativos**: Ao usar Emojis + Títulos (ex: `🎯 1.0 - Objetivo`), você DEVE usar os estilos nativos do Word (Heading 1, Heading 2), apenas sobrepondo a cor (ex: Normatiza `1B365D`) e a fonte (`Segoe UI`), para que o Word consiga montar o Sumário nativo (Painel de Navegação).

---

## 3. Diretrizes de Rigor Técnico e Científico (Estrutura Obrigatória)

O agente deve elevar o texto técnico ao nível de um Engenheiro Sênior.

### 3.1. PGR (Programa de Gerenciamento de Riscos)
1. Objetivo e Introdução.
2. Estabelecimento e Unidades.
3. Insalubridade e Periculosidade.
4. Da Proteção Individual.
5. Identificação e Inventário de Riscos Ocupacionais.
6. Plano de Ação.
7. Conclusão.

### 3.2. LTCAT (Laudo Técnico das Condições Ambientais do Trabalho)
1. Objetivo e Informações Básicas.
2. Legislação.
3. **O Roteiro de Elaboração do LTCAT (Os 12 Elementos Normativos da IN)**.
4. Medidas de Controle Existentes.
5. Proteção Individual.
6. Conclusão.
7. ANEXO I — Parecer Técnico de Aposentadoria Especial.
8. ANEXO II — Registro Fotográfico.

### 3.3. AEP / AET (Avaliação Ergonômica do Trabalho)
1. Objetivo e Escopo.
2. Caracterização da Empresa.
3. Metodologia e Critérios Avaliativos (NIOSH, RULA, REBA, Moore-Garg, ROSA).
4. Avaliação dos Postos de Trabalho.
5. Plano de Ação Ergonômico.

### 3.4. Laudos de Insalubridade e Periculosidade (LI e LP)
1. **Introdução e Metodologia Pericial**.
2. **Eficácia dos Equipamentos de Proteção Individual (EPIs)**: Foco obrigatório em jurisprudência (Súmula 289 TST e ARE 664335 STF).
3. **Avaliação Universal dos Anexos**: TODO anexo de norma aplicável (ex: Anexos 1 a 14 da NR-15) DEVE ser avaliado com:
   *   Conceito e Critérios.
   *   Avaliação Técnica.
   *   Justificativa Legal.
   *   Conclusão Taxativa.
4. **Parecer Conclusivo**.

---

## 4. O Fluxo de Execução

1. **Ativar o Protocolo**: Triagem de dados.
2. **Planejamento**: Escrever `implementation_plan.md` detalhando como o script garantirá o rigor técnico e a **blindagem estética** (Item 2).
3. **Codificação**: Usar `python-docx` (herdando `template_gerador_sst.py`).
4. **Geração**: Executar script, gerar arquivo e apresentar walkthrough.
