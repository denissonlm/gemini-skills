---
name: gerador-ppp
description: Skill para automação e geração de Perfis Profissiográficos Previdenciários (PPP) em formato Word (.docx) sob padrão estético premium e fiel a legislações previdenciárias vigentes (Instrução Normativa INSS nº 128/2022).
---

# Skill: Gerador de Perfil Profissiográfico Previdenciário (PPP)

Esta skill orquestra a leitura de laudos de segurança do trabalho (PGR, LTCAT), fichas de registro de funcionários e outros insumos contidos em um diretório do cliente, estruturando essas informações em um JSON intermediário e gerando um Perfil Profissiográfico Previdenciário (PPP) premium no Word (.docx) sob a grade geométrica de 36 colunas de alta fidelidade. O documento é gerado com a imagem do cabeçalho corporativo e o rodapé de página dinâmico integrados nativamente nas seções do Word.

## 📁 Recursos da Skill
*   **Imagem de Cabeçalho**: O logo corporativo (`logo_cabecalho.png`) fica armazenado na subpasta `resources/` da skill e é inserido automaticamente em uma tabela no Header de página (Seção de Cabeçalho do Word), ocupando a dimensão exata de 2,66 cm x 1,60 cm.
*   **Rodapé Dinâmico**: Insere automaticamente no rodapé do documento Word a identificação do documento e o campo dinâmico de numeração de página (`PAGE`) alinhado à direita.

## 📋 Fluxo de Trabalho do Agente

Quando o usuário solicitar a criação de um PPP para um cliente a partir de uma pasta ou de arquivos soltos:

### Passo 1: Analisar os Insumos e Fazer a Extração de Dados
O agente deve ler todos os arquivos contidos no diretório indicado pelo usuário:
1.  **Ficha de Registro / Carteira de Trabalho**: Extrair os Dados Pessoais (CPF, Nome, PIS, Nascimento, Mãe, CTPS, Admissão) e o histórico de cargos, setores e GFIP para montar a tabela de **Lotação e Atribuição (Seção I, campo 13)**.
2.  **LTCAT / PGR / PCMSO**: Mapear de forma cronológica estrita todos os fatores de risco (Físicos, Químicos, Biológicos) por subperíodos de medição e associá-los na tabela de **Registros Ambientais (Seção II, campo 15)**.
3.  **Responsáveis Técnicos**: Extrair os Engenheiros/Médicos do Trabalho e seus respectivos registros de conselho de classe (CREA/CRM).

### Passo 2: Validar e Preencher Lacunas de Informação
Se alguma informação vital estiver ausente nos documentos (ex: CPF do representante legal, número do PIS, CPF do trabalhador), o agente deve **perguntar de forma direta e concisa** ao usuário no chat antes de prosseguir.

### Passo 3: Criar o JSON Intermediário (`dados_ppp.json`)
Crie um arquivo chamado `dados_ppp.json` na pasta do projeto do cliente contendo toda a estrutura de dados necessária. Utilize a seguinte estrutura canônica de referência:

```json
{
  "dados_pessoais": {
    "cnpj_empresa": "00.000.000/0000-00",
    "nome_empresa": "RAZÃO SOCIAL DA EMPRESA",
    "nome_trabalhador": "NOME COMPLETO DO COLABORADOR",
    "cpf": "000.000.000-00",
    "data_nascimento": "DD/MM/AAAA",
    "sexo": "M",
    "pis": "000.00000.00-0",
    "nome_mae": "NOME COMPLETO DA MÃE",
    "ctps_numero": "0000000",
    "ctps_serie": "000-0",
    "ctps_uf": "UF",
    "data_admissao": "DD/MM/AAAA",
    "regime_revesamento": "N/A",
    "nit": "000.00000.00-0"
  },
  "lotacao": [
    {
      "periodo": "DD/MM/AAAA a DD/MM/AAAA",
      "cnpj": "00.000.000/0000-00",
      "setor": "NOME DO SETOR",
      "cargo": "NOME DO CARGO",
      "funcao": "NOME DA FUNÇÃO",
      "cbo": "0000-00",
      "gfip": "01"
    }
  ],
  "atividades": [
    {
      "periodo": "DD/MM/AAAA a DD/MM/AAAA",
      "descricao": "Texto descritivo das atividades do trabalhador no período..."
    }
  ],
  "exposicao_riscos": [
    {
      "periodo": "DD/MM/AAAA a DD/MM/AAAA",
      "tipo": "F",
      "fator_risco": "Ruído",
      "intensidade_concentracao": "82,0 dB(A)",
      "tecnica": "NHO - 01 (NEN)",
      "epc_eficaz": "N/A",
      "epi_eficaz": "S",
      "ca": "11.512",
      "requisitos": {
        "med_prot": "S",
        "cond_func": "S",
        "prazo_val": "S",
        "periodic": "S",
        "higien": "S"
      }
    }
  ],
  "responsaveis_ambientais": [
    {
      "periodo": "DD/MM/AAAA a DD/MM/AAAA",
      "nit": "000.00000.00-0",
      "registro_conselho": "CREA 000000",
      "nome": "NOME DO ENGENHEIRO DE SEGURANÇA"
    }
  ],
  "monitoracao_biologica": [
    {
      "periodo": "DD/MM/AAAA a DD/MM/AAAA",
      "nit": "000.00000.00-0",
      "registro_conselho": "CRM 00000",
      "nome": "NOME DO MÉDICO DO TRABALHO"
    }
  ],
  "responsaveis_informacoes": {
    "data_emissao": "DD/MM/AAAA",
    "representante_legal": {
      "cpf": "000.000.000-00",
      "nome": "NOME DO REPRESENTANTE LEGAL",
      "cargo": "CARGO DO REPRESENTANTE"
    }
  },
  "observacoes": [
    "Informações adicionais relevantes, legislações citadas ou detalhamento técnico dos exames e riscos..."
  ]
}
```

### Passo 4: Executar o Script de Geração
Chame o script genérico em Python fornecido por esta skill para gerar o Word final de alta fidelidade:

```bash
python3 "/Users/denisson/Documents/Antigravity/skills/gerador-ppp/scripts/generate_ppp_generic.py" "<caminho_para_dados_ppp.json>" "<caminho_de_saida_novo_ppp.docx>"
```

### Passo 5: Validação Estética
Verifique se o arquivo Word gerado foi salvo sem erros no diretório de destino do cliente e se seu tamanho é superior a 40 KB. Informe ao usuário o caminho de destino do arquivo gerado.
