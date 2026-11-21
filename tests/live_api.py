"""Teste opt-in: só envia as frases sintéticas abaixo à instância Vipernet."""
import json
from test_plugin import load, tool

if __name__ == '__main__':
    f = tool(load().BASE_URL)['handler']
    for language, bad, good, replacement in [
        (None, 'Comprei bilhetes para a secção de cinema das nove.', 'Comprei bilhetes para a sessão de cinema das nove.', 'sessão'),
        ('en-US','This is an test.','This is a test.','a'),
        ('en-GB','This is an test.','This is a test.','a'),
    ]:
        opts = {'idioma':language} if language else {}
        issue = json.loads(f(dict(texto=bad, **opts)))
        clean = json.loads(f(dict(texto=good, **opts)))
        if 'error' in issue or 'error' in clean:
            raise SystemExit(f'{language or "pt-PT"}: {issue.get("error") or clean.get("error")}')
        matches = [m for m in issue['alertas'] if replacement in m['sugestoes']]
        assert matches and clean['total'] == 0, 'Resultado linguístico inesperado'
        print(f'{issue["idioma"]}: {issue["total"]} alerta(s); {matches[0]["regra"]} → {replacement}; controlo: {clean["total"]}')
