import sentry_sdk
from sentry_sdk import capture_message, flush
from pathlib import Path
import shutil
import json
from models import Vendas
from pydantic import ValidationError

sentry_sdk.init(
    dsn="meu_acesso",
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # set profile_sample_rate to 1.0 to enable performance profiling
    profiles_sample_rate=1.0,
)

# definindo os caminhos para os diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_DADOS = BASE_DIR / "..\\data\\input"
CAMINHO_VALIDOS = BASE_DIR / "..\\data\\output_validos"
CAMINHO_INVALIDOS = BASE_DIR / "..\\data\\output_invalidos"

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
        data = json.loads(caminho_arquivo.read_text(encodin='utf-8'))
        Vendas.model_validate(data)
        return CAMINHO_VALIDOS
    except ValidationError as e:
        capture_message(f"Erro de validação: {e.json()}")
        return CAMINHO_INVALIDOS
    
def main():
    """
    Função principal
    """
    arquivos_json = CAMINHO_DADOS.glob("*.json")  # Iterando sobre todos os arquivos do diretório
    houve_erro = False


    for arquivo in arquivos_json:
        valido = validar_json(arquivo)  # Validando o arquivo
        if not valido:
            houve_erro = True
        mover_arquivo(arquivo, valido)

if __name__ == "__main__":
    try: 
        main()
    finally:
        flush(timeout=2.0)
