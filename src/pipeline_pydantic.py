#  src\pipeline.py

# 1. Importe as bibliotecas necessárias
from pathlib import Path
import shutil
import json
from models import Vendas
from pydantic import ValidationError    # Importando a função ValidationError


# 2. Defina o caminho para o diretório de dados
BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_DADOS = BASE_DIR / "C:\\Users\\hethe\\data-quality\\data\\input"
CAMINHO_VALIDOS = BASE_DIR / "C:\\Users\\hethe\\data-quality\\data\\output_validos"
CAMINHO_INVALIDOS = BASE_DIR / "C:\\Users\\hethe\\data-quality\\data\\output_invalidos"

def mover_arquivo(caminho_arquivo, caminho_saida):
    """
    Move o arquivo para o Diretório de dados válidos
    """
    shutil.move(str(caminho_arquivo), caminho_saida / caminho_arquivo.name)

def validar_json(caminho_arquivo):
    """
    Valida os dados do arquivo JSON
    """
    try:
        data = json.loads(caminho_arquivo.read_text(encoding='utf-8'))
        Vendas.model_validate(data)
        return CAMINHO_VALIDOS
    except ValidationError as e:
        print(f"Erro de validação: {e.json()}")
        return CAMINHO_INVALIDOS

def main():
    """
    Função principal
    """
    arquivos_json = CAMINHO_DADOS.glob("*.json")  # Iterando sobre todos os arquivos do diretório
    for arquivo in arquivos_json:
        mover_arquivo(arquivo, CAMINHO_VALIDOS)  # Movendo o arquivo para o diretório de dados válidos

    status_final  = f"Arquivos movidos com sucesso para {CAMINHO_VALIDOS}"
    print(f"Pipeline Finalidada: {status_final}")

if __name__ == "__main__":
    main()