# Governance

## Primary rule

The unit of analysis is the **claim**, not the contributor.

Contributors are source nodes. Claims require receipts. Evidence determines status. Protocol admission is separate from evidence status.

## Object model

```text
Contributor → Source → Quote/Receipt → Claim → Evidence → Risk → Protocol Decision
```

## Non-negotiable distinctions

```text
Contributor ≠ claim
Claim ≠ evidence
Evidence status ≠ protocol permission
Popularity ≠ truth
Anecdote ≠ generalizable outcome
Mechanism ≠ clinical result
Biomarker ≠ hard outcome
Keto ≠ strict carnivore ≠ animal-based ≠ low-carb
```

## Extraction rules

Every extracted claim must be:

1. Attributable.
2. Atomic.
3. Timestamped where video/audio.
4. Separated from the contributor's broader worldview.
5. Separated from host framing.
6. Separated from thumbnail/title unless the contributor controls it.
7. Stored with quote and normalized claim separately.
8. Risk-classified before evidence review.
9. Deduplicated against existing claims.
10. Marked as unreviewed until evidence review occurs.

## Do not strengthen claims

Do not infer a stronger claim than the source makes.

Example:

```text
Source says: "I felt better without plants."
Incorrect normalization: "Plants cause disease."
Correct normalization: "The contributor reports subjective improvement after removing plant foods."
```

## Claim deduplication levels

```text
D0_exact_duplicate
D1_same_claim_same_contributor_different_source
D2_same_claim_different_contributor
D3_same_family_materially_different_claim
D4_related_but_distinct_claim
```

## Red-team requirement

High-risk claims require red-team review before protocol admission or public-safe wording.

Automatic red-team triggers include:

```text
cure
reverse
cause
toxic
poison
essential
never
always
harmless
safe for everyone
cancer
statin
insulin
chemotherapy
pregnancy
children
kidney disease
LDL
ApoB
autoimmune
bipolar
schizophrenia
medication
deprescribing
```
