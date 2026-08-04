---
name: word-document-formatting
description: Formata qualquer documento técnico em Microsoft Word (.docx) sob padrões estéticos premium, utilizando python-docx com fontes Segoe UI, tabelas em Arial Narrow e blocos de destaque alinhados à margem esquerda, suportando os padrões de cores Normatiza e Deni.
---

# Diretrizes de Formatação de Documentos Técnicos no Word (.docx)

Esta skill orienta o agente a criar e formatar documentos técnicos profissionais e corporativos no formato Microsoft Word (.docx). A formatação é executada via programação em Python utilizando a biblioteca `python-docx`.

---

## 1. Protocolo de Alinhamento com o Usuário (Pré-execução)

Antes de gerar qualquer documento Word utilizando esta skill, o agente **deve perguntar ativamente ao usuário** três informações no chat:
1. **Paleta de Cores Desejada**: Padrão **Normatiza** (tons de azul e verde) ou Padrão **Deni** (tons de preto, cinza e vermelho de destaque).
2. **Descrição da Revisão**: O texto descritivo para a tabela de histórico (ex: "Emissão Inicial", "Revisão de Campo", etc.).
3. **Credenciais do Profissional**: Dados para assinatura e identificação no final do documento e na tabela de revisões. Caso o usuário não forneça dados alternativos, utilize o padrão do usuário:
   * **Nome**: Denisson Lopes Monteiro
   * **Formação**: Engenheiro de Controle e Automação, Pós Graduado em Segurança do Trabalho
   * **CREA**: 5069572289/SP

---

## 2. Padrões Geométricos e Idioma do Documento

*   **Margens**: 2,0 cm em todas as bordas (superior, inferior, esquerda, direita).
*   **Primeira Página (Capa)**: Configurada em branco ("Different First Page") para receber imagem de capa externa. Cabeçalhos e rodapés devem ser ocultos apenas nesta folha.
*   **Segunda Página (Sumário e Histórico de Revisões)**:
    *   **Sumário**: Deixar uma seção em branco reservada para o índice. O sumário não deve ser gerado programaticamente; inclua apenas uma nota orientando o usuário a inseri-lo nativamente pelo Word para manter a numeração perfeita.
    *   **Tabela de Histórico de Revisões**: Inserida logo após o espaço do sumário na segunda página, formatada de acordo com o padrão de tabelas técnicas (Arial Narrow 8pt, padding de 3pt, texto centralizado verticalmente nas células, alinhamento centralizado para respostas curtas).
        *   **Colunas**: `Rev.` (Revisão, ex: "00"), `Data` (Data atual do processamento, ex: "04/07/2026"), `Descrição da Alteração` (Texto obtido na pergunta de pré-execução), e `Responsável` (Nome e CREA do profissional).
*   **Cabeçalho**: Deve ser removido (vazio) de todas as páginas para manter o visual limpo.
*   **Rodapé**: Inserir numeração de página dinâmica no formato `"Página X"` centralizado no rodapé a partir da segunda página.
*   **Controle Ortográfico e Idioma**: Configurar programaticamente o idioma padrão do documento e de todos os estilos criados como **Português Brasileiro (pt-BR)**. Isso impede que o Word marque textos válidos com locais ondulados vermelhos de erro de grafia.

---

## 3. Padrões de Tipografia por Paleta de Cores e Estilos de Título

*   **Corpo de Texto (Estilo Normal)**:
    *   **Fonte**: `Segoe UI Light`
    *   **Tamanho**: 12pt
    *   **Alinhamento**: Justificado (`WD_ALIGN_PARAGRAPH.JUSTIFY`)
    *   **Espaçamento de Linha**: 1.15
    *   **Espaçamento Depois**: 6pt
    *   **Cor**: Cinza Escuro (`#333333`).

### 3.1 Definição e Numeração de Títulos Estruturais (Word Heading Styles)
Os títulos **devem ser formalmente vinculados** aos estilos nativos do Word (`Heading 1`, `Heading 2`, `Heading 3`) para que apareçam na árvore de navegação e no sumário automático. Eles devem conter numeração estruturada e sequencial dinâmica no próprio texto (`1.0`, `1.1`, `1.1.1`):
*   **Nível 1 (Heading 1)**: Formato `X.0 - Título`. Ex: `1.0 - Objetivo`, `2.0 - Introdução`.
*   **Nível 2 (Heading 2)**: Formato `X.Y - Subtítulo`. Ex: `2.1 - Critérios da NR-1`.
*   **Nível 3 (Heading 3)**: Formato `X.Y.Z - Seção`. Ex: `2.1.1 - Conceito Geral`.

