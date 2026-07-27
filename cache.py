"""
Módulo de Gerenciamento de Cache Local para Endereços de IP.

Este módulo é responsável por persistir e ler o último endereço de IP público
sincronizado em um arquivo de texto local, servindo como mecanismo de cache para
evitar requisições desnecessárias às APIs externas e à Cloudflare.
"""

from pathlib import Path

# Diretório base absoluto do módulo para resolução dinâmica de arquivos
DIRETORIO = Path(__file__).resolve().parent

def cacheLer(NOME_ARQUIVO):
    """
        Lê o endereço de IP armazenado no arquivo de cache local.

        Abre o arquivo especificado em modo de leitura com codificação UTF-8 e
        retorna o seu conteúdo textual por completo.

        :param NOME_ARQUIVO: O caminho ou nome do arquivo de texto que atua como cache.
        :type NOME_ARQUIVO: str
        :return: O endereço de IP gravado no arquivo.
        :rtype: str
        """

    caminhoAbsoluto = DIRETORIO/NOME_ARQUIVO

    with open(caminhoAbsoluto, 'r', encoding='utf-8') as arquivo:
        ip = arquivo.read()
    return ip


def cacheAtualizar(IP_PUBLICO, NOME_ARQUIVO):
    """
        Escreve ou atualiza o novo endereço de IP público no arquivo de cache local.

        Valida se o IP fornecido é válido (não nulo ou vazio) antes de abrir o arquivo
        em modo de escrita ('w'), o que sobrescreve o conteúdo anterior de forma limpa.

        :param IP_PUBLICO: O novo endereço de IP público obtido para ser persistido.
        :type IP_PUBLICO: str
        :param NOME_ARQUIVO: O caminho ou nome do arquivo de texto que atua como cache.
        :type NOME_ARQUIVO: str
        :return: None

        :raises ValueError: Se o parâmetro `IP_PUBLICO` estiver vazio ou nulo,
                            impedindo a gravação de um cache inválido.
        """

    if not IP_PUBLICO:
        raise ValueError("O IP informado está vazio, arquivo cache não pode ser gravado.")

    caminhoAbsoluto = DIRETORIO/NOME_ARQUIVO

    with open(caminhoAbsoluto, 'w', encoding='utf-8') as arquivo:
        arquivo.write(IP_PUBLICO)
    return
