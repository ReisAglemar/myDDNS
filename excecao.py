"""
Módulo de Exceções Personalizadas do Projeto.

Este módulo centraliza todas as exceções personalizadas utilizadas pela
aplicação, permitindo que cada camada da arquitetura comunique falhas de
forma semântica e desacoplada.

Ao encapsular exceções nativas do Python em exceções específicas do domínio
da aplicação, torna-se possível distinguir, por exemplo, falhas do serviço
de envio de e-mails das demais exceções da aplicação, permitindo que a
camada principal (main) adote estratégias de tratamento diferentes para
cada cenário.

As exceções personalizadas preservam a exceção original através do comando
'raise ... from ...', mantendo o traceback completo para fins de diagnóstico
e depuração.
"""


class ErroEmail(Exception):
    """
      Exceção lançada quando ocorre qualquer falha durante o processo de envio
      de e-mails.

      Esta exceção funciona como um encapsulador para qualquer exceção gerada
      pelas bibliotecas utilizadas no envio de e-mails (erros de rede,
      autenticação, DNS, timeout, HTTP, entre outros), permitindo que a camada
      principal identifique que o subsistema responsável pela notificação
      apresentou falha.

      A exceção original deve ser preservada utilizando:

          raise ErroEmail(...) from excecao_original

      Dessa forma, o traceback mantém tanto a exceção de alto nível
      (ErroEmail) quanto a causa raiz do problema.

      :raises ErroEmail: Indica que o serviço responsável pelo envio de e-mails
                         não conseguiu concluir sua operação.
      """
    pass