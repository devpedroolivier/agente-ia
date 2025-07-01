import pandas as pd
from datetime import datetime, timedelta
from app.processamento import transformar_dados_para_intervalo, filtrar_por_setor_ou_polo
from app.mapeamento import SETOR_PARA_POLO

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
    df = transformar_dados_para_intervalo(df, dias=15)  # transforma antes, adiciona SETOR_CODIGO e POLO

    # filtro por setor
    df_setor = filtrar_por_setor_ou_polo(df, setor="042")
    assert all(df_setor["SETOR_CODIGO"] == "042")

    # filtro por polo
    df_polo = filtrar_por_setor_ou_polo(df, polo="n")
    assert all(df_polo["POLO"] == "n")

def test_filtrar_por_multiplos_polos():
    df = criar_df_exemplo()
    df = transformar_dados_para_intervalo(df, dias=15)
    df_multi = filtrar_por_setor_ou_polo(df, polos=["p", "n"])
    assert all(df_multi["POLO"].isin(["p", "n"]))
