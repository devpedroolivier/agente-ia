import os
import logging
from io import BytesIO
from app.relatorio import gerar_grafico_por_polo
from app.processamento import (
    carregar_dados_mais_recentes,
    transformar_dados_para_intervalo,
    filtrar_por_setor_ou_polo,
    gerar_resumo_textual
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
    mensagem_usuario = mensagem_usuario.lower().strip()
    logging.info(f"📩 Mensagem recebida de {numero}: {mensagem_usuario}")

    try:
        if "ajuda" in mensagem_usuario:
            resposta = COMANDOS["ajuda"]["mensagem"]
            return {"numero": numero, "mensagem": resposta}

        if "relatorio" in mensagem_usuario:
            comando = COMANDOS["relatorio"]
            dados = comando["interpretador"](mensagem_usuario)

            if not dados.get("polo") and not dados.get("setor"):
                return {"numero": numero, "mensagem": "❌ Por favor, informe um CEO ou setor válido após o comando."}

            df = carregar_dados_mais_recentes()
            df_intervalo = transformar_dados_para_intervalo(df, dados["dias"])
            df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, dados["setor"], dados["polo"])

            if df_filtrado.empty:
                texto = "⚠️ Nenhum dado encontrado para o filtro solicitado."
                return {"numero": numero, "mensagem": texto, "imagem": None}

            titulo = f"Relatório de {dados['dias']} dia(s)"
            imagem_buffer = gerar_grafico_por_polo(df_filtrado, titulo)

            texto = gerar_resumo_textual(df_filtrado, dados["dias"], dados.get("polo"), dados.get("setor"))

            return {
                "numero": numero,
                "mensagem": texto,
                "imagem_bytes": imagem_buffer.read() if imagem_buffer else None
            }

        return {"numero": numero, "mensagem": fallback()}
    except Exception as e:
        logging.exception("Erro ao processar a mensagem.")
        return {"numero": numero, "mensagem": erro_geral()}
