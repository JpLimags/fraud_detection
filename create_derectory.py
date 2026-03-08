import os
from pathlib import Path
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Definindo o diretório raiz do projeto
project_root = Path('fraud_detection')
project_root.mkdir(exist_ok=True)

# Criando a estrutura de diretórios conforme o README
directories = [
    project_root / 'data' / 'raw',
    project_root / 'data' / 'processed',
    project_root / 'notebooks',
    project_root / 'src' / 'data_prep',
    project_root / 'src' / 'features',
    project_root / 'src' / 'models',
    project_root / 'src' / 'utils',
    project_root / 'config',
    project_root / 'outputs',
    project_root / 'app',
    project_root / '.github' / 'workflows'
]

for dir_path in directories:
    dir_path.mkdir(parents=True, exist_ok=True)

# Criando arquivos placeholders iniciais (opcionais, mas úteis para git)
(notebooks_dir := project_root / 'notebooks').joinpath('01_eda.ipynb').touch()
notebooks_dir.joinpath('02_feature_engineering.ipynb').touch()
notebooks_dir.joinpath('03_model_training.ipynb').touch()

project_root.joinpath('requirements.txt').touch()
project_root.joinpath('Dockerfile').touch()
project_root.joinpath('README.md').touch()

# Nota: A pasta .dvc/ será criada automaticamente ao inicializar o DVC, não criamos manualmente aqui.

print("Estrutura de pastas criada com sucesso!")

# Configurando e baixando o dataset do Kaggle
# Instruções prévias:
# 1. Instale a biblioteca kaggle: pip install kaggle
# 2. Crie uma conta no Kaggle e baixe o arquivo kaggle.json em https://www.kaggle.com/settings/account (API token)
# 3. Coloque o kaggle.json em ~/.kaggle/kaggle.json (ou defina KAGGLE_USERNAME e KAGGLE_KEY como variáveis de ambiente)
# 4. Aceite as regras do dataset no Kaggle (vá para a página do dataset e clique em "Download" uma vez manualmente se necessário)

try:
    api = KaggleApi()
    api.authenticate()

    dataset_slug = 'kartik2112/fraud-detection'
    download_path = project_root / 'data' / 'raw'

    # Baixando o dataset como ZIP
    api.dataset_download_files(dataset_slug, path=download_path, unzip=False)

    # Extraindo o ZIP (assume que o dataset vem compactado)
    zip_file = next(download_path.glob('*.zip'), None)
    if zip_file:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        zip_file.unlink()  # Remove o ZIP após extrair
        print("Dataset baixado e extraído com sucesso em data/raw!")
    else:
        print("Dataset baixado, mas sem ZIP para extrair.")

except Exception as e:
    print(f"Erro ao conectar ou baixar do Kaggle: {e}")
    print("Verifique sua autenticação Kaggle e tente novamente.")