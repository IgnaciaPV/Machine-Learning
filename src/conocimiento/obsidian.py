"""Generación automática de una bóveda Obsidian navegable."""
from __future__ import annotations

import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from .utilidades import clave_entidad, normalizar_visual, slugify


class EscritorObsidian:
    def escribir_noticia(self, data: dict[str, Any]) -> Path:
        ...

    def escribir_entidades(self, noticias: list[dict[str, Any]]) -> None:
        ...

    def escribir_vault(self, noticias: list[dict[str, Any]]) -> None:
        ...


class EscritorVaultObsidian(EscritorObsidian):
    CARPETAS = {
        "delitos": "Delitos",
        "personas": "Personas",
        "organizaciones": "Organizaciones",
        "lugares": "Lugares",
        "objetos": "Objetos",
    }

    def __init__(self, vault_dir: Path) -> None:
        self.vault_dir = Path(vault_dir)
        self._registro: dict[str, dict[str, tuple[str, str]]] = {}
        self._relaciones_por_noticia: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
        self._personas_repetidas: set[str] = set()

    def _preparar(self, limpiar: bool = False) -> None:
        if limpiar and self.vault_dir.exists():
            shutil.rmtree(self.vault_dir)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        for carpeta in ["Noticias", *self.CARPETAS.values(), "Relaciones"]:
            (self.vault_dir / carpeta).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _valor_objeto(obj: dict[str, Any]) -> str:
        return normalizar_visual(obj.get("nombre") or obj.get("tipo") or "Objeto sin nombre")

    def _construir_registro(self, noticias: list[dict[str, Any]]) -> None:
        self._registro = {tipo: {} for tipo in self.CARPETAS}
        apariciones: dict[str, set[str]] = defaultdict(set)
        for data in noticias:
            for persona in data.get("personas", []):
                if isinstance(persona, dict) and persona.get("nombre"):
                    apariciones[clave_entidad(persona["nombre"])].add(str(data["id_noticia"]))
        # Una etiqueta repetida no prueba identidad entre documentos.
        self._personas_repetidas = {k for k, ids in apariciones.items() if len(ids) > 1}
        for data in noticias:
            for delito in data.get("delitos", []):
                self._registrar("delitos", str(delito))
            for persona in data.get("personas", []):
                if isinstance(persona, dict) and persona.get("nombre"):
                    self._registrar("personas", str(persona["nombre"]), str(data["id_noticia"]))
            for org in data.get("organizaciones", []):
                self._registrar("organizaciones", str(org))
            for lugar in data.get("lugares", []):
                self._registrar("lugares", str(lugar))
            for obj in data.get("objetos", []):
                if isinstance(obj, dict):
                    self._registrar("objetos", self._valor_objeto(obj))

    def _clave_registro(self, tipo: str, valor: str, nid: str | None = None) -> str:
        clave = clave_entidad(valor)
        if tipo == "personas" and clave in self._personas_repetidas:
            if nid is None:
                raise ValueError("Una referencia de persona repetida requiere id_noticia")
            return f"{clave}::{nid}"
        return clave

    def _registrar(self, tipo: str, valor: str, nid: str | None = None) -> tuple[str, str]:
        valor = normalizar_visual(valor)
        clave = self._clave_registro(tipo, valor, nid)
        if not clave:
            clave = "sin_nombre"
        existente = self._registro.setdefault(tipo, {}).get(clave)
        if existente:
            return existente
        carpeta = self.CARPETAS[tipo]
        slug = slugify(valor)
        if tipo == "personas" and clave_entidad(valor) in self._personas_repetidas:
            slug = f"{nid}_{slug}"
        ruta = f"{carpeta}/{slug}"
        self._registro[tipo][clave] = (valor, ruta)
        return valor, ruta

    def _enlace(self, tipo: str, valor: str, nid: str | None = None) -> str:
        valor = normalizar_visual(valor)
        registro = self._registro.get(tipo, {}).get(self._clave_registro(tipo, valor, nid))
        if not registro:
            registro = self._registrar(tipo, valor, nid)
        display, ruta = registro
        return f"[[{ruta}|{display}]]"

    def _buscar_tipo_endpoint(self, valor: str, nid: str | None = None) -> str | None:
        for tipo in ("personas", "organizaciones", "delitos", "lugares", "objetos"):
            if self._clave_registro(tipo, valor, nid) in self._registro.get(tipo, {}):
                return tipo
        return None

    def _enlace_endpoint(self, valor: str, nid: str | None = None) -> str:
        tipo = self._buscar_tipo_endpoint(valor, nid)
        if tipo:
            return self._enlace(tipo, valor, nid)
        return normalizar_visual(valor)

    def escribir_noticia(self, data: dict[str, Any]) -> Path:
        nid = str(data["id_noticia"])
        ruta = self.vault_dir / "Noticias" / f"{nid}.md"
        lineas = [
            "---",
            f"id: {json.dumps(nid, ensure_ascii=False)}",
            f"fecha_publicacion: {json.dumps(data.get('fecha_publicacion'), ensure_ascii=False)}",
            f"fuente: {json.dumps(data.get('fuente'), ensure_ascii=False)}",
            f"url: {json.dumps(data.get('url'), ensure_ascii=False)}",
            "---",
            "",
            f"# {data.get('titulo') or nid}",
            "",
            "## Resumen",
            str(data.get("resumen") or "Sin resumen disponible."),
            "",
            "## Delitos",
        ]
        lineas.extend([f"- {self._enlace('delitos', x)}" for x in data.get("delitos", [])] or ["- Sin datos explícitos."])
        lineas += ["", "## Personas"]
        personas = []
        for p in data.get("personas", []):
            nombre = str(p.get("nombre", "")).strip()
            if not nombre:
                continue
            rol = p.get("rol")
            texto = f"- {self._enlace('personas', nombre, nid)}"
            if rol:
                texto += f" — rol: {rol}"
            personas.append(texto)
        lineas.extend(personas or ["- Sin datos explícitos."])

        lineas += ["", "## Organizaciones"]
        lineas.extend([f"- {self._enlace('organizaciones', x)}" for x in data.get("organizaciones", [])] or ["- Sin datos explícitos."])
        lineas += ["", "## Lugares"]
        lineas.extend([f"- {self._enlace('lugares', x)}" for x in data.get("lugares", [])] or ["- Sin datos explícitos."])
        lineas += ["", "## Objetos"]
        objetos = []
        for obj in data.get("objetos", []):
            nombre = self._valor_objeto(obj)
            detalle = []
            if obj.get("cantidad") is not None:
                detalle.append(str(obj["cantidad"]))
            if obj.get("unidad"):
                detalle.append(str(obj["unidad"]))
            sufijo = f" — {' '.join(detalle)}" if detalle else ""
            objetos.append(f"- {self._enlace('objetos', nombre)}{sufijo}")
        lineas.extend(objetos or ["- Sin datos explícitos."])

        lineas += ["", "## Relaciones"]
        relaciones = self._relaciones_por_noticia.get(nid, [])
        if relaciones:
            for rid, rel in relaciones:
                label = f"{rel['origen']} — {rel['tipo']} → {rel['destino']}"
                lineas.append(f"- [[Relaciones/{rid}|{label}]]")
        else:
            lineas.append("- Sin relaciones explícitas extraídas.")

        lineas += ["", "## Fuente original", f"- [{data.get('fuente')}]({data.get('url')})", ""]
        ruta.write_text("\n".join(lineas), encoding="utf-8")
        return ruta

    def _escribir_relaciones(self, noticias: list[dict[str, Any]]) -> None:
        self._relaciones_por_noticia = defaultdict(list)
        for data in noticias:
            nid = str(data["id_noticia"])
            for idx, rel in enumerate(data.get("relaciones", []), start=1):
                rid = f"{nid}_R{idx:03d}"
                self._relaciones_por_noticia[nid].append((rid, rel))
                ruta = self.vault_dir / "Relaciones" / f"{rid}.md"
                origen = str(rel.get("origen", ""))
                destino = str(rel.get("destino", ""))
                tipo = str(rel.get("tipo", ""))
                contenido = [
                    f"# {rid}: {tipo}",
                    "",
                    "Tipo: Relación explícita extraída de una noticia.",
                    "",
                    f"- Origen: {self._enlace_endpoint(origen, nid)}",
                    f"- Tipo: `{tipo}`",
                    f"- Destino: {self._enlace_endpoint(destino, nid)}",
                    f"- Evidencia documental: [[Noticias/{nid}|{nid}]]",
                    "",
                    "La relación conserva el carácter descriptivo de la fuente y no implica culpabilidad.",
                ]
                ruta.write_text("\n".join(contenido), encoding="utf-8")

    def escribir_entidades(self, noticias: list[dict[str, Any]]) -> None:
        indices: dict[str, dict[str, dict[str, Any]]] = {
            tipo: defaultdict(lambda: {"noticias": set(), "roles": set(), "detalles": []})
            for tipo in self.CARPETAS
        }
        for data in noticias:
            nid = str(data["id_noticia"])
            for delito in data.get("delitos", []):
                indices["delitos"][clave_entidad(str(delito))]["noticias"].add(nid)
            for p in data.get("personas", []):
                if not isinstance(p, dict) or not p.get("nombre"):
                    continue
                item = indices["personas"][self._clave_registro("personas", str(p["nombre"]), nid)]
                item["noticias"].add(nid)
                if p.get("rol"):
                    item["roles"].add(str(p["rol"]))
            for org in data.get("organizaciones", []):
                indices["organizaciones"][clave_entidad(str(org))]["noticias"].add(nid)
            for lugar in data.get("lugares", []):
                indices["lugares"][clave_entidad(str(lugar))]["noticias"].add(nid)
            for obj in data.get("objetos", []):
                if not isinstance(obj, dict):
                    continue
                valor = self._valor_objeto(obj)
                item = indices["objetos"][clave_entidad(valor)]
                item["noticias"].add(nid)
                detalle = " ".join(str(x) for x in (obj.get("cantidad"), obj.get("unidad")) if x not in (None, ""))
                if detalle:
                    item["detalles"].append(f"{nid}: {detalle}")

        for tipo, carpeta in self.CARPETAS.items():
            for clave, (display, ruta_rel) in sorted(self._registro.get(tipo, {}).items(), key=lambda x: x[1][0].casefold()):
                item = indices[tipo].get(clave, {"noticias": set(), "roles": set(), "detalles": []})
                lineas = [f"# {display}", "", f"Tipo: {carpeta[:-1] if carpeta.endswith('s') else carpeta}", "", "## Noticias relacionadas"]
                if tipo == "personas" and "::" in clave:
                    lineas[4:4] = ["Referencia limitada a esta noticia. La coincidencia de palabras con otra nota no demuestra que sea la misma persona.", ""]
                lineas.extend([f"- [[Noticias/{nid}|{nid}]]" for nid in sorted(item["noticias"])])
                if item.get("roles"):
                    lineas += ["", "## Roles explícitos observados"]
                    lineas.extend([f"- {rol}" for rol in sorted(item["roles"])])
                if item.get("detalles"):
                    lineas += ["", "## Cantidades explícitas observadas"]
                    lineas.extend([f"- {d}" for d in item["detalles"]])
                (self.vault_dir / f"{ruta_rel}.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def _escribir_indice(self, noticias: list[dict[str, Any]]) -> None:
        lineas = [
            "# Laboratorio 01 — Grafo de conocimiento de noticias delictuales",
            "",
            "Bóveda generada automáticamente desde JSON validados. El análisis es académico y exploratorio; una mención, detención o imputación no equivale a culpabilidad.",
            "",
            "## Noticias",
        ]
        for data in sorted(noticias, key=lambda x: str(x.get("id_noticia"))):
            lineas.append(f"- [[Noticias/{data['id_noticia']}|{data['id_noticia']} — {data.get('titulo') or 'Sin título'}]]")
        lineas += ["", "## Índices de entidades"]
        for tipo, carpeta in self.CARPETAS.items():
            lineas.append(f"### {carpeta}")
            for _, (display, ruta) in sorted(self._registro.get(tipo, {}).items(), key=lambda x: x[1][0].casefold()):
                lineas.append(f"- [[{ruta}|{display}]]")
            lineas.append("")
        lineas += ["## Relaciones explícitas"]
        for nid in sorted(self._relaciones_por_noticia):
            for rid, rel in self._relaciones_por_noticia[nid]:
                lineas.append(f"- [[Relaciones/{rid}|{rid}: {rel['origen']} — {rel['tipo']} → {rel['destino']}]]")
        (self.vault_dir / "00_Indice.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def escribir_vault(self, noticias: list[dict[str, Any]]) -> None:
        self._preparar(limpiar=True)
        self._construir_registro(noticias)
        self._escribir_relaciones(noticias)
        for data in noticias:
            self.escribir_noticia(data)
        self.escribir_entidades(noticias)
        self._escribir_indice(noticias)

    def auditar_enlaces(self) -> list[str]:
        """Comprueba que los wikilinks con ruta apunten a un .md existente."""
        import re

        rotos: list[str] = []
        patron = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
        for md in self.vault_dir.rglob("*.md"):
            texto = md.read_text(encoding="utf-8")
            for destino in patron.findall(texto):
                destino = destino.strip()
                candidato = self.vault_dir / f"{destino}.md"
                if not candidato.exists():
                    rotos.append(f"{md.relative_to(self.vault_dir)} -> {destino}")
        return sorted(set(rotos))
