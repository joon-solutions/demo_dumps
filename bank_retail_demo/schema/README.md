# Customer 360 Data Model

Star schema design for retail banking Customer 360 dashboard.

## Overview

This data model follows a **star schema** pattern with:
- **5 Dimension Tables**: Customer, Account, Product, Merchant, Date
- **4 Fact Tables**: Transaction, Account Snapshot, Interaction, Loan Schedule

## Entity Relationship Diagram

```
                              ┌─────────────────┐
                              │   dim_date      │
                              │   (date_key)    │
                              └────────┬────────┘
                                       │
┌─────────────┐    ┌─────────────┐    │    ┌─────────────────┐
│ dim_product │    │ dim_merchant│    │    │  dim_customer   │
│ (product_id)│    │(merchant_id)│    │    │  (customer_id)  │
└──────┬──────┘    └──────┬──────┘    │    └────────┬────────┘
       │                  │           │             │
       │                  │           │             │
       │    ┌─────────────┴───────────┴─────────────┤
       │    │                                       │
       │    │         FACT TABLES                   │
       │    │                                       │
       │    ├── fact_transaction ──────────────────┤
       │    │   (transaction_id)                   │
       │    │                                       │
       │    ├── fact_account_snapshot ─────────────┤
       │    │   (snapshot_id)                      │
       │    │                                       │
       │    ├── fact_interaction ──────────────────┤
       │    │   (interaction_id)                   │
       │    │                                       │
       │    └── fact_loan_schedule ────────────────┤
       │        (schedule_id)                      │
       │                                           │
       └───────────────────────────────────────────┘
                              │
                              │
                      ┌───────┴───────┐
                      │  dim_account  │
                      │  (account_id) │
                      └───────────────┘
```

## Dimension Tables

### dim_customer
Customer master data including demographics, segmentation, and behavioral attributes.

| Field | Type | Description |
|-------|------|-------------|
| customer_id | STRING | Primary key |
| segment | STRING | Mass Market, Affluent, High Net Worth |
| persona_tag | STRING | Frequent Traveler, Young Parent, Digital Native, College Student, Boomer |
| engagement_score | INT64 | 0-100 activity-based score |
| churn_status | BOOL | Whether customer has churned |

### dim_account
Account master supporting all product types (CASA, Cards, Loans, CDs, Insurance, Securities).

| Field | Type | Description |
|-------|------|-------------|
| account_id | STRING | Primary key |
| customer_id | STRING | Foreign key to dim_customer |
| account_type | STRING | CASA, Credit Card, Loan, CD, Insurance, Securities |
| status | STRING | Active, Dormant, Closed |

### dim_product
Product catalog reference table.

### dim_merchant
Merchant reference with MCC codes for transaction categorization.

| Field | Type | Description |
|-------|------|-------------|
| merchant_id | STRING | Primary key |
| mcc_code | STRING | 4-digit Merchant Category Code |
| mcc_category | STRING | Human-readable category |
| is_subscription_merchant | BOOL | Flag for recurring charge merchants |

### dim_date
Standard date dimension with banking-specific flags.

| Field | Type | Description |
|-------|------|-------------|
| date_key | INT64 | Primary key (YYYYMMDD) |
| is_salary_day | BOOL | 1st or 15th of month |
| is_business_day | BOOL | Weekday flag |

## Fact Tables

### fact_transaction
Transactional data with behavioral flags.

| Key Field | Description |
|-----------|-------------|
| is_recurring | Subscription detection flag |
| counterparty_type | internal/external/self for wallet leakage |
| mcc_category | Denormalized for query performance |

### fact_account_snapshot
Monthly balance snapshots for trend analysis.

| Key Field | Description |
|-----------|-------------|
| month_avg_balance | For CASA balance trend chart |
| month_end_balance | For CASA balance trend chart |
| credit_utilization_pct | For Cards tab gauge |
| total_credits_mtd | Cash flow velocity |
| total_debits_mtd | Cash flow velocity |

### fact_interaction
Customer touchpoint tracking.

| Key Field | Description |
|-----------|-------------|
| channel | App, Branch, Call Center, Chatbot |
| sentiment_score | 0.0-1.0 for churn signals |

### fact_loan_schedule
Loan repayment tracking.

| Key Field | Description |
|-----------|-------------|
| cumulative_principal_paid | For repayment progress |
| remaining_balance | For pre-payment potential |

## Design Decisions

1. **One-to-Many Customer-Account**: Simplified from many-to-many (joint accounts) for POC
2. **Denormalized mcc_category**: In fact_transaction for query performance
3. **Monthly Snapshots**: fact_account_snapshot at monthly grain, not daily
4. **Behavioral Flags**: is_recurring, counterparty_type added to fact_transaction for analytics

## Data Types

- **STRING**: All IDs and categorical fields
- **NUMERIC**: All monetary amounts (precision preserved)
- **INT64**: Counts, scores, date keys
- **BOOL**: All flags
- **DATE**: Date-only fields
- **TIMESTAMP**: Date+time fields

## BigQuery Notes

- Tables designed for BigQuery compatibility
- Partitioning recommended on date fields
- Clustering recommended on frequently filtered fields (customer_id, account_id)
