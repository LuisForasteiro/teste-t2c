from botcity.plugins.email import BotEmailPlugin
from dotenv import load_dotenv
import os
import json
load_dotenv()

def envia_email(destinatario, assunto, msg, dados, arquivo: list = None):
    try:
        print('Enviadno Email')
        email = BotEmailPlugin()
        
        email.configure_smtp("smtp.gmail.com", port=587)
        email.configure_imap("imap.gmail.com", port=993)
        
        email.login(email=os.getenv('email'), password=os.getenv('email_password'))
        
        dados_formatados = '<br>'.join([f'{chave}: {valor}' for d in dados for chave, valor in d.items()])

        
        to = destinatario
        subject = assunto
        body = f'{msg} <br><br> {dados_formatados}'
        
        if arquivo:
            email.send_message(
                subject, body, to, use_html=True, attachments=arquivo)
            
        email.disconnect()
        
        print('Email enviado com sucesso')
        
    except Exception as e:
        print(f'Erro ao enviar o email: {e}')