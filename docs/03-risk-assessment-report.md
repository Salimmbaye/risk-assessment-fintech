# Information Security Risk Assessment Report
### NorthStar Lending, Inc. — NIST CSF 2.0

> **Portfolio note:** NorthStar Lending is a fictional company. This report is a
> lab exercise demonstrating a GRC risk-assessment deliverable; all data is invented.

**Prepared by:** Salim Mbaye
**Framework:** NIST Cybersecurity Framework (CSF) 2.0
**Method:** Semi-quantitative (NIST SP 800-30), with an annualized-loss layer for top risks
**Date:** October 20th, 2026

---

## 1. Executive summary

NorthStar Lending, a fintech handling customer financial data (PII, SSNs, bank and
card data), was assessed against the NIST CSF 2.0. Fourteen risks were identified
and scored for inherent and residual exposure.

**Headline results (residual, after existing controls):**

| Residual level | Count |
|----------------|-------|
| Critical | 4 |
| High | 6 |
| Moderate | 4 |
| Low | 0 |

The organization carries meaningful unmitigated risk concentrated in **identity and
access** (no enforced MFA), **application/API security**, **cloud configuration**,
and **incident readiness**. None of these require large capital — they require a
formalized security program, which is also a direct **GLBA Safeguards Rule**
obligation. The four Critical risks should be remediated within 30–60 days.

![Residual Risk Heatmap](../outputs/risk-heatmap.png)

## 2. Top risks and recommended treatment

The four Critical residual risks (score 15) are the priority:

| ID | Risk | Residual | Why it matters | Recommended action |
|----|------|----------|----------------|--------------------|
| R02 | No enforced MFA on admin/SSO | Critical | A single phished admin credential compromises every system; #1 breach cause | Enforce phishing-resistant MFA on all admin and SSO accounts |
| R03 | Insecure customer API | Critical | APIs expose regulated financial data directly to the internet | OAuth2 + authorization checks, rate limiting, WAF, API gateway |
| R06 | Public/misconfigured cloud storage | Critical | A single misconfigured bucket can leak the full customer dataset | Block Public Access, deploy CSPM, scan IaC pre-deploy |
| R10 | No incident response plan | Critical | A breach without a plan multiplies cost, downtime, and regulatory exposure | Documented IR plan, roles/runbooks, annual tabletop |

The six High risks (R01, R07, R09, R12 at score 12; plus others) follow on a
60–90 day timeline and are listed in `outputs/risk-register-scored.csv`.

## 3. The quantitative view (why this gets funded)

For R03 (insecure API), a qualitative "Critical" rating is translated into money so
leadership can weigh control cost against risk reduction:

| Metric | Before controls | After controls |
|--------|-----------------|----------------|
| Single Loss Expectancy (SLE) | $1,200,000 | $1,200,000 |
| Annualized Rate of Occurrence (ARO) | 0.4 / yr | 0.1 / yr |
| **Annualized Loss Expectancy (ALE)** | **$480,000 / yr** | **$120,000 / yr** |

**Modeled risk reduction ≈ $360,000/yr** against a control cost (API gateway, WAF,
engineering time) well below that — the investment is justified on expected-value
grounds. (Figures illustrative; see methodology §4.)

## 4. Findings mapped to NIST CSF 2.0 functions

| Function | Theme of gaps | Representative risks |
|----------|---------------|----------------------|
| **GV** Govern | No written security program; no vendor risk mgmt; no risk-assessment cadence (GLBA gap) | R07, R11, R14 |
| **ID** Identify | Incomplete asset inventory; no vulnerability management | R12, R14 |
| **PR** Protect | No enforced MFA; weak API security; inconsistent encryption; cloud misconfig | R01–R06, R08 |
| **DE** Detect | No centralized logging/SIEM; limited monitoring | R09 |
| **RS** Respond | No incident response plan or testing | R10 |
| **RC** Recover | Untested backups; no DR/BCP | R04, R13 |

The spread across all six functions is itself the finding: NorthStar has point
tools but **no program**. The remediation roadmap therefore leads with governance.

## 5. Remediation roadmap

**Phase 1 — 0–60 days (Critical):** Enforce MFA (R02); secure APIs (R03); lock down
cloud storage with Block Public Access + CSPM (R06); write and socialize an incident
response plan (R10). In parallel, stand up the **written information security program
and designate a Qualified Individual** (R11) — the GLBA foundation everything else
hangs on.

**Phase 2 — 60–120 days (High):** Centralized logging/SIEM (R09); vulnerability
management with patch SLAs (R12); vendor risk program (R07); phishing-resistant MFA
rollout to all staff + simulations (R01).

**Phase 3 — 120–180 days (Moderate + maturity):** Least privilege and access reviews
(R08); org-wide encryption enforcement (R05); DR/BCP with tested restores (R13);
SaaS discovery and asset inventory (R14). Re-run this assessment to measure residual
risk reduction.

## 6. How to reproduce

```bash
pip install -r scripts/requirements.txt
python3 scripts/risk_scoring.py
# regenerates outputs/: scored register, heatmap, and summary
```

## 7. Sources & standards referenced

- NIST Cybersecurity Framework (CSF) 2.0
- NIST SP 800-30 Rev. 1 — Guide for Conducting Risk Assessments
- FTC Safeguards Rule, 16 CFR Part 314 (GLBA)
- NIST SP 800-53 Rev. 5 and CIS Controls v8 (control references; see Project 2 crosswalk)
