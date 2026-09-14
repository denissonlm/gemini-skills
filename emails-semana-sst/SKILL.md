---
name: emails-semana-sst
description: "Coleta e processa automaticamente e-mails da última semana útil (segunda a sábado) da conta Exchange denisson.monteiro@acotubo.com.br via Apple Mail no macOS, gerando dashboards executivos em HTML focados em Segurança do Trabalho (SESMT). Use quando solicitado: 'emails da semana', 'report semanal de segurança', 'resumo semanal de emails', 'emails sst'."
---

# Report Semanal de E-mails SST (Grupo Açotubo)

Este skill automatiza a auditoria, extração e consolidação dos e-mails recebidos na conta corporativa **`denisson.monteiro@acotubo.com.br`** no aplicativo **Apple Mail (macOS)**, gerando relatórios executivos em formato HTML com padrão visual de alta fidelidade do Grupo Açotubo.

---

## 🎯 Objetivo e Escopo

Sempre que acionado, este skill deve:
1. Identificar a **última semana útil** fechada (intervalo estrito de **segunda-feira a sábado**, anterior à data da solicitação), ou aceitar datas personalizadas fornecidas pelo usuário.
2. Conectar-se ao aplicativo **Mail** do macOS e acessar a caixa de entrada da conta **Exchange** (`denisson.monteiro@acotubo.com.br`).
3. Varrer as mensagens do período cronológico alvo e aplicar filtros inteligentes de **Segurança e Saúde no Trabalho (SST)**.
4. Categorizar os fatos encontrados em pilares estratégicos de gestão de riscos.
5. Gerar o arquivo HTML interativo na pasta padrão `/Users/denisson/Documents/Antigravity/` e salvar automaticamente uma cópia em `/Users/denisson/Downloads/`.

---

## 📅 Regra de Negócio: Janela Temporal

* **Padrão Automático:** O intervalo analisado compreende a **segunda-feira** até o **sábado** da semana anterior à solicitação.
  * *Exemplo:* Se a solicitação for feita em uma segunda-feira, 14/09/2026, a janela auditada será de **08/09/2026 a 12/09/2026** (ou 07/09 a 12/09 caso segunda-feira tenha sido dia útil).
* **Parâmetros Flexíveis:** Caso o usuário solicite um período específico (ex.: *"analise os e-mails dos dias X a Y"*), a skill deve respeitar os argumentos passados.

---

## 🔍 Pilares de Classificação SST

Os e-mails identificados devem ser organizados nas seguintes frentes:

1. 🚨 **Acidentes & Casos Médicos:**
   * Comunicações de acidentes típicos ou de trajeto.
   * Atendimentos do Ambulatório Médico, atestados, fraturas, suturas e encaminhamentos ao Hospital Carlos Chagas ou rede credenciada.
   * Controle de afastamentos previdenciários e consultas de retorno ao trabalho.

2. 👟 **Gestão de EPIs & Calçados:**
   * Alertas de desabastecimento ou reposições emergenciais no Almoxarifado.
   * Trocas individuais de botinas e sapatos de segurança por desgaste.
   * Conciliação contábil e fechamento de faturas de EPIs com Compras.

3. 🧗 **NR-35 & Segurança Operacional em Fábrica:**
   * Projetos de engenharia de proteção contra quedas (instalação de Linhas de Vida, pontos de ancoragem).
   * Liberação de trabalho em altura para terceiros (limpeza de calhas, telhados, manutenção predial com retenção de ASO/certificados NR-35).
   * Relatórios de Inspeção de Fábrica (**RIF**) e Registro de Ocorrências (**RGO**).

4. 🗳️ **Governança, CIPA & Auditorias:**
   * Processos eleitorais da Comissão Interna de Prevenção de Acidentes e Assédio (**CIPA**) e editais de convocação.
   * Auditorias internas de processos e qualidade (cronogramas e reuniões de abertura).
   * Vistorias técnicas de seguradoras ou consultorias de saúde ocupacional (Porto Seguro/Porto Saúde).

5. 🧪 **Meio Ambiente & Riscos Químicos:**
   * Controle de reagentes de laboratório (ex.: **Nital** / ácido nítrico e etanol para ensaios metalográficos).
   * Diretrizes de FISPQ/FDS, rotulagem e bacias de contenção de vazamentos.

6. ⚖️ **Jurídico Trabalhista & Perícias:**
   * Agendamento de perícias judiciais de periculosidade ou insalubridade.
   * Alinhamentos com assistentes técnicos periciais (Grupo Proto, advogados corporativos).

---

## 🚀 Execução Automatizada

A skill disponibiliza um script Python de referência autônomo em:
📁 **`scripts/gerar_report_semanal.py`**

### Modo de Uso

```bash
# Execução padrão (calcula automaticamente a última semana útil de segunda a sábado):
python3 /Users/denisson/Documents/Antigravity/skills/emails-semana-sst/scripts/gerar_report_semanal.py

# Execução com datas customizadas:
python3 /Users/denisson/Documents/Antigravity/skills/emails-semana-sst/scripts/gerar_report_semanal.py --start-date 2026-09-08 --end-date 2026-09-12
```

---

## 🎨 Padrão Visual (Blindagem Açotubo)

O arquivo HTML gerado deve manter rigorosa conformidade visual:
* **Cores Oficiais:** Vermelho Açotubo (`#E30613`, `#B3050F`, `#FFEBEC`), Slate Dark (`#0F172A`), Branco e tons semânticos de alerta.
* **Tipografia:** Google Font `Plus Jakarta Sans` e ícones `FontAwesome 6`.
* **Identidade Integrada:** Logotipo oficial da Açotubo incorporado diretamente em Base64 (dispensa arquivos externos).
* **Navegação em Abas:**
  * Aba 1: Destaques Executivos com cards analíticos e status.
  * Aba 2: Tabela integral com todas as mensagens capturadas e botão modal para leitura do texto completo do e-mail.
* **Responsividade e Impressão:** Botão de impressão com estilos otimizados para exportação direta em PDF limpo ou formato A4 paisagem.
