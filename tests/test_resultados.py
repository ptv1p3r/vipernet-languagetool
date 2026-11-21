import json
import unittest
from unittest.mock import patch
from test_plugin import load
from test_http import server
from test_plugin import tool

class Resultados(unittest.TestCase):
    def test_revisao_parcial(self):
        with server() as (url, _, r):
            for value in (True, False):
                r['body'] = json.dumps({'matches': [], 'warnings': {'incompleteResults': value}}).encode()
                out = json.loads(tool(url)['handler']({'texto':'Teste.'}))
                self.assertEqual(out['estado'], 'revisão incompleta' if value else 'revisão concluída')

    def test_excerto_utf16(self):
        with server() as (url, _, r):
            m = {'offset': 3, 'length': 3, 'rule': {'id':'teste'}, 'message':'teste', 'replacements':[]}
            r['body'] = json.dumps({'matches':[m]}).encode()
            out = json.loads(tool(url)['handler']({'texto':'📘 não!'}))
            self.assertEqual(out['alertas'][0]['excerto'], 'não')

    def test_sem_servidor_nao_envia(self):
        from types import SimpleNamespace
        t = {}; mod = load()
        mod.register(SimpleNamespace(get_config=lambda k,d: d, register_tool=lambda **kw:t.update(kw)))
        with patch.object(mod,'HTTPConnection') as connect:
            out = json.loads(t['handler']({'texto':'Teste.'}))
            connect.assert_not_called()
            self.assertIn('base_url',out['error'])
