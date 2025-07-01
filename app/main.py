
import os
import requests
from fastapi import FastAPI, Request
from app.remetente import enviar_resposta_padrao

app = FastAPI()
TOKEN = os.getenv("META_TOKEN")
ID_TELEFONE = os.getenv("PHONE_NUMBER_ID")

# 🔒 Cache para evitar loops com comandos repetidos
ULTIMOS_COMANDOS = {}

def enviar_mensagem_whatsapp(numero, mensagem, imagem_bytes=None):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    media_id = None

    if imagem_bytes:
        upload_url = f"https://graph.facebook.com/v19.0/{ID_TELEFONE}/media"
        files = {"file": ("grafico.png", imagem_bytes, "image/png")}
        data = {"messaging_product": "whatsapp", "type": "image"}
        response = requests.post(upload_url, headers=headers, data=data, files=files)
        media_id = response.json().get("id")

    mensagem_segura = f"{mensagem}​"
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text" if not media_id else "image",
        "text": {"body": mensagem_segura} if not media_id else None,
        "image": {"id": media_id, "caption": mensagem_segura} if media_id else None
    }

    mensagem_url = f"https://graph.facebook.com/v19.0/{ID_TELEFONE}/messages"
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
            texto = ""

            # 📌 Captura texto de message text ou de caption da imagem
            if "text" in msg:
                texto = msg["text"]["body"].lower()
            elif "image" in msg and "caption" in msg["image"]:
                texto = msg["image"]["caption"].lower()

            # 🔥 Ignora mensagens automáticas do bot
            if any(x in texto for x in ["total geral", "resumo das reclamações", "nenhuma reclamação", "comandos disponíveis"]):
                print("[DEBUG] Ignorou mensagem automática.")
                continue

            # 🔒 Proteção contra loops: ignora comandos repetidos do mesmo número
            if ULTIMOS_COMANDOS.get(numero) == texto:
                print(f"[DEBUG] Ignorou comando repetido para {numero}")
                continue
            ULTIMOS_COMANDOS[numero] = texto

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