#### Padrão de Cores "Normatiza"
*   **Heading 1**: 18pt, azul escuro (`#1B365D`), espaço antes 18pt, depois 8pt, Segoe UI, Negrito.
*   **Heading 2**: 14pt, azul intermediário (`#4A779D`), espaço antes 14pt, depois 6pt, Segoe UI, Negrito.
*   **Heading 3**: 12pt, cinza escuro (`#333333`), espaço antes 10pt, depois 4pt, Segoe UI, Negrito.
*   **Destaque Nível 1**: Verde escuro (`#2E7D32`) e preenchimento verde claro (`#F1F8F3`).
*   **Destaque Nível 2**: Azul escuro (`#1B365D`) e preenchimento azul claro (`#F4F7FA`).

#### Padrão de Cores "Deni"
*   **Heading 1**: 18pt, preto (`#000000`), espaço antes 18pt, depois 8pt, Segoe UI, Negrito.
*   **Heading 2**: 14pt, cinza escuro (`#555555`), espaço antes 14pt, depois 6pt, Segoe UI, Negrito.
*   **Heading 3**: 12pt, cinza intermediário (`#777777`), espaço antes 10pt, depois 4pt, Segoe UI, Negrito.
*   **Destaque Nível 1**: Vermelho de destaque (`#CC0000`) e preenchimento cinza muito claro (`#F9F9F9`).
*   **Destaque Nível 2**: Preto (`#000000`) e preenchimento cinza claro (`#F2F2F2`).

---

## 4. Estrutura e Formatação de Tópicos (Itens e Listas)

Os tópicos (listas de itens com marcadores) devem ser formatados de forma estrita para manter a elegância e conformidade com a norma culta da língua portuguesa:
*   **Alinhamento**: Alinhados à esquerda, porém com o texto de detalhamento **Justificado**.
*   **Espaçamento de Parágrafo**: 3pt antes e 3pt depois (`space_before = Pt(3)`, `space_after = Pt(3)`).
*   **Tabulação Simples (Recuo)**: Recuo esquerdo do parágrafo de 15pt (`left_indent = Pt(15)`).
*   **Formato de Destaque Interno**:
    *   O marcador deve ser o símbolo padrão de ponto (`•  `).
    *   O título ou assunto principal do tópico deve estar em **Negrito**, seguido obrigatoriamente de dois pontos **":"** (ex: "**Título do Tópico:**").
    *   A explicação ou detalhamento do tópico deve vir na sequência imediata, em texto normal (Segoe UI Light 12pt).
*   **Pontuação de Final de Item**: Seguir estritamente a pontuação oficial da língua portuguesa para listas:
    *   Cada item intermediário da lista deve terminar obrigatoriamente com ponto e vírgula **";"**.
    *   O último item da lista deve terminar obrigatoriamente com ponto final **"."**.

---

## 5. Formatação Avançada de Tabelas (Alinhamentos por Coluna)

As tabelas técnicas devem possuir alta densidade de dados e visual limpo (sem estilo zebra):
*   **Fonte das células**: `Arial Narrow` com tamanho 8pt.
*   **Margens Internas (Padding)**: 3pt superior e inferior (60 dxa no XML) e 5pt esquerdo e direito (100 dxa).
*   **Alinhamento Vertical**: Texto **centralizado verticalmente** em todas as células (usando o elemento XML `w:vAlign val="center"`).
*   **Cabeçalho da Tabela**: Fundo configurado com a Cor Primária da Paleta (`#1B365D` no Normatiza ou `#000000` no Deni) com texto em negrito na cor branca.
*   **Bordas**: Linhas finas de cor cinza claro (`#CCCCCC`) em todas as divisórias.
*   **Alinhamento de Célula Uniforme**: **Toda coluna deve possuir um alinhamento uniforme**. Não é permitido misturar alinhamento à esquerda e centralizado na mesma coluna.
    *   **Colunas de Dados Curtos/Métricas** (ex: CPF, Matrícula, Data, GHE, Dose, Limite, Nível de Risco, Sim/Não, `-`): Devem ser centralizadas por inteiro (`WD_ALIGN_PARAGRAPH.CENTER`).
    *   **Colunas de Dados Longos/Descrições** (ex: Nome do Funcionário, Descrição das Atividades, Recomendações, Observações): Devem ser alinhadas à esquerda por inteiro (`WD_ALIGN_PARAGRAPH.LEFT`).
