# Carnivore Claims Ledger

This repository is a private HUMMBL working surface for claim-level evidence work on
carnivore, ketogenic, low-carb, animal-based, and adjacent health claims.

**Canonical question**

Which carnivore claims are true, for whom, under what conditions, with what risks,
and with what level of evidence?

## Principles

- Primary object is the **claim**, not the contributor.
- Every claim requires a **receipt** (source quote + attribution).
- Evidence status and protocol-admission status are intentionally separate.
- Unsafe clinical directives are quarantined, not deleted.
- Public-facing claims must use HUMMBL-safe wording and include risk framing.

## Repository surface

- `schema/` object definitions (JSON)
- `data/` CSV and YAML ledgers
- `contributors/`, `sources/`, `claim_families/`, `institutions/`, `reviews/`
- `ingestion/` raw processing queues and drafts
- `public_release/` generated public-safe artifacts
- `.github/` issue templates and CI workflow

This repo is private. Public-facing releases are generated from reviewed artifacts and
should not include raw transcripts, long copyrighted material, or private notes.

## Current status

Minimal scaffold. Populate data pipelines and templates first, then begin ingestion of
high-confidence source evidence.
