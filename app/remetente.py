import os
import requests
from app.relatorio import gerar_grafico_por_polo
from app.processamento import carregar_dados_mais_recentes, transformar_dados_para_intervalo

# Variáveis de ambiente
TOKEN = os.getenv("META_TOKEN")
ID_TELEFONE = os.getenv("PHONE_NUMBER_ID")

# ✅ Enviar mensagem de texto padrão
def enviar_resposta_padrao(numero, mensagem_usuario):
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

    # 🧠 Extrair quantidade de dias solicitada
    dias = 1
    try:
        if "5" in mensagem_usuario:
            dias = 5
        elif "3" in mensagem_usuario:
            dias = 3
        elif "7" in mensagem_usuario:
            dias = 7
        elif "1" in mensagem_usuario:
            dias = 1
    except:
        dias = 1

    # 🔄 Geração do gráfico com base nos dados
    try:
        df = carregar_dados_mais_recentes()
        df_transformado = transformar_dados_para_intervalo(df, dias=dias)
        imagem_buffer = gerar_grafico_por_polo(df_transformado, dias=dias)
        enviar_imagem(numero, imagem_buffer)
    except Exception as e:
        print("🔴 Erro ao gerar ou enviar o gráfico:", e)

# ✅ Envia imagem usando API oficial do WhatsApp
def enviar_imagem(numero, imagem_buffer):
    url_upload = f"https://graph.facebook.com/v18.0/{ID_TELEFONE}/media"
    headers_upload = {
        "Authorization": f"Bearer {TOKEN}"
    }
    files = {
        'file': ("relatorio.png", imagem_buffer, 'image/png')
    }
    data = {
        'messaging_product': 'whatsapp',
        'type': 'image'
    }

    response_upload = requests.post(url_upload, headers=headers_upload, files=files, data=data)
    if response_upload.status_code != 200:
        print("🔴 Erro no upload da imagem:", response_upload.text)
        return

    media_id = response_upload.json().get("id")

    # Enviar a imagem com legenda
    url_mensagem = f"https://graph.facebook.com/v18.0/{ID_TELEFONE}/messages"
    headers_msg = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "image",
        "image": {
            "id": media_id,
            "caption": "📊 Relatório de reclamações de falta d'água"
        }
    }

    response_send = requests.post(url_mensagem, headers=headers_msg, json=payload)
    print(f"🟢 Imagem enviada para {numero}: {response_send.status_code}")
    print("📦 Conteúdo:", response_send.text)
