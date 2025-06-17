import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
from datetime import datetime, timedelta
import matplotlib
import pandas as pd
matplotlib.use("Agg")

def gerar_grafico_por_polo(df, dias=1):
    df['POLO_NOME'] = df['POLO_NOME'].replace({
        'CEO Gopouva': 'CEO Guarulhos',
        'CEO Pimentas': 'CEO Guarulhos'
    })

    df['DH_ACATAMENTO'] = pd.to_datetime(df['DH_ACATAMENTO'])
    df['DATA'] = df['DH_ACATAMENTO'].dt.date
    data_limite = datetime.now().date() - timedelta(days=dias - 1)
    df = df[df['DATA'] >= data_limite]
    agrupado = df.groupby(['DATA', 'POLO_NOME']).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    if dias == 1:
        valores = agrupado.iloc[-1]
        barras = ax.bar(valores.index, valores.values, color=plt.cm.tab10.colors)
        for barra in barras:
            y = barra.get_height()
            if y > 0:
                ax.text(barra.get_x() + barra.get_width() / 2, y + 1, int(y), ha='center', color='black')
    else:
        largura_barra = 0.15
        x = np.arange(len(agrupado.columns))
        for i, dia in enumerate(agrupado.index[-dias:]):
            y = agrupado.loc[dia]
            pos = x + (i - (dias - 1) / 2) * largura_barra
            ax.bar(pos, y.values, width=largura_barra, label=dia.strftime('%d/%b'))

        ax.legend()

    ax.set_title(f"Reclamações por Polo - Últimos {dias} dia(s)")
    ax.set_xlabel("Polos")
    ax.set_ylabel("Quantidade")
    ax.set_xticks(np.arange(len(agrupado.columns)))
    ax.set_xticklabels(agrupado.columns, rotation=20)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer
