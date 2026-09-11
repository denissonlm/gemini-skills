---
name: processar-investigacao-acidente
description: "Processa uma pasta de ocorrência do SESMT e prepara comunicado e investigação de acidente em DOCX/PDF, escolhendo sem mistura entre o template RAT (acidente do trabalho/típico) e o template Trajeto. Use quando o usuário pedir comunicado, investigação, RAT, análise 6Ms/5 Porquês, plano de ação ou documentos ilustrados a partir de uma pasta de acidente. Bloqueia a geração quando houver fato ausente, conflitante ou não confirmado."
---

# Processar investigação de acidente

## Princípio central

Trate comunicado e investigação como registros oficiais de alta criticidade. Não invente, complete por padrão, transporte fatos de outro acidente nem transforme inferência em fato.

Use sempre a skill `official-records-safeguard` junto desta skill. Preserve os originais e trabalhe em cópia. Não sobrescreva um documento oficial existente sem autorização. Gere primeiro uma minuta fora da pasta oficial; após a aprovação expressa do usuário, conclua o trabalho gravando o DOCX e o PDF finais diretamente na pasta do caso. Não deixe uma investigação aprovada somente na pasta temporária ou de saídas.

## Fluxo obrigatório

1. Inventarie todos os arquivos da pasta com `scripts/inventory_case.py`.
2. Quando houver áudio ou vídeo com fala, gere uma transcrição local conforme `references/transcricao-local.md`, confira os trechos usados contra a gravação e preserve marcações de incerteza.
3. Leia cada fonte disponível e monte uma matriz `campo → valor → fonte → página/tempo → status`.
4. Classifique a ocorrência como `trabalho` ou `trajeto` somente com evidência explícita.
5. Se a classificação estiver ausente, ambígua ou conflitante, pare e pergunte ao usuário.
6. Selecione exatamente um template:
   - `assets/template-rat.dotx` para acidente do trabalho/típico.
   - `assets/template-trajeto.dotx` para acidente de trajeto.
7. Não misture campos, rótulos ou estrutura entre os dois templates. Leia `references/dois-templates.md`.
8. Compare até três investigações históricas semelhantes somente para calibrar concisão e padrão visual. Nunca copie nomes, datas, causas, ações, responsáveis, imagens ou conclusões históricas.
9. Apresente ao usuário todos os fatos apurados, conflitos e campos ausentes em um único bloco conciso.
10. Proponha 6Ms, 5 Porquês, causa raiz conclusiva, ofensores e plano de ação como **análise para aprovação**. Não os trate como conclusões confirmadas antes da aprovação do usuário/SESMT.
11. Aguarde a resposta do usuário sempre que existir qualquer campo ausente ou análise não aprovada.
12. Registre a aprovação e a proveniência no JSON do caso; valide com `scripts/validate_case.py`.
13. Gere o comunicado primeiro com `scripts/build_comunicado.py` e valide visualmente uma página.
14. Gere a investigação com `scripts/build_investigation.py`; o documento deve ter exatamente duas páginas paisagem:
    - página 1: investigação técnica;
    - página 2: plano de ação e assinaturas.
15. Converta o DOCX para PDF, renderize todas as páginas e faça inspeção visual. Use a skill `documents` para DOCX e `pdf` para PDF.
16. Execute verificações anti-vazamento e de proveniência antes de entregar.
17. Após a aprovação final e a verificação visual, publique obrigatoriamente o DOCX e o PDF na própria pasta da ocorrência, com os nomes oficiais definidos abaixo. A cópia em `outputs/` é apenas rascunho ou apoio de entrega, não o destino final.

Para converter o comunicado HTML em PDF, use `scripts/html_to_pdf.py`. O script utiliza prioritariamente o Google Chrome / Chromium headless (`--headless=new`) para garantir fidelidade visual absoluta aos ícones, emojis, flexbox e caixas, com validação via `pypdf` de exatamente uma página A4; mais páginas bloqueiam a entrega.

