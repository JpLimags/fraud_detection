import os
import json
import subprocess

def setup_kaggle_api(kaggle_json_path):
    """
    Lê o arquivo kaggle.json e configura as variáveis de ambiente necessárias para autenticação com a API do Kaggle.

    Parâmetros:
    kaggle_json_path (str): Caminho para o arquivo kaggle.json contendo as credenciais de acesso.
    """
    with open(kaggle_json_path, "r") as f:
        creds = json.load(f)
        os.environ["KAGGLE_USERNAME"] = creds["username"]
        os.environ["KAGGLE_KEY"] = creds["key"]
    print("API do Kaggle configurada com sucesso.")

def download_dataset(dataset_name, output_path):
    """
    Faz o download e descompacta um dataset disponível no Kaggle para o diretório especificado.

    Parâmetros:
    dataset_name (str): Nome do dataset conforme registrado no Kaggle (ex: 'autor/dataset').
    output_path (str): Caminho do diretório onde os dados serão armazenados após o download.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f"Iniciando o download do dataset '{dataset_name}' para o diretório '{output_path}'...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", dataset_name,
        "-p", output_path,
        "--unzip"
    ])
    print("Download concluído e arquivos descompactados.")

if __name__ == "__main__":
    # Caminho local do arquivo kaggle.json contendo as credenciais de acesso
    kaggle_json_path = os.path.join("secrets", "kaggle.json")

    # Nome do dataset a ser baixado
    dataset_name = "mlg-ulb/creditcardfraud"

    # Diretório onde os dados serão salvos
    output_data_path = "data"

    # Execução das funções de configuração e download
    setup_kaggle_api(kaggle_json_path)
    download_dataset(dataset_name, output_data_path)
