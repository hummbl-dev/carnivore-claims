# Carnivore Claims Ledger — Public Export

This directory is the public-facing output boundary for the private workbench.

- `README_PUBLIC.md`: user-facing summary
- `README.md`: repo metadata for the release artifacts
- `export_config.yaml`: export controls
- `exports/`: generated public-safe CSVs consumed by downstream agents and API clients
- `claims.json`: curated public claim payload
- `evidence.json`: curated public evidence payload
- `public_api_schema.json`: export schema contract

Generate/update the export artifacts with:

```bash
python scripts/export_public.py
python scripts/validate_public_release.py
```
