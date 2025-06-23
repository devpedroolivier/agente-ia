
import os
import matplotlib.pyplot as plt

def gerar_grafico_por_polo(dados, titulo, caminho_saida):
    if dados.empty:
        return None

    # Ordena os dados por DH_ACATAMENTO
    dados = dados.sort_values(by="DH_ACATAMENTO")
    dias = dados["DH_ACATAMENTO"].dt.strftime("%d/%m")
    valores = dados["Reclamacoes"] if "Reclamacoes" in dados.columns else dados.groupby(dias).size()

    # Criação do gráfico
    plt.figure(figsize=(10, 5), dpi=150)
    bars = plt.bar(dias, valores, width=0.4, color="#2D7DD2")

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

    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel("Dia", fontsize=12)
    plt.ylabel("Nº de Reclamações", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    plt.savefig(caminho_saida, facecolor='white')
    plt.close()

    return caminho_saida