## Hierarquia de fontes

Priorize, nesta ordem:

1. documento original, assinado ou emitido pela empresa/serviço de saúde;
2. oitiva, relato gravado ou resposta expressa do usuário;
3. comunicado inicial explicitamente reconhecido pelo usuário como correto;
4. vídeo/foto para fatos diretamente observáveis, sem interpretação de intenção;
5. cadastro do colaborador para dados cadastrais estritamente necessários;
6. documento derivado (`Investigacao_Acidente.txt`, HTML, infográfico ou análise anterior) apenas como hipótese a validar;
7. histórico de outros acidentes apenas como referência de forma e concisão.

Em caso de conflito, não escolha silenciosamente. Mostre as duas versões e pergunte.

Uma transcrição automática é um índice da gravação, não substitui a gravação como fonte. Só transporte para o documento os trechos claramente audíveis ou expressamente confirmados.

## Bloqueio de dados ausentes

Considere ausente qualquer valor vazio, ilegível, inferido, copiado de caso histórico ou representado por `-`, `?`, `a definir`, `não encontrado`, `desconhecido` ou equivalente.

Não substitua ausência por `N/A` por conta própria. `Não se aplica`, `não houve` ou `não informado` só podem ser usados quando o usuário ou uma fonte confiável confirmar essa condição.

Quando o usuário autorizar expressamente o preenchimento manual posterior, somente campos administrativos previstos pelo validador podem ficar vazios, registrados na matriz com status `confirmed_blank` e fonte `user_confirmation`. Essa exceção não vale para dinâmica, análise, causa, potencial ou qualquer coluna do plano de ação.

Leia a lista de campos em `references/campos-obrigatorios.md`. Agrupe perguntas relacionadas para reduzir idas e vindas, mas pergunte todas as lacunas.

## Regras de análise técnica

- Descreva o evento sem juízo de valor, culpa ou linguagem disciplinar.
- Diferencie `fato confirmado`, `inferência técnica` e `não determinado`.
- Não atribua distração, negligência, imprudência, recusa de EPI, falha de treinamento, falha de supervisão ou descumprimento deliberado sem fonte explícita.
- Não declare falha de máquina, ferramenta, processo ou ambiente sem evidência.
- Um `M` não aplicável deve trazer a justificativa factual aprovada.
- Os 5 Porquês não podem avançar além da evidência. Se a cadeia quebrar, não preencha o documento: registre a lacuna e pergunte ao usuário.
- A causa raiz do documento final deve ser conclusiva e aprovada. Se as fontes não sustentarem uma conclusão, pare e pergunte; não escreva `inconclusiva`, `não determinada`, `a apurar` ou equivalente por conta própria.
- Só use causa raiz inconclusiva quando o usuário afirmar expressamente que esse é o resultado oficial. Registre `approvals.root_cause_inconclusive: true` e a confirmação na matriz de evidências.
- Causa raiz e plano de ação exigem aprovação expressa antes do documento final.
- Ação, responsável, prazo e status não podem ser inventados. Uma ação concluída exige evidência de conclusão.
- Medida disciplinar nunca é gerada automaticamente.

## Ilustrações e privacidade

