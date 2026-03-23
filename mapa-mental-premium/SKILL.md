---
name: mapa-mental-premium
description: Cria mapas mentais interativos de alta fidelidade em formato 16:9 widescreen com fluxo esquerda-para-direita e expansão passo a passo. Use quando precisar transformar informações complexas em apresentações dinâmicas e navegáveis.
---

# Mapa Mental Premium Interativo

Esta skill orienta a criação de mapas mentais profissionais utilizando uma arquitetura robusta de HTML/JS/SVG (sem dependência de Mermaid para evitar erros de sintaxe).

## Workflow de Criação

Sempre siga estas etapas na ordem:

1. **Entrevista Estruturada:** Faça estas perguntas objetivas ao usuário:
   - Qual o Título Central do mapa?
   - Quais as ramificações principais (Nível 1)?
   - Para cada ramificação, quais os detalhes (Nível 2 e Nível 3)?
   - Existe algum destaque visual específico (ex: um gatilho ou badge)?

2. **Geração do Código:** Utilize o template técnico contido em `references/template.html` como base absoluta.
   - Substitua o objeto `data` no JavaScript pela estrutura hierárquica fornecida pelo usuário.
   - Garanta que todos os ícones (emojis) solicitados sejam incluídos.

3. **Salvamento e Entrega:**
   - Salve o arquivo na pasta de Downloads (`C:\Users\denisson.monteiro\Downloads`).
   - Use um nome de arquivo claro: `Mapa_Mental_[Assunto]_Interativo.html`.

## Diretrizes de Design (Imutáveis)

- **Layout:** Widescreen 16:9 com container de bordas arredondadas.
- **Fluxo:** Sempre da esquerda (Raiz) para a direita (Detalhes).
- **Cores:** Caixas brancas, bordas vermelhas brilhantes, texto preto, linhas vinho.
- **Fundo:** Grade quadriculada sutil (blueprint) com gradiente radial.
- **Interatividade:** Botões de expansão/recolhimento animados em cada caixa.
- **Expansão:** Lógica passo a passo (um nível por vez).

## Estrutura de Dados (JSON Interno)

O objeto `data` deve seguir este padrão para que o motor funcione:
```javascript
const data = {
    id: "id_unico",
    text: "Texto com Emoji",
    expanded: true/false,
    children: [ { id: "...", text: "...", expanded: false, children: [...] } ]
};
```
