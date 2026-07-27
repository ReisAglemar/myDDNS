#!/usr/bin/env python3
"""
Módulo Orquestrador Principal do Sistema de Dynamic DNS (myDDNS).

Este módulo gerencia o fluxo de execução do DDNS: carrega as variáveis de ambiente,
verifica o IP público atual, compara com o cache local e atualiza os registros de
DNS na Cloudflare caso ocorram mudanças, notificando o administrador via e-mail.
"""

import os
from pathlib import Path
from carregarEnvs import carregarEnvs
from atualizarIpCloudflare import atualizarIpCloudflare
from buscarIpPublico import buscarIpPublico
from cache import cacheAtualizar, cacheLer
from enviarEmail import enviarEmail
from capturarInfoParaEmail import capturarInfoParaEmail, capturarInfoParaEmailERRO
from excecao import ErroEmail


def main():
    """
        Executa a rotina cíclica de verificação e sincronização do DDNS.

        O fluxo consiste em:
        1. Carregar configurações do arquivo .env.
        2. Descobrir o IP público atual da rede.
        3. Avaliar se o IP mudou em relação ao cache local.
        4. Atualizar a Cloudflare e o cache se houver alteração.
        5. Enviar e-mail de sucesso ou notificar falhas críticas em caso de exceção.
        """

    # Inicialização preventiva das variáveis antes do bloco try/except.
    # Caso ocorra falha na leitura do arquivo .env, evita exceções do tipo
    # UnboundLocalError ao tentar acessar variáveis não atribuídas na captura do erro.
    CLOUDFLARE_TOKEN = None
    ZONE_ID = None
    RECORD_ID = None
    NOME_ARQUIVO = None
    API_IP_PUBLICO = None
    API_KEY_RESEND = None
    EMAIL_REMETENTE = None
    EMAIL_DESTINATARIO = None
    DIRETORIO = None

    try:

        carregarEnvs()

        CLOUDFLARE_TOKEN = os.getenv("CLOUDFLARE_TOKEN", "")
        ZONE_ID = os.getenv("ZONE_ID", "")
        RECORD_ID = os.getenv("RECORD_ID", "")
        NOME_ARQUIVO = os.getenv("NOME_ARQUIVO", "")
        API_IP_PUBLICO = os.getenv("API_IP_PUBLICO", "")
        API_KEY_RESEND = os.getenv("API_KEY_RESEND", "")
        EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "")
        EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "")
        DIRETORIO = Path(__file__).resolve().parent
        IP_PUBLICO = buscarIpPublico(API_IP_PUBLICO)

        caminhoAbsoluto = DIRETORIO/NOME_ARQUIVO

        # testa a existência do cache e a necessidade de atualizar
        atualizar = not caminhoAbsoluto.exists() or IP_PUBLICO != cacheLer(NOME_ARQUIVO)

        if atualizar:
            print(f"ips diferentes! As seguintes ações serão realizadas:\n"
                  f"1 - Atualizar Cloudflare;\n"
                  f"2 - Atualizar Cache;\n"
                  f"3 - Enviar E-mail.")

            # atualizar cloudflare
            atualizarIpCloudflare(IP_PUBLICO, ZONE_ID, RECORD_ID, CLOUDFLARE_TOKEN)

            # atualizar cache
            cacheAtualizar(IP_PUBLICO, NOME_ARQUIVO)

            # disparo de e-mail
            enviarEmail(API_KEY_RESEND,
                        EMAIL_REMETENTE,
                        EMAIL_DESTINATARIO,
                        "sucesso",
                        "IP Alterado",
                        capturarInfoParaEmail())

    except ErroEmail as e:
        print(f"Ops! Algo não saiu conforme o esperado!\n"
              f"Erro: {e}\n"
              f"Contexto: {e.__context__}\n"
              f"Causa: {e.__cause__}")

    except Exception as e:
        print(f"Ops! Algo não saiu conforme o esperado!\n"
              f"Detalhe: {e}")

        enviarEmail(API_KEY_RESEND,
                    EMAIL_REMETENTE,
                    EMAIL_DESTINATARIO,
                    "falha",
                    "Falha no sistema",
                    capturarInfoParaEmailERRO(e))


if __name__ == "__main__":
    main()
