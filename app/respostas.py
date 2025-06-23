def fallback():
    return "🤖 Desculpe, não entendi o comando. Digite *ajuda* para ver as opções disponíveis."

def erro_geral():
    return "⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes."

def resposta_ajuda():
    return (
        "📋 *Comandos disponíveis:*\n"
        "- *relatorio X dia(s) [ceo/setor]*: Gera um resumo e gráfico com base nos dados.\n"
        "   Ex: relatorio 1 dia santana\n"
        "- *ajuda*: Mostra este menu de ajuda.\n\n"
        "📌 *Observações:*\n"
        "- Você pode usar o nome do CEO (santana, pirituba, etc) ou o número do setor.\n"
        "- O intervalo máximo é de 5 dias."
    )
