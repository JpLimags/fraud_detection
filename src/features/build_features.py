import numpy as np
import pandas as pd

def apply_cyclic_transform(df, col, max_val):
    """Aplica transformações de Seno e Cosseno para variáveis cíclicas."""
    df[f'{col}_sin'] = np.sin(2 * np.pi * df[col] / max_val)
    df[f'{col}_cos'] = np.cos(2 * np.pi * df[col] / max_val)
    return df

def generate_time_features(df):
    """Gera features temporais e de velocidade."""
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['hour'] = df['trans_date_trans_time'].dt.hour
    df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
    
    # Velocidade: delta de tempo entre transações do mesmo cartão
    df = df.sort_values(['cc_num', 'trans_date_trans_time'])
    df['time_delta'] = df.groupby('cc_num')['trans_date_trans_time'].diff().dt.total_seconds().fillna(-1)
    
    df = apply_cyclic_transform(df, 'hour', 24)
    df = apply_cyclic_transform(df, 'day_of_week', 7)
    return df