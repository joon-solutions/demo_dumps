# Roadmap: Customer 360 Dashboard

**Created:** 2026-01-21
**Depth:** Standard (5-8 phases)
**Core Value:** Enable RMs to see who the customer is — not just products

## Phase Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Data Model & Schema | Define star schema structure | DATA-01, DATA-02 | Schema documented, tables defined |
| 2 | Mock Data Generator | Generate realistic banking data | DATA-03 to DATA-08 | 5K customers, realistic patterns |
| 3 | BigQuery Setup | Load data to warehouse | — | Data queryable in BigQuery |
| 4 | LookML Foundation | Create views and explores | LKML-01 to LKML-03 | All tables accessible in Looker |
| 5 | Executive Dashboard | Build Level A view | EXEC-01 to EXEC-03 | Portfolio Health, Share of Wallet, Heatmap |
| 6 | Segment Dashboard | Build Level B view | SEGM-01 | Channel Mix by segment |
| 7 | Individual Dashboard | Build Level C view | INDV-01, OVER-01 to SECR-01 | Profile header + 7 portfolio tabs |

---

## Phase 1: Data Model & Schema

**Goal:** Define the complete star schema structure with all dimensions and facts.

**Requirements:**
- DATA-01: Star schema with all dimension tables
- DATA-02: Star schema with all fact tables

**Success Criteria:**
1. [ ] dim_customer schema defined with all fields (demographics, segment, KYC)
2. [ ] dim_account schema defined with all product types (CASA, Cards, Loans, CDs, Insurance, Securities)
3. [ ] dim_product, dim_merchant, dim_date schemas defined
4. [ ] fact_transaction schema defined with transaction_type, is_recurring, counterparty_type
5. [ ] fact_account_snapshot schema defined with balance tracking
6. [ ] fact_interaction and fact_loan_schedule schemas defined
7. [ ] Schema documentation complete with field descriptions

**Deliverables:**
- `schema/` directory with SQL DDL files or schema documentation
- Entity-relationship diagram (optional)

---

## Phase 2: Mock Data Generator

**Goal:** Generate 5,000 realistic customers with persona-driven behavior and cross-sell signals.

**Requirements:**
- DATA-03: 5,000 customers across 5 personas
- DATA-04: Persona-driven spending patterns
- DATA-05: Recurring transaction patterns
- DATA-06: Cross-sell signal data
- DATA-07: Realistic amounts and frequencies
- DATA-08: CD account data

**Success Criteria:**
1. [ ] 5 persona profiles implemented (Frequent Traveler, Young Parent, Digital Native, College Student, Boomer)
2. [ ] Spending patterns match persona (e.g., Traveler has airlines/hotels, Parent has baby stores)
3. [ ] Salary credits appear on consistent dates (1st/15th of month)
4. [ ] Subscriptions recur monthly (Netflix, Spotify, etc.)
5. [ ] Transaction amounts follow realistic distributions (not uniform random)
6. [ ] Insurance gaps exist for cross-sell (e.g., mortgage holders without life insurance)
7. [ ] All CSV files generated and validated

**Deliverables:**
- `financial_data_mockup.py` (enhanced)
- CSV files: dim_customer, dim_account, dim_product, dim_merchant, dim_date
- CSV files: fact_transaction, fact_account_snapshot, fact_interaction, fact_loan_schedule

---

## Phase 3: BigQuery Setup

**Goal:** Load generated data into BigQuery and validate queryability.

**Requirements:**
- (No explicit requirement — infrastructure setup)

**Success Criteria:**
1. [ ] BigQuery dataset created
2. [ ] All dimension tables loaded
3. [ ] All fact tables loaded
4. [ ] Sample queries return expected results
5. [ ] Table relationships validated via test joins

**Deliverables:**
- BigQuery dataset with all tables
- Load scripts or documentation

---

## Phase 4: LookML Foundation

**Goal:** Create LookML views and explores for all tables.

