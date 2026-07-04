# Safety Policy

This repository is a private research workbench. It is not medical advice.

## Prohibited interpretation

Nothing in this repository should be interpreted as advice to:

- stop medication;
- delay medical care;
- replace cancer treatment;
- ignore clinician guidance;
- apply restrictive diets to pregnancy, pediatrics, advanced kidney disease, cancer, type 1 diabetes, severe psychiatric illness, or medication-dependent disease without clinician supervision.

## High-risk domains

Claims involving the following domains require strict review:

- LDL-C, ApoB, LMHR, cardiovascular risk;
- cancer;
- diabetes, insulin, glucose-lowering medication, deprescribing;
- pregnancy, lactation, pediatrics;
- kidney disease, kidney stones, gout;
- severe psychiatric illness;
- autoimmune disease treatment claims;
- medication discontinuation;
- eating disorder risk.

## Unsafe claim quarantine

Unsafe claims should not be deleted. Preserve them internally as observed community artifacts, but quarantine them.

Likely quarantine examples:

```text
Carnivore cures cancer.
Stop chemotherapy.
Stop insulin.
High LDL is always harmless.
Plants are poison for everyone.
Seed oils are equivalent to cigarettes.
Children should be strict carnivore without medical supervision.
Pregnant women should ignore prenatal nutrition standards.
```

Quarantine statuses:

```text
high_risk_without_clinician
do_not_use_publicly
contradicted
unsafe_clinical_directive
```

## Public-safe language policy

Convert overclaims into bounded claims.

| Overclaim | Public-safe downgrade |
|---|---|
| Plants are poison. | Some plant compounds may be poorly tolerated by some people or clinically relevant in specific contexts. |
| Fiber is useless. | Fiber is not classified as essential for survival, but its health effects are context-dependent. |
| Seed oils are toxic. | Some concerns focus on linoleic acid oxidation, deep frying, and ultra-processed food contexts; independent causality remains contested. |
| LDL does not matter on carnivore. | Large LDL-C/ApoB increases on carnivore remain clinically debated and should be evaluated in full cardiovascular context. |
| Carnivore cures autoimmune disease. | Carnivore may function as an elimination diet that improves symptoms in some autoimmune or GI contexts, but disease-specific evidence varies. |
| Carnivore cures cancer. | Do not use as a cancer treatment claim; ketogenic approaches remain investigational or adjunctive in limited contexts. |
