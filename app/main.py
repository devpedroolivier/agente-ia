
from fastapi import FastAPI, Request
from app.remetente import enviar_resposta_padrao
import requests
import os

app = FastAPI()

TOKEN = os.getenv("META_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
URL_API = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def enviar_texto(numero, mensagem):
    body = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensagem}
    }
    requests.post(URL_API, headers=HEADERS, json=body)

def enviar_imagem(numero, caminho_imagem):
    # Passo 1: Upload da mídia
    with open(caminho_imagem, "rb") as img:
        upload_resp = requests.post(
            f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/media",
            headers={"Authorization": f"Bearer {TOKEN}"},
            files={"file": img},
            data={"messaging_product": "whatsapp"}
        )
    media_id = upload_resp.json().get("id")

    # Passo 2: Enviar imagem com media_id
    if media_id:
        body = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "image",
            "image": {"id": media_id}
        }
        requests.post(URL_API, headers=HEADERS, json=body)

@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == "sabesp123":
        return int(challenge)
    return {"status": "forbidden"}, 403

@app.post("/webhook")
async def receber_webhook(request: Request):
    dados = await request.json()
    try:
        value = dados.get("entry", [])[0].get("changes", [])[0].get("value", {})
        mensagens = value.get("messages", [])

        if not mensagens:
            print("🔴 Erro ao processar mensagem: 'messages'")
            return {"status": "no message"}, 200

        for mensagem in mensagens:
            numero = mensagem["from"]
            texto = mensagem.get("text", {}).get("body", "").lower()
            print(f"📥 Mensagem recebida: {texto} de {numero}")

            resposta = enviar_resposta_padrao(numero, texto)

            if isinstance(resposta, dict):
                if resposta.get("mensagem"):
                    enviar_texto(numero, resposta["mensagem"])
                if resposta.get("imagem"):
                    enviar_imagem(numero, resposta["imagem"])
            elif isinstance(resposta, str):
                enviar_texto(numero, resposta)

    except Exception as e:
        print("🔴 Erro ao processar mensagem:", e)

    return {"status": "received"}
