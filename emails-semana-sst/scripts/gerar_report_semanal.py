#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skill: emails-semana-sst
Script: gerar_report_semanal.py
Autor: Antigravity / SESMT Grupo Açotubo

Descrição:
Coleta e processa automaticamente e-mails da conta Exchange (denisson.monteiro@acotubo.com.br)
no aplicativo Apple Mail referentes à última semana útil (segunda a sábado), filtrando temas
estratégicos de Segurança do Trabalho (SST) e gerando um dashboard executivo HTML completo.
"""

import sys
import os
import subprocess
import datetime
import json
import base64
import argparse
import re
import shutil

# Palavras-chave para filtro de Segurança e Saúde no Trabalho
SST_KEYWORDS = [
    "acidente", "incidente", "epi", "epc", "cipa", "sesmt", "segurança", "seguranca",
    "cat", "laudo", "ltcat", "pgr", "pcmso", "treinamento", "integração", "integracao",
    "risco", "perigo", "dss", "dds", "sipat", "brigada", "incendio", "incêndio", "calçado",
    "calcado", "capacete", "luva", "óculos", "oculos", "audit", "abrafac", "rgo", "rif",
    "ergonomia", "ergonômico", "medicina", "aso", "afastamento", "atestado", "refeitorio",
    "sogi8", "sogi", "norma", "nr-", "nr12", "nr35", "nr33", "nr10", "nr06", "nr05", "nr01",
    "linha de vida", "perícia", "pericia", "periculosidade", "insalubridade", "nital", "químico"
]

def calculate_last_week_range():
    """
    Calcula o intervalo de segunda a sábado da semana útil anterior.
    Se hoje for segunda-feira, a semana anterior é a imediatamente anterior.
    """
    today = datetime.date.today()
    # today.weekday(): 0=Segunda, 1=Terça, ..., 6=Domingo
    # Segunda-feira da semana passada:
    days_to_last_monday = today.weekday() + 7
    last_monday = today - datetime.timedelta(days=days_to_last_monday)
    last_saturday = last_monday + datetime.timedelta(days=5)
    return last_monday, last_saturday

def get_exchange_account_name():
    """Descobre o nome da conta que possui o e-mail denisson.monteiro@acotubo.com.br"""
    script = '''
    tell application "Mail"
        set accList to every account
        repeat with acc in accList
            set accName to name of acc
            set emailAddrs to email addresses of acc
            repeat with em in emailAddrs
                if em contains "denisson.monteiro@acotubo.com.br" then
                    return accName
                end if
            end repeat
        end repeat
        return "Exchange"
    end tell
    '''
    try:
        proc = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception:
        pass
    return "Exchange"

def parse_applescript_date(date_str):
    """
    Converte datas em português retornadas pelo AppleScript.
    Exemplo: 'quinta-feira, 10 de setembro de 2026 às 12:29:30' ou '10/09/2026 12:29:30'
    """
    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
        "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
        "outubro": 10, "novembro": 11, "dezembro": 12
    }
    date_str_lower = date_str.lower()
    
    # Formato por extenso: "10 de setembro de 2026"
    match = re.search(r'(\d{1,2})\s+de\s+([a-zçã]+)\s+de\s+(\d{4})', date_str_lower)
    if match:
        day = int(match.group(1))
        mes_nome = match.group(2)
        year = int(match.group(3))
        month = meses.get(mes_nome, 0)
        if month:
            return datetime.date(year, month, day)
            
    # Formato numérico: "10/09/2026" ou "2026-09-10"
    match_num = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str)
    if match_num:
        return datetime.date(int(match_num.group(3)), int(match_num.group(2)), int(match_num.group(1)))
        
    match_iso = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
    if match_iso:
        return datetime.date(int(match_iso.group(1)), int(match_iso.group(2)), int(match_iso.group(3)))
        
    return None

def scan_mailbox_for_range(account_name, start_date, end_date):
    """Varre a Caixa de Entrada da conta e retorna os e-mails dentro do período."""
    print(f"[*] Acessando conta: '{account_name}' no Apple Mail...")
    print(f"[*] Período de busca: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")

    collected = []
    chunk_size = 30
    current_index = 1
    found_older = False

    applescript_batch = '''
    tell application "Mail"
        set acc to account "{acc_name}"
        set mb to mailbox "Caixa de Entrada" of acc
        set res to {{}}
        repeat with i from {start_idx} to {end_idx}
            try
                set msg to message i of mb
                set msgDate to (date received of msg) as string
                set msgSubj to subject of msg
                set msgSender to sender of msg
                set msgContent to content of msg
                if length of msgContent > 800 then
                    set msgContent to text 1 thru 800 of msgContent
                end if
                
                set msgSubj to my sanitizeStr(msgSubj)
                set msgSender to my sanitizeStr(msgSender)
                set msgContent to my sanitizeStr(msgContent)
                
                set end of res to (i as string) & "|||" & msgDate & "|||" & msgSender & "|||" & msgSubj & "|||" & msgContent
            on error
            end try
        end repeat
        set AppleScript's text item delimiters to "###---###"
        return res as text
    end tell

    on sanitizeStr(txt)
        set AppleScript's text item delimiters to "|||"
        set theList to every text item of txt
        set AppleScript's text item delimiters to " - "
        set txt to theList as string
        set AppleScript's text item delimiters to "###---###"
        set theList to every text item of txt
        set AppleScript's text item delimiters to " "
        set txt to theList as string
        set AppleScript's text item delimiters to ""
        return txt
    end sanitizeStr
    '''

    while not found_older and current_index < 3000:
        end_idx = current_index + chunk_size - 1
        script = applescript_batch.format(
            acc_name=account_name,
            start_idx=current_index,
            end_idx=end_idx
        )
        proc = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"[!] Erro ao varrer mensagens {current_index}-{end_idx}: {proc.stderr}")
            break

        out = proc.stdout.strip()
        if not out:
            print("[*] Fim das mensagens disponíveis.")
            break

        items = out.split("###---###")
        for item in items:
            parts = item.split("|||")
            if len(parts) >= 5:
                idx = int(parts[0])
                date_raw = parts[1].strip()
                sender = parts[2].strip()
                subject = parts[3].strip()
                content = parts[4].strip()

                parsed_d = parse_applescript_date(date_raw)
                if parsed_d:
                    if parsed_d < start_date:
                        found_older = True
                        break
                    elif parsed_d <= end_date:
                        collected.append({
                            "index": idx,
                            "date_raw": date_raw,
                            "date_obj": parsed_d,
                            "sender": sender,
                            "subject": subject,
                            "content": content
                        })

        print(f"[*] Varredura até mensagem índice {current_index + len(items) - 1}. Coletados no período: {len(collected)}")
        current_index += chunk_size

    return collected

def filter_sst_emails(emails):
    """Filtra mensagens com relevância técnica para SST."""
    sst_emails = []
    for em in emails:
        full_text = (em["subject"] + " " + em["content"] + " " + em["sender"]).lower()
        matched = [kw for kw in SST_KEYWORDS if kw in full_text]
        if matched:
            em["matched_keywords"] = matched
            sst_emails.append(em)
    return sst_emails

def load_logo_base64():
    """Tenta carregar o logotipo oficial da Açotubo."""
    possible_paths = [
        "/Users/denisson/Documents/Antigravity/checklist-ponte-rolante/logo_acotubo.png",
        "/Users/denisson/Documents/Antigravity/acotubo-sesmt-dashboard/public/logo_acotubo.png",
        "/Users/denisson/.gemini/antigravity-cli/brain/07544824-6c1a-420b-b7d6-7580506fc5f0/scratch/logo_base64.txt"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            if p.endswith(".txt"):
                with open(p, "r") as f:
                    return f.read().strip()
            else:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
    return ""

def categorize_email(subject, content):
    txt = (subject + " " + content).lower()
    if any(w in txt for w in ["acidente", "hospital", "atestado", "fratura", "corte", "raio-x", "joelho", "dedo", "prensamento"]):
        return "Acidente", "badge-danger", "Acidente / Médico"
    elif any(w in txt for w in ["calçado", "sapato", "bota", "epi", "almoxarifado"]):
        return "EPI", "badge-warning", "EPI / Calçados"
    elif any(w in txt for w in ["linha de vida", "altura", "nr-35", "nr35", "queda", "calha"]):
        return "Altura", "badge-danger", "NR-35 / Altura"
    elif any(w in txt for w in ["cipa", "eleição", "edital"]):
        return "CIPA", "badge-success", "CIPA / Eleição"
    elif any(w in txt for w in ["auditoria", "visita técnica", "abertura"]):
        return "Auditoria", "badge-info", "Auditoria"
    elif any(w in txt for w in ["perícia", "pericia", "periculosidade", "processo"]):
        return "Perícia", "badge-warning", "Perícia / Jurídico"
    elif any(w in txt for w in ["nital", "químico", "quimico", "vazamento", "fispq"]):
        return "Químico", "badge-purple", "Químicos / Amb."
    else:
        return "Geral", "badge-info", "Gestão SESMT"

def generate_html_report(all_emails, sst_emails, start_date, end_date, output_path):
    logo_b64 = load_logo_base64()
    start_str = start_date.strftime("%d/%m/%Y")
    end_str = end_date.strftime("%d/%m/%Y")

    total_emails = len(all_emails)
    total_sst = len(sst_emails)
    count_acidentes = sum(1 for e in sst_emails if categorize_email(e["subject"], e["content"])[0] == "Acidente")
    count_epis = sum(1 for e in sst_emails if categorize_email(e["subject"], e["content"])[0] == "EPI")
    count_altura = sum(1 for e in sst_emails if categorize_email(e["subject"], e["content"])[0] == "Altura")
    count_cipa = sum(1 for e in sst_emails if categorize_email(e["subject"], e["content"])[0] == "CIPA")
    count_audit = sum(1 for e in sst_emails if categorize_email(e["subject"], e["content"])[0] in ["Auditoria", "Perícia"])

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Executivo SESMT - Açotubo | {start_str} a {end_str}</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <style>
        :root {{
            --primary: #E30613;
            --primary-dark: #B3050F;
            --primary-light: #FFEBEC;
            --primary-gradient: linear-gradient(135deg, #E30613 0%, #B3050F 100%);
            --text-main: #0F172A;
            --text-muted: #64748B;
            --border-color: #E2E8F0;
            --danger: #EF4444;
            --danger-bg: #FEF2F2;
            --warning: #F59E0B;
            --warning-bg: #FFFBEB;
            --success: #10B981;
            --success-bg: #ECFDF5;
            --info: #3B82F6;
            --info-bg: #EFF6FF;
            --purple: #8B5CF6;
            --purple-bg: #F5F3FF;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }}
        body {{ background-color: #F8FAFC; color: var(--text-main); min-height: 100vh; padding: 30px 20px 60px 20px; }}
        .container {{ max-width: 1440px; margin: 0 auto; }}
        .executive-header {{
            background: #FFFFFF; border-radius: 20px; padding: 24px 32px; border: 1px solid var(--border-color);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05); display: flex; justify-content: space-between;
            align-items: center; margin-bottom: 25px; flex-wrap: wrap; gap: 20px;
        }}
        .header-brand {{ display: flex; align-items: center; gap: 20px; }}
        .logo-img {{ height: 48px; width: auto; object-fit: contain; }}
        .brand-text h1 {{ font-size: 24px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px; }}
        .brand-text p {{ font-size: 13px; font-weight: 600; color: var(--primary); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }}
        .header-actions {{ display: flex; align-items: center; gap: 15px; }}
        .period-badge {{ background: #F1F5F9; border: 1px solid #CBD5E1; border-left: 4px solid var(--primary); padding: 10px 18px; border-radius: 12px; text-align: right; }}
        .period-badge .label {{ font-size: 10px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }}
        .period-badge .val {{ font-size: 14px; font-weight: 800; color: #0F172A; margin-top: 2px; }}
        .btn-print {{ background: var(--primary-gradient); color: white; border: none; padding: 12px 20px; border-radius: 12px; font-size: 13px; font-weight: 700; cursor: pointer; display: flex; align-items: gap: 8px; box-shadow: 0 4px 14px rgba(227, 6, 19, 0.25); }}
        .source-bar {{ background: #0F172A; color: #E2E8F0; padding: 12px 24px; border-radius: 14px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; flex-wrap: wrap; gap: 10px; }}
        .source-bar .tag {{ background: rgba(227, 6, 19, 0.2); color: #FF6B6B; border: 1px solid rgba(227, 6, 19, 0.4); padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 11px; text-transform: uppercase; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 30px; }}
        .kpi-card {{ background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 16px; box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.03); position: relative; overflow: hidden; }}
        .kpi-card::before {{ content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--card-border-color, var(--primary)); }}
        .kpi-icon {{ width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; background: var(--icon-bg, var(--primary-light)); color: var(--icon-color, var(--primary)); }}
        .kpi-val {{ font-size: 28px; font-weight: 800; color: #0F172A; line-height: 1.1; }}
        .kpi-label {{ font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }}
        .kpi-subtext {{ font-size: 11px; color: var(--text-muted); margin-top: 2px; }}
        .tabs-nav {{ display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; overflow-x: auto; }}
        .tab-btn {{ background: transparent; border: none; padding: 10px 20px; border-radius: 10px; font-size: 14px; font-weight: 700; color: var(--text-muted); cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 8px; white-space: nowrap; }}
        .tab-btn.active {{ color: white; background: var(--primary); box-shadow: 0 4px 12px rgba(227, 6, 19, 0.25); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .section-title {{ font-size: 18px; font-weight: 800; color: #0F172A; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }}
        .section-title .bar {{ width: 4px; height: 22px; background: var(--primary); border-radius: 2px; }}
        .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(440px, 1fr)); gap: 20px; margin-bottom: 25px; }}
        .strat-card {{ background: #FFFFFF; border-radius: 18px; border: 1px solid var(--border-color); padding: 24px; box-shadow: 0 4px 15px -2px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: space-between; border-left: 6px solid var(--primary); }}
        .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; gap: 12px; }}
        .card-badge {{ font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 50px; text-transform: uppercase; }}
        .badge-danger {{ background: var(--danger-bg); color: var(--danger); border: 1px solid #FECACA; }}
        .badge-warning {{ background: var(--warning-bg); color: #B45309; border: 1px solid #FDE68A; }}
        .badge-success {{ background: var(--success-bg); color: #047857; border: 1px solid #A7F3D0; }}
        .badge-info {{ background: var(--info-bg); color: #1D4ED8; border: 1px solid #BFDBFE; }}
        .badge-purple {{ background: var(--purple-bg); color: #6D28D9; border: 1px solid #DDD6FE; }}
        .card-title {{ font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 10px; }}
        .card-body {{ font-size: 13px; color: #334155; line-height: 1.6; flex: 1; margin-bottom: 14px; }}
        .card-footer-action {{ background: #F8FAFC; border-radius: 12px; padding: 10px 14px; font-size: 12px; font-weight: 700; color: #1E293B; }}
        .table-responsive {{ background: white; border-radius: 16px; border: 1px solid var(--border-color); overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
        th {{ background: #F8FAFC; padding: 14px 18px; font-weight: 800; color: #475569; text-transform: uppercase; font-size: 11px; border-bottom: 2px solid #E2E8F0; }}
        td {{ padding: 14px 18px; border-bottom: 1px solid #F1F5F9; color: #334155; vertical-align: middle; }}
        .modal-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(6px); z-index: 99999; align-items: center; justify-content: center; padding: 20px; }}
        .modal-overlay.active {{ display: flex; }}
        .modal-container {{ background: white; width: 100%; max-width: 800px; border-radius: 20px; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }}
        .modal-header {{ background: var(--primary-gradient); color: white; padding: 20px 28px; display: flex; justify-content: space-between; align-items: center; }}
        .modal-close {{ background: rgba(255, 255, 255, 0.2); border: none; color: white; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 18px; }}
        .modal-body {{ padding: 28px; overflow-y: auto; font-size: 14px; line-height: 1.7; color: #334155; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #E2E8F0; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: var(--text-muted); }}
    </style>
</head>
<body>
<div class="container">
    <header class="executive-header">
        <div class="header-brand">
            {"<img src='data:image/png;base64," + logo_b64 + "' alt='Açotubo' class='logo-img'>" if logo_b64 else "<div style='font-size:24px; font-weight:800; color:#E30613;'><i class='fas fa-cube'></i> AÇOTUBO</div>"}
            <div class="brand-text">
                <h1>Report Semanal de Segurança do Trabalho (SESMT)</h1>
                <p>Consolidado Executivo • Grupo Açotubo</p>
            </div>
        </div>
        <div class="header-actions">
            <div class="period-badge">
                <div class="label"><i class="far fa-calendar-alt"></i> Semana Útil Auditada</div>
                <div class="val">{start_str} a {end_str}</div>
            </div>
            <button class="btn-print" onclick="window.print()"><i class="fas fa-print"></i> Imprimir / PDF</button>
        </div>
    </header>

    <div class="source-bar">
        <div><i class="fas fa-envelope-open-text" style="color: #E30613; margin-right: 8px;"></i> <strong>Conta:</strong> denisson.monteiro@acotubo.com.br (Exchange)</div>
        <div>
            <span class="tag">{total_emails} E-mails Processados</span>
            <span class="tag" style="background: rgba(16, 185, 129, 0.2); color: #34D399; border-color: rgba(16, 185, 129, 0.4); margin-left: 6px;">{total_sst} Ocorrências SST</span>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card" style="--card-border-color: #EF4444; --icon-bg: #FEE2E2; --icon-color: #DC2626;">
            <div class="kpi-icon"><i class="fas fa-user-injured"></i></div>
            <div class="kpi-info">
                <div class="kpi-val">{count_acidentes:02d}</div>
                <div class="kpi-label">Casos Médicos / Acidentes</div>
                <div class="kpi-subtext">Monitoramento ambulatorial</div>
            </div>
        </div>
        <div class="kpi-card" style="--card-border-color: #F59E0B; --icon-bg: #FEF3C7; --icon-color: #D97706;">
            <div class="kpi-icon"><i class="fas fa-shoe-prints"></i></div>
            <div class="kpi-info">
                <div class="kpi-val">{count_epis:02d}</div>
                <div class="kpi-label">Gestão de EPIs / Calçados</div>
                <div class="kpi-subtext">Trocas e reposições de estoque</div>
            </div>
        </div>
        <div class="kpi-card" style="--card-border-color: #3B82F6; --icon-bg: #DBEAFE; --icon-color: #2563EB;">
            <div class="kpi-icon"><i class="fas fa-helmet-safety"></i></div>
            <div class="kpi-info">
                <div class="kpi-val">{count_altura:02d}</div>
                <div class="kpi-label">Segurança Operacional / NR-35</div>
                <div class="kpi-subtext">Linhas de vida e liberações</div>
            </div>
        </div>
        <div class="kpi-card" style="--card-border-color: #10B981; --icon-bg: #D1FAE5; --icon-color: #059669;">
            <div class="kpi-icon"><i class="fas fa-check-to-slot"></i></div>
            <div class="kpi-info">
                <div class="kpi-val">{count_cipa:02d}</div>
                <div class="kpi-label">Processos CIPA / Comissões</div>
                <div class="kpi-subtext">Editais e alinhamentos</div>
            </div>
        </div>
        <div class="kpi-card" style="--card-border-color: #8B5CF6; --icon-bg: #EDE9FE; --icon-color: #7C3AED;">
            <div class="kpi-icon"><i class="fas fa-scale-balanced"></i></div>
            <div class="kpi-info">
                <div class="kpi-val">{count_audit:02d}</div>
                <div class="kpi-label">Auditorias & Jurídico</div>
                <div class="kpi-subtext">Conformidade e perícias</div>
            </div>
        </div>
    </div>

    <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('tab-destaques')"><i class="fas fa-star"></i> 1. Destaques Executivos</button>
        <button class="tab-btn" onclick="switchTab('tab-todos')"><i class="fas fa-list-check"></i> 2. Todas as Ocorrências ({total_sst})</button>
    </div>

    <!-- TAB 1: DESTAQUES -->
    <div id="tab-destaques" class="tab-content active">
        <div class="section-title"><span class="bar"></span> Casos Críticos e Prioridades da Semana</div>
        <div class="cards-grid">
"""

    for em in sst_emails[:8]:
        cat, badge_class, badge_label = categorize_email(em["subject"], em["content"])
        safe_body = em["content"].replace('"', '&quot;').replace("'", "&#39;").replace("\n", "<br>")
        safe_subj = em["subject"].replace('"', '&quot;').replace("'", "&#39;")
        safe_sender = em["sender"].replace('"', '&quot;').replace("'", "&#39;")
        date_display = em["date_raw"]

        html += f"""
            <div class="strat-card">
                <div class="card-top">
                    <span class="card-badge {badge_class}">{badge_label}</span>
                    <span style="font-size:11px; font-weight:600; color:var(--text-muted);"><i class="far fa-clock"></i> {date_display}</span>
                </div>
                <h3 class="card-title">{safe_subj}</h3>
                <div style="font-size:12px; color:var(--text-muted); margin-bottom:10px;"><strong>Remetente:</strong> {safe_sender}</div>
                <div class="card-body">{safe_body[:350]}...</div>
                <div class="card-footer-action">
                    <button onclick="openModal('{safe_subj}', '{safe_sender}', '{date_display}', '{safe_body}')" style="background:var(--primary); color:white; border:none; padding:6px 14px; border-radius:8px; cursor:pointer; font-weight:700; font-size:11px;"><i class="fas fa-eye"></i> Ver E-mail Completo</button>
                </div>
            </div>
        """

    html += """
        </div>
    </div>

    <!-- TAB 2: TODOS -->
    <div id="tab-todos" class="tab-content">
        <div class="section-title"><span class="bar"></span> Relação Completa de Mensagens de Segurança</div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th style="width: 140px;">Data</th>
                        <th style="width: 220px;">Remetente</th>
                        <th>Assunto</th>
                        <th style="width: 160px;">Tema</th>
                        <th style="width: 90px; text-align: center;">Ações</th>
                    </tr>
                </thead>
                <tbody>
    """

    for em in sst_emails:
        cat, badge_class, badge_label = categorize_email(em["subject"], em["content"])
        safe_body = em["content"].replace('"', '&quot;').replace("'", "&#39;").replace("\n", "<br>")
        safe_subj = em["subject"].replace('"', '&quot;').replace("'", "&#39;")
        safe_sender = em["sender"].replace('"', '&quot;').replace("'", "&#39;")
        date_display = em["date_raw"]

        html += f"""
                    <tr>
                        <td style="font-size: 11px; font-weight: 600; color: #64748B;">{date_display}</td>
                        <td style="font-weight: 700; color: #1E293B;">{safe_sender}</td>
                        <td style="font-weight: 600;">{safe_subj}</td>
                        <td><span class="card-badge {badge_class}">{badge_label}</span></td>
                        <td style="text-align: center;">
                            <button onclick="openModal('{safe_subj}', '{safe_sender}', '{date_display}', '{safe_body}')" style="background:#F1F5F9; border:1px solid #CBD5E1; padding:6px 12px; border-radius:8px; cursor:pointer; font-size:11px; font-weight:700;"><i class="fas fa-eye"></i> Ler</button>
                        </td>
                    </tr>
        """

    html += """
                </tbody>
            </table>
        </div>
    </div>

    <div id="emailModal" class="modal-overlay" onclick="if(event.target.id==='emailModal') closeModal()">
        <div class="modal-container">
            <div class="modal-header">
                <div>
                    <h3 id="modalSubject">Detalhes do E-mail</h3>
                    <div id="modalMeta" style="font-size: 11px; opacity: 0.85; margin-top: 4px;"></div>
                </div>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalBody"></div>
        </div>
    </div>

    <footer>
        <div style="font-weight: 700;"><i class="fas fa-shield-heart" style="color: var(--primary);"></i> GRUPO AÇOTUBO • SEGURANÇA DO TRABALHO E MEIO AMBIENTE (SESMT)</div>
        <div>Gerado pelo Skill <code>emails-semana-sst</code></div>
    </footer>
</div>

<script>
    function switchTab(tabId) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        event.currentTarget.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    }
    function openModal(subj, sender, date, body) {
        document.getElementById('modalSubject').innerText = subj;
        document.getElementById('modalMeta').innerText = 'De: ' + sender + ' | Recebido em: ' + date;
        document.getElementById('modalBody').innerHTML = body;
        document.getElementById('emailModal').classList.add('active');
    }
    function closeModal() {
        document.getElementById('emailModal').classList.remove('active');
    }
</script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[*] Dashboard HTML gerado com sucesso em: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Gera o report semanal de segurança do trabalho a partir dos e-mails do Apple Mail.")
    parser.add_argument("--start-date", type=str, help="Data inicial no formato YYYY-MM-DD")
    parser.add_argument("--end-date", type=str, help="Data final no formato YYYY-MM-DD")
    parser.add_argument("--downloads", action="store_true", default=True, help="Também salvar cópia na pasta Downloads")
    args = parser.parse_args()

    if args.start_date and args.end_date:
        start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
    else:
        start_date, end_date = calculate_last_week_range()

    print("=" * 70)
    print(" SKILL: emails-semana-sst (Grupo Açotubo)")
    print(f" Janela Auditada: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
    print("=" * 70)

    account_name = get_exchange_account_name()
    all_emails = scan_mailbox_for_range(account_name, start_date, end_date)
    print(f"[*] Total de e-mails encontrados no período: {len(all_emails)}")

    sst_emails = filter_sst_emails(all_emails)
    print(f"[*] Total de e-mails de SST identificados: {len(sst_emails)}")

    filename = f"Report_Semanal_SST_{start_date.strftime('%Y%m%d')}_a_{end_date.strftime('%Y%m%d')}.html"
    dest_path = os.path.join("/Users/denisson/Documents/Antigravity", filename)

    generate_html_report(all_emails, sst_emails, start_date, end_date, dest_path)

    if args.downloads:
        dl_path = os.path.join("/Users/denisson/Downloads", filename)
        shutil.copy2(dest_path, dl_path)
        print(f"[*] Cópia salva na pasta Downloads: {dl_path}")

    print("=" * 70)
    print(" Processo concluído com sucesso!")
    print("=" * 70)

if __name__ == "__main__":
    main()