- Para a investigação, use o CFTV somente como evidência de análise; não insira seus quadros no campo `REPRESENTAÇÃO DA DINÂMICA DO ACIDENTE`.
- Gere nesse campo uma reconstituição didática passo a passo com bonecos/maniquins sem identidade facial, baseada exclusivamente nos fatos confirmados. Inclua dentro da imagem: `RECONSTITUIÇÃO ILUSTRATIVA - NÃO É REGISTRO DO ACIDENTE`.
- Para RAT de acidente do trabalho, o campo `Detalhes` deve receber uma segunda ilustração gerada que destaque um ponto técnico importante do caso, sem texto corrido substituindo a imagem. Inclua `ILUSTRAÇÃO DIDÁTICA` dentro da arte.
- Registre `images.dynamics_kind: generated_reconstruction` e, para RAT de acidente do trabalho, `images.details_kind: generated_detail`. O validador bloqueia outro tipo de mídia nesses campos.
- Imagem gerada não é evidência. Não acrescente máquina, falha, EPI, postura, sequência, lesão ou condição que não esteja confirmada; se a composição exigir um fato ausente, pergunte antes.
- Fotos e vídeos usados como evidência devem pertencer ao próprio caso. Prefira foto clínica estritamente necessária e mídia confirmada; nunca use imagem de outro acidente.
- Não exponha CPF, RG, endereço residencial, telefone, prontuário ou outros dados pessoais que não pertençam aos campos do template.
- Uma mídia presente na pasta não prova que seja registro do acidente. Confirme sua natureza.
- Não altere o conteúdo factual da imagem. Recorte ou anonimização só com autorização e mantendo o original intacto.
- O construtor remove mídia residual escondida dos templates antes de inserir as imagens do caso.

## Regras de diagramação da investigação

- Este é o padrão permanente das novas investigações. Não trate estas regras como preferência de um caso específico; só desvie mediante instrução expressa do usuário.
- Preserve os dois templates e aplique as alterações dentro dos campos existentes.
- No campo de lesão, posicione a fotografia primeiro e a descrição imediatamente abaixo.
- No cabeçalho da ocorrência, mantenha `*RAT` no campo amarelo da esquerda e somente o identificador numérico no campo amarelo da direita; o título superior pode manter `RAT <número>`.
- Centralize horizontal e verticalmente o cabeçalho e todos os itens das colunas `QUEM?` e `STATUS` do plano de ação.
- **Tipografia e Estilo Obrigatório das Respostas**:
  - Todo campo de resposta do formulário (na Folha 1 e Folha 2) deve ter **fonte tamanho 7,5 e estar em itálico**.
  - Os campos "O que houve" (narrativa) e "Ações imediatas" devem ter fonte 7,5 e respostas em itálico.
- **Padrões de Conteúdo e Formatação da Primeira Folha**:
  - `Unidade`: Usar nome simplificado — **não o nome completo do SAP/sistema**:
    - Unidades de Guarulhos: `TA Prod` (Tubos e Aços Produção), `Inox Prod` (Inox Produção), `Incotep`, `Soluções`.
    - Filiais (fora de Guarulhos): apenas o nome do local — `Joinville`, `Canoas`, `Caxias do Sul`, `Curitiba`, `Sertãozinho`, `MG`, `RJ`, `Goiânia`, `Brasília`, `Guarulhos`, etc.
    - O script `format_unit()` aplica esse mapeamento automaticamente; conferir se novo caso usa nome fora do mapa.
  - `RE`: Formatado com ponto como separador de milhar (ex.: `12.553`, `5.021`). O script `format_re()` aplica automaticamente.
  - `Nome do acidentado`: Encurtar/abreviar nomes do meio quando necessário para não gerar quebra de linha visual na célula (ex.: `Marcos Alberto de S. Junior`).
  - `Afastamento`: Informar estritamente o número de dias com a unidade (ex.: `60 dias`, `0 dias`).
  - `Contato do acidentado`: Se não houver número, preencher estritamente com `-` (traço simples).
  - `Experiência`: Formatar estritamente em anos e meses decimais/sintéticos (ex.: `2,8 anos`).
  - `Testemunha`: Mencionar apenas o nome do colaborador ou `Não Aplicável`.
  - `Status`: Indicar de forma curta se o colaborador está bem aguardando repouso do afastamento ou se já voltou às atividades (ex.: `Em repouso domiciliar` ou `Retornou às atividades`).
  - `Time`: Conter apenas o nome do participante e o setor entre parênteses, sem título de engenheiro (ex.: `Denisson Monteiro (SESMT)` e `Vanderlei Martins (Produção)`). **Deve sempre incluir alguém da Produção**; se o caso não tiver referência, adicionar o supervisor direto da vítima como representante da Produção. O script `format_team()` aplica normalização e complemento automático.
  - `Causa raiz`: Deve ser objetiva, técnica e direta.
  - **Campo Lesão / Condição / Sinistro (Comunicado)**:
    - No comunicado HTML, a fotografia da lesão deve aparecer **primeiro** (acima), ocupando o espaço disponível (`object-fit: contain`, sem distorção).
    - Abaixo da imagem, exibir `Lesão: <texto>` centralizado e em itálico, com quebra de linha fluida/normal (sem truncamento, `nowrap` ou `ellipsis`), garantindo que a descrição completa da lesão esteja sempre visível e legível.
    - Sem `figcaption` separado — o texto descritivo é suficiente.
  - **Campo Esclarecimento de Trajeto (RAT Trajeto)**:
    - Sempre usar **imagem ilustrativa** no campo de detalhe (reconstituição da rota ou do local) em formato retangular paisagem.
    - Se o espaço comportar, preferir 2 imagens lado a lado no modo paisagem.
    - Texto corrido no campo de detalhe só como texto complementar brevíssimo; nunca substitua a imagem por texto.
  - **Campo Detalhe (RAT Trabalho e Trajeto)**:
    - Sempre preencher com **imagem**, nunca com texto corrido.
    - Se o caso tiver apenas informações textuais para o campo, gerar uma imagem didática ultrarealista com as principais informações do ponto técnico destacado.
    - Registrar `images.details_kind: generated_detail` no JSON.