**Requirements:**
- LKML-01: Views for all dimension tables
- LKML-02: Views for all fact tables
- LKML-03: Explores with proper joins

**Success Criteria:**
1. [ ] dim_customer.view.lkml with all fields and proper types
2. [ ] dim_account.view.lkml with account type filtering
3. [ ] dim_product, dim_merchant, dim_date views created
4. [ ] fact_transaction.view.lkml with measures (sum, count, avg)
5. [ ] fact_account_snapshot.view.lkml with balance measures
6. [ ] fact_interaction, fact_loan_schedule views created
7. [ ] Main explore connects all tables with correct join logic
8. [ ] Test queries work in Explore interface

**Deliverables:**
- LookML project with views/ and explores/ directories
- Model file with explore definitions

---

## Phase 5: Executive Dashboard

**Goal:** Build Level A dashboard for strategic portfolio health.

**Requirements:**
- EXEC-01: Portfolio Health (AUM vs LUM)
- EXEC-02: Share of Wallet (avg products)
- EXEC-03: Segment Heatmap

**Success Criteria:**
1. [ ] Portfolio Health dual bar chart shows total assets vs liabilities
2. [ ] Share of Wallet big number shows average products per customer
3. [ ] Segment Heatmap shows profitability by Mass Market / Affluent / HNW
4. [ ] Dashboard filters work (date range, segment)
5. [ ] Dashboard loads in < 5 seconds

**Deliverables:**
- `dashboards/executive.dashboard.lookml` or Looker dashboard

---

## Phase 6: Segment Dashboard

**Goal:** Build Level B dashboard for segment analysis.

**Requirements:**
- SEGM-01: Channel Mix

**Success Criteria:**
1. [ ] Channel Mix pie chart shows Mobile App vs Branch vs Call Center vs Chatbot
2. [ ] Chart is filterable by customer segment
3. [ ] Drill-down to customer list works

**Deliverables:**
- `dashboards/segment.dashboard.lookml` or Looker dashboard

---

## Phase 7: Individual Dashboard

**Goal:** Build Level C dashboard with customer profile and 7 portfolio tabs.

**Requirements:**
- INDV-01: Customer profile header
- OVER-01, OVER-02, OVER-03: Overview tab donuts
- CASA-01, CASA-02, CASA-03: CASA tab
- CARD-01, CARD-02: Cards tab
- LOAN-01: Loans tab
- CD-01: CDs tab
- INSR-01: Insurance tab
- SECR-01: Securities tab

**Success Criteria:**
1. [ ] Profile header shows: Name, Total Balance, Phone, Email, SSN (masked), Job Title, Customer ID, Type, KYC Status, Address
2. [ ] Overview tab: Assets donut, Liabilities donut, Securities donut with totals
3. [ ] CASA tab: Account table + balance trend line chart + spend category donut
4. [ ] Cards tab: Card details table + spend category donut
5. [ ] Loans tab: Loan details table with all fields
6. [ ] CDs tab: CD details table with all fields
7. [ ] Insurance tab: Policy details table
8. [ ] Securities tab: Holdings table with gain/loss
9. [ ] Customer selector/search works to switch between customers
10. [ ] All tabs load within 3 seconds

**Deliverables:**
- `dashboards/individual.dashboard.lookml` or Looker dashboard
- Dashboard matches Siebel reference layout

---

## Requirement Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Pending |
| DATA-02 | Phase 1 | Pending |
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

## Dependencies

```
Phase 1 (Schema)
    ↓
Phase 2 (Data Generator)
    ↓
Phase 3 (BigQuery)
    ↓
Phase 4 (LookML)
    ↓
Phase 5 (Executive) ──┐
    ↓                 │
Phase 6 (Segment) ────┼── Can run in parallel after Phase 4
    ↓                 │
Phase 7 (Individual) ─┘
```

---
*Roadmap created: 2026-01-21*
