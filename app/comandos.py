from app.respostas import ajuda, relatorio_confirmacao
from app.mapeamento import SETOR_PARA_POLO, POLO_PARA_NOME
from app.processamento import carregar_setores_completos
import re

# Carrega os setores completos uma vez só
SETORES_COMPLETOS = carregar_setores_completos()

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

    # Tenta extrair código setor (3 dígitos)
    setor_codigo = None
    m = re.search(r"setor\s*(\d{3})", mensagem)
    if m:
        setor_codigo = m.group(1)
    else:
        # Procura nome completo do setor na mensagem
        for codigo, nome_completo in SETORES_COMPLETOS.items():
            if nome_completo.lower() in mensagem:
                setor_codigo = codigo
                break

    # Extrai polo
    polo = None
    for cod, nome in POLO_PARA_NOME.items():
        if nome.lower().split("ceo")[-1].strip() in mensagem:
            polo = cod
            break

    return {"dias": dias, "setor": setor_codigo, "polo": polo}

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
