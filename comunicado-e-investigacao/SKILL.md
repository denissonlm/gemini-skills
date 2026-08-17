---
name: comunicado-e-investigacao
description: >
  Orquestra o fluxo de investigação de acidentes do SESMT. Lê os dados da pasta do acidentado, compara com investigações passadas, conduz análise de causa raiz e gera relatórios em TXT e HTML.
---

# Skill: Investigação de Acidente e Comunicado SESMT

## Overview
Esta skill orquestra o processo investigativo de acidentes de trabalho do SESMT. Ela automatiza a coleta de dados, realiza consultas no histórico de acidentes (na pasta "04 RAT") para embasamento analítico, conduz uma entrevista/confirmação com o usuário sobre a Causa Raiz (diagrama de Ishikawa, 5 Porquês, Fatos Contribuintes, gravação em vídeo e status/dias de atestado) e produz os documentos finais padronizados (`Investigacao_Acidente.txt` e `Comunicado.html`).

## Workflow

### 1. Leitura e Validação de Dados Iniciais
- **Ação:** Liste e leia OBRIGATORIAMENTE todos os arquivos da nova pasta indicada pelo usuário (arquivos `.docx` do comunicado expedido pela filial, PDFs de CAT/atestados, planilhas, imagens de ficha de registro e fotos).
- **Validação de Dados:** Extraia as informações fidedignas (Data e hora exata, local real da entrega/cliente, cargo da vítima, descrição do ocorrido, lesão, foto da lesão, número da RAT, status/dias de atestado).
- **Regra de Ouro (Zero Suposição / Zero Invenção):** **NUNCA assuma ou invente dados.** 
  - **PROIBIDO INVENTAR OU SUPOR MÁQUINAS/EQUIPAMENTOS:** NUNCA presuma que a operação envolveu caminhão Munck/guindauto, ponte rolante, empilhadeira ou qualquer equipamento específico sem que conste explicitamente nos relatos/documentos da filial ou seja confirmado pelo usuário.
  - **PROIBIDO INVENTAR DIAS DE ATESTADO:** NUNCA insira quantidades fictícias de dias de afastamento (ex: 3 dias, 15 dias). Se o atestado/afastamento não constar explicitamente nos arquivos ou se a avaliação/cirurgia estiver pendente, declare obrigatoriamente: `"A definir (Sob avaliação médica / Pós-cirúrgico)"`.
  - **PROIBIDO SUBENTENDER VÍDEO DO ACIDENTE:** NUNCA assuma que o acidente foi gravado por haver arquivos `.mp4` na pasta. Pergunta obrigatória ao usuário.
  - **NOMENCLATURA PADRÃO:** Utilize obrigatoriamente a terminologia **"Instrução de Trabalho (IT)"** em vez de "Procedimento Operacional Padrão (POP)".
- **Se faltar confirmação ou dados:** Pergunte proativamente ao usuário antes de gerar os relatórios.

### 2. Comparativo com Investigações Anteriores
- **Ação:** Use suas ferramentas de busca/leitura (como `grep_search` ou listagem) na pasta base `04 RAT` (ex: `/Users/denisson/Library/CloudStorage/OneDrive-GrupoAçotubo/0 SESMT/Organizar/SESMT_v1/SESMT/Ocorrência Indesejada/Gestão 2026/04 RAT`) para localizar investigações de acidentes similares (ex: mesmo cargo, mesma área, ou mesma dinâmica).
- **Objetivo:** Utilizar essa base histórica para enriquecer a análise técnica, identificar reincidências de desvios e sugerir planos de ação mais robustos baseados em aprendizados passados. 

### 3. Entrevista e Confirmação Obrigatória com o Usuário
- **Ação:** Apresente ao usuário os dados apurados e consulte/valide expressamente:
  1. **Status do Afastamento/Atestado:** Confirme os dias exatos de atestado ou se o afastamento está a definir (ex: aguardando cirurgia ou laudo médico).
  2. **Confirmação de Vídeo:** Pergunte se há gravação do evento real por câmeras de segurança/CFTV. Se não houver confirmação do usuário, a seção de vídeo do comunicado DEVE ser totalmente removida.
  3. **Causa Raiz & 5 Porquês:** Apresente o Diagrama de Ishikawa proposto, os 5 Porquês e os Fatores Contribuintes e confirme a aprovação da liderança/SESMT.
- Aguarde a validação do usuário ou ajuste conforme suas orientações.

