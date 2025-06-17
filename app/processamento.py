import os
import pandas as pd
from datetime import datetime, timedelta
from app.mapeamento import SETOR_PARA_POLO, POLO_PARA_NOME

def carregar_dados_mais_recentes():
    pasta_dados = os.path.join(os.path.dirname(__file__), "data")
    arquivos = [f for f in os.listdir(pasta_dados) if f.endswith(".xlsx")]
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo .xlsx encontrado em /data")

    arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(os.path.join(pasta_dados, f)))
    return pd.read_excel(os.path.join(pasta_dados, arquivo_mais_recente))


def transformar_dados_para_intervalo(df: pd.DataFrame, dias: int = 1) -> pd.DataFrame:
    df['SETOR'] = df['SETOR ABASTECIMENTO'].astype(str).str[:3]
    df['POLO'] = df['SETOR'].map(SETOR_PARA_POLO)
    df['POLO_NOME'] = df['POLO'].map(POLO_PARA_NOME)
    df['DH_ACATAMENTO'] = pd.to_datetime(df['DH_ACATAMENTO'])
    
    data_limite = datetime.now().date() - timedelta(days=dias - 1)
    return df[df['DH_ACATAMENTO'].dt.date >= data_limite]
