import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Se modificar estes escopos, delete o arquivo token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.settings.basic'
]

def main():
    """Mostra o uso básico da API do Gmail.
    Gera o arquivo token.json com as credenciais de acesso.
    """
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário,
    # e é criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Se não houver credenciais válidas disponíveis, deixe o usuário fazer o login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERRO: Arquivo 'credentials.json' não encontrado!")
                print("Por favor, baixe o arquivo do Google Cloud Console e coloque-o na pasta 'gmail-cleaner'.")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("SUCESSO: Autenticação concluída! O arquivo 'token.json' foi gerado.")

if __name__ == '__main__':
    main()
