# 💳 Detecção Industrial de Fraude em Cartões de Crédito
  
> **Arquitetura:** Medallion Data Pipeline & Multi-Classifier Benchmark  
> **Modelo com melhor performance:** XGBoost (Crescimento *Level-Wise* Calibrado)

---

## Objetivo e Motivação

De acordo com relatórios globais de risco da PwC, fraudes em meios de pagamento digitais geram **trilhões de dólares** em prejuízos anuais cumulativos. Com o advento do e-commerce em larga escala e sistemas de liquidação instantânea em tempo real, os vetores de ataque tornaram-se dinâmicos, tornando as tradicionais esteiras baseadas exclusivamente em regras de corte fixas obsoletas e caras.

Este ecossistema implementa uma engenharia preditiva fim-a-fim escalável para identificar transações fraudulentas sob extrema esparsidade de classe (~0.57% basal). O foco principal deste projeto assenta-se em três pilares corporativos:

1. **Mitigação de Perdas Financeiras Líquidas:** Maximizar a retenção de capital desviado por ataques (*Recall*).
2. **Preservação da Experiência do Usuário:** Minimizar alarmes falsos (*Falsos Positivos*) para evitar fricção desnecessária com clientes legítimos.
3. **Auditabilidade Estrita (Explainable AI - XAI):** Fornecer rastreabilidade matemática de cada score via Teoria dos Jogos (*SHAP values*) para compliance regulatório.

---

##  Resultados do Benchmark: Champion vs. Challenger

Para evitar o viés de algoritmo único, estruturamos um duelo metrológico rigoroso entre duas topologias de *Gradient Boosting*. O modelo **LightGBM** (então líder de esteira) foi testado contra o **XGBoost**. Ambos foram treinados utilizando separação por corte temporal estrito para evitar vazamento de dados (*Data Leakage*) e otimizados dinamicamente via maximização do F1-Score na curva Precision-Recall.

Abaixo está o painel executivo de homologação extraído do conjunto de dados de teste futuro (massa de validação massiva com mais de 550.000 transações):

| Métrica de Risco | LightGBM (Challenger) | XGBoost (Novo Champion) | Impacto Líquido da Substituição |
| :--- | :---: | :---: | :--- |
| **ROC-AUC** | 0.9943 | **0.9961** | Margem de Separação Ampliada (+0.0018) |
| **PR-AUC (Métrica Alvo)** | 0.8606 | **0.8710** | **Ganho de Estabilidade (+0.0104)** |
| **Threshold Ótimo Calibrado** | 0.2561 | 0.2593 | Ponto de Corte Refinado |
| **Precisão (Classe Fraude)** | 0.8861 | **0.8886** | **Redução de Atrito / Menos Bloqueios Bons** |
| **Recall (Taxa de Captura)** | 0.7506 | **0.7622** | **+25 Ataques Retidos na Barreira** |
| **F1-Score Global** | 0.8127 | **0.8206** | Convergência Estatística Superior |

###  Diagnóstico Operacional (Análise de Matriz de Confusão)

O mapeamento volumétrico traduz a matemática dos modelos diretamente para a eficiência financeira do negócio:

* **Estancamento de Chargebacks:** O **XGBoost bloqueou com sucesso 1.634 fraudes reais**, deixando passar apenas 511 casos. São 25 cartões clonados a menos gerando prejuízos de estorno direto para a instituição parceira em relação ao LightGBM.
* **Fricção Estatisticamente Nula:** Para capturar esse volume de crimes, o XGBoost gerou apenas **191 falsos positivos** em um universo massivo de **553.564 transações legítimas**. Na prática, **a cada 10 alertas gerados pelo motor, aproximadamente 9 são fraudes reais**. A mesa de análise manual opera sem sobrecarga e o cliente bom compra sem bloqueios.

### 🔍 Justificativa de Arquitetura e XAI

A vitória do XGBoost decorre do seu mecanismo de indução baseado em crescimento por níveis (*Level-wise*). Ao expandir as árvores horizontalmente de forma regularizada, ele mostrou-se imune ao ruído provocado pelo severo desbalanceamento de classes, mitigando a convergência gananciosa comum ao crescimento por folhas (*Leaf-wise*) do LightGBM.

A interpretabilidade do modelo foi purificada via **SHAP Values**. Fora os números absolutos distorcidos do ganho de informação tradicional, a auditoria SHAP provou que anomalias monetárias instantâneas em relação ao histórico do portador (`amt` e `amt_to_avg_ratio_24h`) constituem a assinatura de risco mais robusta do sistema.

---

##  Tecnologias e Ferramentas

* **Core Data Science & Boosting:** Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM
* **Governança & Linhagem de Dados:** DVC (Data Version Control) integrado a armazenamento em nuvem
* **Explicabilidade Corporativa (XAI):** SHAP (Explicadores de Árvore baseados em Log-Odds)
* **Persistência & Deploy:** Joblib, Docker, GitHub Actions para CI/CD Automatizado
* **Interface de Homologação:** App interativo em Streamlit para simulação de scores em tempo real

---

##  Estrutura de Diretórios

