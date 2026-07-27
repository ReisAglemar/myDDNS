"""
Módulo de Carregamento de Variáveis de Ambiente.

Este módulo é responsável por ler arquivos de configuração locais (como o `.env`)
e injetá-los diretamente no escopo do sistema operacional, simulando o comportamento
de bibliotecas de terceiros como a `python-dotenv`.
"""

import os
from pathlib import Path

from cache import Path

# Diretório base absoluto do módulo para resolução dinâmica de arquivos
DIRETORIO = Path(__file__).resolve().parent

def carregarEnvs():
    """
        Lê o arquivo '.env' e carrega suas definições para as variáveis de ambiente do sistema.

        A função abre o arquivo em modo de leitura com codificação UTF-8, filtra linhas
        que não contêm o caractere de atribuição '=' ou que iniciam com '#' (comentários),
        e divide cada linha estritamente na primeira ocorrência do '=', populando o `os.environ`.

        :raises RuntimeError: Caso o arquivo `.env` não seja encontrado no diretório
                              raiz da execução do script.
        """

    caminhoAbsoluto = DIRETORIO/".env"
    try:
        with open(caminhoAbsoluto, "r", encoding="utf-8") as f:
            os.environ.update(line.strip().split("=", 1) for line in f if "=" in line and not line.startswith("#"))
    except FileNotFoundError as e:
        raise RuntimeError(f"Arquivo .env não encontrado.\n"
                           f"Detalhe: {e}"
                           )from e
