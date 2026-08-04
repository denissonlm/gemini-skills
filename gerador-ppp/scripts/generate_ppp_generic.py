import os
import sys
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

def set_cell_margins(cell, top=72, bottom=72, left=72, right=72):
    """Define margens internas da célula em dxa (1/20 de ponto)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="000000", bottom="000000", left="000000", right="000000"):
    """Configura bordas finas de 0.5pt (4 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    for side, color in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        if color:
            b_el = OxmlElement(f'w:{side}')
            b_el.set(qn('w:val'), 'single')
            b_el.set(qn('w:sz'), '4')
            b_el.set(qn('w:space'), '0')
            b_el.set(qn('w:color'), color)
            tcBorders.append(b_el)
        else:
            b_el = OxmlElement(f'w:{side}')
            b_el.set(qn('w:val'), 'none')
            tcBorders.append(b_el)
    tcPr.append(tcBorders)

def set_cell_shading(cell, color):
    """Aplica cor de fundo (shading) na célula."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color}"/>'
    cell._element.get_or_add_tcPr().append(parse_xml(shading_xml))

def build_table_section(doc, t_cols, rows_data, col_width_cm):
    """Constrói uma tabela baseada em spans de grade de 36 colunas."""
    table = doc.add_table(rows=0, cols=36)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Configurar larguras exatas para a grade de 36 colunas
    for i, col in enumerate(table.columns):
        col.width = Inches(col_width_cm)
        
    for r_idx, row_spec in enumerate(rows_data):
        row = table.add_row()
        row.height = Inches(0.18)
        
        cells_to_merge = []
        curr_col = 0
        for span, text, align, is_bold, size, is_header in row_spec:
            cell = row.cells[curr_col]
            end_col = curr_col + span - 1
            if span > 1:
                cell.merge(row.cells[end_col])
            
            cells_to_merge.append((cell, span, text, align, is_bold, size, is_header))
            curr_col += span
            
        # Formatar células após merge
        for cell, span, text, align, is_bold, size, is_header in cells_to_merge:
            set_cell_margins(cell, top=50, bottom=50, left=72, right=72)
            
            if is_header:
                set_cell_borders(cell, top="000000", bottom="000000", left="000000", right="000000")
                set_cell_shading(cell, "F2F2F2")
            else:
                set_cell_borders(cell, top="000000", bottom="000000", left="000000", right="000000")
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            
            if align == "center":
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif align == "justify":
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            run = p.add_run(text)
            run.font.name = "Arial Narrow"
            run.font.size = Pt(size)
            run.font.bold = is_bold
            
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def generate_document_from_json(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    doc = Document()
    
    # 1. Configuração de Margens (2.0 cm superior/inferior, 1.0 cm laterais)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.7874)     # 2.0 cm
        section.bottom_margin = Inches(0.7874)  # 2.0 cm
        section.left_margin = Inches(0.3937)    # 1.0 cm
        section.right_margin = Inches(0.3937)   # 1.0 cm
        section.page_width = Inches(8.2677)     # A4
        section.page_height = Inches(11.6929)   # A4
        
        # 1.1 Configurar o cabeçalho da página (imagem e tabela de cabeçalho do template)
        header = section.header
        header.is_linked_to_previous = False
        
        # Limpar parágrafos padrões do cabeçalho
        for p in list(header.paragraphs):
            p_element = p._p
            p_element.getparent().remove(p_element)
            
        header_table = header.add_table(rows=1, cols=2, width=Inches(19.0 / 2.54))
        header_table.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        cell_img = header_table.rows[0].cells[0]
        cell_txt = header_table.rows[0].cells[1]
        
        cell_img.width = Inches(3.185583333333333 / 2.54)
        cell_txt.width = Inches(15.815027777777777 / 2.54)
        
        set_cell_margins(cell_img, top=50, bottom=50, left=72, right=72)
        set_cell_margins(cell_txt, top=50, bottom=50, left=72, right=72)
        
        set_cell_borders(cell_img, top="000000", bottom="000000", left="000000", right="000000")
        set_cell_borders(cell_txt, top="000000", bottom="000000", left="000000", right="000000")
        
        p_img = cell_img.paragraphs[0]
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(3)
        p_img.paragraph_format.space_after = Pt(3)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "..", "resources", "logo_cabecalho.png")
        if not os.path.exists(logo_path):
            logo_path = "logo_cabecalho.png"
            
        if os.path.exists(logo_path):
            try:
                run_img = p_img.add_run()
                run_img.add_picture(logo_path, width=Inches(2.658 / 2.54), height=Inches(1.60 / 2.54))
            except Exception as e:
                p_img.add_run("[AÇOTUBO]")
        else:
            p_img.add_run("[AÇOTUBO]")
            
        p_txt = cell_txt.paragraphs[0]
        p_txt.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_txt.paragraph_format.space_before = Pt(2)
        p_txt.paragraph_format.space_after = Pt(2)
        p_txt.paragraph_format.line_spacing = 1.05
        
        txt_header = (
            "ANEXO XVII\n"
            "INSTRUÇÃO NORMATIVA PRES/INSS Nº 128, DE 28 DE MARÇO DE 2022\n"
            "PERFIL PROFISSIOGRÁFICO PREVIDENCIÁRIO – PPP"
        )
        run_txt = p_txt.add_run(txt_header)
        run_txt.font.name = "Arial Narrow"
        run_txt.font.size = Pt(7.5)
        run_txt.font.bold = True
        
        # 1.2 Configurar o rodapé da página (numeração dinâmica)
        footer = section.footer
        p_footer = footer.paragraphs[0]
        p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_footer.paragraph_format.space_before = Pt(0)
        p_footer.paragraph_format.space_after = Pt(0)
        
        run_foot = p_footer.add_run("Perfil Profissiográfico Previdenciário - PPP | Página ")
        run_foot.font.name = "Arial Narrow"
        run_foot.font.size = Pt(8)
        run_foot.font.italic = True
        run_foot.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        p_footer._p.append(fldSimple)
        
    # Idioma padrão pt-BR
    doc.styles['Normal'].font.name = 'Segoe UI'
    doc.styles['Normal'].font.size = Pt(9)
    doc.styles['Normal'].element.xpath('w:rPr')[0].append(parse_xml('<w:lang %s w:val="pt-BR"/>' % nsdecls('w')))
    
    # Grade de 36 colunas, largura total 19.0 cm (col_width = 19.0 / 36.0 = 0.5278 cm)
    col_width_cm = 19.0 / 36.0 / 2.54 # dxa/Inches
    t_cols = [col_width_cm * (i+1) for i in range(36)]
    
    # ----------------------------------------------------
    # TABELA 1: SEÇÃO I - DADOS ADMINISTRATIVOS (36 colunas, largura total 19.0 cm)
    # ----------------------------------------------------
    dp = data.get("dados_pessoais", {})
    t2_rows = [
        [(36, "SEÇÃO I - DADOS ADMINISTRATIVOS", "center", True, 10, True)],
        [(18, f"1. CNPJ do Domicílio Tributário do Estabelecimento:\n{dp.get('cnpj_empresa', '')}", "left", False, 8, False),
         (18, f"2. Nome da Empresa:\n{dp.get('nome_empresa', '')}", "left", False, 8, False)],
        [(36, f"3. Nome do Trabalhador:\n{dp.get('nome_trabalhador', '')}", "left", False, 8, False)],
        [(9, f"4. CPF:\n{dp.get('cpf', '')}", "left", False, 8, False),
         (9, f"5. Data de Nascimento:\n{dp.get('data_nascimento', '')}", "left", False, 8, False),
         (4, f"6. Sexo:\n{dp.get('sexo', '')}", "left", False, 8, False),
         (14, f"7. PIS/PASEP / NIT:\n{dp.get('pis', '')}", "left", False, 8, False)],
        [(36, f"8. Nome da Mãe:\n{dp.get('nome_mae', '')}", "left", False, 8, False)],
        [(15, f"9. CTPS (Nº, Série, UF):\n{dp.get('ctps_numero', '')} - {dp.get('ctps_serie', '')} / {dp.get('ctps_uf', '')}", "left", False, 8, False),
         (10, f"10. Data de Admissão:\n{dp.get('data_admissao', '')}", "left", False, 8, False),
         (11, f"11. Regime de Revesamento:\n{dp.get('regime_revesamento', '')}", "left", False, 8, False)]
    ]
    build_table_section(doc, t_cols, t2_rows, col_width_cm)
    
    # ----------------------------------------------------
    # TABELA 3: LOTAÇÃO E ATRIBUIÇÃO (campos 13 e 14)
    # ----------------------------------------------------
    t3_rows = [
        [(36, "13. LOTAÇÃO E ATRIBUIÇÃO", "center", True, 10, True)],
        [(5, "13.1 Período", "center", True, 8, False), 
         (6, "13.2 CNPJ/CEI", "center", True, 8, False), 
         (6, "13.3 Setor", "center", True, 8, False), 
         (7, "13.4 Cargo", "center", True, 8, False), 
         (7, "13.5 Função", "center", True, 8, False), 
         (3, "13.6 CBO", "center", True, 8, False), 
         (2, "13.7 GFIP", "center", True, 8, False)]
    ]
    
    for item in data.get("lotacao", []):
        t3_rows.append([
            (5, item.get("periodo", ""), "center", False, 8, False),
            (6, item.get("cnpj", ""), "center", False, 8, False),
            (6, item.get("setor", ""), "left", False, 8, False),
            (7, item.get("cargo", ""), "left", False, 8, False),
            (7, item.get("funcao", ""), "left", False, 8, False),
            (3, item.get("cbo", ""), "center", False, 8, False),
            (2, item.get("gfip", ""), "center", False, 8, False)
        ])
    build_table_section(doc, t_cols, t3_rows, col_width_cm)
    
    # ----------------------------------------------------
    # TABELA 4: DESCRIÇÃO DAS ATIVIDADES (campo 14)
    # ----------------------------------------------------
    t4_rows = [
        [(36, "14. DESCRIÇÃO DAS ATIVIDADES", "center", True, 10, True)],
        [(6, "14.1 - Período", "center", True, 8, False), 
         (30, "14.2 - Descrição Detalhada das Atividades", "center", True, 8, False)]
    ]
    
    for item in data.get("atividades", []):
        t4_rows.append([
            (6, item.get("periodo", ""), "center", False, 8, False),
            (30, item.get("descricao", ""), "justify", False, 8, False)
        ])
    build_table_section(doc, t_cols, t4_rows, col_width_cm)
    
    # ----------------------------------------------------
    # TABELA 5: EXPOSIÇÃO A FATORES DE RISCOS (campo 15)
    # ----------------------------------------------------
    t5_rows = [
        [(36, "REGISTROS AMBIENTAIS", "center", True, 10, True)],
        [(36, "15 - EXPOSIÇÃO A FATORES DE RISCOS", "center", True, 10, True)],
        [(5, "15.1 - Período", "center", True, 7.5, False), 
         (2, "15.2 Tipo", "center", True, 7.5, False), 
         (6, "15.3 - Fator de Risco", "center", True, 7.5, False), 
         (3, "15.4 - Int./Conc.", "center", True, 7.5, False), 
         (4, "15.5 - Técnica", "center", True, 7.5, False), 
         (2, "15.6 EPC", "center", True, 7.5, False), 
         (2, "15.7 EPI", "center", True, 7.5, False), 
         (2, "15.8 CA", "center", True, 7.5, False), 
         (10, "15.9 - Requisitos NR-06 / NR-01 (*)", "center", True, 7.5, False)],
        [(5, "", "center", True, 8, False), 
         (2, "", "center", True, 8, False), 
         (6, "", "center", True, 8, False), 
         (3, "", "center", True, 8, False), 
         (4, "", "center", True, 8, False), 
         (2, "", "center", True, 8, False), 
         (2, "", "center", True, 8, False), 
         (2, "", "center", True, 8, False), 
         (2, "Med. Prot.", "center", True, 6.5, False), 
         (2, "Cond. Func.", "center", True, 6.5, False), 
         (2, "Prazo Val.", "center", True, 6.5, False), 
         (2, "Periodic.", "center", True, 6.5, False), 
         (2, "Higien.", "center", True, 6.5, False)]
    ]
    
    for item in data.get("exposicao_riscos", []):
        req = item.get("requisitos", {})
        t5_rows.append([
            (5, item.get("periodo", ""), "center", False, 8, False),
            (2, item.get("tipo", ""), "center", False, 8, False),
            (6, item.get("fator_risco", ""), "left", False, 8, False),
            (2, item.get("intensidade_concentracao", ""), "center", False, 8, False),
            (4, item.get("tecnica", ""), "center", False, 8, False),
            (2, item.get("epc_eficaz", ""), "center", False, 8, False),
            (2, item.get("epi_eficaz", ""), "center", False, 8, False),
            (2, item.get("ca", ""), "center", False, 8, False),
            (2, req.get("med_prot", "N"), "center", False, 8, False),
            (2, req.get("cond_func", "N"), "center", False, 8, False),
            (2, req.get("prazo_val", "N"), "center", False, 8, False),
            (2, req.get("periodic", "N"), "center", False, 8, False),
            (2, req.get("higien", "N"), "center", False, 8, False)
        ])
        
    t5_rows.append([
        (36, "*Legenda do item 15.9: Medida de Proteção: Foi tentada a implementação de medidas de proteção coletiva, de caráter administrativo ou de organização do trabalho, optando-se pelo Equipamento de Proteção Individual - EPI por inviabilidade técnica, insuficiência ou interinidade, ou ainda em caráter complementar ou emergencial?", "left", False, 7, False)
    ])
    t5_rows.append([
        (36, "Condição de Funcionamento do EPI: Foram observadas as condições de funcionamento e do uso ininterrupto do EPI ao longo do tempo, conforme especificação técnica do fabricante, ajustada às condições? Prazo de Validade do EPI: Foi observado o prazo de validade, conforme Certificado de Aprovação - CA do MTP? Periocidade da Troca do EPI: Foi observada a periodicidade de troca definida pelos programas ambientais, comprovada mediante recibo assinado pelo usuário em época própria? Higienização do EPI: Foi observada a higienização?", "left", False, 7, False)
    ])
    build_table_section(doc, t_cols, t5_rows, col_width_cm)
    
    # ----------------------------------------------------
    # TABELA 5: RESPONSÁVEL PELOS REGISTROS AMBIENTAIS (campo 16)
    # ----------------------------------------------------
    t6_rows = [
        [(36, "16. RESPONSÁVEL PELOS REGISTROS AMBIENTAIS", "center", True, 10, True)],
        [(7, "16.1 - Período", "center", True, 8, False), 
         (9, "16.2 - CPF", "center", True, 8, False), 
         (9, "16.3 - Registro Conselho de Classe", "center", True, 8, False), 
         (11, "16.4 - Nome do profissional legalmente habilitado", "center", True, 8, False)]
    ]
    
    for item in data.get("responsaveis_ambientais", []):
        t6_rows.append([
            (7, item.get("periodo", ""), "center", False, 8, False),
            (9, item.get("nit", "Não Encontrado"), "center", False, 8, False), # Pode conter CPF ou NIT conforme o JSON
            (9, item.get("registro_conselho", ""), "center", False, 8, False),
            (11, item.get("nome", ""), "left", False, 8, False)
        ])
    build_table_section(doc, t_cols, t6_rows, col_width_cm)
    
    # ----------------------------------------------------
    # TABELA 6: RESPONSÁVEIS PELAS INFORMAÇÕES (Assinaturas e Declaração)
    # ----------------------------------------------------
    ri = data.get("responsaveis_informacoes", {})
    rep = ri.get("representante_legal", {})
    
    decl_text = (
        "Declaramos, para todos os fins de direito, que as informações prestadas neste documento "
        "são verídicas e foram transcritas fielmente dos registros administrativos, das demonstrações "
        "ambientais e dos programas médicos de responsabilidade da empresa. É de nosso conhecimento que "
        "a prestação de informações falsas neste documento constitui crime de falsificação de documento "
        "público, nos termos do art. 297 do Código Penal e, também, que tais informações são de caráter "
        "privativo do trabalhador, constituindo crime, nos termos da Lei nº 9.029, de 13 de abril de 1995, "
        "práticas discriminatórias decorrentes de sua exigibilidade por outrem, bem como de sua divulgação "
        "para terceiros, ressalvado quando exigida pelos órgãos públicos competentes."
    )
    
    t8_rows = [
        [(36, "RESPONSÁVEIS PELAS INFORMAÇÕES", "center", True, 10, True)],
        [(36, decl_text, "justify", False, 7.5, False)],
        [(9, "17 - Data da Emissão do PPP", "center", True, 8, False),
         (27, "18 - Representante Legal da Empresa", "center", True, 8, False)],
        [(9, ri.get("data_emissao", ""), "center", False, 8.5, False),
         (9, "18.1 - CPF do Representante Legal", "center", True, 7.5, False),
         (18, "18.2 - Nome do Representante Legal", "center", True, 7.5, False)],
        [(9, "", "center", False, 8.5, False),
         (9, rep.get("cpf", ""), "center", False, 8.5, False),
         (18, f"{rep.get('nome', '')} | {rep.get('cargo', '')}", "center", False, 8.5, False)],
        [(9, "", "center", False, 8.5, False),
         (9, "(Carimbo da Empresa)", "center", False, 7, False),
         (18, "(Assinatura física ou eletrônica)", "center", False, 7, False)]
    ]
    build_table_section(doc, t_cols, t8_rows, col_width_cm)
    
    # ----------------------------------------------------
    # TABELA 7: OBSERVAÇÕES
    # ----------------------------------------------------
    obs_lines = data.get("observacoes", [])
    obs_text = "\n\n".join(obs_lines)
    
    t9_rows = [
        [(36, "OBSERVAÇÕES", "center", True, 10, True)],
        [(36, obs_text, "justify", False, 8.5, False)]
    ]
    build_table_section(doc, t_cols, t9_rows, col_width_cm)

    
    # Criar pasta de saída se não existir
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    doc.save(output_path)
    print(f"PPP gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 generate_ppp_generic.py <dados_ppp.json> <output_ppp.docx>")
        sys.exit(1)
    generate_document_from_json(sys.argv[1], sys.argv[2])
