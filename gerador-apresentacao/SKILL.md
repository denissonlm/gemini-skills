---
name: gerador-apresentacao
description: "Gera apresentações HTML premium (16:9) no padrão visual SESMT/Açotubo, incluindo logo oficial, fontes Plus Jakarta Sans e componentes interativos (Gantt, Status Cards)."
---

# Skill: Gerador de Apresentações Premium v2 (SESMT/Açotubo)

Esta skill automatiza a criação de apresentações interativas de alto impacto baseadas no **Padrão Interativo 2026**, garantindo consistência visual absoluta com a identidade do Grupo Açotubo e SESMT Corporativo.

## 🛡️ Regras de Hiper Blindagem (Inalteráveis)
1. **Reset Universal & Geometria:** Todo HTML deve iniciar com reset de margens/padding e `box-sizing: border-box`. O container principal (`slideshow`) deve ter largura máxima de `860px` e altura mínima de `540px` para garantir visualização perfeita em telas 16:9 e tablets.
2. **Sistema de Cores (Paleta SESMT):**
   - `Primary Red:` #c0392b (Uso em botões, destaques e ícones)
   - `Secondary Red:` #E30613 (Uso em logos e bordas de destaque)
   - `Light Red (Background):` #f8e9e8
   - `Deep Navy / Dark:` #111111 (Capa e rodapés escuros)
   - `Neutral Gray:` #555555
   - `Gray Light:` #f2f2f2 (Cards de fundo)
3. **Tipografia:** Uso obrigatório da fonte **'Inter'** ou **'Plus Jakarta Sans'** (Google Fonts) com pesos 400, 600, 800 e 900.
4. **Tarja de Privacidade (LGPD):** Dados sensíveis (Nomes, REs, Fotos de rosto) DEVEM ser protegidos por uma tarja visual (`background: #111; color: #111; border-radius: 3px;`).

## 🏗️ Estrutura Obrigatória de Slides

### 1. Slide de Capa (Hero Slide)
- **Badge SESMT:** Pílula superior vermelha com texto em branco "SESMT · GRUPO AÇOTUBO".
- **Título:** Fonte 900, `clamp(1.6rem, 4vw, 2.6rem)`, com palavras-chave em vermelho.
- **SVG Animado:** Incluir um ícone SVG flutuante central (`animation: floatY 3.5s ease-in-out infinite`).
- **Meta Chips:** Grid inferior com ícones sutis para Número do RAT, Data e Unidade.

### 2. Slide de Comunicado (Padrão RAT)
- **Header:** Gradiente marinho escuro (#2d3748 a #1a202c) com borda inferior vermelha (4px).
- **InfoBar:** Faixa cinza clara com borda lateral esquerda vermelha para Data e Expedição.
- **Grid de Dados:** 4 colunas para Vítima, Cargo, RE, Unidade, Local, Tempo e Tipo.
- **Categorização de Risco:** 3 boxes (Leve, Moderado, Grave) com cores semânticas e o ícone `✓` no box ativo (animado com `pulse`).

### 3. Slides de Conscientização (Content Cards)
- **Header Lateral:** Ícone em card 64x64px com fundo `red-light`.
- **Card List:** Lista de itens em fundo `gray-light` com borda lateral esquerda vermelha.
- **Alert Box:** Box de destaque com borda vermelha suave e ícone de alerta para conclusões críticas.

### 4. Slide de Encerramento
- **Background Dark:** Fundo #111 com texto em branco.
- **Pills de Resumo:** Grid de pílulas cinzas com os 3 ou 4 aprendizados principais do treinamento.

## 🎞️ Sistema de Animações (CSS Base)
O agente DEVE incluir obrigatoriamente as seguintes animações para cada troca de slide:
- `@keyframes fadeUp`: Opacidade 0 a 1 com deslocamento de 22px para cima.
- `@keyframes scaleIn`: Zoom suave de 0.88 para 1.
- `anim-up-[1-6]`: Delays escalonados (0.1s a 0.85s) para entrada sequencial de elementos.

## ⌨️ Interatividade e Navegação
- **Progress Bar:** Barra superior (`#progressFill`) que atualiza dinamicamente conforme o slide.
- **Botões de Navegação:** Botões flutuantes fixos no rodapé (Anterior/Próximo) com estados `:hover` e `:disabled`.
- **Key Binding:** Escuta de eventos `ArrowRight`, `ArrowLeft`, `ArrowUp` e `ArrowDown`.

## 📁 Gestão de Arquivos e Recursos
- **Logo:** `C:\Users\denisson.monteiro\OneDrive - Grupo Açotubo\0 SESMT\Organizar\SESMT_v1\SESMT\Ocorrência Indesejada\Gestão 2026\01 Fluxo, indicadores e templates\Logo.png`
- **Destino Padrão:** Salvar sempre em `C:\Users\denisson.monteiro\Downloads`.
- **Multiskill:** Após gerar, invocar `dss-acotubo` para a Lista de Presença correspondente.

## 🚫 Blindagem de Formato
- **NÃO** utilizar Markdown nos textos de conteúdo (usar `<strong>`, `<span>`, `<p>`).
- **NÃO** alterar a paleta de cores para tons que não sejam o Vermelho Açotubo ou Marinho Escuro.
- **NÃO** remover o rodapé de créditos do SESMT.