*   **Propriedades de Linha**: Impedir que as linhas se dividam entre páginas (`cantSplit`) e configurar a repetição do cabeçalho no topo de novas páginas (`tblHeader`).

---

## 6. Blocos de Destaque Visual (Caixas de Alerta e Conclusões)

Os pareceres, notas e decisões importantes devem ser visualmente realçados. Para que a barra vertical de destaque fique alinhada com a margem do texto principal, o parágrafo correspondente deve conter um recuo esquerdo compensatório equivalente à medida da margem interna (`w:space`).

### 6.1 Bloco de Destaque de Nível 1 (Verde no Normatiza / Vermelho no Deni)
*   **Borda Esquerda**: Espessura 3pt (`w:sz="36"`), cor conforme a paleta (`#2E7D32` ou `#CC0000`), espaçamento (`w:space="15"`).
*   **Fundo**: Sombreamento conforme a paleta (`#F1F8F3` ou `#F9F9F9`).
*   **Compensação de Margem**: Recuo esquerdo de 15pt (`left_indent = Pt(15)`). Recuo direito em `Pt(0)`.
*   **Alinhamento**: Texto justificado.

### 6.2 Bloco de Destaque de Nível 2 (Azul no Normatiza / Preto no Deni)
*   **Borda Esquerda**: Espessura 4pt (`w:sz="48"`), cor conforme a paleta (`#1B365D` ou `#000000`), espaçamento (`w:space="20"`).
*   **Fundo**: Sombreamento conforme a paleta (`#F4F7FA` ou `#F2F2F2`).
*   **Compensação de Margem**: Recuo esquerdo de 20pt (`left_indent = Pt(20)`). Recuo direito em `Pt(0)`.
*   **Alinhamento**: Texto justificado.

### 6.3 Bloco de Observações / Notas Especiais (Cinza com Borda Azul/Preta)
*   **Estrutura**: Tabela de 1x1.
*   **Borda Esquerda**: Espessura 3pt (`w:sz="36"`), cor da paleta (`#1B365D` ou `#000000`), espaçamento (`w:space="15"`).
*   **Fundo**: Sombreamento cinza claro (`#F4F6F9`).
*   **Compensação de Margem**: Texto interno com recuo esquerdo de 15pt (`Pt(15)`) e alinhamento à esquerda.

---

## 7. Gestão de Imagens e Relatório Fotográfico

*   **Posicionamento**: As imagens devem ser inseridas em parágrafos de linha única centralizados, com espaçamento de 3pt antes e depois.
*   **Legenda**: Inserida no parágrafo imediatamente abaixo da imagem.
    *   **Alinhamento**: Alinhada à esquerda (`WD_ALIGN_PARAGRAPH.LEFT`).
    *   **Fonte**: `Times New Roman`, Itálico, tamanho 9.5pt.
    *   **Formato do Texto**: A legenda deve ser inserida programaticamente **sem passar caracteres literais de formatação markdown** (como `*` ou `***`). O script deve dividir a string de legenda (ex: dividindo pelo separador `" - "`) para formatar o marcador `"Figura X"` em **Negrito e Itálico** e o texto descritivo restante em **Itálico regular**. Exemplo visual resultante no Word: "***Figura 1*** - *Descrição ou legenda explicativa da evidência física.*"
*   **Validação de Coerência de Legendas**: O script **deve implementar um sistema ativo de validação** (ex: dicionário de correspondência de palavras-chave por imagem). O código de geração deve validar se as palavras-chave esperadas para cada arquivo de foto constam na legenda fornecida, lançando erro imediato se houver divergência de contexto para evitar legendas trocadas no documento final.
*   **Anexo Fotográfico Final**: Dispor as fotos do anexo em tabelas estruturadas (gride 2x2 ou side-by-side de colunas de tabela de largura definida, ex: `3.15 Inches`) para que fotos e legendas fiquem perfeitamente alinhadas e não se fragmentem em páginas distintas de forma desordenada.

