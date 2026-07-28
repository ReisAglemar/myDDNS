"""
Módulo de Consulta ao Endereço de IP Público da Rede.

Este módulo realiza requisições HTTP a serviços externos baseados em JSON para
descobrir e extrair o endereço IPv4 público atual sob o qual o servidor local
está operando na internet.
"""

import urllib.request
import json


def buscarIpPublico(API_IP_PUBLICO):
    """
        Efetua uma requisição GET nativa à API configurada para obter o IP público.

        A função adiciona um cabeçalho 'User-Agent' para contornar bloqueios comuns de
        firewalls corporativos e implementa um limite de tempo de resposta (timeout) de 10
        segundos para garantir a resiliência do script em execuções agendadas (Cron).

        :param API_IP_PUBLICO: A URL do endpoint da API que retorna o IP (ex: ipify ou ipinfo).
        :type API_IP_PUBLICO: str
        :return: O endereço de IP público em formato textual (ex: '111.111.011.37').
        :rtype: str

        :raises RuntimeError: Se houver problemas de timeout, indisponibilidade da API externa,
                              falhas na decodificação do JSON ou ausência da chave 'ip' na resposta.
        """

    try:
        requisao = urllib.request.Request(API_IP_PUBLICO, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(requisao, timeout=10) as resposta:
            dadosTexto = resposta.read().decode('utf-8')
            dadosJson = json.loads(dadosTexto)
            ip = dadosJson.get("ip")
            return ip

    except urllib.error.HTTPError as httpErr:
        raise RuntimeError(f"Falha ao obter o IP público {httpErr.code}") from httpErr

    except Exception as e:
        raise RuntimeError(f"Erro ao obter ip público {e}")from e
