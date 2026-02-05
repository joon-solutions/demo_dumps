# Customer 360 Dashboard

## What This Is

A Looker-based Customer 360 dashboard for retail banking that shifts from a static "Product-View" to a dynamic "Customer-Lifestyle-View." This POC demonstrates how behavioral spending data can drive "Next Best Actions" for Relationship Managers, enabling proactive advising instead of reactive service.

## Core Value

RMs can see *who the customer is* (behavior, life stage, needs) — not just what products they hold — enabling personalized cross-sell and proactive engagement.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Data Generation:**
- [ ] Realistic mock data generator (Python → CSV → BigQuery)
- [ ] 5,000 customers across 5 personas (Frequent Traveler, Young Parent, Digital Native, College Student, Boomer)
- [ ] Star schema with proper dimensional modeling (dim/fact tables)
- [ ] Realistic transaction patterns (salary cycles, subscriptions, seasonal spending)
- [ ] Cross-sell signals baked into data (insurance gaps, loan pre-payment potential, idle cash)

**Dashboard — Level A (Executive View):**
- [ ] Portfolio Health: Total AUM vs LUM (Dual Bar Chart)
- [ ] Share of Wallet: Avg products per customer (Big Number Trend)
- [ ] Segment Heatmap: Profitability by segment (Heatmap)

**Dashboard — Level B (Segment View):**
- [ ] Wallet Leakage: Funds transferred to external fintechs (Red Bar Chart)
- [ ] Channel Mix: Mobile App vs Branch usage % (Pie Chart)

**Dashboard — Level C (Individual View):**
- [ ] Profile Header: Persona Tag, Engagement Score (0-100), Churn Risk (Low/Med/High)
- [ ] CASA Tab: Cash Flow Velocity, Salary Detector
- [ ] Cards Tab: Spend by Category (Donut), Top Merchants, Credit Utilization
- [ ] Loans Tab: Repayment Progress bar, Pre-payment Potential flag
- [ ] Insurance Tab: Coverage Gap Analysis with cross-sell flags
- [ ] Securities Tab: Risk Appetite gauge, Portfolio ROI
- [ ] Lifestyle Tab: Subscription Manager, Life Events alerts

**LookML:**
- [ ] Views for all dimension and fact tables
- [ ] Explores with proper joins
- [ ] Derived tables for KPIs (engagement score, churn risk, coverage gaps)

### Out of Scope

- Real-time data integration — POC uses static mock data
- Authentication/RBAC — using existing Looker permissions
- Mobile-specific views — desktop-first for exec demo
- Multi-currency support — single currency (USD) for simplicity
- Historical trend comparisons beyond 2 years — mock data covers ~2 years

## Context

**Purpose:** POC for Senior Management to demonstrate the value of behavioral analytics in retail banking.

**Current State:** Existing mockup (`financial_data_mockup.py`) generates basic customer/transaction data but lacks:
- Account-level product holdings (CASA, Cards, Loans, Insurance, Securities)
- Realistic spending patterns tied to personas
- Attributes needed for cross-sell analysis (marital status, dependents, home ownership)
- Proper dimensional modeling

**Tech Stack:** Python (data generation) → CSV → BigQuery → Looker

**Reference Document:** `BRD.rtf` contains the original business requirements and dashboard architecture.

## Data Model

### Dimension Tables

**dim_customer:**
- `customer_id`, `first_name`, `last_name`
- `date_of_birth`, `age`, `gender`
- `email`, `phone`
- `address_city`, `address_state`, `address_country`
- `marital_status`, `has_children`, `num_dependents`
- `occupation`, `employment_type`, `income_bracket`
- `home_ownership`
- `segment` (Mass Market, Affluent, High Net Worth)
- `kyc_status`, `join_date`
- `preferred_channel`, `engagement_score`
- `persona_tag`, `risk_tolerance`
- `churn_status`, `churn_date`

**dim_account:**
- `account_id`, `customer_id`
- `account_type` (CASA, Credit Card, Loan, Insurance, Securities)
- `product_name` (e.g., "Premium Savings", "Gold Card", "Home Mortgage")
- `status` (Active, Dormant, Closed)
- `open_date`, `maturity_date`
- `credit_limit` (for cards)
- `interest_rate` (for loans/savings)
- `coverage_amount` (for insurance)
- `beneficiary_count` (for insurance)
- `principal_amount` (for loans)

**dim_product:**
- `product_id`, `product_name`, `product_type`, `product_category`
- `min_balance`, `annual_fee`, `interest_rate_range`

**dim_merchant:**
- `merchant_id`, `merchant_name`
- `mcc_code`, `mcc_category`
- `merchant_type` (Retail, Online, Subscription)

**dim_date:**
- Standard date dimension (date_key, date, day, month, quarter, year, is_weekend, etc.)

### Fact Tables

**fact_transaction:**
- `transaction_id`, `customer_id`, `account_id`, `merchant_id`, `date_key`
- `amount`, `transaction_type` (credit/debit/transfer)
- `payment_method` (Credit Card, Debit, Transfer)
- `mcc_category`
- `is_recurring` (for subscription detection)
- `counterparty_type` (internal/external — for wallet leakage)

**fact_account_snapshot:**
- `snapshot_id`, `account_id`, `customer_id`, `date_key`
- `balance`, `available_credit` (for cards)
- `principal_paid`, `principal_remaining` (for loans)
- `product_count` (customer-level)

**fact_interaction:**
- `interaction_id`, `customer_id`, `date_key`
- `channel` (App, Call Center, Branch, Chatbot)
- `reason`, `sentiment_score`, `resolution_status`

**fact_loan_schedule:**
- `schedule_id`, `account_id`, `customer_id`, `date_key`
- `payment_due`, `principal_portion`, `interest_portion`
- `payment_status` (Paid, Due, Overdue)

### Personas (5)

| Persona | Age Range | Characteristics |
|---------|-----------|-----------------|
| Frequent Traveler | 30-50 | Airlines, hotels, foreign transactions, travel insurance |
| Young Parent | 28-42 | Baby stores, family activities, education savings, life insurance |
| Digital Native | 22-35 | Heavy app usage, fintech transfers, subscriptions, crypto |
| College Student | 18-24 | Low balances, food/entertainment spend, no loans yet |
| Boomer | 55-75 | Conservative investments, branch preference, mortgage paid off |

## Constraints

- **Data Source**: BigQuery — Looker connects to BQ for the POC
- **Schema Design**: Star schema with clear fact/dimension separation
- **Customer-Account Relationship**: Simplified to one-to-many (customer owns multiple accounts, each account has one primary owner) for POC

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Simplified customer-account relationship | Full many-to-many (joint accounts) adds complexity without POC value | — Pending |
| 5 persona types | Covers key retail banking segments for demo variety | — Pending |
| No additional fact tables | Keep model lean; enhance fact_transaction instead | — Pending |
| Static mock data | Speed to delivery; no backend integration for POC | — Pending |

---
*Last updated: 2026-01-21 after initialization*
