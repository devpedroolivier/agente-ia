
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

        # 🔄 Múltiplos polos
        if polos and len(polos) > 1:
            dados["POLO"] = dados["SETOR"].map(SETOR_PARA_POLO).map(lambda p: POLO_PARA_NOME.get(p, p.upper()))
            agrupado = dados.groupby(["DIA", "POLO"]).size().unstack(fill_value=0)
            agrupado = agrupado[sorted(agrupado.columns)]  # ordena os polos alfabeticamente

            if agrupado.empty:
                logging.warning("⚠️ Nenhum dado após agrupamento por dia e polo.")
                return None

            plt.figure(figsize=(10, 5))
            agrupado.plot(kind="bar", stacked=True, ax=plt.gca())

            plt.title(f"Reclamações por Polo (últimos {dias_intervalo} dias)", fontsize=13, fontweight='bold')
            plt.xlabel("Dia", fontsize=11)
            plt.ylabel("Nº de Reclamações", fontsize=11)
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()

        # ✅ Gráfico de único polo
        else:
            polo = polo or (polos[0] if polos else None)
            agrupado = dados.groupby("DIA").size()

            if agrupado.empty:
                logging.warning("⚠️ Nenhum dado após agrupamento por dia.")
                return None

            dias_ordenados = list(agrupado.index)
            nome_polo = POLO_PARA_NOME.get((polo or "").lower(), (polo or "").upper())
            titulo = f"Reclamações - Polo {nome_polo} ({dias_ordenados[0]} a {dias_ordenados[-1]})"

            plt.figure(figsize=(10, 5), dpi=150)
            bars = plt.bar(agrupado.index, agrupado.values, width=0.35, color="#2D7DD2")

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=9)

            plt.title(titulo, fontsize=13, fontweight='bold')
            plt.xlabel("Dia", fontsize=11)
            plt.ylabel("Nº de Reclamações", fontsize=11)
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            plt.tight_layout()

        # Exporta imagem
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
