import logging
import re
from app.relatorio import gerar_grafico_por_polo
from app.processamento import (
    carregar_dados_mais_recentes,
    transformar_dados_para_intervalo,
    filtrar_por_setor_ou_polo,
    gerar_resumo_textual
)

# 🔍 Extração dinâmica de dias via regex
def extrair_dias(mensagem):
    match = re.search(r"(\d+)\s*dias?", mensagem)
    return int(match.group(1)) if match else 1

# 🔍 Extração inteligente do polo com base em palavras-chave
def extrair_polo(mensagem):
    mensagem = mensagem.lower()
    if "freguesia" in mensagem:
        return "f"
    elif "santana" in mensagem:
        return "s"
    elif "pimentas" in mensagem:
        return "m"
    elif "pirituba" in mensagem:
        return "p"
    elif "gopouva" in mensagem:
        return "g"
    elif "extremo norte" in mensagem or "norte" in mensagem:
        return "n"
    return None

# ✅ Função principal
def enviar_resposta_padrao(numero, mensagem_usuario):
    try:
        mensagem_usuario = mensagem_usuario.lower()

        dias = extrair_dias(mensagem_usuario)
        polo = extrair_polo(mensagem_usuario)

        df = carregar_dados_mais_recentes()
        df_intervalo = transformar_dados_para_intervalo(df, dias)
        df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, polo=polo)

        imagem_buffer = gerar_grafico_por_polo(df_filtrado, polo=polo, dias_intervalo=dias)

        if imagem_buffer:
            resumo = gerar_resumo_textual(df_filtrado, polo=polo, dias_total=dias)
            return {
                "imagem_bytes": imagem_buffer,
                "mensagem": resumo,
                "numero": numero
            }
        else:
            return {
                "mensagem": "⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes.",
                "numero": numero
            }

    except Exception as e:
        logging.exception("❌ Erro ao processar a mensagem.")
        return {
            "mensagem": "⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes.",
            "numero": numero
        }
