# Requirements: Customer 360 Dashboard

**Defined:** 2026-01-21
**Core Value:** Enable RMs to see who the customer is (behavior, life stage) — not just products — driving proactive advising

**Reference:** Siebel Customer 360 Dashboard for Banking (see screenshots)

## v1 Requirements

Requirements for initial POC release. Focus: realistic data + clean dashboard structure matching Siebel reference.

### Data Generation

- [ ] **DATA-01**: Star schema with all dimension tables (customer, account, product, merchant, date)
- [ ] **DATA-02**: Star schema with all fact tables (transaction, account_snapshot, interaction, loan_schedule)
- [ ] **DATA-03**: 5,000 customers across 5 personas (Frequent Traveler, Young Parent, Digital Native, College Student, Boomer)
- [ ] **DATA-04**: Persona-driven spending patterns (spending behavior matches persona type)
- [ ] **DATA-05**: Recurring transaction patterns (salary cycles, subscriptions, monthly bills)
- [ ] **DATA-06**: Cross-sell signal data (insurance gaps, loan balances vs savings for pre-payment potential)
- [ ] **DATA-07**: Realistic transaction amounts and frequencies (not uniformly random)
- [ ] **DATA-08**: CD (Certificate of Deposit) account data with terms, rates, yields

### Executive View (Level A)

- [ ] **EXEC-01**: Portfolio Health — Total AUM vs LUM visualization (dual bar chart)
- [ ] **EXEC-02**: Share of Wallet — Average products held per customer (big number with trend)
- [ ] **EXEC-03**: Segment Heatmap — Profitability breakdown by customer segment

### Segment View (Level B)

- [ ] **SEGM-01**: Channel Mix — Mobile App vs Branch usage percentage by segment (pie chart)

### Individual View (Level C) — Profile Header

- [ ] **INDV-01**: Customer profile header with: Name, Total Balance, Phone, Email, SSN (masked), Job Title, Customer ID, Type (Retail/Business), KYC Status indicator, Full Address

### Individual View — Customer Portfolio Tabs

**Overview Tab:**
- [ ] **OVER-01**: Assets donut chart — breakdown by Savings, DDAs, CDs, TDs with total value
- [ ] **OVER-02**: Liabilities donut chart — breakdown by Home Loan, Credit Cards with total value
- [ ] **OVER-03**: Securities donut chart — breakdown by SIP, Equity, Mutual Fund with total value

**CASA Tab:**
- [ ] **CASA-01**: Account list table — A/c no, Type (icon), Status, Balance($)
- [ ] **CASA-02**: Balance trend line chart — Month Avg Balance vs Month End Balance over time
- [ ] **CASA-03**: Spend breakdown donut — % Spend by category (Lifestyle, Apparel, Travel, Furniture, Electronics, Other)

**Cards Tab:**
- [ ] **CARD-01**: Cards list table — Card name, Number, Limit, Available Balance($), Total Outstanding($), Payment Due Date
- [ ] **CARD-02**: Spend breakdown donut — Total Spend by category

**Loans Tab:**
- [ ] **LOAN-01**: Loans list table — Loan name, Type, Acc#, Term, % Rate, Outstanding Balance, Payoff Amount, Loan Amount

**CDs Tab:**
- [ ] **CD-01**: CDs list table — Name, Acc#, Term, Rate, Balance, Type, Annual Yield, Current Balance, Average Balance, TIN, TIN Number

**Insurance Tab:**
- [ ] **INSR-01**: Insurance list table — Policy Name, Status, Sub-Status, Effective Date, Description

**Securities Tab:**
- [ ] **SECR-01**: Securities list table — holdings with Name, Type, Units, Purchase Price, Current Value, Gain/Loss

### LookML

- [ ] **LKML-01**: Views for all dimension tables with proper field definitions
- [ ] **LKML-02**: Views for all fact tables with measures and dimensions
- [ ] **LKML-03**: Explores with proper joins between facts and dimensions
- [ ] **LKML-04**: Dashboard layouts for Executive, Segment, and Individual views

## v2 Requirements

Deferred to future release. Derived insights and advanced analytics.

### Derived Metrics

- **DERV-01**: Persona Tag — Automatically derived from spending patterns
- **DERV-02**: Engagement Score — 0-100 calculated from login frequency and activity
- **DERV-03**: Churn Risk — Low/Med/High prediction based on balance trends and sentiment
- **DERV-04**: Salary Detector — Highlight recurring salary credit date automatically
- **DERV-05**: Pre-payment Potential — Flag when savings balance exceeds loan payoff threshold
- **DERV-06**: Coverage Gap Analysis — Flag missing insurance based on life stage
- **DERV-07**: Risk Appetite Gauge — Derived from investment portfolio composition

### Lifestyle Tab (v2)

- **LIFE-01**: Subscription Manager — Auto-detect recurring merchants (Netflix, Spotify, Gym)
- **LIFE-02**: Life Events Alerts — Detect triggers from spending (baby stores, movers)

### Supporting Sections (v2)

- **SUPP-01**: Member Points / Loyalty tier display
- **SUPP-02**: Tickets section — support ticket counts by status/type
- **SUPP-03**: Recent Activities timeline
- **SUPP-04**: Offers carousel
- **SUPP-05**: Opportunity funnel

## Out of Scope

| Feature | Reason |
|---------|--------|
| Wallet Leakage metric | Requires external fintech data mapping — defer to v2 |
| Real-time data integration | POC uses static mock data |
| Multi-currency support | Single currency (USD) for simplicity |
| Joint account handling | Simplified to one-to-many customer-account relationship |
| Mobile-specific views | Desktop-first for exec demo |
| Authentication/RBAC | Using existing Looker permissions |
| RM assignment | Not needed for POC |
| Action buttons (Notify for Renewal, Claim History) | Display only for POC |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Complete |
| DATA-02 | Phase 1 | Complete |
| DATA-03 | Phase 2 | Pending |
| DATA-04 | Phase 2 | Pending |
| DATA-05 | Phase 2 | Pending |
| DATA-06 | Phase 2 | Pending |
| DATA-07 | Phase 2 | Pending |
| DATA-08 | Phase 2 | Pending |
| EXEC-01 | Phase 5 | Pending |
| EXEC-02 | Phase 5 | Pending |
| EXEC-03 | Phase 5 | Pending |
| SEGM-01 | Phase 6 | Pending |
| INDV-01 | Phase 7 | Pending |
| OVER-01 | Phase 7 | Pending |
| OVER-02 | Phase 7 | Pending |
| OVER-03 | Phase 7 | Pending |
| CASA-01 | Phase 7 | Pending |
| CASA-02 | Phase 7 | Pending |
| CASA-03 | Phase 7 | Pending |
| CARD-01 | Phase 7 | Pending |
| CARD-02 | Phase 7 | Pending |
| LOAN-01 | Phase 7 | Pending |
| CD-01 | Phase 7 | Pending |
| INSR-01 | Phase 7 | Pending |
| SECR-01 | Phase 7 | Pending |
| LKML-01 | Phase 4 | Pending |
| LKML-02 | Phase 4 | Pending |
| LKML-03 | Phase 4 | Pending |
| LKML-04 | Phase 5-7 | Pending |

**Coverage:**
- v1 requirements: 29 total
- Mapped to phases: 29
- Unmapped: 0 ✓

---
*Requirements defined: 2026-01-21*
*Last updated: 2026-01-21 after Siebel reference review*
