"""Apoyo reproducible para la auditoría humana obligatoria de 10 noticias."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AuditorManual:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.ref_path = self.root / "docs" / "referencia_auditoria_manual.json"
        self.json_dir = self.root / "data" / "json"
        self.processed_dir = self.root / "data" / "processed"
        self.raw_dir = self.root / "data" / "raw"
        self.out_path = self.root / "docs" / "auditoria_llm.md"

    @staticmethod
    def _texto_json(data: dict[str, Any]) -> str:
        partes: list[str] = []
        partes.extend(str(x) for x in data.get("delitos", []))
        partes.extend(str(x) for x in data.get("organizaciones", []))
        partes.extend(str(x) for x in data.get("lugares", []))
        for p in data.get("personas", []):
            if isinstance(p, dict):
                partes.extend(str(p.get(k, "")) for k in ("nombre", "rol"))
        for o in data.get("objetos", []):
            if isinstance(o, dict):
                partes.extend(str(o.get(k, "")) for k in ("tipo", "nombre", "cantidad", "unidad"))
        for r in data.get("relaciones", []):
            if isinstance(r, dict):
                partes.extend(str(r.get(k, "")) for k in ("origen", "tipo", "destino"))
        return " ".join(partes).casefold()

    def ejecutar(self) -> dict[str, int]:
        referencia = json.loads(self.ref_path.read_text(encoding="utf-8"))["muestras"]
        lineas = [
            "# Auditoría manual de extracción LLM",
            "",
            "La referencia fue construida revisando noticia original/snapshot y texto limpio antes de observar la salida del LLM. La tabla siguiente sirve como guía de revisión humana; las coincidencias automáticas no sustituyen la lectura comparativa.",
            "",
        ]
        completos = 0
        faltantes_json = 0
        for caso in referencia:
            nid = caso["id_noticia"]
            raw_ok = (self.raw_dir / f"{nid}.html").exists()
            clean_path = self.processed_dir / f"{nid}.txt"
            json_path = self.json_dir / f"{nid}.json"
            lineas += [f"## {nid}", ""]
            lineas.append(f"- Original/snapshot disponible: **{'sí' if raw_ok else 'no'}**")
            lineas.append(f"- Texto limpio disponible: **{'sí' if clean_path.exists() else 'no'}**")
            if not json_path.exists():
                faltantes_json += 1
                lineas.append("- JSON Gemini: **no disponible**")
                lineas.append("- Estado: pendiente de ejecutar Gemini; no se declara auditado el JSON.")
                lineas.append("")
                continue
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                bolsa = self._texto_json(data)
                completos += 1
                lineas.append("- JSON Gemini: **disponible y legible**")
                lineas.append("- Hechos que la revisión humana exige preservar:")
                for item in caso.get("hechos_clave", []):
                    lineas.append(f"  - {item}")
                lineas.append("- Riesgos de inferencia que deben comprobarse manualmente:")
                for item in caso.get("prohibido_inferir", []):
                    lineas.append(f"  - {item}")
                lineas.append("- Señales automáticas de cobertura (solo apoyo):")
                for grupo in ("delitos_esperados", "lugares_esperados", "organizaciones_esperadas", "objetos_esperados"):
                    for item in caso.get(grupo, []):
                        tokens = [t for t in item.casefold().replace("/", " ").split() if len(t) >= 4]
                        cubierto = any(t in bolsa for t in tokens) if tokens else False
                        lineas.append(f"  - {'✓' if cubierto else '△'} {grupo}: {item}")
                lineas.append("- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.")
                lineas.append("")
            except Exception as exc:
                lineas.append(f"- JSON Gemini: **inválido** ({type(exc).__name__}: {exc})")
                lineas.append("")
        self.out_path.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        return {"muestras_referencia": len(referencia), "json_disponibles": completos, "json_faltantes": faltantes_json}
