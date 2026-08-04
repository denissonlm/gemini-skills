import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import os

# ==============================================================================
# FUNÇÕES DE HERANÇA DA SKILL WORD-DOCUMENT-FORMATTING
# (NÃO ALTERAR ESTAS FUNÇÕES - ELAS GARANTEM A BLINDAGEM ESTÉTICA)
# ==============================================================================

def add_first_blank_page(doc):
    """Insere uma primeira página em branco para capa posterior no Canva."""
    p = doc.add_paragraph()
    p.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)

def format_paragraph_3pt_single(p):
    """Aplica 3pt antes, 3pt depois e entrelinhas simples em um parágrafo."""
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)

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
        if len(footer.paragraphs) == 0:
            footer_para = footer.add_paragraph()
        else:
            footer_para = footer.paragraphs[0]
            
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = footer_para.add_run("Página ")
        frun.font.name = 'Segoe UI Light'
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        
        # XML para campo dinâmico do Word (PAGE)
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
            try:
                cell = table.cell(r_idx, c_idx)
                text = cell.text.strip()
                total_cells += 1
                if len(text.split()) <= 2 or text.lower() in ["sim", "não", "nao", "-", "ghe-01", "ghe-02", "ghe-03", "ghe-04", "ghe-05"]:
                    short_count += 1
            except IndexError:
                pass
        
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
            tcMar = OxmlElement('w:tcMar')
            for margin_name, val in [('top', '60'), ('bottom', '60'), ('left', '100'), ('right', '100')]:
                node = OxmlElement(f'w:{margin_name}')
                node.set(qn('w:w'), val)
                node.set(qn('w:type'), 'dxa')
                tcMar.append(node)
            tcPr.append(tcMar)
            
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
                format_paragraph_3pt_single(p)
                
                if row_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    try:
                        p.alignment = col_alignments[cell_idx]
                    except IndexError:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        
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
    p.paragraph_format.left_indent = Pt(15)
    
    run_bullet = p.add_run("•  ")
    run_bullet.font.name = 'Segoe UI Light'
    run_bullet.font.size = Pt(12)
    
    run_title = p.add_run(f"{title}:")
    run_title.font.name = 'Segoe UI'
    run_title.font.bold = True
    run_title.font.size = Pt(12)
    
    punctuation = "." if is_last else ";"
    run_text = p.add_run(f" {text}{punctuation}")
    run_text.font.name = 'Segoe UI Light'
    run_text.font.size = Pt(12)


# ==============================================================================
# LÓGICA PRINCIPAL DO LAUDO (EXEMPLO)
# ==============================================================================

def gerar_documento(output_path, padrao="Normatiza"):
    # 1. PROCESSAMENTO IN-PLACE (Blindagem)
    if os.path.exists(output_path):
        print(f"O arquivo {output_path} já existe. Abrindo para edição In-Place.")
        doc = Document(output_path)
        # Lógica de edição cirúrgica em parágrafos e tabelas aqui...
        
    else:
        print(f"Gerando novo documento {output_path} a partir do zero.")
        doc = Document()
        setup_document_layout(doc)
        
        # 2. DEFINIR ESTILOS BASEADOS NO PADRÃO DE COR
        # (Exemplo simplificado)
        if padrao == "Normatiza":
            cor_h1 = RGBColor(0x1B, 0x36, 0x5D)
        else: # Deni
            cor_h1 = RGBColor(0x00, 0x00, 0x00)
            
        style_h1 = doc.styles['Heading 1']
        style_h1.font.name = 'Segoe UI'
        style_h1.font.bold = True
        style_h1.font.size = Pt(18)
        style_h1.font.color.rgb = cor_h1
        
        # 3. CONTEÚDO DO DOCUMENTO SST
        doc.add_heading('1.0 - Objetivo do Laudo', level=1)
        
        p = doc.add_paragraph("Este é um documento de SST. Lembre-se do rigor técnico, aplicando NR, Fundacentro e Métodos quantitativos dependendo do laudo gerado (PGR, LTCAT, AET, LI ou LP).")
        p.style = doc.styles['Normal']
        p.runs[0].font.name = 'Segoe UI Light'
        
        # 4. SALVAR
        doc.save(output_path)
        print(f"Documento salvo em: {output_path}")

if __name__ == "__main__":
    gerar_documento("Laudo_Exemplo.docx")
