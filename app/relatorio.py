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
        dados["POLO"] = dados["SETOR"].map(SETOR_PARA_POLO)
        dados["CEO"] = dados["POLO"].map(POLO_PARA_NOME)

        # 🔧 Nova coluna: CEO_NORMALIZADO (agrupa Guarulhos de verdade)
        def normalizar_ceo(nome_ceo):
            if nome_ceo == "CEO Guarulhos":
                return "CEO Guarulhos"
            return nome_ceo

        dados["CEO_NORMALIZADO"] = dados["CEO"].apply(normalizar_ceo)


        resultados = []

        if polos and len(polos) == 1 and dias_intervalo == 1:
            setores = dados["SETOR"].unique().tolist()
            setores.sort()
            blocos = [setores[i:i+7] for i in range(0, len(setores), 7)]

            for idx, bloco in enumerate(blocos):
                df_blocado = dados[dados["SETOR"].isin(bloco)]
                agrupado = df_blocado["SETOR"].value_counts().reindex(bloco, fill_value=0)

                if agrupado.empty:
                    continue

                plt.figure(figsize=(10, 5))
                agrupado.plot(kind="bar", color="#2D7DD2")
                for i, v in enumerate(agrupado):
                    plt.text(i, v + 0.2, str(v), ha='center', fontsize=8)

                plt.title(f"Reclamações por Setor (1 dia) - Gráfico {idx + 1}", fontsize=13)
                plt.xlabel("Setor")
                plt.ylabel("Qtd de Reclamações")
                plt.xticks(rotation=45)
                plt.grid(axis='y', linestyle='--', alpha=0.5)
                plt.tight_layout()

                buffer = BytesIO()
                plt.savefig(buffer, format='png', bbox_inches="tight", facecolor='white')
                plt.close()
                buffer.seek(0)
                resultados.append(buffer)

            return resultados if resultados else None

        if polos and len(polos) == 1 and dias_intervalo > 1:
            agrupado = dados.groupby("DIA").size()

            if agrupado.empty:
                return None

            plt.figure(figsize=(10, 5))
            agrupado.plot(kind="bar", color="#1f77b4")
            for i, v in enumerate(agrupado):
                plt.text(i, v + 0.2, str(v), ha='center', fontsize=8)

            nome_ceo = POLO_PARA_NOME.get(polos[0], polos[0].upper())
            plt.title(f"Reclamações por Dia - {nome_ceo}", fontsize=13)
            plt.xlabel("Dia")
            plt.ylabel("Qtd de Reclamações")
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight", facecolor="white")
            plt.close()
            buffer.seek(0)
            return buffer.getvalue()

        if polos and len(polos) > 1 and dias_intervalo <= 5:
            agrupado = dados.groupby(["CEO_NORMALIZADO", "DIA"]).size().unstack(fill_value=0)
            todos_ceos = sorted(set(dados["CEO_NORMALIZADO"]))
            for ceo in todos_ceos:
                if ceo not in agrupado.index:
                    agrupado.loc[ceo] = 0
            agrupado = agrupado.loc[todos_ceos]


            if agrupado.empty:
                return None

            fig, ax = plt.subplots(figsize=(12, 6))
            bar_plot = agrupado.T.plot(kind="bar", ax=ax)

            # Adiciona número em cima de cada barra
            for bars in bar_plot.containers:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        bar_plot.text(
                            bar.get_x() + bar.get_width() / 2,
                            height + 0.5,
                            str(int(height)),
                            ha='center',
                            fontsize=8
                        )

            plt.title(f"Reclamações por CEO (últimos {dias_intervalo} dias)", fontsize=14, fontweight='bold')
            plt.xlabel("CEO")
            plt.ylabel("Qtd de Reclamações")
            plt.xticks(rotation=0)
            plt.legend(title="Dia", fontsize=9)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format="png", facecolor='white', bbox_inches="tight")
            plt.close()
            buffer.seek(0)
            return buffer.getvalue()

        return None

    except Exception as e:
        logging.exception("❌ Erro ao gerar gráfico por polo:")
        return None
