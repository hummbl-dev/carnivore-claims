# Release Criteria

- Private artifacts contain no raw transcripts in public exports.
- Every claim has:
  - `claim_id`
  - receipt (`source_id`, `contributor_id`, quote provenance)
  - evidence status
  - protocol status
  - risk class
- High-risk claims have red-team assignment and outcome.
- Public exports pass schema/headers validation.

## v1 minimum

- At least 300 claims with reviewed risk labels.
- At least 10 completed high-risk audit packets.
- Public-safe wording for all protocol-admissible claims.
- Evidence and protocol status both populated.
