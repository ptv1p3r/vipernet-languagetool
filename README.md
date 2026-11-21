# vipernet-languagetool

`rever_texto` pede sugestões ao LanguageTool quando o utilizador pede revisão linguística. Não observa conversas, não interceta respostas nem edita o original. Exemplo: «Revê esta frase em inglês britânico: This is an test.» A ferramenta recebe `{"texto":"This is an test.","idioma":"en-GB"}` e sugere «a» em vez de «an».

Se não indicares um idioma, usa `pt-PT`. Também aceita `en-US` e `en-GB`. Em documentos mistos, o agente deve enviar só os parágrafos de prosa e excluir código, comandos, URLs, caminhos, identificadores, citações literais e segredos. Esta seleção é uma instrução ao agente, não um filtro infalível: a ferramenta envia o argumento `texto` tal como o recebe.

## Instalação manual posterior

No contentor Hermes, a partir da pasta desta entrega, executar **apenas quando se pretender instalar**:

```sh
P=/opt/data/profiles/pessoal
D="$P/plugins/vipernet-languagetool"
mkdir "$D" && cp __init__.py plugin.yaml README.md "$D/" && \
  hermes -p pessoal config set plugins.entries.vipernet-languagetool.settings.base_url http://192.168.2.37:8010 && \
  hermes -p pessoal plugins enable vipernet-languagetool
```

O `mkdir` sem `-p` impede a substituição de uma instalação existente. Neste ambiente, `pessoal/plugins` aponta à pasta partilhada: os ficheiros ficam visíveis aos outros perfis, mas este comando só pede ativação no `pessoal`. Abrir uma sessão nova no perfil depois de o gateway carregar a ativação. Para desativar: `hermes -p pessoal plugins disable vipernet-languagetool`.

O exemplo em `config.example.yaml` mostra a chave do perfil; não substituas o `config.yaml` por esse excerto. Para mudar de servidor, repetir `config set` com a nova origem HTTP(S), sem caminho, credenciais, query ou fragmento. O plugin consulta essa chave em cada chamada. Se a chave não existir, usa o servidor Vipernet indicado acima. O modelo não pode fornecer outro destino como argumento.

## Dados e limites

O plugin envia um único `POST /v2/check` diretamente ao servidor configurado; não segue redirecionamentos, não usa proxies do ambiente e não faz novas tentativas. O endereço fornecido usa HTTP sem cifra: só deve ser usado numa rede de confiança. O plugin não escreve ficheiros, logs, histórico ou cache, não executa subprocessos e não precisa de credenciais nem dependências externas. A conversa e os argumentos das ferramentas podem ficar no histórico do Hermes; a retenção do servidor LanguageTool também é independente deste plugin.

Cada pedido admite até 10 000 caracteres. A resposta inclui o idioma, o total de alertas e, para os primeiros 50, posição e comprimento nativos do LanguageTool (unidades UTF-16), regra, mensagem e até cinco alternativas. Não devolve a frase de contexto nem um documento corrigido. `truncado` indica omissão de alertas; zero alertas não certifica o texto. O timeout de socket é de 10 segundos e a resposta HTTP está limitada a 1 MiB. Um erro devolve `error`, nunca uma revisão vazia.

## Repetir os testes sem instalar

Na pasta desta entrega:

```sh
python3 -B -m unittest discover -s tests -v
hermes plugins doctor "$PWD" --ci
hermes plugins validate "$PWD" --json
python3 -B tests/live_api.py
```

Os testes unitários usam um servidor em loopback. Só o último comando envia frases sintéticas à instância Vipernet: para cada idioma, exige a sugestão esperada na frase com erro e zero alertas na frase correta. O caso português também verifica o comportamento da regra local de cinema.
