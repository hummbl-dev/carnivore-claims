# Carnivore Claims Ledger

The Carnivore Claims Ledger is a provenance-aware claim-evaluation system for carnivore, ketogenic, low-carbohydrate, animal-based, ancestral-health, metabolic-health, and relevant counterclaims.

## Canonical question

> Which carnivore claims are true, for whom, under what conditions, with what risks, and with what level of evidence?

This question is the constitutional frame for the project.

## Core principle

The unit of analysis is the **claim**, not the contributor.

Contributors are source nodes. Claims require receipts. Evidence determines status. Protocol admission is separate from truth status.

## Object model

```text
Contributor → Source → Quote/Receipt → Claim → Evidence → Risk → Protocol Decision
```

## Repository role

This is the **public documentation and projection surface** for the Carnivore Claims Ledger. It is not a private workbench.

The repository contract is:

- `ccl-workbench-private` → `carnivore-claims-ledger` → `carnivore-claims`
- **`ccl-workbench-private`**: raw discovery, evidence and counterevidence, unresolved claims, private review, rights assessment, protocol analysis.
- **`carnivore-claims-ledger`**: reviewed, public-bound clean claim records and promotion receipts; private until v1.
- **`carnivore-claims`** (this repo): public methodology, schemas, corrections, and generated approved projections only.

### Exclusions

Raw ingestion, private-workbench material, and unreviewed claims do not belong in this repository. Raw research belongs in `ccl-workbench-private`.

### Public claim requirements

Public claims require provenance, evidence distance, risk, uncertainty, rights status, and promotion receipts. Truth evaluation, public publication, and protocol admission remain separate decisions.

Not medical advice.

## Safety

This project does not recommend stopping medication, delaying medical care, replacing cancer treatment, or applying restrictive diets to high-risk populations without clinician supervision.

High-risk claims must be clearly marked, reviewed, red-teamed, and converted into public-safe wording before any future public release or protocol use.

## Durable operating principle

> Every claim gets a receipt. Every receipt gets provenance. Every claim gets risk. Every risky claim gets red-team review. Every public claim gets safer wording. Every protocol claim gets admission gates.
