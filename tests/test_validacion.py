import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.modelos import NoticiaFuente
from src.validacion import ValidadorJSON


class TestValidadorJSON(unittest.TestCase):
    def fixture(self):
        return {
            "id_noticia":"N001","titulo":"Título","fecha_publicacion":None,
            "fuente":"Medio","url":"https://ejemplo.cl/a","resumen":"Resumen",
            "delitos":["Homicidio"],"personas":[{"nombre":"Persona A","rol":"imputado"}],
            "organizaciones":["PDI"],"lugares":["Coquimbo"],
            "objetos":[{"tipo":"arma","nombre":"cuchillo","cantidad":None,"unidad":None}],
            "relaciones":[{"origen":"Persona A","tipo":"DETENIDO_EN","destino":"Coquimbo"}]
        }

    def test_valido_y_trazable(self):
        with TemporaryDirectory() as d:
            ruta=Path(d)/"N001.json"
            ruta.write_text(json.dumps(self.fixture()),encoding="utf-8")
            esperado=NoticiaFuente("N001","Medio","https://ejemplo.cl/a")
            r=ValidadorJSON().validar(ruta,esperado)
            self.assertTrue(r.valido, r.errores)

    def test_detecta_campo_faltante(self):
        with TemporaryDirectory() as d:
            data=self.fixture(); del data["relaciones"]
            ruta=Path(d)/"N001.json"; ruta.write_text(json.dumps(data),encoding="utf-8")
            r=ValidadorJSON().validar(ruta)
            self.assertFalse(r.valido)
            self.assertTrue(any("relaciones" in e for e in r.errores))
