
import os
import matplotlib.pyplot as plt
import logging

def gerar_grafico_por_polo(dados, titulo, caminho_saida):
    try:
        if dados.empty:
            logging.warning("⚠️ DataFrame vazio — gráfico não será gerado.")
            return None

        dados = dados.copy()  # Evita SettingWithCopyWarning
        dados["DIA"] = dados["DH_ACATAMENTO"].dt.strftime("%d/%m")
        agrupado = dados.groupby("DIA").size()

        if agrupado.empty:
            logging.warning("⚠️ Nenhum dado após agrupamento por dia.")
            return None

        plt.figure(figsize=(10, 5), dpi=150)
        bars = plt.bar(agrupado.index, agrupado.values, width=0.4, color="#2D7DD2")

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

    except Exception as e:
        logging.exception("Erro ao gerar gráfico:")
        return None
