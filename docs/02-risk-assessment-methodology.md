# Risk Assessment Methodology

This assessment uses a **semi-quantitative** model for all risks, plus a
**quantitative (annualized loss) layer** for the highest-priority risks. The
approach aligns with **NIST SP 800-30** (Guide for Conducting Risk Assessments)
and the risk-assessment expectation of the **GLBA Safeguards Rule**.

## 1. Risk model

For each risk we assess **inherent risk** (before considering controls) and
**residual risk** (after existing controls), so the register shows both the raw
exposure and what current controls actually buy down.

```
Risk Score = Likelihood  ×  Impact
```

Both factors use a **1–5 scale**. Scores range from 1 to 25 and are banded into
qualitative levels for reporting and prioritization.

### 1.1 Likelihood scale

| Value | Rating | Meaning (annualized) |
|-------|--------|----------------------|
| 1 | Rare | Not expected in a multi-year horizon (< ~5%/yr) |
| 2 | Unlikely | Could occur but not expected (~5–20%/yr) |
| 3 | Possible | Might occur at some point (~20–50%/yr) |
| 4 | Likely | Expected to occur (~50–80%/yr) |
| 5 | Almost certain | Expected to occur repeatedly (> ~80%/yr) |

### 1.2 Impact scale

Impact is rated on the **worst plausible** outcome across three dimensions —
**financial, regulatory/legal, and reputational** — reflecting NorthStar's data
and obligations.

| Value | Rating | Example impact for NorthStar |
|-------|--------|------------------------------|
| 1 | Insignificant | Minor internal disruption; no data or regulatory effect |
| 2 | Minor | Limited disruption; easily remediated; no reportable data loss |
| 3 | Moderate | Localized data exposure; customer notification; recoverable cost |
| 4 | Major | Breach of regulated financial data; regulatory scrutiny; material cost |
| 5 | Severe | Large-scale breach of SSN/bank data; GLBA enforcement; existential cost |

### 1.3 Risk level bands

| Score (L × I) | Level | Action expectation |
|---------------|-------|--------------------|
| 1–4 | Low | Accept / monitor |
| 5–9 | Moderate | Plan remediation |
| 10–14 | High | Remediate on a defined timeline |
| 15–25 | Critical | Remediate urgently; escalate to leadership |

## 2. Control effectiveness → residual risk

Existing controls reduce likelihood, impact, or both. Each risk records the
current controls and a **control-effectiveness rating** that justifies the
residual scores:

| Rating | Meaning |
|--------|---------|
| None | No meaningful control in place |
| Low | Partial/ad-hoc control; easily bypassed |
| Moderate | Control exists but has gaps or isn't consistently enforced |
| Strong | Well-designed, consistently operating control |

Residual likelihood and impact are re-rated on the same 1–5 scales given those
controls. **Residual risk is what drives the treatment decision.**

## 3. Risk treatment

Each risk is assigned one of the four standard treatments (per ISO 31000 /
NIST 800-30):

- **Mitigate** — add or strengthen controls to reduce the risk.
- **Transfer** — shift risk via insurance or contractual terms.
- **Avoid** — stop the activity that creates the risk.
- **Accept** — formally accept the residual risk (documented, owner sign-off).

## 4. Quantitative layer (top risks) — the finance view

For the highest-residual risks, a qualitative score isn't enough to justify spend.
We add a **single-loss / annualized-loss** estimate so leadership can compare the
cost of a control to the risk it reduces — the same expected-value logic used in
financial analysis.

```
SLE  (Single Loss Expectancy)      = Asset Value × Exposure Factor
ALE  (Annualized Loss Expectancy)  = SLE × ARO (Annualized Rate of Occurrence)
Risk-reduction value of a control  = ALE(before) − ALE(after)
```

Where:
- **Exposure Factor (EF):** the fraction of the asset's value lost if the event occurs.
- **ARO:** how many times per year the event is expected (derived from the
  likelihood rating, e.g., "Possible" ≈ 0.35/yr).

> **Worked example (Risk R03 — insecure API exposing customer data):**
> Estimated loss per breach event (notification, regulatory, remediation,
> churn) **SLE = $1,200,000**; estimated frequency **ARO = 0.4/yr** →
> **ALE ≈ $480,000/yr**. Implementing API authentication, rate-limiting, and a
> WAF is estimated to cut ARO to ~0.1/yr → **ALE ≈ $120,000/yr**, a modeled
> **risk reduction of ~$360,000/yr** against a control cost well under that.
> The investment is justified on expected-value grounds.

These figures are **illustrative estimates** for a fictional company — the point
is the *method* of translating a security risk into a financial decision, which is
how GRC earns a seat at the budget table.

## 5. Limitations

- Likelihood and impact ratings are expert-judgment estimates, not actuarial data.
- The quantitative layer uses modeled loss figures; a real program would refine
  these with industry breach-cost data (e.g., IBM Cost of a Data Breach) and
  internal financials.
- This is a point-in-time assessment; risk should be re-assessed at least annually
  and on major change (a GLBA expectation).
