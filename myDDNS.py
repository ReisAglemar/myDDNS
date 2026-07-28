#!/usr/bin/env python3
"""
Módulo Orquestrador Principal do Sistema de Dynamic DNS (myDDNS).

Este módulo gerencia o fluxo de execução do DDNS: carrega as variáveis de ambiente,
verifica o IP público atual, compara com o cache local e atualiza os registros de
DNS na Cloudflare caso ocorram mudanças, notificando o administrador via e-mail.
"""
import logging
import os
from pathlib import Path

from carregarEnvs import carregarEnvs
from gerarLog import configurarLogging
from buscarIpPublico import buscarIpPublico
from atualizarIpCloudflare import atualizarIpCloudflare
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

        IP_PUBLICO = buscarIpPublico(API_IP_PUBLICO).strip()
        caminhoAbsoluto = DIRETORIO / NOME_ARQUIVO

        # testa a existência do cache e a necessidade de atualizar
        atualizar = not caminhoAbsoluto.exists() or IP_PUBLICO != cacheLer(NOME_ARQUIVO)

        if atualizar:
            configurarLogging()
            logging.info("=" * 30 + " NOVO EVENTO " + "=" * 30)
            logging.info(f"Detectada alteração no IP.")

            # atualizar cloudflare
            logging.info(f"Iniciando atualização na Cloudflare...")
            atualizarIpCloudflare(IP_PUBLICO, ZONE_ID, RECORD_ID, CLOUDFLARE_TOKEN)
            logging.info(f"Cloudflare atualizada com sucesso.")

            # atualizar cache
            logging.info(f"Iniciando atualização do cache local...")
            cacheAtualizar(IP_PUBLICO, NOME_ARQUIVO)
            logging.info(f"Cache atualizado com sucesso. Novo IP: {IP_PUBLICO}")

            # disparo de e-mail
            logging.info(f"Iniciando o disparo nativo de e-mail...")
            enviarEmail(API_KEY_RESEND,
                        EMAIL_REMETENTE,
                        EMAIL_DESTINATARIO,
                        "sucesso",
                        "IP Alterado",
                        capturarInfoParaEmail(IP_PUBLICO))
            logging.info(f"E-mail enviado com sucesso para: {EMAIL_DESTINATARIO}")
        return 0


    except ErroEmail as e:
        configurarLogging()
        logging.info("=" * 30 + " ERRO NO SISTEMA " + "=" * 30)
        logging.error(f"Exceção: {e}.")
        logging.error(f"Contexto: {e.__context__}.")
        logging.error(f"Causa: {e.__cause__}.")
        return 1


    except Exception as e:
        configurarLogging()
        logging.info("=" * 30 + " ERRO NO SISTEMA " + "=" * 30)
        logging.error(f"Falha na execução principal")
        logging.error(f"Exceção: {e}.")
        logging.error(f"Contexto: {e.__context__}.")
        logging.error(f"Causa: {e.__cause__}.")

        try:
            logging.info(f"Iniciando o disparo nativo de e-mail de alerta...")
            enviarEmail(API_KEY_RESEND,
                        EMAIL_REMETENTE,
                        EMAIL_DESTINATARIO,
                        "falha",
                        "Falha no sistema",
                        capturarInfoParaEmailERRO(e))
            logging.info(f"E-mail enviado com sucesso para: {EMAIL_DESTINATARIO}")
            return 1


        except ErroEmail as e:
            logging.info("=" * 30 + " ERRO NO SISTEMA " + "=" * 30)
            logging.error(f"Exceção: {e}.")
            logging.error(f"Contexto: {e.__context__}.")
            logging.error(f"Causa: {e.__cause__}.")
        return 1


if __name__ == "__main__":
    main()
