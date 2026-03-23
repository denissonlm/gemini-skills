---
name: gerador-orcamentos
description: Elabora orçamentos profissionais de serviços em formato HTML (A4 retrato) com design moderno. Use quando o usuário solicitar um orçamento, proposta comercial ou estimativa de custos para prestação de serviços.
---

# Gerador de Orçamentos Profissionais (Versão Travada 2026)

Esta skill utiliza um motor de design fixo para garantir que todos os orçamentos mantenham a mesma identidade visual e funcionalidade premium. **Não altere a estrutura do template base.**

## Fluxo de Trabalho Obrigatório

1. **Coleta de Dados**: Identifique ou solicite os seguintes dados ao usuário:
   - Dados do Cliente (Nome, Empresa, Contato).
   - Dados do Elaborador (Nome, Especialidade, Contato).
   - Escopo (O que será feito e como será entregue).
   - Itens de Preço (Descrição, Quantidade, Valor Unitário).
   - Condições (Prazo de entrega e Condição de Pagamento).

2. **Geração do Documento (Imutabilidade)**:
   - **Template Único**: Utilize SEMPRE o arquivo em `assets/template.html`.
   - **Injeção de Dados**: Preencha os campos `contenteditable="true"` no HTML com as informações fornecidas, mas **mantenha todas as classes CSS, scripts e IDs originais intactos.**
   - **Funcionalidades Dinâmicas**: O botão "Adicionar Item" e a função de remoção de linhas no HTML devem ser preservados para que o usuário possa ajustar o documento no navegador.
   - **Cálculos**: Não faça cálculos manuais no texto; preencha os valores unitários e deixe o script interno do HTML realizar os cálculos totais.

3. **Salvamento e Entrega**:
   - Salve o arquivo em `C:\Users\denisson.monteiro\Downloads\Orcamento_CLIENTE_DATA.html`.
   - Informe ao usuário que o design está travado conforme o padrão de excelência estabelecido e que ele pode adicionar/remover itens diretamente no documento aberto.

## Padrões Estéticos (Design System Travado)

- **Cores**: Primária `#CC0000`, Secundária `#1A1A1A`.
- **Tipografia**: Fontes 'Inter' (sistema) e 'Playfair Display' (marca) via Google Fonts.
- **Layout**: Formato A4, sombras suaves (`box-shadow`), bordas arredondadas de 8px em cards e botões.
- **Interatividade**: Botão flutuante vermelho para impressão e botões de controle de linha na tabela.

## Exemplo de Comando
"Gere um orçamento para [Cliente] sobre [Serviço] no valor de [Valor]." -> A IA deve injetar esses dados no template premium sem alterar uma linha sequer do CSS ou JS.
