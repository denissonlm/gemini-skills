---
name: gmail-cleaner
description: Limpeza e organização eficiente do Gmail utilizando Python e Google API. Use para listar remetentes frequentes, apagar mensagens em massa, criar filtros de bloqueio e realizar limpezas baseadas em buscas complexas.
---

# Gmail Cleaner Skill

Esta skill permite a manutenção automatizada do seu Gmail, focando em remover o lixo eletrônico e organizar sua caixa de entrada.

## Configuração Inicial

Antes de usar as ferramentas de limpeza, você precisa de autorização:

1.  Certifique-se de que o arquivo `credentials.json` está na pasta da skill.
2.  Execute o script de setup:
    ```bash
    python3 scripts/setup_gmail.py
    ```
3.  Siga o link no navegador para gerar o `token.json`.

## Ferramentas de Manutenção

### 1. Identificar quem mais te envia e-mails
Útil para descobrir newsletters ou serviços que estão inundando sua caixa.
```bash
python3 scripts/gmail_manager.py top
```

### 2. Bloquear um remetente (Filtro)
Cria um filtro no Gmail que envia automaticamente todos os futuros e-mails de um remetente para a Lixeira.
```bash
python3 scripts/gmail_manager.py block "spam@exemplo.com"
```

### 3. Apagar e-mails existentes de um remetente
Remove todas as mensagens já recebidas de um endereço específico.
```bash
python3 scripts/gmail_manager.py delete "velho-servico@exemplo.com"
```

### 4. Limpeza por Busca (Cleanup)
Executa uma busca do Gmail e deleta todos os resultados.
*   **Promoções com mais de 30 dias:** `cleanup "category:promotions older_than:30d"`
*   **Social com mais de 90 dias:** `cleanup "category:social older_than:90d"`
*   **Termos específicos:** `cleanup "assunto:oferta imperdivel"`

```bash
python3 scripts/gmail_manager.py cleanup "QUERY_AQUI"
```

## Referências Úteis

- [Documentação da Gmail API](https://developers.google.com/gmail/api/guides)
- [Sintaxe de Busca do Gmail](https://support.google.com/mail/answer/7190)
