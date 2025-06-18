from app.respostas import ajuda, relatorio_confirmacao
from app.mapeamento import SETOR_PARA_POLO, POLO_PARA_NOME
import re

def extrair_dias(mensagem):
    for d in ["7", "5", "3", "1"]:
        if d in mensagem:
            return int(d)
    if "hoje" in mensagem:
        return 1
    return 1

def interpretar_mensagem(mensagem):
    mensagem = mensagem.lower()
    dias = extrair_dias(mensagem)

    # Extrai setor
    setor_match = re.search(r"setor\s*(\d{3})", mensagem)
    setor = setor_match.group(1) if setor_match else None

    # Identifica polo baseado no nome
    polo = None
    for cod, nome_completo in POLO_PARA_NOME.items():
        if nome_completo.lower().split("ceo")[-1].strip() in mensagem:
            polo = cod
            break

    return {"dias": dias, "setor": setor, "polo": polo}

COMANDOS = {
    "relatório": {
        "tipo": "gerar",
        "interpretador": interpretar_mensagem,
        "resposta": relatorio_confirmacao
    },
    "ajuda": {
        "tipo": "texto",
        "mensagem": ajuda()
    }
}
