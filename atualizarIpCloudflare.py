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
        "name": "arreis.com.br",
        "type": "A",
        "ttl": 1,
        "proxied": False,
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

        with urllib.request.urlopen(requisicao, timeout=10) as resposta:
            codigo = resposta.getcode()
            respostaCorpo = json.loads(resposta.read().decode('utf-8'))

            if codigo == 200 and respostaCorpo.get("success"):
                print("DNS atualizado com sucesso")
                return True
            else:
                raise RuntimeError(f"Erro ao atualizar IP: {IP_PUBLICO}\n"
                                   f"Código: {codigo}\n"
                                   f"Resposta: {respostaCorpo}")

    except urllib.error.HTTPError as httpErr:
        detalhe = httpErr.read().decode('utf-8')
        raise RuntimeError(f"Falha na API da Cloudflare (Status {httpErr.code}).\n"
                           f"Detalhe: {detalhe}"
                           )from httpErr

    except Exception as e:
        raise RuntimeError(f"Falha crítica ao atualizar IP: {IP_PUBLICO}\n"
                           f"Código: {codigo}\n"
                           f"Resposta: {respostaCorpo}"
                           f"Erro: {e}"
                           )from e
