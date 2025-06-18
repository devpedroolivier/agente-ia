import os
import requests
import logging
from app.relatorio import gerar_grafico_por_polo
from app.processamento import (
    carregar_dados_mais_recentes,
    transformar_dados_para_intervalo,
    filtrar_por_setor_ou_polo
)
from app.comandos import COMANDOS
from app.respostas import fallback, erro_geral

# Configuração de logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/agente.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

TOKEN = os.getenv("META_TOKEN")
ID_TELEFONE = os.getenv("PHONE_NUMBER_ID")

def enviar_resposta_padrao(numero, mensagem_usuario):
    mensagem_usuario = mensagem_usuario.lower()
    logging.info(f"📩 Mensagem recebida de {numero}: {mensagem_usuario}")

    for chave, acao in COMANDOS.items():
        if chave in mensagem_usuario:
            if acao["tipo"] == "texto":
                logging.info(f"📤 Enviando resposta de texto para comando: {chave}")
                return enviar_texto(numero, acao["mensagem"])
            elif acao["tipo"] == "gerar":
                parametros = acao["interpretador"](mensagem_usuario)
                dias = parametros.get("dias", 1)
                setor = parametros.get("setor")
                polo = parametros.get("polo")

                logging.info(f"🔍 Parâmetros interpretados: dias={dias}, setor={setor}, polo={polo}")

                try:
                    df = carregar_dados_mais_recentes()
                    df = transformar_dados_para_intervalo(df, dias=dias)
                    df = filtrar_por_setor_ou_polo(df, setor=setor, polo=polo)

                    if df.empty:
                        logging.warning("⚠️ Nenhum dado encontrado para o filtro solicitado.")
                        return enviar_texto(numero, "⚠️ Nenhum dado encontrado para o filtro solicitado.")

                    imagem_buffer = gerar_grafico_por_polo(df, dias=dias)
                    logging.info(f"📊 Gerando e enviando gráfico de {dias} dia(s)")
                    enviar_texto(numero, acao["resposta"](dias))
                    return enviar_imagem(numero, imagem_buffer)

                except Exception as e:
                    logging.error("❌ Erro ao gerar ou enviar o gráfico", exc_info=True)
                    return enviar_texto(numero, erro_geral())

    logging.info("🤖 Nenhum comando reconhecido, enviando fallback")
    return enviar_texto(numero, fallback())

def enviar_texto(numero, texto):
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
            "body": texto
        }
    }

    try:
        resposta = requests.post(url, headers=headers, json=payload)
        logging.info(f"📤 Texto enviado para {numero}: {resposta.status_code}")
    except Exception as e:
        logging.error("❌ Erro ao enviar texto", exc_info=True)

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
        logging.error(f"❌ Erro no upload da imagem: {response_upload.text}")
        return

    media_id = response_upload.json().get("id")

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
    logging.info(f"📤 Imagem enviada para {numero}: {response_send.status_code}")