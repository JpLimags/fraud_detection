# Detecção de Fraude em Cartões de Crédito 💳

## 🎯 Objetivo e Motivação

De acordo com relatório da PwC de 2024, fraudes financeiras geram **trilhões de dólares** em prejuízos anuais no mundo. Com o crescimento do e-commerce e dos pagamentos instantâneos (Pix, Pix Automático, carteiras digitais, etc.), a frequência de fraudes em transações digitais só aumenta.

Sistemas baseados apenas em regras fixas têm dificuldade para identificar padrões sofisticados e em constante evolução. O **Machine Learning** permite analisar grandes volumes de transações em tempo real, detectando anomalias sutis que indicam possível fraude.

Este projeto implementa um pipeline completo de detecção de fraude em cartões de crédito, com foco em:

- Alta performance preditiva  
- Explicabilidade do modelo  
- Facilidade de deploy e monitoramento

Ideal para bancos, fintechs, processadoras de pagamento e plataformas de e-commerce que buscam reduzir perdas por fraude e aumentar a segurança digital.

## 🚀 Tecnologias e Ferramentas

- **Linguagem e bibliotecas principais**  
  Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM

- **Experimentação e versionamento**  
  MLflow, DVC, Optuna

- **Explicabilidade**  
  SHAP

- **Interface interativa**  
  Streamlit **ou** Gradio

- **CI/CD e containerização**  
  GitHub Actions, Docker

## 📁 Estrutura de Diretórios
```
fraud_detection/
├── data/
│   ├── raw/                 # Dados originais (não alterados)
│   └── processed/           # Dados limpos e com features criadas
│
├── notebooks/
│   ├── 01_eda.ipynb         # Análise exploratória
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
│
├── src/
│   ├── data_prep/           # Carregamento e limpeza de dados
│   ├── features/            # Criação e seleção de features
│   ├── models/              # Treinamento, avaliação e predição
│   └── utils/               # Funções auxiliares
│
├── config/                  # Arquivos de configuração (YAML/JSON)
├── outputs/                 # Relatórios, gráficos, modelos salvos, logs
├── app/                     # Código da aplicação web (Streamlit/Gradio)
│
├── .dvc/                    # Cache do DVC
├── requirements.txt
├── Dockerfile
├── .github/workflows/       # Pipelines de CI/CD
└── README.md
```

📦 Principais Dependências (requirements.txt)
```
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
matplotlib>=3.7
seaborn>=0.12
shap>=0.45
mlflow>=2.10
dvc>=3.0
optuna>=3.5
imbalanced-learn>=0.11
streamlit>=1.30          # ou gradio
joblib>=1.3
pyyaml>=6.0
```

📊 Métricas de Avaliação

AUC-ROC (principal)
Precision, Recall, F1-Score
Precision@K, Recall@K (especialmente úteis em cenários de alto desbalanceamento)
Matriz de Confusão
Business metrics (ex.: economia estimada em R$)

✅ Resultados Esperados

Modelo com boa capacidade de detecção e baixa taxa de falsos positivos
Explicações claras via SHAP values (global e local)
Interface web interativa para teste de transações em tempo real
Pipeline reprodutível e preparado para deploy em cloud


### English Version 🇺🇸


# Credit Card Fraud Detection 💳

## 🎯 Objective & Motivation

According to PwC's 2024 report, financial fraud causes **trillions of dollars** in global losses every year. With the rapid growth of e-commerce and instant payment systems (Pix, Zelle, UPI, etc.), digital payment fraud continues to increase in both volume and sophistication.

Rule-based systems struggle to keep up with fast-evolving fraud patterns. **Machine Learning** enables real-time analysis of massive transaction volumes, identifying subtle anomalies that indicate potential fraud.

This project builds a complete fraud detection pipeline with emphasis on:

- Strong predictive performance  
- Model explainability  
- Easy deployment and monitoring

Suitable for banks, fintechs, payment processors, and e-commerce platforms looking to reduce fraud losses and increase digital trust.

## 🚀 Technologies & Tools

- **Core stack**  
  Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM

- **Experiment tracking & versioning**  
  MLflow, DVC, Optuna

- **Explainability**  
  SHAP

- **Interactive UI**  
  Streamlit **or** Gradio

- **CI/CD & Containerization**  
  GitHub Actions, Docker

## 📁 Project Structure

```text
fraud_detection/
├── data/
│   ├── raw/                 # Original untouched data
│   └── processed/           # Cleaned + feature-engineered datasets
│
├── notebooks/
│   ├── 01_eda.ipynb         # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
│
├── src/
│   ├── data_prep/           # Data loading & preprocessing
│   ├── features/            # Feature creation & selection
│   ├── models/              # Training, evaluation, inference
│   └── utils/               # Helper functions
│
├── config/                  # YAML/JSON configuration files
├── outputs/                 # Reports, plots, saved models, logs
├── app/                     # Web app code (Streamlit/Gradio)
│
├── .dvc/                    # DVC cache
├── requirements.txt
├── Dockerfile
├── .github/workflows/       # CI/CD pipelines
└── README.md
```
📦 Main Dependencies (requirements.txt)
```text
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
matplotlib>=3.7
seaborn>=0.12
shap>=0.45
mlflow>=2.10
dvc>=3.0
optuna>=3.5
imbalanced-learn>=0.11
streamlit>=1.30          # or gradio
joblib>=1.3
pyyaml>=6.0
```
📊 Evaluation Metrics

AUC-ROC (primary metric)
Precision, Recall, F1-Score
Precision@K, Recall@K (useful in highly imbalanced settings)
Confusion Matrix
Business-oriented metrics (estimated fraud loss reduction)

✅ Expected Outcomes

High-performing fraud detection model with low false-positive rate
Clear model explanations using SHAP values (global & local)
Interactive web interface for real-time transaction testing
Fully reproducible pipeline ready for cloud deployment