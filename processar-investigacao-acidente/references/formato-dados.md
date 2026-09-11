# Formato do JSON do caso

Use `assets/exemplo-caso.json` como estrutura. Todos os valores usados no documento devem ter uma entrada em `evidence_ledger` com `status: confirmed`, fonte e localização. Para análises aprovadas pelo usuário, use `source: user_approval` e registre a data da aprovação.

As chaves `approvals.classification`, `approvals.technical_analysis` e `approvals.action_plan` precisam estar verdadeiras para a versão final.

`images.dynamics` deve apontar para a reconstituição ilustrativa, não para quadros de CFTV, e usar `images.dynamics_kind: generated_reconstruction`. Para RAT de acidente do trabalho, informe também `images.details` com a ilustração didática do ponto técnico relevante e `images.details_kind: generated_detail`. Esses campos precisam ter proveniência registrada como artes geradas a partir de fatos confirmados e aprovados.

Se, e somente se, o usuário afirmar expressamente que a causa raiz oficial é inconclusiva, registre `approvals.root_cause_inconclusive: true`. A ausência dessa confirmação faz o validador bloquear expressões como `inconclusiva`, `não determinada` e `a apurar` na causa raiz.

O validador rejeita lacunas e termos genéricos de preenchimento. Convenções obrigatórias de formatação:
- `victim.name`: Encurtar nomes do meio quando necessário para manter em linha única (ex.: "Marcos Alberto de S. Junior");
- `victim.absence`: Informar estritamente o número de dias com a unidade (ex.: "60 dias", "0 dias");
- `victim.contact`: Quando não houver número, usar estritamente "-" (traço simples);
- `victim.experience`: Expressar em anos e meses decimais/sintéticos (ex.: "2,8 anos");
- `victim.witnesses` / `signatures.witnesses`: Quando não aplicável, usar estritamente "Não Aplicável".
