
import os
import pandas as pd
from datetime import datetime, timedelta
from app.mapeamento import SETOR_PARA_POLO, POLO_PARA_NOME

def carregar_dados_mais_recentes(filtro_nome=None):
    pasta_dados = os.path.join(os.path.dirname(__file__), "../data")

    if not os.path.exists(pasta_dados):
        raise FileNotFoundError(f"Pasta de dados não encontrada: {pasta_dados}")

    arquivos = [f for f in os.listdir(pasta_dados) if f.endswith(".xlsx")]

    if filtro_nome:
        arquivos = [f for f in arquivos if filtro_nome.lower() in f.lower()]

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo .xlsx encontrado na pasta /data")

    arquivo_mais_recente = max(arquivos, key=lambda f: os.path.getmtime(os.path.join(pasta_dados, f)))
    caminho_completo = os.path.join(pasta_dados, arquivo_mais_recente)

    print(f"📂 Arquivo carregado: {arquivo_mais_recente}")
    return pd.read_excel(caminho_completo)

def transformar_dados_para_intervalo(df: pd.DataFrame, dias: int = 1) -> pd.DataFrame:
    df['SETOR'] = df['SETOR ABASTECIMENTO'].astype(str).str[:3]
    df['POLO'] = df['SETOR'].map(SETOR_PARA_POLO)
    df['POLO_NOME'] = df['POLO'].map(POLO_PARA_NOME)
    df['DH_ACATAMENTO'] = pd.to_datetime(df['DH_ACATAMENTO'], errors='coerce')

    df = df.dropna(subset=['DH_ACATAMENTO', 'POLO_NOME'])  # Garante integridade
    data_limite = datetime.now().date() - timedelta(days=dias - 1)

    return df[df['DH_ACATAMENTO'].dt.date >= data_limite]

def filtrar_por_setor_ou_polo(df: pd.DataFrame, setor: str = None, polo: str = None) -> pd.DataFrame:
    if setor:
        return df[df["SETOR"] == setor]
    elif polo:
        return df[df["POLO"] == polo]
    return df

def gerar_resumo_textual(df, dias=None, polo=None, setor=None):
    total = len(df)
    if df.empty:
        dias = dias or 1
        media_diaria = 0
    else:
        if not dias or not isinstance(dias, int):
            dias = (df['DH_ACATAMENTO'].max().date() - df['DH_ACATAMENTO'].min().date()).days + 1
        media_diaria = total / dias if dias > 0 else total

    resumo = f"📋 Resumo de reclamações nos últimos {dias} dias:\n"
    resumo += f"- Total: {total}\n"
    resumo += f"- Média diária: {media_diaria:.2f}\n"
    if setor:
        resumo += f"- Setor: {str(setor).strip()}\n"
    if polo:
        resumo += f"- Polo: {str(polo).strip()}\n"

    return resumo

def carregar_setores_completos():
    df = carregar_dados_mais_recentes()
    setores = df['SETOR ABASTECIMENTO'].dropna().unique()
    dicionario = {}
    for s in setores:
        codigo = s.split()[0]
        dicionario[codigo] = s
    return dicionario
