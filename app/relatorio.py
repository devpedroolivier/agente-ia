import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib
from io import BytesIO

matplotlib.use('Agg')  # Para servidores sem interface gráfica

# ===== MAPEAMENTOS =====
SETOR_PARA_POLO = {
    '003': 'f', '007': 's', '008': 's', '010': 's', '011': 's',
    '024': 'm', '026': 'f', '028': 'f', '031': 's', '032': 's',
    '035': 'f', '038': 'f', '042': 'p', '045': 'p', '098': 'g',
    '116': 'p', '118': 'p', '119': 'n', '120': 'n', '121': 'n',
    '122': 'n', '132': 'n', '152': 'n', '165': 's', '172': 'f',
    '206': 'p', '219': 'n', '223': 'm', '224': 'm', '225': 'm',
    '226': 'g', '228': 'm', '230': 'm', '232': 'm', '233': 'm',
    '247': 'm', '319': 'f', '320': 's', '342': 'f', '343': 's',
    '344': 'n', '346': 'n', '360': 'm', '361': 'm', '362': 'm',
    '597': 'g', '598': 'm', '599': 'm', '611': 'n', '612': 'n',
    '628': 'g', '642': 'n', '651': 'n', '653': 'n', '655': 'n',
    '659': 'n', '661': 'n', '671': 'n', '681': 'n'
}

POLO_PARA_NOME = {
    'f': 'CEO Freguesia', 's': 'CEO Santana',
    'm': 'CEO Pimentas', 'p': 'CEO Pirituba',
    'g': 'CEO Gopouva', 'n': 'CEO Extremo Norte'
}

# ===== FUNÇÃO PRINCIPAL PARA USO NA API =====
def gerar_relatorio(qtd_dias: int = 1) -> BytesIO:
    pasta_dados = r"C:\Users\poliveira.eficien.SBSP\Desktop\automação\reclamacoes_sabesp\data"
    arquivos = sorted(
        [os.path.join(pasta_dados, f) for f in os.listdir(pasta_dados) if f.endswith(".xlsx")],
        key=os.path.getmtime,
        reverse=True
    )

    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo Excel encontrado na pasta '{pasta_dados}'")

    df = pd.read_excel(arquivos[0])
    df["DATA"] = pd.to_datetime(df["DATA"])
    data_limite = datetime.now().date() - timedelta(days=qtd_dias - 1)
    df_filtrado = df[df["DATA"].dt.date >= data_limite]

    df_filtrado["SETOR"] = df_filtrado["SETOR"].astype(str).str.zfill(3)
    df_filtrado["POLO"] = df_filtrado["SETOR"].map(SETOR_PARA_POLO)
    df_filtrado["POLO_NOME"] = df_filtrado["POLO"].map(POLO_PARA_NOME)

    resumo = df_filtrado.groupby(["DATA", "POLO_NOME"]).size().reset_index(name="RECLAMACOES")

    if resumo.empty:
        raise ValueError("Nenhuma reclamação encontrada no período selecionado.")

    plt.figure(figsize=(12, 6))
    for polo_nome in resumo["POLO_NOME"].unique():
        dados_polo = resumo[resumo["POLO_NOME"] == polo_nome]
        plt.plot(dados_polo["DATA"], dados_polo["RECLAMACOES"], marker="o", label=polo_nome)

    plt.xlabel("Data")
    plt.ylabel("Reclamações")
    plt.title(f"Reclamações por Polo - Últimos {qtd_dias} dia(s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer  # Buffer pronto para ser enviado por API
