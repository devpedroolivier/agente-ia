
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

        # ➕ Novo bloco: gráfico por CEO com múltiplos dias (barra agrupada com labels)
        if not polos and dias_intervalo > 1:
            tabela = dados.groupby(["CEO", "DIA"]).size().unstack(fill_value=0)

            ceos_ordenados = ['CEO Guarulhos', 'CEO São Miguel', 'CEO Itaim', 'CEO Vila Maria', 'CEO Guaianases']
            for ceo in ceos_ordenados:
                if ceo not in tabela.index:
                    tabela.loc[ceo] = 0
            tabela = tabela.loc[ceos_ordenados]

            ax = tabela.T.plot(kind="bar", figsize=(10, 6))

            for container in ax.containers:
                ax.bar_label(container, label_type='edge', fontsize=8, padding=2)

            plt.title("Reclamações por CEO nos Últimos 5 Dias")
            plt.xlabel("Dias")
            plt.ylabel("Quantidade de Reclamações")
            plt.xticks(rotation=0)
            plt.legend(title="CEO")
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight", facecolor="white")
            plt.close()
            buffer.seek(0)
            return buffer.getvalue()

        return None

    except Exception as e:
        logging.exception(f"Erro ao gerar gráfico: {e}")
        return None
