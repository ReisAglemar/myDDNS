"""
Módulo de Configuração Global de Logging da Aplicação.

Centraliza a inicialização do manipulador de logs gravando diretamente
no diretório padrão de logs do sistema (/var/log/myddns.log).
"""

import logging
from pathlib import Path


def configurarLogging():
    """
    Inicializa o logger nativo salvando os eventos diretamente em /var/log/myddns.log.
    """
    DIRETORIO = Path(__file__).resolve().parent
    localLog = DIRETORIO / "myddns.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(localLog, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
