# Vipernet LanguageTool

Pede ao Hermes «Revê esta frase: Eu fui á escola». A ferramenta `rever_texto` envia o texto à tua instância do LanguageTool e apresenta os excertos assinalados com sugestões. Não altera o original. Usa português de Portugal por omissão; também aceita inglês britânico e americano (`en-GB`, `en-US`).

## Instalação e configuração

Precisas do Hermes 0.23.3 ou posterior e de um servidor LanguageTool acessível a partir do Hermes. O plugin não inclui o servidor. Enquanto não estiver no catálogo, instala pelo URL do repositório público, escolhendo o commit que queres instalar com `--ref`:

```
hermes plugins install https://github.com/ptv1p3r/vipernet-languagetool --ref <SHA-completo> --no-enable
hermes config set plugins.entries.vipernet-languagetool.settings.base_url http://127.0.0.1:8010
hermes plugins enable vipernet-languagetool
```

Abre uma nova sessão. Substitui o endereço pelo do teu servidor, sem `/v2/check`. Se o Hermes correr num contentor, `127.0.0.1` aponta para o próprio contentor. Para desativar usa `hermes plugins disable vipernet-languagetool` no mesmo perfil.

## Dados e permissões

Cada chamada envia `texto` e `idioma` num único POST para `/v2/check`. O destino vem da configuração do perfil, nunca dos argumentos da ferramenta. Sem endereço não há envio. Usa HTTPS fora de uma rede de confiança. A ferramenta não segue redirecionamentos, não usa proxies do ambiente e não repete pedidos. Não precisa de credenciais, não lê documentos, não escreve ficheiros nem registos, não executa comandos e não tem telemetria nem tarefas em segundo plano. A retenção pelo Hermes e pelo servidor é independente do plugin. O agente deve excluir citações, código e segredos; o plugin não anonimiza o texto que recebe.

## Resultados e testes

Aceita até 10 000 caracteres por pedido e devolve até 50 alertas, com excerto, posição em UTF-16 e até cinco alternativas. `estado` distingue uma revisão incompleta de uma revisão concluída; `truncado` indica que há alertas omitidos. Um erro de ligação não conta como revisão sem alertas.

```
python3 -B -m unittest discover -s tests -v
hermes plugins validate "$PWD" --install-deps
```

Opcional: define `LT_BASE_URL` e executa `python3 -B tests/live_api.py` para verificar três pares de frases sintéticas no teu servidor. Não requer regras personalizadas. O funcionamento não depende de bibliotecas Python de terceiros. Licença: MIT ou Apache-2.0, à escolha.
