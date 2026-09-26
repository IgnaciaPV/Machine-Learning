import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.extraccion import ExtractorGemini
from src.modelos import NoticiaFuente


class TestExtractorGemini(unittest.TestCase):
    def test_prompt_contiene_reglas_eticas_y_trazabilidad(self):
        with TemporaryDirectory() as d:
            ext = ExtractorGemini(Path(d))
            n = NoticiaFuente("N001", "Medio", "https://ejemplo.cl/a", texto="Un imputado fue detenido.")
            p = ext.construir_prompt(n)
            self.assertIn("No infieras culpabilidad", p)
            self.assertIn("N001", p)
            self.assertIn("Detenido, imputado", p)

    def test_recupera_json_con_fences(self):
        data = ExtractorGemini._extraer_json_de_texto('```json\n{"a": 1}\n```')
        self.assertEqual(data, {"a": 1})
