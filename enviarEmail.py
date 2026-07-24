"""
Módulo de Integração com a API de E-mails do Resend.

Este módulo realiza o disparo de e-mails de forma 100% nativa utilizando as
bibliotecas padrões do Python (urllib e json), sem a necessidade de instalar
SDKs ou dependências externas no ambiente do servidor.
"""

import urllib.request
import json
from gerarHtml import gerarHtml
from excecao import ErroEmail


def enviarEmail(API_KEY_RESEND,
                EMAIL_REMETENTE,
                EMAIL_DESTINATARIO,
                status,
                assunto,
                corpo):
    """
        Dispara uma requisição HTTP POST para a API do Resend para enviar um e-mail formatado.

        A função consome a função `gerarHtml` para envelopar o corpo em um template
        visual profissional e injeta um cabeçalho 'User-Agent' personalizado para evitar
        bloqueios de segurança contra bots (WAF / Cloudflare 403 Forbidden).

        :param API_KEY_RESEND: Chave de API de autenticação do Resend (Bearer token).
        :type API_KEY_RESEND: str
        :param EMAIL_REMETENTE: E-mail de origem validado no Resend (ex: nome@dominio.com).
        :type EMAIL_REMETENTE: str
        :param EMAIL_DESTINATARIO: Endereço de e-mail que receberá a notificação.
        :type EMAIL_DESTINATARIO: str
        :param status: Define a estilização do template ('sucesso' ou 'falha').
        :type status: str
        :param assunto: O título/assunto que aparecerá na caixa de entrada.
        :type assunto: str
        :param corpo: O conteúdo em formato texto ou HTML com os detalhes da execução.
        :type corpo: str

        :raises RuntimeError: Se a API do Resend rejeitar a requisição (HTTPError)
                              ou se houver falhas de conectividade com a rede.
        """

    url = "https://api.resend.com/emails"

    # Gera o HTML injetando o conteúdo dinâmico
    html = gerarHtml(status, assunto, corpo)

    headers = {
        "Authorization": f"Bearer {API_KEY_RESEND}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    corpoRequisicao = {
        "from": EMAIL_REMETENTE,
        "to": EMAIL_DESTINATARIO,
        "subject": assunto,
        "html": html
    }

    try:
        print("Iniciando envio de e-mail via request nativo...")
        dadosFinais = json.dumps(corpoRequisicao).encode("utf-8")

        requisicao = urllib.request.Request(
            url,
            data=dadosFinais,
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(requisicao) as resposta:
            if resposta.status in (200, 201):
                print(f"E-mail disparado com sucesso para {EMAIL_DESTINATARIO}!")

    except Exception as e:
        raise ErroEmail(e)from e
