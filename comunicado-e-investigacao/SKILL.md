---
name: comunicado-e-investigacao
description: >
  Orquestra o fluxo de investigação de acidentes do SESMT. Lê os dados da pasta do acidentado, compara com investigações passadas, conduz análise de causa raiz e gera relatórios em TXT e HTML.
---

# Skill: Investigação de Acidente e Comunicado SESMT

## Overview
Esta skill orquestra o processo investigativo de acidentes de trabalho do SESMT. Ela automatiza a coleta de dados, realiza consultas no histórico de acidentes (na pasta "04 RAT") para embasamento analítico, conduz uma entrevista com o usuário sobre a Causa Raiz (diagrama de Ishikawa, 5 Porquês, Fatos Contribuintes) e produz os documentos finais padronizados (`Investigacao_Acidente.txt` e `Comunicado.html`).

## Workflow

### 1. Leitura e Validação de Dados Iniciais
- **Ação:** Liste os arquivos da nova pasta indicada pelo usuário. Extraia as informações do relato inicial e dos arquivos fornecidos (fotos, laudos, depoimentos).
- **Validação:** Verifique se as informações mínimas estão presentes (Data/hora exata, cargo da vítima, descrição do ocorrido, lesão, foto da lesão, número da RAT, dias de atestado/afastamento).
- **Se faltar dados:** Interrompa e pergunte proativamente ao usuário pelos dados faltantes. **NUNCA assuma ou invente dados que não estejam explícitos nos arquivos de origem.**

### 2. Comparativo com Investigações Anteriores
- **Ação:** Use suas ferramentas de busca/leitura (como `grep_search` ou listagem) na pasta base `04 RAT` (ex: `/Users/denisson/Library/CloudStorage/OneDrive-GrupoAçotubo/0 SESMT/Organizar/SESMT_v1/SESMT/Ocorrência Indesejada/Gestão 2026/04 RAT`) para localizar investigações de acidentes similares (ex: mesmo cargo, mesma área, ou mesma dinâmica).
- **Objetivo:** Utilizar essa base histórica para enriquecer a análise técnica, identificar reincidências de desvios e sugerir planos de ação mais robustos baseados em aprendizados passados. 

### 3. Entrevista e Análise de Causa Raiz
- **Ação:** Pergunte ao usuário se ele já possui uma "Causa Raiz" pré-definida em mente.
- **Interação:** Baseado na resposta do usuário e nos dados apurados, apresente e valide com ele:
  1. O Diagrama de Ishikawa (Espinha de Peixe)
  2. Os 5 Porquês
  3. Os Fatores Contribuintes (Classificados em Atos Inseguros e Condições Inseguras)
- Aguarde a validação/correção do usuário antes de prosseguir para o próximo passo.

### 4. Geração do Relatório de Investigação (TXT)
- **Ação:** Escreva o arquivo `Investigacao_Acidente.txt` na pasta do acidentado.
- **Conteúdo:** Utilize linguagem técnica apropriada para o SESMT. O arquivo deve conter: Dinâmica do Acidente, Análise Comparativa (do passo 2), Ferramentas Analíticas (Ishikawa, 5 Porquês validados) e Planos de Ação (5W2H).

