"""
Módulo de Formatação de Mensagens para Notificação de E-mail.

Este módulo centraliza a construção das strings e fragmentos em HTML que servem
como o corpo descritivo dos e-mails enviados pelo sistema, segmentando as mensagens
entre fluxos de sucesso e falhas críticas.
"""

import os
from buscarIpPublico import buscarIpPublico


def capturarInfoParaEmail(iP):
    """
        Gera o fragmento HTML descritivo para cenários de sincronização bem-sucedida.

        A função consome a API de IP público configurada nas variáveis de ambiente
        para exibir no corpo do e-mail qual endereço foi injetado na Cloudflare.

        :return: String com tags HTML contendo o status e o IP atualizado.
        :rtype: str
        """

    return (f"DDNS Atualizado com Sucesso!<br>"
            f"<br>"
            f"IP Atual: <strong>{iP}</strong><br>")


def capturarInfoParaEmailERRO(e):
    """
        Gera o fragmento HTML descritivo isolando e estilizando exceções do Python.

        Recebe a exceção capturada no bloco try/except principal e envelopa a mensagem
        técnica em uma tag `<code>` estilizada para facilitar a depuração direto pelo e-mail.

        :param e: Instância da exceção ou erro capturado durante a execução do script.
        :type e: Exception
        :return: String com tags HTML contendo o diagnóstico do erro e o caminho dos logs.
        :rtype: str
        """

    return (f"<strong>Falha Crítica na Execução do Script!</strong><br>"
            f"O processo automatizado de sincronização de DDNS foi interrompido.<br>"
            f"<br>"
            f"<strong>Detalhe do Erro:</strong><br>"
            f"<code style='background-color: #f1f5f9; "
            f"padding: 2px 6px; "
            f"border-radius: 4px; "
            f"color: #dc2626; "
            f"font-family: monospace;'>{e}</code><br>"
            f"<br>"
            f"Por favor, verifique os logs do servidor em <code>/var/log/myddns.log</code> para mais informações.")
