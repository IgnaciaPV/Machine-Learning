import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.conocimiento import EscritorVaultObsidian


class TestObsidian(unittest.TestCase):
    def test_vault_navegable_sin_enlaces_rotos(self):
        noticia={
            "id_noticia":"N001","titulo":"Prueba","fecha_publicacion":"2026-01-01",
            "fuente":"Medio","url":"https://ejemplo.cl/a","resumen":"Resumen",
            "delitos":["Homicidio"],
            "personas":[{"nombre":"Persona A","rol":"imputado"}],
            "organizaciones":["PDI"],"lugares":["Coquimbo"],
            "objetos":[{"tipo":"arma","nombre":"cuchillo","cantidad":1,"unidad":"unidad"}],
            "relaciones":[{"origen":"Persona A","tipo":"DETENIDO_EN","destino":"Coquimbo"}],
        }
        with TemporaryDirectory() as d:
            w=EscritorVaultObsidian(Path(d))
            w.escribir_vault([noticia])
            self.assertTrue((Path(d)/"00_Indice.md").exists())
            self.assertTrue((Path(d)/"Noticias/N001.md").exists())
            self.assertEqual(w.auditar_enlaces(),[])
