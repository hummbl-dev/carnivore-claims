# Contributor Notes (Internal)

## Required fields

- `contributors.csv`: `contributor_id`, `display_name`, `type`, `status`
- `sources.csv`: `source_id`, `source_type`, `title`, `url`, `contributors`
- `claims.csv`: `claim_id`, `claim_family`, `normalized_claim`, `risk_class`,
  `evidence_status`, `protocol_status`
- `claim_sources.csv`: `claim_source_id`, `claim_id`, `contributor_id`, `source_id`

## Suggested workflow

1. Add/Update source metadata.
2. Add receipts first in `claim_sources.csv`.
3. Add normalized claim in `claims.csv`.
4. Add evidence references in `evidence.csv` + `claim_evidence.csv`.
5. Add protocol decision only after evidence and review.

## Status labels to use

- `needs-receipt`, `needs-evidence`, `needs-red-team`, `public-safe`, `quarantined`.
