"""Extracción estructurada con Gemini y salida JSON controlada."""
from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.modelos import NoticiaEstructurada, NoticiaFuente

LOGGER = logging.getLogger(__name__)


class ExtractorLLM:
    def construir_prompt(self, noticia: NoticiaFuente) -> str:
        ...

    def extraer(self, noticia: NoticiaFuente) -> dict[str, Any]:
        ...


class ExtractorGemini(ExtractorLLM):
    """Extractor con Gemini, esquema estructurado y validación Pydantic posterior."""

    # Por defecto se priorizan modelos con nivel gratuito y salida estructurada.
    # Gemini 3.5 Flash-Lite está optimizado para procesamiento simple/de alto volumen,
    # que corresponde mejor a esta extracción académica de noticias.
    MODELOS_PREFERIDOS = (
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
    )

    def __init__(
        self,
        salida_dir: Path,
        raw_dir: Path | None = None,
        model: str | None = None,
        max_reintentos: int = 2,
    ) -> None:
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.salida_dir = Path(salida_dir)
        self.raw_dir = Path(raw_dir) if raw_dir else self.salida_dir.parent / "llm_raw"
        self.salida_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.model_solicitado = model or os.getenv("GEMINI_MODEL")
        self.max_reintentos = max_reintentos
        self._client = None
        self._model = None

    def verificar_disponibilidad(self) -> str:
        """Comprueba credencial, SDK y un modelo compatible antes de procesar el lote."""
        self._crear_cliente()
        return self._resolver_modelo()

    def _crear_cliente(self):
        if not self.api_key:
            raise RuntimeError(
                "No existe GEMINI_API_KEY/GOOGLE_API_KEY. Cree un archivo .env local a partir de "
                ".env.example y agregue GEMINI_API_KEY=...; .env está excluido de Git."
            )
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError(
                "No está instalado google-genai. Cree/active el entorno Conda desde environment.yml."
            ) from exc
        if self._client is None:
            # Evita que una cuota/modelo no disponible bloquee el pipeline durante
            # varios minutos. El extractor ya aplica reintentos controlados a nivel
            # de noticia.
            http_options = types.HttpOptions(
                timeout=60_000,
                retry_options=types.HttpRetryOptions(attempts=1),
            )
            self._client = genai.Client(api_key=self.api_key, http_options=http_options)
        return self._client

    @staticmethod
    def _normalizar_nombre_modelo(nombre: str) -> str:
        return nombre.split("/")[-1].strip()

    def _resolver_modelo(self) -> str:
        if self._model:
            return self._model
        if self.model_solicitado:
            self._model = self._normalizar_nombre_modelo(self.model_solicitado)
            return self._model

        client = self._crear_cliente()
        disponibles: set[str] = set()
        try:
            for modelo in client.models.list():
                nombre = getattr(modelo, "name", None)
                if nombre:
                    disponibles.add(self._normalizar_nombre_modelo(str(nombre)))
        except Exception as exc:  # listar modelos no debe impedir un intento con modelo actual
            LOGGER.warning("No fue posible listar modelos Gemini: %s", exc)

        for candidato in self.MODELOS_PREFERIDOS:
            if not disponibles or candidato in disponibles:
                self._model = candidato
                return candidato
        raise RuntimeError(
            "No se encontró un modelo Gemini compatible con salida estructurada. "
            f"Modelos visibles: {sorted(disponibles)[:20]}"
        )

    def construir_prompt(self, noticia: NoticiaFuente) -> str:
        if not noticia.texto:
            raise ValueError(f"{noticia.id_noticia} no tiene texto procesado")
        return f"""Analiza la siguiente noticia delictual con criterio estrictamente extractivo.

REGLAS OBLIGATORIAS:
- Extrae SOLAMENTE información explícita del texto. No completes por conocimiento externo.
- No infieras culpabilidad, identidad, parentesco, intención ni relaciones no declaradas.
- Conserva exactamente el rol indicado por la fuente. Detenido, imputado, acusado, condenado, víctima y testigo NO son equivalentes.
- Si un dato escalar no aparece, usa null. Si una colección no tiene elementos respaldados, usa [].
- Las relaciones deben estar explícitamente respaldadas por el texto y usar un tipo breve en MAYÚSCULAS_CON_GUIONES_BAJOS.
- No crees una persona u organización solo porque pueda deducirse del contexto.
- Incluye también referencias grupales explícitas cuando sean actores centrales del hecho (por ejemplo, "cinco gendarmes" o "dos hombres detenidos"), aunque no tengan nombre propio.
- Evita duplicar una misma entidad por correferencias obvias dentro de la noticia (por ejemplo, "un hombre", "el sujeto" y "el imputado" cuando el texto deja claro que son la misma persona). Conserva la denominación explícita más informativa.
- Para objetos conserva tipo, nombre, cantidad y unidad solo cuando existan explícitamente. Una valoración monetaria de bienes o drogas NO debe convertirse en un objeto "dinero" si no se incautó dinero efectivo.
- Si una relación usa expresiones de incertidumbre de la fuente (presunto, habría, se investiga, sindicado), conserva esa incertidumbre en el tipo de relación; no conviertas una atribución provisional en un hecho definitivo.
- Todo origen y destino de una relación debe corresponder EXACTAMENTE al texto de una entidad, delito, lugar u objeto ya incluido en el mismo JSON. No expandas ni reformules el nombre dentro de relaciones.
- No registres como persona a colectivos institucionales como "detectives", "personal policial", "Carabineros" o "funcionarios" cuando el texto los presenta actuando como institución; usa organizaciones. Nunca asignes a policías/detectives el rol de detenido por confundir el verbo "detuvieron".
- La cantidad de un objeto describe cuántos objetos o cuánto de esa sustancia se menciona. No uses como cantidad el número de heridas, estocadas, usos o eventos relacionados con el objeto.
- No separes un delito compuesto en otro delito adicional por coincidencia léxica: "homicidio frustrado" no implica además "homicidio" si la fuente no menciona ambos por separado.
- Cuando una expresión sea solo una valorización ("más de un millón de pesos en jarabes"), no crees una entidad dinero salvo que el texto diga que se incautó dinero efectivo.
- El resumen debe describir el hecho sin añadir conclusiones ni culpabilidad.
- Devuelve únicamente la estructura JSON solicitada por el esquema de salida de la API; no agregues explicaciones.

METADATOS DE TRAZABILIDAD (deben conservarse):
id_noticia: {noticia.id_noticia}
fuente: {noticia.fuente}
url: {noticia.url}

TEXTO PROCESADO:
{noticia.texto}
"""

    @staticmethod
    def _extraer_json_de_texto(texto: str) -> dict[str, Any]:
        texto = texto.strip()
        texto = re.sub(r"^```(?:json)?\s*", "", texto, flags=re.IGNORECASE)
        texto = re.sub(r"\s*```$", "", texto)
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            inicio = texto.find("{")
            if inicio < 0:
                raise
            profundidad = 0
            en_cadena = False
            escape = False
            for i in range(inicio, len(texto)):
                c = texto[i]
                if en_cadena:
                    if escape:
                        escape = False
                    elif c == "\\":
                        escape = True
                    elif c == '"':
                        en_cadena = False
                    continue
                if c == '"':
                    en_cadena = True
                elif c == "{":
                    profundidad += 1
                elif c == "}":
                    profundidad -= 1
                    if profundidad == 0:
                        return json.loads(texto[inicio : i + 1])
            raise json.JSONDecodeError("No se encontró objeto JSON completo", texto, inicio)

    def _llamar_interactions(self, client, model: str, prompt: str) -> str:
        interaction = client.interactions.create(
            model=model,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": NoticiaEstructurada.model_json_schema(),
            },
        )
        salida = getattr(interaction, "output_text", None)
        if not salida:
            raise RuntimeError("Gemini Interactions API no devolvió output_text")
        return str(salida)

    def _llamar_generate_content(self, client, model: str, prompt: str) -> str:
        # Fallback compatible con versiones del SDK que aún exponen GenerateContent.
        try:
            from google.genai import types

            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=NoticiaEstructurada,
                temperature=0,
            )
        except Exception:
            config = {
                "response_mime_type": "application/json",
                "response_json_schema": NoticiaEstructurada.model_json_schema(),
                "temperature": 0,
            }
        response = client.models.generate_content(model=model, contents=prompt, config=config)
        salida = getattr(response, "text", None)
        if not salida:
            parsed = getattr(response, "parsed", None)
            if parsed is not None:
                if hasattr(parsed, "model_dump"):
                    return json.dumps(parsed.model_dump(), ensure_ascii=False)
                return json.dumps(parsed, ensure_ascii=False)
            raise RuntimeError("Gemini GenerateContent no devolvió texto ni objeto parseado")
        return str(salida)

    def _llamar(self, prompt: str) -> tuple[str, str]:
        client = self._crear_cliente()
        model = self._resolver_modelo()
        errores: list[str] = []
        # La documentación vigente recomienda Interactions; se conserva fallback para instalaciones previas.
        if hasattr(client, "interactions") and hasattr(client.interactions, "create"):
            try:
                return self._llamar_interactions(client, model, prompt), model
            except Exception as exc:
                errores.append(f"interactions={type(exc).__name__}: {exc}")
                LOGGER.warning("Interactions falló; se prueba GenerateContent: %s", exc)
        try:
            return self._llamar_generate_content(client, model, prompt), model
        except Exception as exc:
            errores.append(f"generate_content={type(exc).__name__}: {exc}")
            raise RuntimeError("; ".join(errores)) from exc

    def extraer(self, noticia: NoticiaFuente) -> dict[str, Any]:
        prompt = self.construir_prompt(noticia)
        ultimo_error: Exception | None = None
        for intento in range(self.max_reintentos + 1):
            try:
                texto_respuesta, model = self._llamar(prompt)
                (self.raw_dir / f"{noticia.id_noticia}.txt").write_text(texto_respuesta, encoding="utf-8")
                data = self._extraer_json_de_texto(texto_respuesta)

                # La trazabilidad no se delega al LLM: estos metadatos provienen del CSV/origen.
                data["id_noticia"] = noticia.id_noticia
                data["fuente"] = noticia.fuente
                data["url"] = noticia.url
                if not data.get("titulo") and noticia.titulo:
                    data["titulo"] = noticia.titulo
                if not data.get("fecha_publicacion") and noticia.fecha_publicacion:
                    data["fecha_publicacion"] = noticia.fecha_publicacion

                validado = NoticiaEstructurada.model_validate(data)
                salida = validado.model_dump(mode="json")
                ruta = self.salida_dir / f"{noticia.id_noticia}.json"
                ruta.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
                LOGGER.info("%s extraída con %s", noticia.id_noticia, model)
                return salida
            except Exception as exc:
                ultimo_error = exc
                LOGGER.error(
                    "Gemini falló id=%s intento=%d/%d: %s",
                    noticia.id_noticia,
                    intento + 1,
                    self.max_reintentos + 1,
                    exc,
                )
                if intento < self.max_reintentos:
                    time.sleep(2**intento)
        assert ultimo_error is not None
        raise ultimo_error
