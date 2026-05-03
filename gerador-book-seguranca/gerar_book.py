import os
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from PIL import Image
import sys
import platform
import unicodedata

# --- CONFIGURAÇÕES ADAPTÁVEIS ---
is_mac = platform.system() == 'Darwin'
home = os.path.expanduser("~")

if is_mac:
    # Caminho no MacBook (OneDrive via CloudStorage)
    BASE_DIR = os.path.join(home, 'Library/CloudStorage/OneDrive-GrupoAçotubo/0 SESMT/Organizar/SESMT_v1/SESMT/Infográficos e Apresentações')
    TEMP_DIR = os.path.join(home, '.gemini/tmp/denisson/skill_book_temp')
else:
    # Caminho no Windows (Mantido para retrocompatibilidade)
    BASE_DIR = r'C:\Users\denisson.monteiro\OneDrive - Grupo Açotubo\0 SESMT\Organizar\SESMT_v1\SESMT\Infográficos e Apresentações'
    TEMP_DIR = r'C:\Users\denisson.monteiro\.gemini\tmp\denisson-monteiro\skill_book_temp'

BOOK_ART_DIR = os.path.join(BASE_DIR, 'Book de Segurança')
PATH_CAPA = os.path.join(BOOK_ART_DIR, 'Capa.pdf')
PATH_JORNADA = os.path.join(BOOK_ART_DIR, 'Nossa Jornada.pdf')
PATH_TRANSICAO = os.path.join(BOOK_ART_DIR, 'Folha de transição.pdf')
PATH_ENCERRAMENTO = os.path.join(BOOK_ART_DIR, 'Encerramento.pdf')

# Destinos Finais
OUT_COMPLETO = os.path.join(BOOK_ART_DIR, 'Book_Seguranca_Acotubo_Oficial_COMPLETO.pdf')
OUT_ULTRA_LITE = os.path.join(BOOK_ART_DIR, 'Book_Seguranca_Acotubo_Oficial_ULTRA_LITE.pdf')

if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)

# Categorias e seus padrões de nomes (Normalizados para NFC)
def normalize_str(s):
    return unicodedata.normalize('NFC', s).lower()

categories = {
    "1. EQUIPAMENTOS DE PROTEÇÃO INDIVIDUAL (EPIS)": ["calçado", "capacete", "creme", "luvas", "óculos", "proteção auditiva", "botina", "integração de epis"],
    "2. AÇÕES COMPORTAMENTAIS E CULTURA": [
        "atos", "janeiro branco", "piloto automático", "tabagismo", "falar em público", 
        "ato e condição", "medida disciplinar", "regras de ouro", "palavras de segurança",
        "maio amarelo", "abril verde", "celular", "direito de recusa", "adornos", 
        "comportamento", "conscientização"
    ],
    "3. OPERAÇÃO E LOGÍSTICA SEGURA": ["queda de carga", "carga segura", "cunhamento", "empilhadeira", "ponte rolante", "içamento"],
    "4. PROCEDIMENTOS E INTEGRAÇÃO": ["5s", "integração", "acidente do trabalho", "apr", "checklist", "escada", "estilete", "termo de acesso"]
}

# Normalizar chaves das categorias
norm_categories = {k: [normalize_str(kw) for kw in v] for k, v in categories.items()}

def create_transition_overlay(title):
    path = os.path.join(TEMP_DIR, "overlay.pdf")
    c = canvas.Canvas(path, pagesize=A4); w, h = A4
    c.setFillColor(HexColor('#000000'))
    
    # Normalizar título para exibição correta
    clean = unicodedata.normalize('NFC', title).replace(".pdf", "").replace(".png", "").replace("Apresentação", "APRESENTAÇÃO:").replace("Info", "INFOGRÁFICO:").upper()
    
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
    if not os.path.exists(PATH_TRANSICAO):
        print(f"ERRO: Folha de transição não encontrada em {PATH_TRANSICAO}")
        return overlay_path
    doc_base = fitz.open(PATH_TRANSICAO)
    doc_overlay = fitz.open(overlay_path)
    doc_base[0].show_pdf_page(doc_base[0].rect, doc_overlay, 0)
    out_p = os.path.join(TEMP_DIR, f"trans_{abs(hash(title))}.pdf")
    doc_base.save(out_p); doc_base.close(); doc_overlay.close()
    return out_p

def scan_files():
    # Lista arquivos soltos na pasta base (PDF e PNG) e normaliza para NFC
    try:
        all_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f)) and f.lower().endswith(('.pdf', '.png'))]
    except Exception as e:
        print(f"ERRO ao ler BASE_DIR: {e}")
        return {}

    organized = {cat: [] for cat in categories}
    
    for f in all_files:
        fnorm = normalize_str(f)
        matched = False
        for cat, keywords in norm_categories.items():
            if any(key in fnorm for key in keywords):
                organized[cat].append(f)
                matched = True
                break
        if not matched: organized["4. PROCEDIMENTOS E INTEGRAÇÃO"].append(f)
    
    # Ordenar arquivos dentro de cada categoria
    for cat in organized:
        organized[cat].sort(key=lambda x: normalize_str(x))
        
    return organized

