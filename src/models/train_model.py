"""
Módulo de Orquestração de Modelagem Preditiva Multimodelo.
Gerencia o ciclo de vida de treinamento do LightGBM (Champion) e XGBoost (Challenger).
"""

import os
import joblib
import pandas as pd
import numpy as np
import lightgbm as lgb
import xgboost as xgb
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve, auc, confusion_matrix

def train_lightgbm_model(X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series) -> lgb.LGBMClassifier:
    """
    Instancia e executa o fit do classificador LightGBM sob parâmetros defensivos.
    Utiliza crescimento estruturado vertical (Leaf-wise).
    """
    model = lgb.LGBMClassifier(
        n_estimators=1000,
        learning_rate=0.03,
        num_leaves=31,
        max_depth=6,
        scale_pos_weight=1.0,  # Mantém probabilidade real do ecossistema do negócio
        random_state=42,
        n_jobs=-1,
        importance_type='gain'
    )
    
    # Execução acoplada ao callback de Early Stopping para mitigar Overfitting
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
    )
    return model

def train_xgboost_model(X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame, y_val: pd.Series) -> xgb.XGBClassifier:
    """
    Instancia e executa o fit do classificador XGBoost sob parâmetros defensivos.
    Utiliza crescimento estruturado horizontal (Level-wise) como regularizador natural.
    """
    model = xgb.XGBClassifier(
        n_estimators=1000,
        learning_rate=0.03,
        max_depth=6,
        scale_pos_weight=1.0,
        random_state=42,
        n_jobs=-1,
        eval_metric='logloss',
        early_stopping_rounds=50)
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    return model

def evaluate_model_pipeline(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Pipeline unificado de avaliação metrológica de risco e calibração de corte.
    Mapeia as probabilidades brutas e extrai o threshold ótimo via F1-Score.

    Parameters:
    -----------
    model : Classificador Homologado (LightGBM ou XGBoost)
    X_test : pd.DataFrame -> Matriz de características do conjunto de teste futuro.
    y_test : pd.Series -> Alvo binário real ('is_fraud').

    Returns:
    --------
    dict -> Dicionário contendo os scores calibrados e a volumetria da matriz de confusão.
    """
    # Extração de probabilidades pertencentes à classe positiva (Fraude)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Computação da Curva Precision-Recall e cálculo de Área Alvo (PR-AUC)
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recalls, precisions)
    
    # Busca pelo Limiar de Decisão Ótimo (Vetorização matemática estável)
    f1_scores = np.divide(
        2 * (precisions * recalls), 
        (precisions + recalls), 
        out=np.zeros_like(precisions), 
        where=(precisions + recalls) != 0
    )
    best_idx = np.argmax(f1_scores[:-1])
    optimal_threshold = thresholds[best_idx]
    
    # Aplicação do ponto de corte customizado pós-treinamento
    y_pred_custom = (y_proba >= optimal_threshold).astype(int)
    
    return {
        'classification_report': classification_report(y_test, y_pred_custom, output_dict=True),
        'roc_auc': roc_auc_score(y_test, y_proba),
        'pr_auc': pr_auc,
        'optimal_threshold': optimal_threshold,
        'y_proba': y_proba,
        'confusion_matrix': confusion_matrix(y_test, y_pred_custom)
    }

def save_model_artifact(model, folder_path: str, model_name: str) -> None:
    """
    Persiste fisicamente o modelo serializado no formato binário .pkl
    dentro da infraestrutura de governança definida.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    full_path = os.path.join(folder_path, model_name)
    joblib.dump(model, full_path)
    print(f"💾 Artefato de Produção salvo com sucesso em: {full_path}")