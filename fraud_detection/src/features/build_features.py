import numpy as np
import pandas as pd

def calculate_haversine(lat1, lon1, lat2, lon2):
    """Cálculo vetorizado da distância de Haversine entre dois pontos."""
    R = 6371  # Raio da Terra em km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    
    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

def apply_cyclic_features(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma variáveis temporais em componentes seno/cosseno."""
    df = df.copy()
    df['hour'] = df['trans_date_trans_time'].dt.hour
    df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
    
    # Horas (0-23)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    # Dia da semana (0-6)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    return df

def add_transaction_velocity(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula o tempo desde a última transação por cartão."""
    df = df.sort_values(['cc_num', 'trans_date_trans_time'])
    df['last_trans_time'] = df.groupby('cc_num')['unix_time'].shift(1)
    df['velocity_sec'] = df['unix_time'] - df['last_trans_time']
    return df.fillna({'velocity_sec': -1}) # -1 indica primeira transação