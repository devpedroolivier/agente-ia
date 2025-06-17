from fastapi import FastAPI, Request
from app.remetente import enviar_resposta_padrao

app = FastAPI()

# ✅ Rota de verificação do webhook da Meta
@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == "sabesp123":
        return int(challenge)
    return {"status": "forbidden"}, 403

# ✅ Rota para receber mensagens do WhatsApp
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
            enviar_resposta_padrao(numero, texto)
    except Exception as e:
        print("🔴 Erro ao processar mensagem:", e)
    return {"status": "received"}
