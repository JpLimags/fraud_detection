"""
Módulo de Engenharia de Atributos Comportamentais e Velocity Features.
Responsável pela transformação de dados brutos da camada Silver para Gold.
"""

import pandas as pd
import numpy as np

def haversine_vectorized(lat1: pd.Series, lon1: pd.Series, lat2: pd.Series, lon2: pd.Series) -> pd.Series:
    """
    Calcula a distância geodésica em quilômetros entre dois pontos no globo 
    terrestre utilizando a fórmula de Haversine vetorizada para alta performance.

    Parameters:
    -----------
    lat1, lon1 : pd.Series -> Coordenadas de latitude e longitude do portador do cartão.
    lat2, lon2 : pd.Series -> Coordenadas de latitude e longitude do estabelecimento (Merchant).

    Returns:
    --------
    pd.Series -> Vetor contendo as distâncias em quilômetros (float64).
    """
    # Conversão explícita de graus para radianos
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Aplicação matemática da equação de Haversine
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c  # Raio médio da Terra estimado em 6367 km
    return km

def engineer_stateless_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquestra a pipeline de criação de features temporais, espaciais e de velocidade.
    
    CRITICAL (Garantia de Compliance):
    ---------------------------------
    O DataFrame de entrada DEVE estar unificado e ordenado cronologicamente por cliente.
    Este método aplica cálculo contínuo de janelas móveis para evitar o vazamento de 
    informações futuras para o passado (Data Leakage).

    Parameters:
    -----------
    df : pd.DataFrame -> Matriz contendo dados transacionais brutos extraídos do bando de dados.

    Returns:
    --------
    pd.DataFrame -> Matriz enriquecida com assinaturas comportamentais pronta para modelagem.
    """
    df_out = df.copy()
    
    # 1. Normalização Rígida de Tipos Temporais
    df_out['trans_date_trans_time'] = pd.to_datetime(df_out['trans_date_trans_time'])
    df_out['dob'] = pd.to_datetime(df_out['dob'])
    
    # 2. Ordenação Cronológica por Entidade (Blindagem Temporal)
    df_out = df_out.sort_values(['cc_num', 'trans_date_trans_time']).reset_index(drop=True)
    
    # 3. Engenharia Temporal Básica e Demográfica
    df_out['trans_hour'] = df_out['trans_date_trans_time'].dt.hour
    df_out['trans_day_of_week'] = df_out['trans_date_trans_time'].dt.dayofweek
    df_out['age'] = (df_out['trans_date_trans_time'] - df_out['dob']).dt.days // 365
    
    # 4. Engenharia de Distância Espacial (Detecção de Inconsistência Geográfica)
    df_out['distance_to_merchant'] = haversine_vectorized(
        df_out['lat'], df_out['long'], df_out['merch_lat'], df_out['merch_long']
    )
    
    # 5. Delta de Tempo entre Transações Consecutivas
    df_out['time_since_last_trans'] = df_out.groupby('cc_num')['trans_date_trans_time'].diff().dt.total_seconds()
    df_out['time_since_last_trans'] = df_out['time_since_last_trans'].fillna(-1)
    
    # 6. Agregações Móveis Comportamentais (Velocity Features - Janela de 24 horas)
    df_temp = df_out.set_index('trans_date_trans_time')
    df_out['tx_count_24h'] = df_temp.groupby('cc_num')['amt'].rolling('24h').count().reset_index(level=0, drop=True).values
    df_out['avg_amt_24h'] = df_temp.groupby('cc_num')['amt'].rolling('24h').mean().reset_index(level=0, drop=True).values
    
    # 7. Razão de Desvio Monetário (Score de Anomalia Local)
    df_out['amt_to_avg_ratio_24h'] = df_out['amt'] / (df_out['avg_amt_24h'] + 0.01)
    
    return df_out