### 4. Geração do Relatório de Investigação (TXT)
- **Ação:** Escreva o arquivo `Investigacao_Acidente.txt` na pasta do acidentado.
- **Conteúdo:** Utilize linguagem técnica apropriada para o SESMT. O arquivo deve conter: Dinâmica do Acidente, Análise Comparativa (do passo 2), Ferramentas Analíticas (Ishikawa, 5 Porquês validados) e Planos de Ação (5W2H). Sempre utilizar o termo "Instrução de Trabalho (IT)".

### 5. Geração do Comunicado (HTML)
- **Ação:** Leia o template padronizado localizado em `resources/Comunicado_Template.html` (dentro da pasta desta skill).
- **Substituição:** Substitua rigorosamente as tags `{{PLACEHOLDER}}` pelas informações reais extraídas. (Ex: `{{NOME_VITIMA}}`, `{{DESCRICAO_LESAO}}`, `{{IMAGEM_LESAO_TAG}}`).
- **Como executar a substituição:** Escreva um script Python (usando a ferramenta `run_command`) que leia o `Comunicado_Template.html`, faça o `replace` de cada chave pelo seu valor correspondente e grave o arquivo de saída como `Comunicado.html` diretamente na pasta do acidentado.
- **Inserção de Foto:** O script Python deve ler o arquivo de imagem da lesão, encodá-lo em base64 e substituir a tag `{{IMAGEM_LESAO_TAG}}` por `<img src="data:image/jpeg;base64,...">`.
- **Regras Críticas do HTML (Anti-Vazamento & Remoção de Vídeo Inexistente):**
  - **Remoção Estrita de Vídeo Inexistente:** Se NÃO houver confirmação de vídeo gravado do acidente real, o script Python DEVE obrigatoriamente remover toda a div `<div class="vid">...</div>` utilizando substituição por corte/regex (`re.sub(r'<!-- ▌VIDEO -->.*?(?=<!-- ▌FOOTER -->)', '', html, flags=re.DOTALL)`).
  - **Validação Obrigatória:** Após gerar o arquivo `Comunicado.html` e o `Investigacao_Acidente.txt`, o agente DEVE obrigatoriamente inspecionar ambos os arquivos gerados em busca de vestígios de acidentes de terceiros ou seções/dados indevidos.
  - NÃO altere nenhuma linha de CSS do arquivo `Comunicado_Template.html`. O layout é sagrado.
- **Salvamento:** O script salvará o arquivo `Comunicado.html` final dentro da pasta do acidentado.

### 6. Conclusão
- **Ação:** Informe ao usuário que os documentos estão prontos e lembre-o de abrir o `Comunicado.html` no Chrome, teclar Cmd+P, remover margens e salvar como PDF (escala 100%).

## Diretrizes de Blindagem e Exatidão de Dados

1. **Vedação Absoluta a Invenções de Dados (Zero Alucinação):** 
   - **NÃO INVENTE OU SUBENTENDA** a quantidade de dias de atestado, o número da RAT, o horário exato, o local físico ou a existência de equipamentos (como Munck ou guindauto) que não estejam documentados. Se o atestado não estiver emitido, registre `"A definir (Sob avaliação médica/pós-cirúrgica)"`.
2. **Diferenciação e Proibição de Presunção de Mídias (Vídeo Real vs. Reconstituição):** 
   - A mera presença de arquivos `.mp4` na pasta NÃO AUTORIZA declarar que há vídeo do acidente. O comunicado e a investigação NÃO devem declarar a existência de vídeo da ocorrência nem incluir a seção de vídeo no HTML a menos que o usuário confirme expressamente.
3. **Limpeza de Nomenclatura Sistêmica:** 
   - Não inclua códigos ou siglas de sistemas cadastrais internos do Grupo Açotubo (como "Ramz" ou "RAMS") na descrição do local físico ou do local do evento nos comunicados e investigações oficiais. Mantenha a nomenclatura estritamente física e operacional (ex: "Cliente Bermo (Blumenau/SC)", "Nave 3", "Pátio Interno de Estocagem").

## Common Mistakes
- **Inventar maquinários/equipamentos ou dinâmicas:** Assumir que o acidente envolveu caminhão Munck quando a operação utilizava ponte rolante do cliente, ou inventar dinâmicas não relatadas no documento da filial.
- **Inventar dias de afastamento/atestado:** Inserir um número fictício de dias de atestado sem que o médico tenha emitido o laudo final.
- **Subentender a existência de vídeo do acidente:** Assumir que o acidente foi gravado por câmeras sem confirmação prévia do usuário.
- **Quebrar o HTML:** Alterar o CSS do template ou injetar textos gigantescos que fazem o conteúdo vazar da primeira folha do A4.
- **Pular a validação com o usuário:** Gerar relatórios sem confirmar a causa raiz, atestado e vídeos antes.
