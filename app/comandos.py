
from app.respostas import ajuda, relatorio_confirmacao
from app.mapeamento import SETOR_PARA_POLO, POLO_PARA_NOME
from app.processamento import carregar_setores_completos
import re

# Carrega os setores completos uma vez só
SETORES_COMPLETOS = carregar_setores_completos()

def extrair_dias(mensagem):
    if "último dia" in mensagem or "hoje" in mensagem:
        return 1
    match = re.search(r"(\d+)\s*dias?", mensagem)
    if match:
        return int(match.group(1))
    return 1

def interpretar_mensagem(mensagem):
    mensagem = mensagem.lower()
    dias = extrair_dias(mensagem)

    # Verifica se é setor
    setor_codigo = None
    match_setor = re.search(r"setor\s*(\d{3})", mensagem)
    if match_setor:
        setor_codigo = match_setor.group(1)
    else:
        for codigo, nome_completo in SETORES_COMPLETOS.items():
            if nome_completo.lower() in mensagem:
                setor_codigo = codigo
                break

    # Verifica se é CEO
    polo = None
    for cod, nome in POLO_PARA_NOME.items():
        if nome.lower().replace("ceo", "").strip() in mensagem:
            polo = cod
            break

    return {"dias": dias, "setor": setor_codigo, "polo": polo}

COMANDOS = {
    "relatorio": {
        "tipo": "gerar",
        "interpretador": interpretar_mensagem,
        "resposta": relatorio_confirmacao
    },
    "ajuda": {
        "tipo": "texto",
        "mensagem": ajuda()
    }
}
