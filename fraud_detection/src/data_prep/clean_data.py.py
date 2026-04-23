import pandas as pd

def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza limpeza inicial: remove nulos, duplicatas e colunas irrelevantes."""
    df = df.copy()
    # Remoção de índice redundante se existir
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Conversão de tipos
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['dob'] = pd.to_datetime(df['dob'])
    
    return df.drop_duplicates()