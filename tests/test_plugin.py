import importlib.util
import json
from pathlib import Path
import unittest
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]

def load():
    spec = importlib.util.spec_from_file_location('lt_plugin', ROOT / '__init__.py')
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def tool(url):
    registered = []
    ctx = SimpleNamespace(get_config=lambda key, default: url if key == 'base_url' else default,
                          register_tool=lambda **kw: registered.append(kw))
    load().register(ctx)
    t, = registered
    return t

class Registration(unittest.TestCase):
    def test_on_demand_prose_only(self):
        self.assertTrue((ROOT / '__init__.py').is_file(), 'Plugin ainda não implementado')
        t = tool('invalid')
        self.assertEqual(t['name'], 'rever_texto')
        self.assertIn('prosa', t['schema']['description'])
        self.assertEqual(t['schema']['parameters']['properties']['idioma']['default'], 'pt-PT')
