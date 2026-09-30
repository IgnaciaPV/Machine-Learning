import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.conocimiento import EscritorVaultObsidian


class TestObsidian(unittest.TestCase):
    def test_no_fusiona_personas_por_descripcion_compartida(self):
        noticias = [
            {"id_noticia": "N001", "titulo": "A", "personas": [{"nombre": "un hombre", "rol": "detenido"}], "delitos": ["robo"], "relaciones": [{"origen": "un hombre", "tipo": "INVESTIGADO_POR", "destino": "robo"}]},
            {"id_noticia": "N005", "titulo": "B", "personas": [{"nombre": "Un hombre", "rol": "víctima"}]},
        ]
        with TemporaryDirectory() as d:
            w = EscritorVaultObsidian(Path(d))
            w.escribir_vault(noticias)
            self.assertEqual(w.auditar_enlaces(), [])
            self.assertEqual(len(list((Path(d) / "Personas").glob("*.md"))), 2)
            a = (Path(d) / "Personas/N001_un_hombre.md").read_text()
            self.assertNotIn("Noticias/N005", a)
            self.assertNotIn("víctima", a)

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
