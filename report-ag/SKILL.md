---
name: report-ag
description: "Gera dashboards executivos premiums baseados na arquitetura V4 High-Fidelity para o Grupo Açotubo."
---
# Report-AG (Alta Gestão - Executive Edition V4 Standard)

Este skill atua como um Especialista em Design Estratégico e UX do Grupo Açotubo. Gera dashboards executivos premiums baseados na arquitetura **V4 High-Fidelity**.

## 🛑 MANDATO DE BLINDAGEM (DNA V4 PREMIUM)
O layout, CSS e estrutura de JavaScript da **V4** são IMUTÁVEIS. Qualquer nova geração DEVE:
1.  **Fonte Única:** Ler obrigatoriamente o arquivo `assets/template.html`.
2.  **Formato Widescreen 16:9 (PROIBIDO ALTERAR):** O arquivo HTML DEVE obrigatoriamente utilizar as dimensões `width: 338.67mm; height: 190.5mm;` na classe `.page` e no bloco `@media print { @page { size: 338.67mm 190.5mm; ... } }` para se adequar perfeitamente a slides do PowerPoint.
3.  **Layout Grid 2x2:** A seção de Análise Estratégica DEVE obrigatoriamente usar `display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, 1fr);` para garantir 4 cards equilibrados horizontalmente e verticalmente.
4.  **Gráfico com Rótulos:** O gráfico de acidentes DEVE obrigatoriamente exibir rótulos de dados (Data Labels) no topo das barras e não possuir barra de rolagem.
