#!/usr/bin/env python3
"""Orquestador oficial del Laboratorio 01: noticias, Gemini y Obsidian."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from src.pipeline import PipelineLaboratorio
from src.auditoria_manual import AuditorManual

ROOT = Path(__file__).resolve().parent


def configurar_logging(verbose: bool = False) -> None:
    log_dir = ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    nivel = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "pipeline.log", encoding="utf-8"),
        ],
    )


def parser_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Laboratorio 01 — noticias delictuales, Gemini y Obsidian")
    parser.add_argument("--verbose", action="store_true", help="Activa logging detallado")
    sub = parser.add_subparsers(dest="comando", required=True)

    sub.add_parser("descubrir", help="Google News RSS -> data/urls.csv")
    p_cap = sub.add_parser("capturar", help="URLs -> data/raw + data/processed")
    p_cap.add_argument("--forzar", action="store_true", help="Ignora cache RAW y recaptura")
    p_ext = sub.add_parser("extraer", help="Texto -> Gemini -> JSON validado")
    p_ext.add_argument("--forzar", action="store_true", help="Reextrae incluso JSON válidos existentes")
    sub.add_parser("obsidian", help="JSON válidos -> vault Markdown enlazado")
    sub.add_parser("analizar", help="Data Understanding + visualizaciones")
    sub.add_parser("auditar", help="Genera guía de auditoría manual original -> limpio -> JSON")
    p_pipe = sub.add_parser("pipeline", help="Ejecuta la secuencia completa")
    p_pipe.add_argument("--sin-descubrir", action="store_true", help="Usa solo el corpus congelado de data/urls.csv")
    p_pipe.add_argument("--forzar", action="store_true", help="Recaptura/reextrae")
    return parser


def main() -> int:
    args = parser_cli().parse_args()
    configurar_logging(args.verbose)
    pipeline = PipelineLaboratorio(ROOT)
    try:
        if args.comando == "descubrir":
            resultado = pipeline.descubrir()
        elif args.comando == "capturar":
            resultado = pipeline.capturar(forzar=args.forzar).to_dict()
        elif args.comando == "extraer":
            resultado = pipeline.extraer(forzar=args.forzar).to_dict()
        elif args.comando == "obsidian":
            resultado = pipeline.obsidian()
        elif args.comando == "analizar":
            resultado = pipeline.analizar()
        elif args.comando == "auditar":
            resultado = AuditorManual(ROOT).ejecutar()
        elif args.comando == "pipeline":
            resultado = pipeline.pipeline(
                incluir_descubrimiento=not args.sin_descubrir,
                forzar=args.forzar,
            )
        else:
            raise AssertionError("Comando no manejado")
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        logging.getLogger(__name__).exception("La ejecución terminó con error")
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