---

## 8. Protocolo de Blindagem e Regras de Sobrevivência (Checklist Anti-Erros)

Esta seção constitui a blindagem operacional para o agente no desenvolvimento de qualquer documento técnico no Word:

### 8.1 Regra 1: Preservação de Edições do Usuário (Processamento In-Place)
*   **Mandatório**: Antes de executar ou reescrever qualquer documento que já foi gerado, verifique se o arquivo já existe no diretório final do usuário.
*   **Ação**: Caso o arquivo exista, pergunte se o usuário efetuou edições manuais nele. Se sim, **nunca gere o arquivo do zero**. Em vez disso, carregue o arquivo usando `docx.Document(caminho)` e modifique parágrafos e tabelas de forma cirúrgica na árvore OXML, salvando o mesmo arquivo para preservar 100% de suas alterações manuais.

### 8.2 Regra 2: Blindagem contra Markdown Literal no Word
*   **Mandatório**: Nunca passe asteriscos (`*`, `**`, `***`) ou underscores (`_`) em strings de texto que serão adicionados ao documento. O Word tratará esses marcadores como caracteres literais textuais.
*   **Ação**: Sempre aplique formatações de negrito e itálico dividindo a string em múltiplos `runs` e setando explicitamente `.font.bold = True` e `.font.italic = True` em cada run individual.

### 8.3 Regra 3: Alinhamento Uniforme e Dinâmico de Tabelas
*   **Mandatório**: Jamais misture alinhamento à esquerda e centralizado para células diferentes sob a mesma coluna técnica.
*   **Ação**: Desenvolva uma varredura de dados por coluna antes de aplicar os alinhamentos nas linhas. Defina se a coluna é de dados curtos/status (alinhada por inteiro ao centro) ou de dados longos/descrições (alinhada por inteiro à esquerda).

### 8.4 Regra 4: Definição Estrita de Estilos Heading Nativos
*   **Mandatório**: Sempre vincule seus títulos e subtítulos de seções aos estilos de parágrafo nativos do Word (`Heading 1`, `Heading 2`, `Heading 3`, `Heading 4`) para permitir o funcionamento perfeito do mapa de navegação de cabeçalhos e da tabela de sumário dinâmico.
*   **Ação**: Configure a formatação visual (fonte, cores da paleta, tamanho e espaçamento) redefinindo os estilos nativos no início do código com `doc.styles['Heading X']` e adicione os parágrafos usando `doc.add_heading(text, level=X)`.

---

## 9. Credenciais e Finalização do Documento (Sem Assinatura Manual)

O documento não deve conter campos de assinatura convencionais (ex: linhas `_____`). O encerramento deve apenas expor as credenciais do profissional informadas no alinhamento pré-execução, alinhadas de forma limpa. Exemplo:

**Denisson Lopes Monteiro**
Engenheiro de Controle e Automação, Pós Graduado em Segurança do Trabalho
CREA: 5069572289/SP

---

## 10. Funções Auxiliares de Programação em Python (`python-docx`)

Abaixo estão as funções recomendadas em Python para aplicar estas regras programaticamente:

