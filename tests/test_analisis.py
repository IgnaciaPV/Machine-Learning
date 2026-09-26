import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.analisis import ExploradorDatos


class TestAnalisis(unittest.TestCase):
    def test_genera_resumen_y_visualizaciones(self):
        with TemporaryDirectory() as d:
            base=Path(d); j=base/"json"; o=base/"out"; v=base/"validation"
            j.mkdir(); v.mkdir()
            data={
                "id_noticia":"N001","titulo":"Prueba","fecha_publicacion":"2026-01-01",
                "fuente":"Medio","url":"https://ejemplo.cl/a","resumen":"Resumen",
                "delitos":["Homicidio"],"personas":[],"organizaciones":["PDI"],
                "lugares":["Coquimbo"],"objetos":[],"relaciones":[]
            }
            (j/"N001.json").write_text(json.dumps(data),encoding="utf-8")
            r=ExploradorDatos(j,o,v).ejecutar()
            self.assertEqual(r["noticias_procesadas"],1)
            self.assertTrue((o/"resumen_data_understanding.json").exists())
            self.assertTrue((o/"visualizaciones/01_noticias_por_fuente.png").exists())
