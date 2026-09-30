import unittest
from pathlib import Path
from src.pipeline import PipelineLaboratorio

ROOT=Path(__file__).resolve().parents[1]

class TestTrazabilidadCorpus(unittest.TestCase):
    def test_corpus_semilla_tiene_entregables_versionados(self):
        p=PipelineLaboratorio(ROOT)
        noticias=p.leer_urls()
        self.assertGreaterEqual(len(noticias),10)
        for n in noticias:
            self.assertTrue((ROOT/"data/processed"/f"{n.id_noticia}.txt").exists(), n.id_noticia)
            self.assertTrue((ROOT/"data/json"/f"{n.id_noticia}.json").exists(), n.id_noticia)
            self.assertTrue((ROOT/"data/validation"/f"{n.id_noticia}.validation.json").exists(), n.id_noticia)

    def test_raw_y_meta_cuando_se_restaura_evidencia(self):
        if not list((ROOT / "data/raw").glob("N*.html")):
            self.skipTest("RAW conservado como artifact; restaurarlo para verificar captura histórica")
        for n in PipelineLaboratorio(ROOT).leer_urls():
            self.assertTrue((ROOT/"data/raw"/f"{n.id_noticia}.html").exists(), n.id_noticia)
            self.assertTrue((ROOT/"data/raw"/f"{n.id_noticia}.meta.json").exists(), n.id_noticia)
