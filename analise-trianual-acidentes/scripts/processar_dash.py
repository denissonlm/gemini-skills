import pandas as pd
import json
import os
from datetime import datetime
import locale
import base64

# Configuração de locale para PT-BR
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return "data:image/png;base64," + base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return ""

def processar(planilha_path, logo_path, output_file, insights_custom=None):
    df = pd.read_excel(planilha_path, sheet_name='BD')
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df = df.dropna(subset=['Data'])
    df['Ano'] = df['Data'].dt.year.astype(int)
    df['Mes'] = df['Data'].dt.month.astype(int)
    
    df = df[df['Ano'].isin([2024, 2025, 2026])].copy()
    
    matrix = df.groupby(['Ano', 'Mes']).size().unstack(fill_value=0)
    matrix = matrix.reindex(index=[2024, 2025, 2026], columns=range(1, 13), fill_value=0)
    
    df_26 = df[df['Ano'] == 2026]
    ultimo_mes_26 = int(df_26['Mes'].max()) if not df_26.empty else 1
    total_26_ytd = int(matrix.loc[2026, :ultimo_mes_26].sum())
    
    total_24 = int(matrix.loc[2024].sum())
    total_25 = int(matrix.loc[2025].sum())
    
    media_24 = round(total_24 / 12, 1)
    media_25 = round(total_25 / 12, 1)
    media_26_ytd = round(total_26_ytd / ultimo_mes_26, 1)
    
    proj_26 = int(media_26_ytd * 12)
    var_25_vs_24 = int(((total_25 / total_24) - 1) * 100) if total_24 > 0 else 0
    var_ritmo = int(((media_26_ytd / media_25) - 1) * 100) if media_25 > 0 else 0
    
    meses_abr = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    
    # Insights Automáticos (se não houver customização)
    if not insights_custom:
        pico_val = int(matrix.loc[2026].max())
        pico_mes = meses_abr[int(matrix.loc[2026].idxmax())-1].capitalize()
        insights_custom = [
            {"num": "1", "cor": "#E30613", "titulo": f"{pico_mes}/2026 - Pico Histórico", "texto": f"{pico_val} acidentes em {pico_mes.lower()} de 2026 é o maior volume mensal nos últimos 3 anos."},
            {"num": "!", "cor": "#B3050F", "titulo": "Janeiro - Risco Consistente", "texto": f"Janeiro elevado: {int(matrix.loc[2024,1])} (2024), {int(matrix.loc[2025,1])} (2025) e {int(matrix.loc[2026,1])} (2026)."},
            {"num": "📈", "cor": "#666", "titulo": "Tendência de Prevenção", "texto": "Monitoramento das RIFs e presença constante em campo são vitais para reverter o ritmo atual."},
            {"num": "✓", "cor": "#28a745", "titulo": f"2024-2025: Queda de {abs(var_25_vs_24)}%", "texto": f"A redução de {total_24} para {total_25} acidentes indica efetividade das ações. Fundamental resgatar as práticas."}
        ]

    logo_b64 = get_base64_image(logo_path)
    data_hoje = datetime.now().strftime('%B / %Y').upper()
    
    heatmap_rows = ""
    for ano in [2024, 2025, 2026]:
        heatmap_rows += f"<tr><td style='font-weight:800;color:#4B5563;padding-right:15px;'>{ano}</td>"
        for v in matrix.loc[ano].tolist():
            cls = "h-null" if v==0 else ("h-low" if v<=3 else ("h-med" if v<=6 else "h-high"))
            heatmap_rows += f"<td class='{cls}'>{v}</td>"
        heatmap_rows += "</tr>"

    cards_html = ""
    for ins in insights_custom:
        cards_html += f'''
        <div class="insight-card">
            <div class="insight-head"><div class="insight-icon" style="background:{ins['cor']};color:#FFF">{ins['num']}</div><h4 contenteditable="true">{ins['titulo']}</h4></div>
            <p contenteditable="true">{ins['texto']}</p>
        </div>'''

    html = f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><title>Dashboard SESMT Açotubo</title><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"><script src="https://cdn.jsdelivr.net/npm/chart.js"></script><style>:root{{--red:#E30613;--dark-grey:#111827;--bg-page:#FFF}}*{{margin:0;padding:0;box-sizing:border-box;font-family:'Plus Jakarta Sans',sans-serif}}body{{background:#f3f4f6;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:0}}.page{{width:338.67mm;height:190.5mm;background:var(--bg-page);padding:8mm 15mm;position:relative;display:flex;flex-direction:column;overflow:hidden;border:1px solid #ddd}}header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:25px}}.header-left{{display:flex;align-items:center;gap:20px}}.logo-img{{height:55px}}.title-group{{border-left:2px solid #EEE;padding-left:20px}}.title-group h2{{font-size:10px;color:var(--red);font-weight:800;text-transform:uppercase;letter-spacing:2px}}.title-group h1{{font-size:24px;font-weight:800;color:#111;line-height:1}}.sesmt-banner{{background:var(--dark-grey);color:white;padding:10px 20px;border-radius:12px;display:flex;align-items:center;gap:15px;box-shadow:0 4px 6px rgba(0,0,0,0.1)}}.sesmt-banner .brand{{font-size:14px;font-weight:800}}.sesmt-banner .brand span{{color:var(--red)}}.sesmt-banner .meta{{font-size:8px;font-weight:700;color:#9CA3AF;text-transform:uppercase;text-align:right}}.main-layout{{display:grid;grid-template-columns:240px 1fr;gap:30px;flex:1;min-height:0}}.sidebar{{display:flex;flex-direction:column;gap:10px}}.section-label{{font-size:17px;font-weight:800;color:var(--red);display:flex;align-items:center;gap:10px}}.section-label::after{{content:'';flex:1;height:2px;background:#F3F4F6}}.kpi-card{{background:#F9FAFB;border-radius:15px;padding:12px 18px;border:1px solid #E5E7EB;position:relative;display:flex;flex-direction:column;justify-content:center;height:105px}}.kpi-card.active{{border:2px solid var(--red);background:#FFF}}.kpi-card .year{{font-size:13px;font-weight:800;color:#6B7280}}.kpi-card h3{{font-size:44px;font-weight:800;color:#111;line-height:0.9;margin:4px 0}}.kpi-card .details{{font-size:10px;color:#6B7280;font-weight:700}}.kpi-card .meta{{font-size:9px;color:var(--red);font-weight:800;margin-top:2px}}.kpi-card .badge{{position:absolute;top:15px;right:15px;font-size:9px;font-weight:800;color:var(--red)}}.content-body{{display:flex;flex-direction:column;gap:12px;min-height:0}}.chart-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}}.chart-header h2{{font-size:18px;font-weight:800}}.legend{{display:flex;gap:15px;font-size:9px;font-weight:800;text-transform:uppercase}}.legend-item{{display:flex;align-items:center;gap:5px}}.dot{{width:10px;height:10px;border-radius:2px}}.chart-container{{flex:1;min-height:160px;position:relative}}.heatmap-table{{width:100%;border-collapse:collapse;text-align:center;font-size:10px}}.heatmap-table th{{padding:4px;color:#9CA3AF;font-weight:800}}.heatmap-table td{{width:42px;height:28px;border:3px solid #FFF;font-weight:800;border-radius:8px}}.h-low{{background:#FEE2E2;color:#EF4444}}.h-med{{background:#FCA5A5;color:#FFF}}.h-high{{background:#DC2626;color:#FFF}}.h-null{{background:#F3F4F6;color:#D1D5DB}}.attention-box{{background:#FFF1F2;border-radius:12px;padding:10px 20px;border-left:8px solid var(--red)}}.attention-box p{{font-size:15px;line-height:1.4;color:#1F2937}}.attention-box b{{color:var(--red);font-weight:800}}.insights-section{{margin-top:15px;padding-top:10px;border-top:1px solid #EEE}}.insights-title{{font-size:18px;font-weight:800;color:var(--red);margin-bottom:12px}}.insights-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px}}.insight-card{{background:#F9FAFB;padding:14px;border-radius:12px;border-top:4px solid var(--red)}}.insight-head{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}.insight-icon{{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:11px}}.insight-card h4{{font-size:11.5px;font-weight:800;color:#111}}.insight-card p{{font-size:10.5px;color:#374151;line-height:1.5;font-weight:500}}[contenteditable="true"]:hover{{background:rgba(227,6,19,0.05)}}@media print{{body{{background:#FFF}}.page{{border:none}}@page{{size:338.67mm 190.5mm;margin:0}}}}</style></head><body><div class="page"><header><div class="header-left"><img src="{logo_b64}" class="logo-img"><div class="title-group"><h2>Grupo Açotubo - SESMT</h2><h1 contenteditable="true">Análise de Acidentes por Mês</h1></div></div><div class="sesmt-banner"><div class="brand">SESMT <span>Grupo Açotubo</span></div><div class="meta"><div contenteditable="true">"Segurança é compromisso de todos."</div><div contenteditable="true" style="color:var(--red);font-weight:800">ELABORADO PELO SESMT • {data_hoje}</div></div></div></header><div class="main-layout"><div class="sidebar"><div class="section-label">Panorama Geral</div><div class="kpi-card"><div class="year">2024</div><h3 contenteditable="true">{total_24}</h3><div class="details">acidentes | 12 meses</div><div class="meta">média {str(media_24).replace(".", ",")} / mês</div></div><div class="kpi-card"><div class="year">2025</div><h3 contenteditable="true">{total_25}</h3><div class="details">acidentes | 12 meses</div><div class="meta">média {str(media_25).replace(".", ",")} / mês</div><div class="badge">▼ {abs(var_25_vs_24)}% vs 24</div></div><div class="kpi-card active"><div class="year">2026</div><h3 contenteditable="true">{total_26_ytd}</h3><div class="details">acidentes | jan-{meses_abr[ultimo_mes_26-1]}</div><div class="meta">média {str(media_26_ytd).replace(".", ",")} / mês</div><div class="badge">▲ ritmo acelerado</div></div></div><div class="content-body"><div class="chart-header"><h2>Comparativo Mensal</h2><div class="legend"><div class="legend-item"><div class="dot" style="background:var(--red)"></div> 2024</div><div class="legend-item"><div class="dot" style="background:#111827"></div> 2025</div><div class="legend-item"><div class="dot" style="background:#D1D5DB"></div> 2026</div></div></div><div class="chart-container"><canvas id="accChart"></canvas></div><div class="heatmap-table-wrap"><table class="heatmap-table"><thead><tr><th></th><th>Jan</th><th>Fev</th><th>Mar</th><th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov</th><th>Dez</th></tr></thead><tbody>{heatmap_rows}</tbody></table></div><div class="attention-box"><p contenteditable="true"><b>Atenção:</b> o ritmo de 2026 ({str(media_26_ytd).replace(".", ",")} acid./mês) é <b>{abs(var_ritmo)}% {"maior" if var_ritmo > 0 else "menor"}</b> que o de 2025 ({str(media_25).replace(".", ",")}/mês). Se mantido, 2026 projetaria <b>~{proj_26} acidentes no ano</b>.</p></div></div></div><div class="insights-section"><div class="insights-title">Períodos de Atenção</div><div class="insights-row">{cards_html}</div></div></div><script>const ctx = document.getElementById("accChart").getContext("2d");new Chart(ctx,{{type:"bar",data:{{labels:{json.dumps([m.capitalize() for m in meses_abr])},datasets:[{{label:"2024",data:{json.dumps(matrix.loc[2024].tolist())},backgroundColor:"#E30613",borderRadius:4}},{{label:"2025",data:{json.dumps(matrix.loc[2025].tolist())},backgroundColor:"#111827",borderRadius:4}},{{label:"2026",data:{json.dumps([float(x) for x in matrix.loc[2026,:ultimo_mes_26].tolist()]+[None]*(12-ultimo_mes_26)).replace("NaN", "null")},backgroundColor:"#D1D5DB",borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{beginAtZero:true,grid:{{display:false}},ticks:{{font:{{weight:"700",size:10}},color:"#9CA3AF"}}}},x:{{grid:{{display:false}},ticks:{{font:{{weight:"700",size:10}},color:"#111"}}}}}}}}}});</script></body></html>"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
