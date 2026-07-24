"""
Módulo de Geração de Templates HTML para Notificações.

Este módulo é responsável por estruturar layouts HTML responsivos, limpos e
profissionais para o envio de e-mails informativos ou de alertas de erro.
"""


def gerarHtml(status, titulo, corpo):
    """
        Gera um template HTML customizado com base no status da operação.

        O layout adapta dinamicamente a cor da barra superior decorativa para
        sinalizar visualmente se o e-mail representa um evento de sucesso ou falha.

        :param status: O estado do alerta, aceitando 'sucesso' (verde) ou qualquer outro valor (vermelho).
        :type status: str
        :param titulo: O assunto principal que será exibido no cabeçalho do e-mail.
        :type titulo: str
        :param corpo: O conteúdo ou os detalhes da mensagem em formato HTML/Texto.
        :type corpo: str
        :return: Uma string contendo o código HTML completo e formatado pronto para envio.
        :rtype: str
        """

    corTopo = "#10b981" if status == "sucesso" else "#ef4444"
    corBorda = "#e2e8f0"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
    </head>
    <body style="margin: 0; padding: 0; 
    background-color: #f8fafc; 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" 
        style="max-width: 600px; margin: 20px auto; background-color: #ffffff; 
        border-radius: 8px; overflow: hidden; border: 1px solid {corBorda}; 
        border-collapse: collapse; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <!-- Topo Colorido indicador de Status -->
           
            <tr>
                <td style="background-color: {corTopo}; padding: 4px; text-align: center;"></td>
            </tr>

            <!-- Conteúdo Principal -->
            <tr>
                <td style="padding: 40px 32px;">
                    <h2 style="margin-top: 0; margin-bottom: 16px; color: #1e293b; font-size: 22px; 
                    font-weight: 700; letter-spacing: -0.025em;">
                        {titulo}
                    </h2>

                    <div style="color: #475569; font-size: 15px; line-height: 24px; margin-bottom: 24px;">
                        {corpo}
                    </div>
                </td>
            </tr>

            <!-- Rodapé / Footer -->
            <tr>
                <td style="background-color: #f1f5f9; padding: 24px 32px; text-align: center; border-top: 1px solid {corBorda};">
                    <p style="margin: 0; font-size: 12px; color: #94a3b8; line-height: 18px;">
                        Este é um alerta automático gerado pelo sistema de monitoramento self-hosted.<br>
                        <b>Servidor Local</b> • Domínio: <a href="https://arreis.com.br" style="color: #64748b; 
                        text-decoration: underline;">arreis.com.br</a>
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
