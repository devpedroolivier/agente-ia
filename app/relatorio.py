
import os
import logging
import matplotlib.pyplot as plt
from io import BytesIO
from app.mapeamento import POLO_PARA_NOME, SETOR_PARA_POLO

def gerar_grafico_por_polo(dados, polo=None, polos=None, dias_intervalo=1, caminho_saida=None):
    try:
        if dados.empty:
            logging.warning("⚠️ DataFrame vazio — gráfico não será gerado.")
            return None

        dados = dados.copy()
        dados["DIA"] = dados["DH_ACATAMENTO"].dt.strftime("%d/%m")
        dados["POLO"] = dados["SETOR"].map(SETOR_PARA_POLO).map(lambda p: POLO_PARA_NOME.get(p, p.upper()))

        # Agrupar por CEO (POLO) no eixo X e por DIA na legenda
        agrupado = dados.groupby(["POLO", "DIA"]).size().unstack(fill_value=0)

        # Garantir que todos os CEOs estejam no gráfico
        todos_ceos = sorted(set(POLO_PARA_NOME.values()))
        agrupado = agrupado.reindex(todos_ceos, fill_value=0)

        if agrupado.empty:
            logging.warning("⚠️ Nenhum dado após agrupamento por polo e dia.")
            return None

        plt.figure(figsize=(12, 6))
        agrupado.plot(kind="bar", ax=plt.gca())

        plt.title(f"Reclamações por CEO (últimos {dias_intervalo} dias)", fontsize=14, fontweight='bold')
        plt.xlabel("CEO", fontsize=12)
        plt.ylabel("Nº de Reclamações", fontsize=12)
        plt.xticks(rotation=30, ha='right')
        plt.legend(title="Dia", fontsize=9)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()

        # Exportar imagem
        if caminho_saida:
            os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
            plt.savefig(caminho_saida, facecolor='white', bbox_inches="tight")
            plt.close()
            return caminho_saida
        else:
            buffer = BytesIO()
            plt.savefig(buffer, format='png', facecolor='white', bbox_inches="tight")
            plt.close()
            buffer.seek(0)
            return buffer

    except Exception as e:
        logging.exception("❌ Erro ao gerar gráfico por polo:")
        return None