- **Padrões de Conteúdo e Formatação da Segunda Folha**:
  - `Plano de Ação - Linha 1 (Obrigatória)`:
    - **Quem**: `SESMT`
    - **Status**: `CONCLUÍDO`
    - **Ação**: `Alerta de Segurança`
    - **Como**: `Diálogo de segurança in loco`
    - **Quando**: Próximo dia útil subsequente à data da ocorrência do acidente (excluindo sábados e domingos).
    - As demais linhas (2 e 3) são definidas conforme a análise da investigação.
  - `Responsáveis / Campos de Assinatura (Quadros Brancos)`:
    - Deve conter apenas **Nome** e **RE** (sem cargo ou setor).
    - Se não houver referência de nome/RE cadastrado para a função, deixar os rótulos em branco um abaixo do outro para preenchimento manual:
      `Nome:`
      `RE:`
    - No quadro de Testemunhas, se não houver testemunhas, preencher apenas `Não Aplicável`.

## Nomes e aprovação

Enquanto não houver aprovação final, use nomes com prefixo `RASCUNHO -` e mantenha fora da pasta oficial.

Após aprovação expressa:

- DOCX: começa por `2026`, conforme o nome da pasta do caso.
- PDF: mesmo nome, prefixado por `A`, começando por `A2026`.
- Comunicado: preserve a convenção aprovada pelo usuário para a pasta.
- Salve sempre os dois arquivos na pasta da investigação correspondente. A publicação na pasta do caso faz parte da conclusão obrigatória do fluxo.
- Se já existir um arquivo com o mesmo nome, confirme se há autorização vigente para substituí-lo; sem essa autorização, preserve o existente e solicite decisão do usuário.

Nunca assine digitalmente nem simule assinatura. Os campos de assinatura permanecem destinados aos responsáveis reais.

## Verificação final

Antes da entrega:

- valide o JSON e a matriz de fontes;
- confirme o template correto;
- confirme exatamente duas páginas na investigação;
- confirme que a página 2 contém plano de ação e assinaturas;
- procure nomes, datas, REs, RATs e imagens de terceiros;
- procure resíduos dos templates, inclusive `23/02/2026`, `Cleber Edmar` e a imagem antiga incorporada;
- confira se cada afirmação técnica tem fonte ou aprovação registrada;
- renderize o DOCX e o PDF e examine todas as páginas;
- não copie para a pasta oficial antes da aprovação expressa;
- depois da aprovação, confirme que o DOCX e o PDF oficiais existem e podem ser abertos na pasta da ocorrência.
