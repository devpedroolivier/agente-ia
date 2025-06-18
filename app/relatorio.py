import os
import matplotlib.pyplot as plt

def gerar_grafico_por_polo(dados, titulo, caminho_saida):
    if dados.empty:
        return None

    # Ordena os dados por data
    dados = dados.sort_values(by="Data")
    dias = dados["Data"].dt.strftime("%d/%m")
    valores = dados["Reclamacoes"]

    # Criação do gráfico
    plt.figure(figsize=(10, 5), dpi=150)
    bars = plt.bar(dias, valores, width=0.4, color="#2D7DD2")

    # Adiciona números em cima de cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.5,
            int(yval),
            ha='center',
            va='bottom',
            fontsize=9
        )

    # Título e eixos
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel("Dia", fontsize=12)
    plt.ylabel("Nº de Reclamações", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # Salvar gráfico
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    plt.savefig(caminho_saida, facecolor='white')
    plt.close()

    return caminho_saida
