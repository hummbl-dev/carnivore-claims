# Governance

This repo is a claim-ledger workbench for healthy-claims handling.

## Scope

- Raw source discovery and extraction
- Receipt-attached claim normalization
- Evidence and protocol labeling
- Red-team review routing for high-risk claims
- Public-safe export prep

## Object model

`Contributor -> Source -> ClaimSource -> Claim -> Evidence -> ProtocolDecision`

## Non-negotiables

1. Contributors are not canon.
2. Claims are not evidence.
3. Evidence status does not imply protocol permission.
4. Anecdote is not generalizable outcome.
5. High-risk claims need red-team review.

## Red-team routing

Claims with medical directive language, cancer/cardiometabolic direct-claims, or absolute
health claims are routed to `reviews/red-team/` with `status` labels and `needs-red-team`.
