---
name: dss-acotubo
description: "Skill especializada para geração de Diálogos de Segurança (DSS) e Listas de Presença seguindo o padrão visual \"Açotubo Web Modern\"."
---
# Especialista SESMT Açotubo (DSS & Listas)

Skill especializada para geração de Diálogos de Segurança (DSS) e Listas de Presença seguindo o padrão visual "Açotubo Web Modern".

## 🛡️ Regras de Hiper Blindagem (Inalteráveis)
1. **Obrigatoriedade de Duas Páginas (FRENTE E VERSO)**: O HTML gerado DEVE SEMPRE conter dois blocos `<div class="page">`. NUNCA gere apenas uma página, mesmo que o conteúdo seja curto. A segunda página é reservada para as 32 assinaturas de continuação.
2. **Layout Fixo de Topo (11.5cm)**: O bloco inicial (Header + Tema + Resumo + Riscos) DEVE ter exatamente `height: 11.5cm`. Use `overflow: hidden` para garantir que o texto excedente não empurre a tabela.
3. **Proibição de Markdown**: NUNCA use `**` ou `*` para negrito. Use APENAS tags HTML puras: `<strong>` para negrito e `<br>` para quebras de linha.
4. **Limites de Caracteres (Truncamento)**:
   - **Título do Tema**: Máximo de 80 caracteres (deve caber em uma linha).
   - **Resumo**: Máximo de 650 caracteres (contando as tags HTML).
   - **Riscos**: Exatamente 3 a 4 riscos, cada um com no máximo 100 caracteres.
5. **Padrão de Páginas (Frente e Verso)**:
   - **Página 1 (Frente)**: Header + Conteúdo + 18 linhas de assinatura (0.8cm cada).
   - **Página 2 (Verso)**: Rodapé de Continuação + 32 linhas de assinatura (0.8cm cada).
6. **Campos Editáveis Reais**: Os campos "Divisão", "Responsável Local" e "Data / Horário" DEVEM obrigatoriamente possuir o atributo `contenteditable="true"`. O campo "Responsável SESMT" deve ser fixo como "Denisson Monteiro".
7. **Estilo Visual "Açotubo Modern"**: 
   - Logo: DEVE ser embutido como **Base64** no HTML para garantir compatibilidade com todos os navegadores (Safari/Chrome).
   - Fonte do Logo: `/Users/denisson/Library/CloudStorage/OneDrive-GrupoAçotubo/0 SESMT/Organizar/SESMT_v1/SESMT/Ocorrência Indesejada/Gestão 2026/01 Fluxo, indicadores e templates/Logo.png`.
   - Vermelho Açotubo (`#cc0000`) nas bordas e faixas de destaque.
   - Fonte 'Inter' com pesos 700 e 900.

## Workflow
1. Analisar material base.
2. Extrair: Tema (curto), Resumo Educativo (conciso) e 3 Riscos Críticos.
3. **Processamento de Logo**: Converter o arquivo de logo em `/Users/denisson/Library/CloudStorage/OneDrive-GrupoAçotubo/0 SESMT/Organizar/SESMT_v1/SESMT/Ocorrência Indesejada/Gestão 2026/01 Fluxo, indicadores e templates/Logo.png` para uma string Base64.
4. Gerar HTML em `Downloads\Lista_Presenca_DSS.html` usando o template blindado, inserindo a string Base64 no atributo `src` da tag de imagem.
5. **VERIFICAÇÃO DE FUNCIONALIDADE**: O agente DEVE garantir que os campos de cabeçalho permitam edição manual via browser (`contenteditable="true"`) antes de salvar.
6. **VERIFICAÇÃO DE ESTRUTURA**: O agente DEVE conferir se o código HTML possui EXATAMENTE DUAS tags `<div class="page">` antes de salvar.
7. Aplicar rigorosamente os limites de caracteres no prompt de geração.
