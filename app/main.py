
import os
import requests
from fastapi import FastAPI, Request
from app.remetente import enviar_resposta_padrao

app = FastAPI()
TOKEN = os.getenv("META_TOKEN")
ID_TELEFONE = os.getenv("PHONE_NUMBER_ID")

def enviar_mensagem_whatsapp(numero, mensagem, imagem_bytes=None):
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    # Upload da imagem para o servidor da Meta, se existir
    media_id = None
    if imagem_bytes:
        upload_url = f"https://graph.facebook.com/v19.0/{ID_TELEFONE}/media"
        files = {
            "file": ("grafico.png", imagem_bytes, "image/png")
        }
        data = {
            "messaging_product": "whatsapp",
            "type": "image"
        }
        response = requests.post(upload_url, headers=headers, data=data, files=files)
        response_json = response.json()
        media_id = response_json.get("id")

    # Envio da mensagem
    mensagem_url = f"https://graph.facebook.com/v19.0/{ID_TELEFONE}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text" if not media_id else "image",
        "text": {"body": mensagem} if not media_id else None,
        "image": {"id": media_id, "caption": mensagem} if media_id else None
    }

    return requests.post(mensagem_url, headers=headers, json=payload)

@app.post("/webhook")
async def receber_webhook(request: Request):
    dados = await request.json()
    try:
        mensagens = dados.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])
        if not mensagens:
            return {"status": "no message"}

        for msg in mensagens:
            numero = msg["from"]
            texto = msg["text"]["body"]

            respostas = enviar_resposta_padrao(numero, texto)
            if not isinstance(respostas, list):
                respostas = [respostas]
            for resposta in respostas:
                enviar_mensagem_whatsapp(
                    numero=resposta["numero"],
                    mensagem=resposta["mensagem"],
                    imagem_bytes=resposta.get("imagem_bytes")
                )
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == "sabesp123":
        return int(challenge)
    return {"status": "forbidden"}, 403
