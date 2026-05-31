# src/features/build_features.py
import numpy as np
import pandas as pd

def haversine_vectorized(lat1, lon1, lat2, lon2):
    """Calcula a distância em quilômetros entre dois pontos geográficos."""
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c

def engineer_fraud_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica engenharia de atributos focada em detecção de fraude e risco:
    - Variáveis temporais e idade
    - Distância até o estabelecimento
    - Velocidade e frequência de transações (Carding)
    """
    # Evita modificar o dataframe original (boa prática de pipeline)
    df_out = df.copy()
    
    # 1. Garante os tipos datetime
    df_out['trans_date_trans_time'] = pd.to_datetime(df_out['trans_date_trans_time'])
    df_out['dob'] = pd.to_datetime(df_out['dob'])
    
    # 2. Variáveis Temporais Avançadas e Idade do Portador
    df_out['trans_hour'] = df_out['trans_date_trans_time'].dt.hour
    df_out['trans_day_of_week'] = df_out['trans_date_trans_time'].dt.dayofweek
    df_out['age'] = (df_out['trans_date_trans_time'] - df_out['dob']).dt.days // 365
    
    # 3. Cálculo de Distância Geométrica Vetorizada
    df_out['distance_to_merchant'] = haversine_vectorized(
        df_out['lat'], df_out['long'], df_out['merch_lat'], df_out['merch_long']
    )
    
    # 4. Análise de Velocidade e Frequência
    df_out = df_out.sort_values(['cc_num', 'trans_date_trans_time'])
    df_out['time_since_last_trans'] = df_out.groupby('cc_num')['trans_date_trans_time'].diff().dt.total_seconds()
    df_out['time_since_last_trans'] = df_out['time_since_last_trans'].fillna(-1)
    
    return df_out