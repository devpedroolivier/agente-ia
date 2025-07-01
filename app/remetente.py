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
from app.respostas import mensagem_boas_vindas
from app.mapeamento import SETOR_PARA_POLO

warnings.simplefilter("ignore", UserWarning)

def extrair_dias(mensagem):
    match = re.search(r"(\d+)\s*dias?", mensagem)
    return int(match.group(1)) if match else 1

def extrair_polos(mensagem):
    mensagem = mensagem.lower()
    polos = []

    # novo suporte para "setor XXX"
    match = re.search(r"setor\s*(\d{3})", mensagem)
    if match:
        setor_codigo = match.group(1)
        polo_do_setor = SETOR_PARA_POLO.get(setor_codigo)
        if polo_do_setor:
            print(f"[DEBUG] Encontrou setor {setor_codigo} mapeado para polo {polo_do_setor}")
            return [polo_do_setor]

    if "todos" in mensagem:
        return ["f", "s", "m", "g", "p", "n"]
    if "freguesia" in mensagem:
        polos.append("f")
    if "santana" in mensagem:
        polos.append("s")
    if "pimentas" in mensagem:
        polos.append("m")
    if "gopouva" in mensagem:
        polos.append("g")
    if "guarulhos" in mensagem:
        polos.extend(["m", "g"])
    if "pirituba" in mensagem:
        polos.append("p")
    if "extremo norte" in mensagem or "norte" in mensagem:
        polos.append("n")

    return list(dict.fromkeys(polos)) or ["f"]

def eh_saudacao(mensagem):
    saudacoes = [
        "oi", "olá", "ola", "e aí", "fala", "tudo bem", "tudo bom",
        "bom dia", "boa tarde", "boa noite", "salve"
    ]
    mensagem = mensagem.lower()
    return any(s in mensagem for s in saudacoes)

def enviar_resposta_padrao(numero, mensagem_usuario):
    try:
        mensagem_usuario = mensagem_usuario.lower()
        print(f"[DEBUG] Mensagem recebida: {mensagem_usuario}")

        if any(x in mensagem_usuario for x in ["resumo das reclamações", "total geral", "nenhuma reclamação", "comandos disponíveis"]):
            print("[DEBUG] Ignorou mensagem automática do próprio bot.")
            return {
                "mensagem": "Mensagem automática ignorada.",
                "numero": numero
            }

        if eh_saudacao(mensagem_usuario):
            return {
                "mensagem": mensagem_boas_vindas(),
                "numero": numero
            }

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

        print(f"[DEBUG] Dias: {dias}, Polos extraídos: {polos}")

        if not polos:
            return {
                "mensagem": "❌ Não entendi o polo informado. Envie algo como: *relatorio 3 dias santana*",
                "numero": numero
            }

        df = carregar_dados_mais_recentes()
        df_intervalo = transformar_dados_para_intervalo(df, dias)
        respostas = []

        # 🔥 Novo: consolida todos os CEOs em dias > 5 com multiplos CEOs
        if dias > 5 and len(polos) > 1:
            print("[DEBUG] Entrou no caso múltiplos CEOs + dias > 5 consolidado")
            df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, polos=polos)
            imagens = gerar_grafico_por_polo(df_filtrado, polos=polos, dias_intervalo=dias)
            resumo = gerar_resumo_textual(df_filtrado, polos=polos, dias_total=dias)

            if imagens:
                if isinstance(imagens, list):
                    for imagem in imagens:
                        respostas.append({"imagem_bytes": imagem, "mensagem": resumo, "numero": numero})
                else:
                    respostas.append({"imagem_bytes": imagens, "mensagem": resumo, "numero": numero})
            print(f"[DEBUG] Total de respostas geradas: {len(respostas)}")
            return respostas if len(respostas) > 1 else respostas[0]

        if dias <= 5 and len(polos) > 1:
            print("[DEBUG] Entrou no caso múltiplos CEOs + dias ≤ 5")
            df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, polos=polos)
            imagem_buffer = gerar_grafico_por_polo(df_filtrado, polos=polos, dias_intervalo=dias)
            resumo = gerar_resumo_textual(df_filtrado, polos=polos, dias_total=dias)
            return {
                "imagem_bytes": imagem_buffer,
                "mensagem": resumo,
                "numero": numero
            }

        for polo in polos:
            print(f"[DEBUG] Entrou no caso único CEO: {polo}")
            df_filtrado = filtrar_por_setor_ou_polo(df_intervalo, polo=polo)
            resultado_imagem = gerar_grafico_por_polo(df_filtrado, polo=polo, polos=[polo], dias_intervalo=dias)
            resumo = gerar_resumo_textual(df_filtrado, polo=polo, dias_total=dias)

            if resultado_imagem:
                if isinstance(resultado_imagem, list):
                    for imagem in resultado_imagem:
                        respostas.append({"imagem_bytes": imagem, "mensagem": resumo, "numero": numero})
                else:
                    respostas.append({"imagem_bytes": resultado_imagem, "mensagem": resumo, "numero": numero})

        print(f"[DEBUG] Total final de respostas: {len(respostas)}")
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
