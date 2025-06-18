# app/respostas.py
from datetime import datetime

def saudacao(nome=None):
    return f"✅ Olá{', ' + nome if nome else ''}! Como posso te ajudar hoje?"

def ajuda():
    return (
        "📌 *Comandos disponíveis:*\n"
        "- relatório de hoje\n"
        "- relatório de 5 dias\n"
        "- setor 003\n"
        "- ajuda"
    )

def erro_geral():
    return "⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes."

def relatorio_confirmacao(dias):
    hoje = datetime.now().strftime('%d/%m')
    return f"📊 Enviando o relatório de {dias} dia(s). Data atual: {hoje}"

def fallback():
    return "🤖 Não entendi sua mensagem. Envie *ajuda* para ver os comandos disponíveis."
