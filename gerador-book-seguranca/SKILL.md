---
name: gerador-book-seguranca
description: Automatiza a geração do Book de Segurança do Grupo Açotubo (Completo e Ultra Lite) utilizando artes oficiais e lógica de agrupamento de slides.
---

# Skill: Gerador de Books de Segurança - Grupo Açotubo

Esta skill automatiza a criação do material de divulgação de segurança do trabalho do Grupo Açotubo, consolidando apresentações e infográficos em um material de alto nível.

## 🛡️ Regras de Blindagem (Inalteráveis)

1.  **Artes Oficiais:** A skill DEVE obrigatoriamente usar as artes presentes na pasta `Book de Segurança` para Capa, Nossa Jornada, Folha de transição e Encerramento.
2.  **Transição Dinâmica:** Para cada material novo, deve-se usar a `Folha de transição.pdf` como base e escrever o título centralizado sobre ela em cor PRETA.
3.  **Layout 2-Up:** Slides em formato paisagem devem ser agrupados em 2 por página (superior/inferior) para otimização de espaço.
4.  **Dual Output:** Sempre gerar dois arquivos:
    *   `Book_Seguranca_Acotubo_Oficial_COMPLETO.pdf`: Com índice navegável e links funcionais.
    *   `Book_Seguranca_Acotubo_Oficial_ULTRA_LITE.pdf`: Versão rasterizada (120 DPI) para compartilhamento leve (sem links).
5.  **Localização:** Os arquivos gerados devem ser salvos na pasta: `C:\Users\denisson.monteiro\OneDrive - Grupo Açotubo\0 SESMT\Organizar\SESMT_v1\SESMT\Infográficos e Apresentações\Book de Segurança`.

## 🛠️ Como Atualizar o Book

Sempre que houver novos arquivos de treinamento na pasta raiz de Infográficos, execute os seguintes passos:

1.  Ative esta skill: `activate_skill("gerador-book-seguranca")`.
2.  Solicite: "Atualizar os Books de Segurança".
3.  O agente executará o script `gerar_book.py` e substituirá os arquivos na pasta oficial.

## 📋 Integrantes do SESMT (Fixos no Encerramento)
- Denisson Monteiro (Engenheiro)
- Cleber Edmar (Supervisor)
- Adeni Lima, Valdecir Bento, Wagner Conceição (Técnico)
