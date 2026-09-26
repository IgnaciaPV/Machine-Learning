import unittest
from src.limpieza import LimpiadorHTML


class TestLimpiadorHTML(unittest.TestCase):
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
