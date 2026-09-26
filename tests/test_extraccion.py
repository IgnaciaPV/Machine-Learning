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
        data = ExtractorGemini._extraer_json_de_texto('''```json
{"a": 1}
```''')
        self.assertEqual(data, {"a": 1})

    def test_postprocesado_descarta_relacion_huerfana(self):
        data = {
            "delitos": ["homicidio", "homicidio"],
            "personas": [{"nombre": "víctima", "rol": "víctima"}],
            "organizaciones": [], "lugares": ["Coquimbo"], "objetos": [],
            "relaciones": [
                {"origen": "víctima", "tipo": "VICTIMA_DE", "destino": "homicidio"},
                {"origen": "víctima", "tipo": "VIO_A", "destino": "entidad inexistente"},
            ],
        }
        limpio = ExtractorGemini._postprocesar_estructurado(data)
        self.assertEqual(limpio["delitos"], ["homicidio"])
        self.assertEqual(len(limpio["relaciones"]), 1)

    def test_postprocesado_evitar_sobreafirmar_culpabilidad(self):
        data = {
            "delitos": ["receptación de vehículo"],
            "personas": [{"nombre": "persona detenida", "rol": "detenido"}],
            "organizaciones": [], "lugares": [], "objetos": [],
            "relaciones": [
                {"origen": "persona detenida", "tipo": "COMETIO_DELITO", "destino": "receptación de vehículo"}
            ],
        }
        limpio = ExtractorGemini._postprocesar_estructurado(data)
        self.assertEqual(limpio["relaciones"], [])

    def test_postprocesado_valorizacion_no_es_cantidad_fisica(self):
        data = {
            "delitos": [], "personas": [], "organizaciones": [], "lugares": [],
            "objetos": [{"tipo": "medicamento", "nombre": "jarabes", "cantidad": "más de un millón de pesos", "unidad": None}],
            "relaciones": [],
        }
        limpio = ExtractorGemini._postprocesar_estructurado(data)
        self.assertIsNone(limpio["objetos"][0]["cantidad"])


if __name__ == "__main__":
    unittest.main()
