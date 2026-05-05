---
name: analise-trianual-acidentes
description: Gera dashboards premium widescreen (16:9) de análise de acidentes trianual do Grupo Açotubo. Use para processar a planilha de acidentes, gerar insights automáticos e criar relatórios HTML fiéis ao padrão visual institucional.
---

# Análise Trianual de Acidentes (Açotubo)

Este skill automatiza a geração do relatório de acidentes do Grupo Açotubo, comparando os últimos três anos (2024, 2025 e 2026) com fidelidade visual total.

## 📁 Banco de Dados Padrão
A skill utiliza por padrão o arquivo:
`C:\Users\denisson.monteiro\OneDrive - Grupo Açotubo\0 SESMT\Organizar\SESMT_v1\SESMT\Ocorrência Indesejada\Gestão 2026\01 Fluxo, indicadores e templates\Dash Acidentes.xlsx` (Aba: **BD**)

## 🚀 Fluxo de Trabalho

1.  **Validação do Caminho:** Confirme se o banco de dados acima é o correto ou se há um novo arquivo.
2.  **Processamento de Dados:** A skill deve ler a aba 'BD', filtrar os anos de 2024 a 2026 e calcular:
    *   Totais anuais e médias mensais (com 1 casa decimal).
    *   Matriz de acidentes por mês (Heatmap).
    *   Projeção para o final de 2026 com base no ritmo atual.
3.  **Apresentação de Insights:** Antes de gerar o arquivo, a skill DEVE mostrar os insights detectados (Picos, Variações, Tendências) e perguntar: *"Gostaria de alterar algum texto destes insights antes de gerar o dashboard?"*.
4.  **Geração do HTML:** Criar o arquivo `Dashboard_Acidentes_Acotubo.html` na pasta de **Downloads** utilizando o layout widescreen 16:9 aprovado.

## 🎨 Padrão Visual (Blindagem)
O dashboard gerado deve seguir rigorosamente:
*   **Widescreen (16:9):** Dimensões fixas para slides e impressão.
*   **Cabeçalho Unificado:** Logo oficial à esquerda, título central e faixa escura do SESMT à direita.
*   **KPIs Compactos:** Números grandes (44px) sem espaços vazios exagerados.
*   **Gráfico Comparativo:** Barras verticais (Vermelho/Preto/Cinza) para os 3 anos.
*   **Mapa de Intensidade:** Grid de cores semânticas (Fundo branco com cores de calor).
*   **Períodos de Atenção:** 4 cards no rodapé com ícones circulares e texto de 10.5px.
*   **Edição Direta:** Atributo `contenteditable="true"` em todos os textos para ajustes rápidos pós-geração.

## 🛠️ Script de Referência
Utilize o script de processamento em `scripts/processar_dash.py` para garantir a precisão matemática.
