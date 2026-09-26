import unittest
from pathlib import Path
from src.pipeline import PipelineLaboratorio

ROOT=Path(__file__).resolve().parents[1]

class TestTrazabilidadCorpus(unittest.TestCase):
    def test_corpus_semilla_tiene_raw_meta_y_processed(self):
        p=PipelineLaboratorio(ROOT)
        noticias=p.leer_urls()
        self.assertGreaterEqual(len(noticias),10)
        for n in noticias:
            self.assertTrue((ROOT/"data/raw"/f"{n.id_noticia}.html").exists(), n.id_noticia)
            self.assertTrue((ROOT/"data/raw"/f"{n.id_noticia}.meta.json").exists(), n.id_noticia)
            self.assertTrue((ROOT/"data/processed"/f"{n.id_noticia}.txt").exists(), n.id_noticia)