```text
fraud_detection/
├── data/
│   ├── raw/                 # Ingestão de dados brutos (Imutáveis)
│   └── processed/           # Camadas Silver/Gold (Velocity Features calculadas pré-split)
│
├── notebooks/
│   ├── 01_eda.ipynb         # Análise Exploratória e Assinatura Estatística do Crime
│   ├── 02_feature_engineering.ipynb # Pipelines de Janela Móvel Temporal (Rolling Window)
│   └── 03_model_training.ipynb      # Benchmark Multimodelo e Otimização de Thresholds
│
├── src/
│   ├── data_prep/           # Scripts modulares de limpeza e tipagem rígida
│   ├── features/            # Motores de cálculo comportamental de velocidade
│   ├── models/              # Funções de Fit, Matrizes de Validação e Serialização
│   └── utils/               # Utilitários de IoC, Loggers e Gerenciamento de Pastas
│
├── config/                  # Arquivos de Hiperparâmetros Históricos (YAML)
├── outputs/                 # Gráficos SHAP, Curvas PR e Logs Operacionais
├── app/                     # Interface Web do Motor Antifraude (Streamlit)
│
├── requirements.txt         # Manifesto de Dependências Certificadas
├── Dockerfile               # Especificação de Containerização Pronta para Cloud
└── README.md                # Documentação Técnica Principal
```

## Dependências (requirements.txt)

```text
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
matplotlib>=3.7
seaborn>=0.12
shap>=0.45
joblib>=1.3
pyyaml>=6.0
```

# English Version
## 💳 Industrial Credit Card Fraud Detection Pipeline
Status: Certified & Ready for Deployment 

Architecture: Medallion Data Pipeline & Multi-Classifier Benchmark

Champion Model: XGBoost (Calibrated Level-Wise Tree Growth)

#### Objective & Motivation
According to global risk data from PwC, payment fraud accounts for trillions of dollars in cumulative losses annually. With the expansion of digital ecosystems and real-time settlement rails, fraud patterns evolve rapidly, rendering classic static rule-based systems both obsolete and highly inefficient.

This project deploys an end-to-end scalable predictive engine designed to intercept fraudulent transactions under extreme class imbalance (~0.57% fraud base rate). The core architecture targets three primary enterprise goals:

Direct Loss Mitigation: Maximize the interception of stolen capital (Recall).

User Experience Protection: Minimize false alarms (False Positives) to eliminate friction for legitimate cardholders.

Strict Auditability (Explainable AI - XAI): Deliver mathematical transparency for every decision using game-theoretic formulations (SHAP values) to satisfy regulatory and anti-money laundering (AML) compliance.

## Benchmark Evaluation: Champion vs. Challenger
To eliminate single-algorithm bias, a rigorous multi-model evaluation framework was deployed. The incumbent LightGBM model (Challenger) was pitted against a tuned XGBoost model (Champion). Both models were evaluated using strict temporal splitting to prevent future data leakage and dynamically calibrated via F1-Score optimization across the Precision-Recall curve space.

The standardized performance dashboard below was derived from a future test validation set containing over 550,000 production-scale transactions:

| Risk Metric | LightGBM (Challenger) | XGBoost (Novo Champion) | Net Impact of Upgrading |
| :--- | :---: | :---: | :--- |
| **ROC-AUC** | 0.9943 | **0.9961** | Enhanced Stochastic Separation (+0.0018) |
| **PR-AUC (Métrica Alvo)** | 0.8606 | **0.8710** | **Predictive Reliability Gain (+0.0104)** |
| **Threshold Ótimo Calibrado** | 0.2561 | 0.2593 | Calibrated Operational Cut-off |
| **Precisão (Classe Fraude)** | 0.8861 | **0.8886** | **Lower Friction / Fewer Good Card Rejections** |
| **Recall (Taxa de Captura)** | 0.7506 | **0.7622** | **+25 Actual Attacks Blocked at the Gate** |
| **F1-Score Global** | 0.8127 | **0.8206** | Superior Model Convergence |

## Operational Impact Analysis (Confusion Matrix Breakdown)
Translating confusion matrix quadrants directly into business economics yields clear operational advantages:

Chargeback Prevention: The XGBoost model successfully intercepted 1,634 actual fraud cases, letting only 511 slip through. This translates to 25 fewer compromised cards impacting the platform's chargeback ratios relative to the LightGBM baseline.

Frictionless Base Operations: To stop this volume of cybercrime, XGBoost flagged only 191 false positives out of a massive baseline of 553,564 legitimate purchases. In practice, out of every 10 alerts generated by the engine, approximately 9 are verified frauds. The risk manual review desk operates with zero overhead, and valid customers encounter clean checkouts.

## Architectural Justification & XAI
XGBoost’s edge is rooted in its horizontal growth strategy (Level-wise). By expanding trees level by level under conservative regularization constraints, it acts as an intrinsic regularizer against the severe sparsity of the minority class, avoiding the greedy local convergence traps that degrade leaf-wise algorithms like LightGBM under extreme imbalance.

Model decisions are audited via SHAP Values. Moving away from raw uncalibrated information gain charts, SHAP diagnostics proved that short-term monetary shocks relative to the cardholder's baseline (amt and amt_to_avg_ratio_24h) serve as the primary, robust risk signatures for the production engine.