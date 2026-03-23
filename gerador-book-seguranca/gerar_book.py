import os
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from PIL import Image
import sys

# --- CONFIGURAÇÕES BLINDADAS ---
BASE_DIR = r'C:\Users\denisson.monteiro\OneDrive - Grupo Açotubo\0 SESMT\Organizar\SESMT_v1\SESMT\Infográficos e Apresentações'
BOOK_ART_DIR = os.path.join(BASE_DIR, 'Book de Segurança')
PATH_CAPA = os.path.join(BOOK_ART_DIR, 'Capa.pdf')
PATH_JORNADA = os.path.join(BOOK_ART_DIR, 'Nossa Jornada.pdf')
PATH_TRANSICAO = os.path.join(BOOK_ART_DIR, 'Folha de transição.pdf')
PATH_ENCERRAMENTO = os.path.join(BOOK_ART_DIR, 'Encerramento.pdf')

# Destinos Finais
OUT_COMPLETO = os.path.join(BOOK_ART_DIR, 'Book_Seguranca_Acotubo_Oficial_COMPLETO.pdf')
OUT_ULTRA_LITE = os.path.join(BOOK_ART_DIR, 'Book_Seguranca_Acotubo_Oficial_ULTRA_LITE.pdf')

TEMP_DIR = r'C:\Users\denisson.monteiro\.gemini\tmp\denisson-monteiro\skill_book_temp'
if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)

# Categorias e seus padrões de nomes (Garante a ordem)
categories = {
    "1. EQUIPAMENTOS DE PROTEÇÃO INDIVIDUAL (EPIS)": ["calçado", "capacete", "creme", "luvas", "óculos", "proteção auditiva", "botina", "integração de epis"],
    "2. AÇÕES COMPORTAMENTAIS E CULTURA": ["atos", "janeiro branco", "piloto automático", "tabagismo", "falar em público", "ato e condição", "medida disciplinar", "regras de ouro", "palavras de segurança"],
    "3. OPERAÇÃO E LOGÍSTICA SEGURA": ["queda de carga", "carga segura", "cunhamento", "empilhadeira", "ponte rolante", "içamento"],
    "4. PROCEDIMENTOS E INTEGRAÇÃO": ["5s", "direito de recusa", "integração", "celular em fábrica", "acidente do trabalho", "apr", "checklist", "escada", "estilete", "termo de acesso"]
}

def create_transition_overlay(title):
    path = os.path.join(TEMP_DIR, "overlay.pdf")
    c = canvas.Canvas(path, pagesize=A4); w, h = A4
    c.setFillColor(HexColor('#000000'))
    clean = title.replace(".pdf", "").replace(".png", "").replace("Apresentação", "APRESENTAÇÃO:").replace("Info", "INFOGRÁFICO:").upper()
    lines = simpleSplit(clean, "Helvetica-Bold", 24, w - 160)
    y = h/2 + (len(lines) * 24 / 2)
    for l in lines:
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(w/2, y, l)
        y -= 34
    c.showPage(); c.save()
    return path

def get_merged_transition(title):
    overlay_path = create_transition_overlay(title)
    doc_base = fitz.open(PATH_TRANSICAO)
    doc_overlay = fitz.open(overlay_path)
    doc_base[0].show_pdf_page(doc_base[0].rect, doc_overlay, 0)
    out_p = os.path.join(TEMP_DIR, f"trans_{hash(title)}.pdf")
    doc_base.save(out_p); doc_base.close(); doc_overlay.close()
    return out_p

def scan_files():
    # Lista arquivos soltos na pasta base (PDF e PNG)
    all_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f)) and f.lower().endswith(('.pdf', '.png'))]
    organized = {cat: [] for cat in categories}
    
    for f in all_files:
        matched = False
        for cat, keywords in categories.items():
            if any(key in f.lower() for key in keywords):
                organized[cat].append(f)
                matched = True
                break
        if not matched: organized["4. PROCEDIMENTOS E INTEGRAÇÃO"].append(f)
    return organized

