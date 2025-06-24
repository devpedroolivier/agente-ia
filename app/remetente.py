
import logging
import re
import warnings
from app.relatorio import gerar_grafico_por_polo
from app.processamento import (
    carregar_dados_mais_recentes,
    transformar_dados_para_intervalo,
    filtrar_por_setor_ou_polo,
    gerar_resumo_textual
)

warnings.simplefilter("ignore", UserWarning)  # Ignora warning de estilo do openpyxl

# 🔍 Extração dinâmica de dias via regex
def extrair_dias(mensagem):
    match = re.search(r"(\d+)\s*dias?", mensagem)
    return int(match.group(1)) if match else 1

# 🔍 Extração inteligente de múltiplos polos com base em palavras-chave
def extrair_polos(mensagem):
    mensagem = mensagem.lower()
    polos = []
    if "todos" in mensagem:
        return ["f", "s", "m", "p"]
    if "freguesia" in mensagem:
        polos.append("f")
    if "santana" in mensagem:
        polos.append("s")
    if "pimentas" in mensagem:
        polos.append("m")
    if "pirituba" in mensagem:
        polos.append("p")
    if "gopouva" in mensagem:
        polos.append("g")
    if "extremo norte" in mensagem or "norte" in mensagem:
        polos.append("n")
    return polos or ["f"]  # padrão para evitar lista vazia

# ✅ Função principal com tratamento de comandos inválidos e ajuda
def enviar_resposta_padrao(numero, mensagem_usuario):
    try:
        mensagem_usuario = mensagem_usuario.lower()

        # 🧠 Ajuda ou comando inválido
        if any(p in mensagem_usuario for p in ["ajuda", "comandos", "menu", "opções"]):
            return {
                "mensagem": (
                    "🤖 *Comandos disponíveis:*\n"
                    "- relatorio 1 dia santana\n"
                    "- relatorio 5 dias gopouva\n"
                    "- relatorio 10 dias freguesia\n"
                    "- relatorio 3 dias extremo norte"
                ),
                "numero": numero
            }

        dias = extrair_dias(mensagem_usuario)
        polos = extrair_polos(mensagem_usuario)

        if not polos:
            return {
                "mensagem": "❌ Não entendi o polo informado. Envie algo como: *relatorio 3 dias santana*",
                "numero": numero
            }

        df = carregar_dados_mais_recentes()
        df_intervalo = transformar_dados_para_intervalo(df, dias)

        respostas = []

        # Se até 5 dias e múltiplos CEOs → um gráfico combinado
        if dias <= 5 and len(polos) > 1:
            df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, polos=polos)
            imagem_buffer = gerar_grafico_por_polo(df_filtrado, polos=polos, dias_intervalo=dias)
            resumo = gerar_resumo_textual(df_filtrado, polos=polos, dias_total=dias)
            return {
                "imagem_bytes": imagem_buffer,
                "mensagem": resumo,
                "numero": numero
            }

        # Caso contrário → gerar gráfico por polo
        for polo in polos:
            df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, polo=polo)
            imagem_buffer = gerar_grafico_por_polo(df_filtrado, polo=polo, dias_intervalo=dias)
            resumo = gerar_resumo_textual(df_filtrado, polo=polo, dias_total=dias)
            if imagem_buffer:
                respostas.append({"imagem_bytes": imagem_buffer, "mensagem": resumo, "numero": numero})

        if respostas:
            return respostas if len(respostas) > 1 else respostas[0]
        else:
            return {
                "mensagem": "⚠️ Nenhuma reclamação encontrada no período solicitado.",
                "numero": numero
            }

    except Exception as e:
        logging.exception("❌ Erro ao processar a mensagem.")
        return {
            "mensagem": "⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes.",
            "numero": numero
        }
