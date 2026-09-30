import unittest
from src.limpieza import LimpiadorHTML


class TestLimpiadorHTML(unittest.TestCase):
    def test_conserva_fragmentos_inline_y_calificadores(self):
        html = '<article><p>El imputado <strong>habría</strong> agredido a la víctima en el <a>Hospital San Pablo</a>, según la investigación.</p></article>'
        cuerpo = LimpiadorHTML().limpiar(html)
        self.assertIn("habría agredido", cuerpo)
        self.assertIn("Hospital San Pablo", cuerpo)

    def test_elimina_ruido_y_conserva_cuerpo(self):
        html = '''<html><body><nav>Menú de navegación que no debe sobrevivir a la limpieza.</nav>
        <article><h1>Título de prueba</h1>
        <p>Este párrafo contiene información relevante de la noticia y debe conservarse completamente.</p>
        <p>Este párrafo contiene información relevante de la noticia y debe conservarse completamente.</p>
        <script>var secreto = 'ruido';</script></article><footer>Pie muy largo que tampoco debe estar.</footer></body></html>'''
        resultado = LimpiadorHTML().limpiar_documento(html)
        self.assertIn("información relevante", resultado.cuerpo)
        self.assertEqual(resultado.cuerpo.count("información relevante"), 1)
        self.assertNotIn("secreto", resultado.cuerpo)
        self.assertNotIn("navegación", resultado.cuerpo)

    def test_elimina_tarjeta_lee_tambien(self):
        html = '''<html><body><article>
        <h1>Titular principal suficientemente largo</h1>
        <p>Párrafo principal del hecho con información relevante y suficientemente extensa para conservarse.</p>
        <p>Lee también...</p>
        <p>Noticia ajena sobre un homicidio de hincha de fútbol en otra causa.</p>
        <p>Jueves 19 Marzo, 2026 | 12:08</p>
        <p>Continuación del artículo principal con otra oración suficientemente extensa para conservarse.</p>
        </article></body></html>'''
        resultado = LimpiadorHTML().limpiar_documento(html)
        self.assertIn("Párrafo principal", resultado.cuerpo)
        self.assertIn("Continuación del artículo", resultado.cuerpo)
        self.assertNotIn("hincha de fútbol", resultado.cuerpo)


if __name__ == "__main__":
    unittest.main()