def generate():
    print("Iniciando geração dos Books...")
    content = scan_files()
    doc_main = fitz.open()
    idx_entries = []; cur = 0

    # Capa e Jornada
    doc_main.insert_file(PATH_CAPA); cur += 1
    doc_main.insert_file(PATH_JORNADA); cur += 1
    idx_start = cur; doc_main.new_page(); doc_main.new_page(); cur += 2

    # Processar Conteúdo
    for cat, files in content.items():
        if not files: continue
        idx_entries.append({"label": cat, "page": cur, "is_cat": True})
        doc_main.insert_file(get_merged_transition(cat)); cur += 1
        
        for f in sorted(files):
            full = os.path.join(BASE_DIR, f)
            idx_entries.append({"label": f, "page": cur, "is_cat": False})
            doc_main.insert_file(get_merged_transition(f)); cur += 1
            
            pending = []
            if f.lower().endswith('.pdf'):
                src = fitz.open(full)
                for p in src: pending.append(("pdf", src, p.number, p.rect))
            else:
                img = Image.open(full); iw, ih = img.size; pending.append(("png", full, (iw, ih)))
            
            i = 0
            while i < len(pending):
                s = pending[i]; npg = doc_main.new_page(); cur += 1
                is_l = s[3].width > s[3].height if s[0]=="pdf" else True
                if is_l and (i+1 < len(pending)):
                    nxt = pending[i+1]
                    nis_l = nxt[3].width > nxt[3].height if nxt[0]=="pdf" else True
                    if nis_l:
                        r1, r2 = fitz.Rect(40, 60, A4[0]-40, A4[1]/2-20), fitz.Rect(40, A4[1]/2+20, A4[0]-40, A4[1]-60)
                        if s[0]=="pdf": npg.show_pdf_page(r1, s[1], s[2])
                        else: npg.insert_image(r1, filename=s[1], keep_proportion=True)
                        if nxt[0]=="pdf": npg.show_pdf_page(r2, nxt[1], nxt[2])
                        else: npg.insert_image(r2, filename=nxt[1], keep_proportion=True)
                        i += 2; continue
                rf = fitz.Rect(40, 60, A4[0]-40, A4[1]-80)
                if s[0]=="pdf": npg.show_pdf_page(rf, s[1], s[2])
                else: npg.insert_image(rf, filename=s[1], keep_proportion=True)
                i += 1
            if f.lower().endswith('.pdf'): src.close()

    # Encerramento
    doc_main.insert_file(PATH_ENCERRAMENTO); cur += 1

    # Índice Navegável
    for i in range(2):
        pg = doc_main[idx_start+i]; pg.draw_rect(fitz.Rect(0,0,A4[0],80), color=None, fill=(0.1,0.1,0.1))
        pg.insert_text((50, 50), "ÍNDICE GERAL NAVEGÁVEL", fontname="hebo", fontsize=22, color=(1,1,1))
        y = 130; st = 0 if i == 0 else 38
        for entry in idx_entries[st:st+38]:
            lbl = entry["label"].replace(".pdf","").replace(".png",""); tar = entry["page"]
            if entry["is_cat"]:
                y += 8; pg.insert_text((50,y), lbl.upper(), fontname="hebo", fontsize=11)
                pg.insert_text((A4[0]-80,y), str(tar+1), fontname="hebo", fontsize=11)
                pg.insert_link({"kind": fitz.LINK_GOTO, "page": tar, "from": fitz.Rect(50, y-10, A4[0]-50, y+2)}); y += 22
            else:
                pg.insert_text((70,y), lbl, fontname="helv", fontsize=9)
                pg.insert_text((A4[0]-80,y), str(tar+1), fontname="helv", fontsize=9)
                pg.insert_link({"kind": fitz.LINK_GOTO, "page": tar, "from": fitz.Rect(70, y-8, A4[0]-50, y+2)}); y += 15
            if y > A4[1]-60: break

    # Numeração
    for i in range(len(doc_main)):
        if i < 4 or i == len(doc_main)-1: continue
        doc_main[i].insert_text((A4[0]-80, A4[1]-30), f"Pg {i+1}", fontname="helv", fontsize=8, color=(0.5,0.5,0.5))

    # Salvar Completo
    doc_main.save(OUT_COMPLETO, garbage=4, deflate=True, clean=True)
    print(f"Salvo: {OUT_COMPLETO}")

    # Gerar Ultra Lite por Rasterização
    print("Gerando versão ULTRA LITE (Comprimida)...")
    doc_lite = fitz.open()
    for i in range(len(doc_main)):
        page = doc_main[i]
        pix = page.get_pixmap(dpi=120)
        doc_lite.new_page(width=page.rect.width, height=page.rect.height).insert_image(page.rect, stream=pix.tobytes("jpg"))
    doc_lite.save(OUT_ULTRA_LITE, garbage=4, deflate=True)
    doc_lite.close(); doc_main.close()
    print(f"Salvo: {OUT_ULTRA_LITE}")

if __name__ == "__main__":
    generate()
