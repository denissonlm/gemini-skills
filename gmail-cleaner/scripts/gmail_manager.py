import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import collections

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.settings.basic'
]

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("ERRO: token.json não encontrado. Rode o setup_gmail.py primeiro.")
            return None
    return build('gmail', 'v1', credentials=creds)

def list_top_senders(max_messages=500):
    service = get_gmail_service()
    if not service: return
    
    print(f"Analisando as últimas {max_messages} mensagens...")
    results = service.users().messages().list(userId='me', maxResults=max_messages).execute()
    messages = results.get('messages', [])
    
    senders = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From']).execute()
        headers = m.get('payload', {}).get('headers', [])
        for header in headers:
            if header['name'] == 'From':
                senders.append(header['value'])
    
    counter = collections.Counter(senders)
    print("\n--- TOP REMETENTES ---")
    for sender, count in counter.most_common(10):
        print(f"{count} e-mails: {sender}")

def delete_messages_from(sender_email):
    service = get_gmail_service()
    if not service: return
    
    query = f"from:{sender_email}"
    print(f"Buscando mensagens de: {sender_email}...")
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("Nenhuma mensagem encontrada.")
        return

    print(f"Encontradas {len(messages)} mensagens. Movendo para a lixeira...")
    for msg in messages:
        service.users().messages().trash(userId='me', id=msg['id']).execute()
    print("Sucesso: Mensagens deletadas.")

def block_sender_with_filter(sender_email):
    """Cria um filtro para enviar e-mails de um remetente direto para a lixeira."""
    service = get_gmail_service()
    if not service: return
    
    filter_body = {
        'criteria': {
            'from': sender_email
        },
        'action': {
            'addLabelIds': ['TRASH'],
            'removeLabelIds': ['INBOX']
        }
    }
    
    service.users().settings().filters().create(userId='me', body=filter_body).execute()
    print(f"Filtro criado: E-mails de {sender_email} agora irão direto para a Lixeira.")

def cleanup_by_query(query):
    """Exemplo: 'category:promotions older_than:30d'"""
    service = get_gmail_service()
    if not service: return
    
    print(f"Executando busca de limpeza: {query}...")
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("Nenhuma mensagem encontrada para esta busca.")
        return

    print(f"Encontradas {len(messages)} mensagens. Movendo para a lixeira...")
    for msg in messages:
        service.users().messages().trash(userId='me', id=msg['id']).execute()
    print(f"Sucesso: {len(messages)} mensagens removidas.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 gmail_manager.py [top|delete|block|cleanup] [argumento]")
    else:
        cmd = sys.argv[1]
        if cmd == 'top':
            list_top_senders()
        elif cmd == 'delete' and len(sys.argv) > 2:
            delete_messages_from(sys.argv[2])
        elif cmd == 'block' and len(sys.argv) > 2:
            block_sender_with_filter(sys.argv[2])
        elif cmd == 'cleanup' and len(sys.argv) > 2:
            cleanup_by_query(sys.argv[2])
