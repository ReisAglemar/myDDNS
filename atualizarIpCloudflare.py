"""
Módulo de Integração com a API da Cloudflare para Atualização de DNS.

Este módulo realiza a comunicação com os endpoints da Cloudflare para alterar
dinamicamente o conteúdo de um registro do tipo 'A', atualizando-o com o novo
IP público detectado no servidor.
"""

import urllib.request
import json


def atualizarIpCloudflare(IP_PUBLICO, ZONE_ID, RECORD_ID, CLOUDFLARE_TOKEN):
    """
        Envia uma requisição HTTP PATCH para atualizar o IP do registro DNS na Cloudflare.

        A função utiliza uma requisição parcial (PATCH) nativa para modificar apenas
        o conteúdo do IP, mantendo o TTL em modo automático (1) e desativando o proxy
        (proxied: False) para garantir conexões diretas ao servidor local.

        :param IP_PUBLICO: O novo endereço de IP público a ser injetado no registro.
        :type IP_PUBLICO: str
        :param ZONE_ID: O identificador único da zona do domínio na Cloudflare.
        :type ZONE_ID: str
        :param RECORD_ID: O identificador único do registro DNS específico (tipo A).
        :type RECORD_ID: str
        :param CLOUDFLARE_TOKEN: Token de API de autenticação com permissões de edição de DNS.
        :type CLOUDFLARE_TOKEN: str
        :return: True se a Cloudflare responder com sucesso.
        :rtype: bool

        :raises RuntimeError: Se a Cloudflare rejeitar os dados ou se houver falhas críticas
                              de rede/timeout durante a comunicação.
        """

    URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"

    corpo = {
        "content": IP_PUBLICO
    }

    bytes = json.dumps(corpo).encode('utf-8')

    try:
        requisicao = urllib.request.Request(
            URL,
            data=bytes,
            headers={
                "authorization": f"Bearer {CLOUDFLARE_TOKEN}",
                "content-type": "application/json"
            },
            method="PATCH"
        )

        with urllib.request.urlopen(requisicao, timeout=10):
            # Requisição concluída com sucesso dentro do limite de tempo
            return True


    except urllib.error.HTTPError as httpErr:
        raise RuntimeError(f"Erro ao atualizar IP na Cloudflare {httpErr.code}") from httpErr

    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar IP na Cloudflare {e}")from e
