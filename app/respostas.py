from datetime import datetime

def saudacao(nome=None):
    return f"✅ Olá{', ' + nome if nome else ''}! Como posso te ajudar hoje?"

def ajuda():
    return (
        "📌 *Comandos disponíveis:*\n"
        "- guarulhos 5 dias\n"
        "- setor 451 hoje\n"
        "- pimentas último dia\n"
        "- relatório de hoje\n"
        "- relatório de 5 dias\n"
        "- ajuda"
    )

def mensagem_boas_vindas():
    return (
        "👋 Olá! Bem-vindo ao assistente automático de monitoramento da Sabesp.\n\n"
        "Você pode solicitar relatórios com comandos como:\n"
        "🔹 *guarulhos 5 dias*\n"
        "🔹 *setor 451 hoje*\n"
        "🔹 *pimentas último dia*\n\n"
        "Digite um comando e eu trarei o resumo e o gráfico atualizado! 📈"
    )

def erro_geral():
    return "⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes."

def relatorio_confirmacao(dias):
    hoje = datetime.now().strftime('%d/%m')
    return f"📊 Enviando o relatório de {dias} dia(s). Data atual: {hoje}"

def fallback():
    return "🤖 Não entendi sua mensagem. Envie *ajuda* para ver os comandos disponíveis."
