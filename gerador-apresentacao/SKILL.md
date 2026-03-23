---
name: gerador-apresentacao
description: "Gera apresentações HTML premium (16:9) no padrão visual SESMT/Açotubo, incluindo logo oficial, fontes Plus Jakarta Sans e componentes interativos (Gantt, Status Cards)."
---

# Skill: Gerador de Apresentações Premium (SESMT/Açotubo)

Esta skill automatiza a criação de apresentações interativas de alto impacto, garantindo consistência visual com a identidade do Grupo Açotubo e SESMT Corporativo.

## Identidade Visual Obrigatória
- **Logo Oficial:** `C:\Users\denisson.monteiro\OneDrive - Grupo Açotubo\0 SESMT\Organizar\SESMT_v1\SESMT\Ocorrência Indesejada\Gestão 2026\01 Fluxo, indicadores e templates\Logo.png`
- **Fontes:** Plus Jakarta Sans (Google Fonts).
- **Cores:**
  - `Primary Red:` #E30613
  - `Dark Navy:` #0f172a
  - `Success Green:` #22c55e
  - `Alert Red:` #e11d48
- **Geometria:**
  - **Apresentação (16:9):** 338.67mm x 190.5mm.
  - **Placas/Avisos (A4 Paisagem):** Container 280mm x 195mm centralizado em body 297mm x 210mm.
  - **Placas/Avisos (A4 Retrato):** Container 195mm x 280mm centralizado em body 210mm x 297mm.

## Componentes Disponíveis (Templates HTML/CSS)

### 1. Slide de Capa / Cabeçalho de Placa
- Título principal com borda lateral esquerda (15px solid #E30613).
- Subtítulo com recuo de 35px.
- Elementos de fundo: `grid-pattern` (malha) e `blob-red` (gradiente suave).
- Watermark de escudo (`fas fa-shield-alt`) ao fundo.

### 2. Slide de Objetivos / Cards de Aviso
- Grid de colunas com cards brancos/cinza claro.
- Ícones FontAwesome em vermelho.
- Numeração de passos (`card-step`) em fonte gigante com opacidade 0.05 ao fundo do card.

### 3. Slide de Cronograma (Gantt Premium) / Escalas de Horário
- Tabela temporal interativa ou tabelas de horários com listras sutis.
- Fins de semana ou períodos destacados com `period-tag`.

### 4. Slide de Status / Alertas Críticos
- Utilizar cores semânticas (Verde para Confirmado, Vermelho para Suspenso/Alerta).
- Bordas superiores espessas (12px) nos cards de status.

## Diretrizes de Geração e Blindagem de Layout
1. **Reset Universal (Obrigatório):** Sempre incluir `* { box-sizing: border-box; margin: 0; padding: 0; }` para evitar que paddings quebrem o layout.
2. **Harmonização de Containers:**
   - O container principal deve ter dimensões fixas em `mm` ligeiramente menores que a página para garantir margens de impressão.
   - Usar `display: flex; flex-direction: column;` no container principal.
   - Usar `flex-grow: 1; min-height: 0;` em grids internos (`content-grid`) para que eles ocupem o espaço restante sem estourar o container pai.
3. **Navegação (Slides):** Sempre incluir o script de controle por teclado (Setas/Espaço) e botões flutuantes.
4. **Rodapé:** Manter "GRUPO AÇOTUBO | SEGURANÇA E SAÚDE OCUPACIONAL" e contador de slides (se aplicável).
5. **Destino:** Salvar os arquivos por padrão em `C:\Users\denisson.monteiro\Downloads`.
6. **Interatividade:** Transições suaves (0.8s cubic-bezier) e hover effects sutis nos cards.

## Integração de Fluxo (Multiskill)
- **Lista de Presença (DSS):** Após gerar qualquer apresentação de segurança, treinamento ou alerta crítico, o agente DEVE invocar automaticamente a skill `dss-acotubo` para gerar a **Lista de Presença** correspondente, utilizando o título da apresentação como tema principal.
- **Consistência:** Garanta que a data e o responsável (SESMT Corporativo) sejam consistentes entre a apresentação e a lista de presença.