def generate():
    print("Iniciando geração dos Books...")
    content = scan_files()
    doc_main = fitz.open()
    idx_entries = []; cur = 0

    # Capa e Jornada
    for path in [PATH_CAPA, PATH_JORNADA]:
        if os.path.exists(path):
            doc_main.insert_file(path); cur += 1
        else:
            print(f"AVISO: Arquivo obrigatório não encontrado: {path}")

    idx_start = cur; doc_main.new_page(); doc_main.new_page(); cur += 2

    # Processar Conteúdo
    month_order = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

    for cat, files in content.items():
        if not files: continue
        
        # Ordenação especial para Comportamental
        if "COMPORTAMENTAIS" in cat:
            monthly = []
            others = []
            for f in files:
                fname = normalize_str(f)
                found_month = -1
                for idx, month in enumerate(month_order):
                    if month in fname:
                        found_month = idx
                        break
                if found_month != -1:
                    monthly.append((found_month, f))
                else:
                    others.append(f)
            
            # Ordenar meses cronologicamente e outros alfabeticamente
            monthly.sort(key=lambda x: x[0])
            others.sort(key=lambda x: normalize_str(x))
            files = [m[1] for m in monthly] + others

        print(f"Processando categoria: {cat}")
        idx_entries.append({"label": cat, "page": cur, "is_cat": True})
        doc_main.insert_file(get_merged_transition(cat)); cur += 1
        
        for f in files:
            full = os.path.join(BASE_DIR, f)
            print(f"  -> Adicionando: {f}")
            idx_entries.append({"label": f, "page": cur, "is_cat": False})
            doc_main.insert_file(get_merged_transition(f)); cur += 1
            
            pending = []
            try:
                if f.lower().endswith('.pdf'):
                    src = fitz.open(full)
                    for p in src: pending.append(("pdf", src, p.number, p.rect))
                else:
                    img = Image.open(full); iw, ih = img.size; pending.append(("png", full, (iw, ih)))
            except Exception as e:
                print(f"    ERRO ao abrir {f}: {e}")
                continue
            
            i = 0
            while i < len(pending):
                s = pending[i]; npg = doc_main.new_page(); cur += 1
                
                # Definir se é paisagem (Landscape)
                if s[0] == "pdf":
                    is_l = s[3].width > s[3].height
                else:
                    is_l = s[2][0] > s[2][1]

                if is_l and (i+1 < len(pending)):
                    nxt = pending[i+1]
                    if nxt[0] == "pdf":
                        nis_l = nxt[3].width > nxt[3].height
                    else:
                        nis_l = nxt[2][0] > nxt[2][1]
                        
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
    if os.path.exists(PATH_ENCERRAMENTO):
        doc_main.insert_file(PATH_ENCERRAMENTO); cur += 1

    # Índice Navegável
    max_y = A4[1] - 60
    entry_idx = 0
    for i in range(2):
        if idx_start + i >= len(doc_main): break
        pg = doc_main[idx_start + i]
        pg.draw_rect(fitz.Rect(0, 0, A4[0], 80), color=None, fill=(0.1, 0.1, 0.1))
        pg.insert_text((50, 50), "ÍNDICE GERAL NAVEGÁVEL", fontname="helv", fontsize=22, color=(1, 1, 1))
        y = 130
        
        while entry_idx < len(idx_entries):
            entry = idx_entries[entry_idx]
            is_cat = entry["is_cat"]
            
            # Altura necessária: Categoria (30) ou Item (15)
            h_req = 30 if is_cat else 15
            
            # Se for categoria, verificar se cabe ela E o próximo item (evitar órfãos)
            if is_cat:
                next_h = 15 if (entry_idx + 1 < len(idx_entries) and not idx_entries[entry_idx+1]["is_cat"]) else 0
                if y + h_req + next_h > max_y:
                    break # Pula para a próxima página do índice
            elif y + h_req > max_y:
                break
            
            lbl = unicodedata.normalize('NFC', entry["label"]).replace(".pdf", "").replace(".png", "")
            tar = entry["page"]
            
            if is_cat:
                y += 8
                pg.insert_text((50, y), lbl.upper(), fontname="hebo", fontsize=11)
                pg.insert_text((A4[0] - 80, y), str(tar + 1), fontname="hebo", fontsize=11)
                pg.insert_link({"kind": fitz.LINK_GOTO, "page": tar, "from": fitz.Rect(50, y - 10, A4[0] - 50, y + 2)})
                y += 22
            else:
                pg.insert_text((70, y), lbl, fontname="helv", fontsize=9)
                pg.insert_text((A4[0] - 80, y), str(tar + 1), fontname="helv", fontsize=9)
                pg.insert_link({"kind": fitz.LINK_GOTO, "page": tar, "from": fitz.Rect(70, y - 8, A4[0] - 50, y + 2)})
                y += 15
            
            entry_idx += 1

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
