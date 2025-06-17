import os
import requests

# Leitura de variáveis de ambiente (Railway já define automaticamente)
TOKEN = os.getenv("META_TOKEN")
ID_TELEFONE = os.getenv("PHONE_NUMBER_ID")

def enviar_resposta_padrao(numero):
    url = f"https://graph.facebook.com/v18.0/{ID_TELEFONE}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": "✅ Olá! Recebemos sua mensagem. Em breve enviaremos o relatório de falta d'água."
        }
    }

    try:
        resposta = requests.post(url, headers=headers, json=payload)
        print(f"🟢 Resposta enviada para {numero}: {resposta.status_code}")
        print("📦 Conteúdo:", resposta.text)
    except Exception as e:
        print("🔴 Erro ao enviar resposta:", e)