### 5. Geração do Comunicado (HTML)
- **Ação:** Leia o template padronizado localizado em `resources/Comunicado_Template.html` (dentro da pasta desta skill).
- **Substituição:** Substitua rigorosamente as tags `{{PLACEHOLDER}}` pelas informações reais extraídas. (Ex: `{{NOME_VITIMA}}`, `{{DESCRICAO_LESAO}}`, `{{IMAGEM_LESAO_TAG}}`).
- **Como executar a substituição:** Para garantir a integridade do HTML e não perder trechos longos, escreva um script Python (usando a ferramenta `run_command`) que leia o `Comunicado_Template.html`, faça o `replace` de cada chave pelo seu valor correspondente e grave o arquivo de saída como `Comunicado.html` diretamente na pasta do acidentado.
- **Inserção de Foto:** O script Python deve ler o arquivo de imagem da lesão, encodá-lo em base64 e substituir a tag `{{IMAGEM_LESAO_TAG}}` por `<img src="data:image/jpeg;base64,...">`.
- **Regras Críticas do HTML (Anti-Vazamento & Exatidão):**
  - **Script de Substituição:** O agente DEVE usar um script Python contendo um dicionário exato com todas as chaves `{{PLACEHOLDER}}` mapeadas para as novas strings.
  - **Remoção de Elementos Inexistentes:** Se não houver vídeo gravado do acidente real (câmeras de segurança/CFTV), a seção inteira correspondente ao vídeo (`<div class="vid">...</div>\s*</div>`) DEVE ser removida do HTML final usando expressões regulares, garantindo que não fiquem botões ou links vazios.
  - **Validação Obrigatória:** Após gerar o arquivo `Comunicado.html` e o `Investigacao_Acidente.txt`, o agente DEVE obrigatoriamente inspecionar ambos os arquivos gerados em busca de vestígios de acidentes de terceiros (ex: pesquisar pelo nome de vítimas históricas usadas no arquivo anterior ou cruzar informações para ter certeza que não vazaram).
  - Caso haja qualquer resquício de outro acidente no bloco narrativo, o agente deve apagar o arquivo, ajustar o script e gerar novamente antes de apresentar ao usuário.
  - NÃO altere nenhuma linha de CSS do arquivo `Comunicado_Template.html`. O layout é sagrado.
- **Salvamento:** O script salvará o arquivo `Comunicado.html` final dentro da pasta do acidentado.

### 6. Conclusão
- **Ação:** Informe ao usuário que os documentos estão prontos e lembre-o de abrir o `Comunicado.html` no Chrome, teclar Cmd+P, remover margens e salvar como PDF (escala 100%).

## Diretrizes de Blindagem e Exatidão de Dados

1. **Vedação a Invenções (Zero Alucinação):** 
   - **NÃO INVENTE** o número da RAT, o horário exato da ocorrência ou a quantidade de dias de atestado. Se essas informações não forem encontradas em documentos cadastrais ou fornecidas no início, **pergunte explicitamente ao usuário**.
2. **Diferenciação de Mídias (Vídeo Real vs. Simulação):** 
   - Arquivos contendo reconstituições ou fotos encenadas (simulando a dinâmica) não devem ser confundidos com "vídeos do acidente real" (imagens reais de segurança da ocorrência). O comunicado e o laudo não devem declarar a existência de vídeo da ocorrência real a menos que haja gravação do fato em si confirmada.
3. **Limpeza de Nomenclatura Sistêmica:** 
   - Não inclua códigos ou siglas de sistemas cadastrais internos do Grupo Açotubo (como "Ramz" ou "RAMS", comumente associados ao cadastro do Centro de Custo no ERP) na descrição do local físico ou do local do evento nos comunicados e investigações oficiais. Mantenha a nomenclatura estritamente física e operacional (ex: "Nave 13", "Pátio Externo de Estocagem").

## Common Mistakes
- **Quebrar o HTML:** Alterar o CSS do template ou injetar textos gigantescos que fazem o conteúdo vazar da primeira folha do A4.
- **Pular a validação:** Não perguntar ao usuário sobre a causa raiz antes de assumir uma, tirando a autonomia do SESMT na decisão final.
- **Esquecer o histórico:** Não vasculhar a pasta "04 RAT" para cruzar dados com ocorrências semelhantes.
- **Inventar dados ou reter termos sistêmicos:** Assumir horários e números de RAT fictícios ou deixar siglas sistêmicas (ex: RAMS) no texto do local físico do acidente.
- **Confundir simulações com o evento real:** Declarar a existência de vídeo de monitoramento do acidente com base apenas em filmagens de encenações/reconstituições posteriores.
