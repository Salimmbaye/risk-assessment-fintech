# Company Scenario — NorthStar Lending, Inc.

> **Portfolio note:** NorthStar Lending is a *fictional* company created for this
> lab project. All systems, data, and findings are invented to demonstrate a
> realistic GRC risk-assessment workflow. No real company or data is involved.

## 1. Business overview

| Attribute | Detail |
|-----------|--------|
| Company | NorthStar Lending, Inc. |
| Sector | Financial services / fintech |
| Business model | Online small-business lending and ACH payment processing |
| Headquarters | Dallas, TX (remote-first workforce) |
| Size | ~50 employees; ~8,000 active small-business borrowers |
| Hosting | Cloud-native (AWS); SaaS-heavy (Google Workspace, Salesforce, Slack) |
| Public/private | Privately held, venture-backed |

NorthStar lets small businesses apply for working-capital loans through a web and
mobile portal, pulls bank and credit data to underwrite, and disburses/collects
funds via ACH. It is scaling quickly and signing larger customers who now demand
evidence of a security program (SOC 2, security questionnaires).

## 2. Why this company has real compliance drivers

Because NorthStar handles consumers' and businesses' financial data, several
obligations apply. These are the "why" behind every risk in the register:

- **GLBA Safeguards Rule (FTC, 16 CFR 314):** As a non-bank financial institution,
  NorthStar must maintain a written information security program, designate a
  qualified individual, perform periodic risk assessments, and implement specific
  safeguards (access controls, encryption, MFA, logging, incident response).
- **PCI DSS:** A portion of repayments are made by debit/credit card, bringing the
  cardholder-data environment into scope.
- **SOC 2 (Trust Services Criteria):** Enterprise customers require a SOC 2 Type II
  report before signing; this drives most of the control expectations.
- **FFIEC / state lending regulation:** As a lender and money-movement business,
  NorthStar is subject to examination expectations and state licensing conditions.
- **State privacy & breach-notification laws** (e.g., Texas, plus every state where
  borrowers reside).

> **Framework choice:** This assessment uses the **NIST Cybersecurity Framework
> (CSF) 2.0** as the organizing backbone, because it is control-neutral, maps
> cleanly to GLBA/FFIEC expectations, and crosswalks to the controls a SOC 2 or
> ISO 27001 effort would require (see Project 2 — Controls Crosswalk).

## 3. Scope of the assessment

**In scope:** the systems that store, process, or transmit customer financial data
and the controls that protect them.

| # | Asset / System | Description | Data sensitivity |
|---|----------------|-------------|------------------|
| A1 | Borrower loan portal (web/mobile) | Customer-facing application and APIs | High — PII, financial, credentials |
| A2 | Underwriting platform | Pulls bank/credit data, scores applicants | High — PII, SSN, bank data |
| A3 | ACH / payments service | Initiates disbursements and collections | High — bank account numbers |
| A4 | Customer database (AWS RDS) | System of record for borrowers and loans | High — PII, financial |
| A5 | Cloud storage (AWS S3) | Documents, statements, exports | High — PII, financial |
| A6 | Corporate SaaS (Workspace, Salesforce, Slack) | Email, CRM, collaboration | Medium — PII, internal |
| A7 | Employee endpoints | Laptops used by remote staff | Medium — access to all above |
| A8 | Identity provider (SSO) | Authentication to all systems | High — keys to the kingdom |

**Out of scope for this iteration:** physical security of the (minimal) office,
and the HR/benefits systems that do not touch customer financial data.

## 4. Data types handled

- **Customer PII:** names, addresses, dates of birth, Social Security Numbers,
  Employer Identification Numbers.
- **Financial data:** bank account and routing numbers, card data, credit reports,
  loan balances and history.
- **Credentials & secrets:** customer portal logins, employee SSO, API keys.

## 5. How this scenario feeds the rest of the project

The business context above determines, for each risk:
- how likely a threat is to materialize (threat environment for a fintech), and
- how large the impact would be (regulatory, financial, and reputational, given
  the data types and obligations listed).

Those two judgments are what the **risk register** (`data/risk-register.csv`) and
the **scoring model** (`scripts/risk_scoring.py`) turn into prioritized, defensible
numbers in the **risk assessment report** (`docs/03-risk-assessment-report.md`).
