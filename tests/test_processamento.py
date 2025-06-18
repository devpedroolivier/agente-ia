import pytest
import pandas as pd
from app.processamento import transformar_dados_para_intervalo, filtrar_por_setor_ou_polo
from datetime import datetime, timedelta

def criar_df_exemplo():
    data = {
        "SETOR ABASTECIMENTO": ["042", "003", "119"],
        "DH_ACATAMENTO": [
            datetime.now(),
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=10)
        ]
    }
    df = pd.DataFrame(data)
    return df

def test_transformar_dados_para_intervalo():
    df = criar_df_exemplo()
    df_resultado = transformar_dados_para_intervalo(df, dias=7)
    assert all(df_resultado["DH_ACATAMENTO"] >= datetime.now() - timedelta(days=6))

def test_filtrar_por_setor_ou_polo():
    df = criar_df_exemplo()
    df["SETOR"] = df["SETOR ABASTECIMENTO"].str[:3]
    df["POLO"] = df["SETOR"].map({"042": "p", "003": "f", "119": "n"})
    
    # filtro por setor
    df_setor = filtrar_por_setor_ou_polo(df, setor="042")
    assert all(df_setor["SETOR"] == "042")

    # filtro por polo
    df_polo = filtrar_por_setor_ou_polo(df, polo="n")
    assert all(df_polo["POLO"] == "n")