```python
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def setup_document_layout(doc):
    """Configura margens de 2cm, cabeçalho diferente na primeira página e idioma pt-BR."""
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)
        section.different_first_page_header_footer = True
        
        # Limpar cabeçalho
        header = section.header
        header.is_linked_to_previous = False
        for p in header.paragraphs:
            p.text = ""
            
        # Adicionar numeração de página no rodapé
        footer = section.footer
        footer_para = footer.paragraphs[0]
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = footer_para.add_run("Página ")
        frun.font.name = 'Segoe UI Light'
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        
        # XML para campo dinâmico do Word
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'separate')
        fldChar3 = OxmlElement('w:fldChar')
        fldChar3.set(qn('w:fldCharType'), 'end')
        frun._r.extend([fldChar1, instrText, fldChar2, fldChar3])

    # Configuração Document-Wide para Português Brasileiro (pt-BR)
    try:
        styles_element = doc.styles.element
        rpr_default = styles_element.xpath('./w:docDefaults/w:rPrDefault/w:rPr')[0]
        lang = rpr_default.xpath('w:lang')
        if lang:
            lang_element = lang[0]
        else:
            lang_element = OxmlElement('w:lang')
            rpr_default.append(lang_element)
        lang_element.set(qn('w:val'), 'pt-BR')
        lang_element.set(qn('w:eastAsia'), 'pt-BR')
        lang_element.set(qn('w:bidi'), 'pt-BR')
    except Exception as e:
        print(f"Aviso ao definir idioma padrão: {e}")

    # Forçar pt-BR em todos os estilos existentes
    for style in doc.styles:
        if hasattr(style, 'element'):
            rPr = style.element.get_or_add_rPr()
            lang_el = OxmlElement('w:lang')
            lang_el.set(qn('w:val'), 'pt-BR')
            lang_el.set(qn('w:eastAsia'), 'pt-BR')
            lang_el.set(qn('w:bidi'), 'pt-BR')
            rPr.append(lang_el)

def format_technical_table(table, header_color_hex="1B365D"):
    """Aplica formatação premium em tabelas: Arial Narrow 8pt, padding 3pt e alinhamentos por coluna."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    num_cols = len(table.columns)
    col_alignments = []
    
    # Determinar alinhamento dinâmico da coluna inteira com base nos dados
    for c_idx in range(num_cols):
        short_count = 0
        total_cells = 0
        for r_idx in range(1, len(table.rows)):
            cell = table.cell(r_idx, c_idx)
            text = cell.text.strip()
            total_cells += 1
            # Se for curto (até 2 palavras) ou símbolos de status comum
            if len(text.split()) <= 2 or text.lower() in ["sim", "não", "nao", "-", "ghe-01", "ghe-02", "ghe-03", "ghe-04", "ghe-05"]:
                short_count += 1
        
        if total_cells > 0 and (short_count / total_cells) >= 0.75:
            col_alignments.append(WD_ALIGN_PARAGRAPH.CENTER)
        else:
            col_alignments.append(WD_ALIGN_PARAGRAPH.LEFT)

    for row_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if row_idx == 0:
            trPr.append(OxmlElement('w:tblHeader'))
            
        for cell_idx, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            
            # Margem interna (Padding): 3pt superior/inferior, 5pt lateral
            tcMar = OxmlElement('w:tcMar')
            for margin_name, val in [('top', '60'), ('bottom', '60'), ('left', '100'), ('right', '100')]:
                node = OxmlElement(f'w:{margin_name}')
                node.set(qn('w:w'), val)
                node.set(qn('w:type'), 'dxa')
                tcMar.append(node)
            tcPr.append(tcMar)
            
            # Centralização vertical do texto
            vAlign = OxmlElement('w:vAlign')
            vAlign.set(qn('w:val'), 'center')
            tcPr.append(vAlign)
            
            if row_idx == 0:
                shading = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), header_color_hex))
                tcPr.append(shading)
                
            borders = parse_xml(
                r'<w:tcBorders {} >'
                r'  <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
                r'  <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
                r'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
                r'  <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
                r'</w:tcBorders>'.format(nsdecls('w'))
            )
            tcPr.append(borders)
            
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                
                # Regra de Alinhamento da coluna inteira
                if row_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = col_alignments[cell_idx]
                        
                for run in p.runs:
                    run.font.name = 'Arial Narrow'
                    run.font.size = Pt(8)
                    if row_idx == 0:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    else:
                        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def add_bullet_topic(doc, title, text, is_last=False):
    """Insere um tópico alinhado à esquerda com título em negrito, dois pontos e pontuação pt-BR."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Pt(15) # Tabulação simples (recuo)
    
    # Marcador
    run_bullet = p.add_run("•  ")
    run_bullet.font.name = 'Segoe UI Light'
    run_bullet.font.size = Pt(12)
    
    # Título do Tópico
    run_title = p.add_run(f"{title}:")
    run_title.font.name = 'Segoe UI'
    run_title.font.bold = True
    run_title.font.size = Pt(12)
    
    # Texto de detalhamento
    punctuation = "." if is_last else ";"
    run_text = p.add_run(f" {text}{punctuation}")
    run_text.font.name = 'Segoe UI Light'
    run_text.font.size = Pt(12)
```
