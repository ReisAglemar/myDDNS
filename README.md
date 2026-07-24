# Sistema de Sincronização Dinâmica de DNS (myDDNS)

O myDDNS é uma solução autônoma desenvolvida em Python para o gerenciamento e atualização automatizada de registros de 
DNS (Dynamic DNS) hospedados na infraestrutura da Cloudflare. O principal objetivo do projeto é monitorar e propagar
alterações de endereços IPv4 públicos em redes residenciais ou servidores locais (self-hosted), garantindo alta
disponibilidade de serviços internos por meio de um domínio personalizado.

Como diferencial técnico, o sistema foi projetado sob os princípios de arquitetura limpa e desenvolvimento nativo, 
eliminando a dependência de pacotes de terceiros (como bibliotecas do ecossistema pip) e mitigando riscos de segurança
associados à cadeia de suprimentos de software (Supply Chain Attacks).

## Diferenciais de Engenharia e Decisões Técnicas

*   **Abordagem Vanilla Python (Zero-Dependency):** Toda a comunicação com APIs externas (Cloudflare e Resend) foi 
implementada utilizando exclusivamente os módulos nativos `urllib.request` e `json`. Essa decisão elimina a necessidade
de ambientes virtuais (venv) no servidor de produção, reduz o consumo de memória e simplifica o deploy do script no
sistema operacional.

*   **Mecanismo de Cache para Otimização de I/O:** Para evitar o overhead de requisições HTTP redundantes para os
provedores, o sistema utiliza um arquivo de persistência local como cache de estado. A API da Cloudflare e o serviço
de notificação só são acionados se o IP público atual for divergente do último registro persistido.

*   **Bypassing de Web Application Firewall (WAF):** O componente de integração foi desenhado com a injeção explícita
de cabeçalhos de identidade (`User-Agent`), evitando falsos positivos de segurança (erros 403 Forbidden / Cloudflare Error 1010)
que barram automações puras que utilizam a assinatura padrão do Python.

*   **Isolamento de Falhas (Fault Tolerance):** O fluxo principal implementa um mecanismo de tratamento de exceções em
cascata. Caso a rotina de atualização ou conexão falhe, o script isola a mensagem de erro do interpretador e engatilha
um fluxo alternativo para alertar o administrador do sistema.

*   **Tratamento Nativo de Arquivos de Configuração:** O módulo responsável pelo gerenciamento de variáveis de ambiente
faz o parsing manual de chaves e valores do arquivo `.env` sem dependências do `python-dotenv`, suportando a
sanitização de comentários e linhas vazias via generators do Python.

## Arquitetura e Estrutura de Módulos

O projeto adota o princípio de responsabilidade única (Single Responsibility Principle), dividindo as capacidades do
sistema em módulos independentes:

*   `myDDNS.py`: Orquestrador central da aplicação. Controla o ciclo de vida da execução, o fluxo de tomada de decisão
baseada no cache e o roteamento de payloads de sucesso ou falha.

*   `carregarEnvs.py`: Gerenciador de infraestrutura local que realiza o parse e a injeção de configurações estáticas
no escopo do sistema operacional (`os.environ`).

*   `buscarIpPublico.py`: Cliente HTTP dedicado a consultar endpoints de descoberta e realizar o tratamento de
payloads no formato JSON.

*   `cache.py`: Camada de persistência em disco encarregada de gerenciar as operações de leitura e escrita do
estado do IP público.

*   `atualizarIpCloudflare.py`: Componente de integração de rede que interage com a API Rest v4 da Cloudflare através
de requisições parciais utilizando o método HTTP `PATCH`.

*   `enviarEmail.py`: Cliente de comunicação responsável pela montagem de requisições de rede destinadas aos
servidores do gateway de e-mail Resend.

*   `gerarHtml.py`: Motor de renderização de templates responsável por gerar layouts estruturados em HTML inline
para fins de padronização visual.

*   `capturarInfoParaEmail.py`: Camada de mapeamento de dados que transforma exceções de sistema ou dados de IP em
mensagens semânticas compatíveis com o motor de e-mail.

## Configuração do Ambiente (.env)

As credenciais e os identificadores de infraestrutura devem ser definidos em um arquivo nomeado como `.env` localizado
na raiz do projeto, seguindo o padrão abaixo:

```text
CLOUDFLARE_TOKEN=seu_token_com_permissao_de_edicao_de_dns
ZONE_ID=identificador_da_zona_do_dominio
RECORD_ID=identificador_do_registro_A_a_ser_atualizado
NOME_ARQUIVO=cache.txt
API_IP_PUBLICO=[https://api.ipify.org?format=json](https://api.ipify.org?format=json)
RESEND_API_KEY=sua_chave_de_autenticacao_resend
EMAIL_REMETENTE=origem_validada@seu_dominio.com.br
EMAIL_DESTINATARIO=seu_email_pessoal@provedor.com