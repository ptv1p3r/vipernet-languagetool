# Submissão ao catálogo do Hermes

Descrição para o pedido: o plugin regista uma ferramenta de revisão a pedido, `rever_texto`, através de `ctx.register_tool`. Lê apenas `base_url` pelo `ctx.get_config` do perfil. Não regista hooks nem middleware, não altera o núcleo, não inclui painel nem atualizador próprio.

Declaração de dados e permissões: envia o texto fornecido e o código de língua à origem HTTP(S) escolhida pelo operador. Sem destino predefinido, credenciais, telemetria, subprocessos, leitura de documentos ou escrita em disco. O texto não é anonimizado. A retenção do Hermes e do LanguageTool é independente. Nenhuma captura de ecrã: a única interface é a ferramenta.

Antes da submissão, integrar dev em main pelo fluxo protegido. A partir de um clone anónimo do espelho público, extrair o SHA da ficha em `plugin-catalog/vipernet-languagetool.yaml`, verificar que pertence ao histórico de main, fazer checkout desse SHA e executar os testes e `hermes plugins validate . --install-deps`. Se o método de integração não preservar o SHA, escolher e testar um novo commit público. No pedido ao NousResearch/hermes-agent incluir apenas a ficha do catálogo; indicar SHA, resultados e declaração acima. A publicação depende de revisão pelos responsáveis do Hermes.
