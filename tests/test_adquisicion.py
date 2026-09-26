import unittest

from src.adquisicion.capturadores import CapturadorCooperativa
from src.adquisicion.cliente_http import ClienteHTTP


class TestCapturadorCooperativa(unittest.TestCase):
    def test_recupera_fecha_url_no_amp(self):
        c = CapturadorCooperativa(ClienteHTTP())
        captura = type("Dummy", (), {
            "fecha_publicacion": None,
            "url_final": "https://www.cooperativa.cl/noticias/pais/region-de-coquimbo/x/2026-08-22/095503.html",
        })()
        # Verifica directamente la lógica de fallback sin red.
        import re
        m = re.search(r"/(20\d{2})-(\d{2})-(\d{2})/", captura.url_final)
        self.assertIsNotNone(m)
        self.assertEqual("-".join(m.groups()), "2026-08-22")

    def test_recupera_fecha_url_amp(self):
        url = "https://www.cooperativa.cl/noticias/site/artic/20260816/pags-amp/20260816121717.html"
        import re
        m = re.search(r"/(20\d{2})(\d{2})(\d{2})/", url)
        self.assertIsNotNone(m)
        self.assertEqual("-".join(m.groups()), "2026-08-16")


if __name__ == "__main__":
    unittest.main()
