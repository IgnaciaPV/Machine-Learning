# Arquitectura

```text
Internet / Google News RSS
        |
        v
 data/urls.csv
        |
        v
FabricaCapturadores -> data/raw/NXXX.html + NXXX.meta.json
        |
        v
LimpiadorHTML -> data/processed/NXXX.txt
        |
        v
ExtractorGemini -> data/llm_raw + data/json/NXXX.json
        |
        v
ValidadorJSON -> data/validation/NXXX.validation.json
        |
        +------------------+
        |                  |
        v                  v
EscritorVaultObsidian   ExploradorDatos
obsidian_vault/         outputs/
```

`main.py` es el único orquestador. `src/pipeline.py` coordina componentes de responsabilidad única y evita que una falla individual detenga innecesariamente el lote.

## Decisiones POO

- `ClienteHTTP`: timeout, User-Agent, redirects y pausas.
- `CapturadorFuente` + adaptadores: encapsulan particularidades por medio.
- `FabricaCapturadores`: elige adaptador y conserva fallback genérico.
- `LimpiadorHTML`: elimina ruido con reglas conservadoras.
- `ExtractorGemini`: prompt controlado, esquema estructurado y fallback entre APIs del SDK.
- `ValidadorJSON`: no confía en el LLM; verifica sintaxis, estructura, tipos y trazabilidad.
- `EscritorVaultObsidian`: persiste conocimiento como Markdown enlazado.
- `ExploradorDatos`: Data Understanding y visualizaciones reproducibles.
