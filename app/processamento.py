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
    df['SETOR_CODIGO'] = df['SETOR ABASTECIMENTO'].astype(str).str[:3]
    df['SETOR_NOME'] = df['SETOR ABASTECIMENTO']
    df['POLO'] = df['SETOR_CODIGO'].map(SETOR_PARA_POLO)
    df['POLO_NOME'] = df['POLO'].map(POLO_PARA_NOME)
    df['DH_ACATAMENTO'] = pd.to_datetime(df['DH_ACATAMENTO'], errors='coerce')

    df = df.dropna(subset=['DH_ACATAMENTO', 'POLO_NOME'])
    data_limite = datetime.now().date() - timedelta(days=dias - 1)

    return df[df['DH_ACATAMENTO'].dt.date >= data_limite]

def filtrar_por_setor_ou_polo(df: pd.DataFrame, setor: str = None, polo: str = None, polos: list = None) -> pd.DataFrame:
    if setor:
        df_filtrado = df[df["SETOR_CODIGO"] == setor]
        print(f"[DEBUG] Filtrando por SETOR_CODIGO={setor}, retornou {len(df_filtrado)} linhas.")
        return df_filtrado
    elif polos:
        df_filtrado = df[df["POLO"].isin(polos)]
        print(f"[DEBUG] Filtrando por POLOS={polos}, retornou {len(df_filtrado)} linhas.")
        return df_filtrado
    elif polo:
        df_filtrado = df[df["POLO"] == polo]
        print(f"[DEBUG] Filtrando por POLO={polo}, retornou {len(df_filtrado)} linhas.")
        return df_filtrado
    return df

def gerar_resumo_textual(df_filtrado, polo=None, polos=None, dias_total=10):
    from app.mapeamento import POLO_PARA_NOME

    if polos and len(polos) > 1:
        df_filtrado = df_filtrado.copy()
        df_filtrado["CEO"] = df_filtrado["POLO"].map(POLO_PARA_NOME)
        contagem_por_ceo = df_filtrado["CEO"].value_counts().sort_index()
        total_geral = len(df_filtrado)

        texto = f"Resumo das Reclamações nos últimos {dias_total} dias:\n"
        texto += f"Total Geral: {total_geral} reclamações\n"
        for ceo, qtd in contagem_por_ceo.items():
            texto += f"- {ceo}: {qtd}\n"
        return texto

    polo = polo or (polos[0] if polos else None)
    if not polo:
        return "⚠️ Nenhuma reclamação encontrada no período solicitado."

    nome_polo = POLO_PARA_NOME.get(polo.lower(), polo.upper())
    total = len(df_filtrado)
    media = total / dias_total if dias_total else 0

    menor_data = pd.to_datetime(df_filtrado["DH_ACATAMENTO"].min(), errors='coerce')
    maior_data = pd.to_datetime(df_filtrado["DH_ACATAMENTO"].max(), errors='coerce')

    if pd.isna(menor_data) or pd.isna(maior_data):
        return f"Resumo das Reclamações – Polo {nome_polo.title()} (últimos {dias_total} dias)\n\n• Nenhuma data válida disponível."

    resumo = (
        f"Resumo das Reclamações – Polo {nome_polo.title()} (últimos {dias_total} dias)\n\n"
        f"• Total: {total} reclamações\n"
        f"• Média diária: {media:.1f}\n"
        f"• Período: {menor_data.strftime('%d/%m')} a {maior_data.strftime('%d/%m')}"
    )
    return resumo

def carregar_setores_completos():
    df = carregar_dados_mais_recentes()
    setores = df['SETOR ABASTECIMENTO'].dropna().unique()
    dicionario = {}
    for s in setores:
        codigo = s.split()[0]
        dicionario[codigo] = s
    return dicionario
