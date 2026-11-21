from contextlib import contextmanager, redirect_stdout, redirect_stderr
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
import json
import threading
from urllib.parse import parse_qs
import unittest
from test_plugin import tool

@contextmanager
def server():
    requests = []
    reply = {'status': 200, 'body': b'{"matches": []}'}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_POST(self):
            data = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            requests.append((self.command, self.path, parse_qs(data.decode())))
            self.send_response(reply['status'])
            self.send_header('Location', '/destino')
            self.end_headers()
            self.wfile.write(reply['body'])
        do_GET = do_POST
    with ThreadingHTTPServer(('127.0.0.1', 0), Handler) as s:
        thread = threading.Thread(target=s.serve_forever, args=(0.02,), daemon=True)
        thread.start()
        try: yield f'http://127.0.0.1:{s.server_port}', requests, reply
        finally: s.shutdown(); thread.join()

class Network(unittest.TestCase):
    def test_review(self):
        with server() as (url, calls, reply):
            handler = tool(url)['handler']
            for language in [None, 'en-GB', 'en-US']:
                args = {'texto': ' & + Câmara\n'}
                if language: args['idioma'] = language
                result = json.loads(handler(args))
                self.assertEqual(result['total'], 0)
                self.assertEqual(calls[-1], ('POST','/v2/check',{'text':[args['texto']], 'language':[language or 'pt-PT']}))
            self.assertEqual(len(calls), 3)

    def test_bad_inputs_stay_local(self):
        with server() as (url, calls, _):
            f = tool(url)['handler']
            for a in [{}, {'texto':' '}, {'texto':3}, {'texto':'\ud800'}, {'texto':'a'*10001}, {'texto':'a','idioma':'en'}, {'texto':'a','url':url}]:
                self.assertIn('error', json.loads(f(a)))
            self.assertFalse(calls)

    def test_redirects_never_followed(self):
        with server() as (url, calls, r):
            f = tool(url)['handler']
            for status in (301, 302, 303, 307, 308):
                r['status'] = status
                self.assertIn('error',json.loads(f({'texto':'Teste.'})))
            self.assertEqual([x[1] for x in calls], ['/v2/check']*5)

    def test_errors_do_not_echo(self):
        with server() as (url, _, r):
            text = 'CANARIO_PRIVADO'
            buf = StringIO()
            with redirect_stdout(buf), redirect_stderr(buf), self.assertNoLogs(level='DEBUG'):
                for status, body in [(500,text), (200,text), (200,'{}'), (200,'{"matches": [null]}')]:
                    r.update(status=status,body=body.encode())
                    result = tool(url)['handler']({'texto':text})
                    self.assertIn('error',json.loads(result)); self.assertNotIn(text,result)
            self.assertEqual(buf.getvalue(),'')

    def test_invalid_origin(self):
        for url in ['file:///tmp/foo','http://u:p@host','https://host/v2','https://host/?a=b','http://host/#abc','http://host:99999','']:
            self.assertIn('error',json.loads(tool(url)['handler']({'texto':'Teste.'})))
