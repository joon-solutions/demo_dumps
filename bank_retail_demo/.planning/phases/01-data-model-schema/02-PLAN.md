# Plan 02: Fact Tables Schema

## Frontmatter

```yaml
wave: 1
depends_on: []
files_modified:
  - schema/fact_transaction.sql
  - schema/fact_account_snapshot.sql
  - schema/fact_interaction.sql
  - schema/fact_loan_schedule.sql
  - schema/README.md
autonomous: true
```

## Objective

Create BigQuery-compatible SQL DDL schema definitions for all fact tables in the Customer 360 data model, plus schema documentation.

## Context

The fact tables capture transactional and snapshot data. The enhanced fact_transaction includes fields for recurring detection, counterparty tracking, and spend categorization as specified in PROJECT.md.

## Tasks

<task id="1">
Create `schema/fact_transaction.sql` with all transaction fields:
- transaction_id (STRING, PRIMARY KEY)
- customer_id (STRING, FOREIGN KEY)
- account_id (STRING, FOREIGN KEY)
- merchant_id (STRING, FOREIGN KEY, NULLABLE)
- date_key (INT64, FOREIGN KEY)
- transaction_date (TIMESTAMP)
- amount (NUMERIC)
- transaction_type (STRING: credit, debit, transfer)
- payment_method (STRING: Credit Card, Debit Card, Bank Transfer, Direct Debit)
- mcc_category (STRING - denormalized for query performance)
- is_recurring (BOOLEAN - for subscription detection)
- recurring_frequency (STRING, NULLABLE: monthly, weekly, annual)
- counterparty_type (STRING: internal, external, self)
- counterparty_name (STRING, NULLABLE)
- description (STRING, NULLABLE)
- channel (STRING: App, Branch, ATM, Online, POS)
</task>

<task id="2">
Create `schema/fact_account_snapshot.sql` with balance tracking:
- snapshot_id (STRING, PRIMARY KEY)
- account_id (STRING, FOREIGN KEY)
- customer_id (STRING, FOREIGN KEY)
- date_key (INT64, FOREIGN KEY)
- snapshot_date (DATE)
- balance (NUMERIC)
- available_credit (NUMERIC, NULLABLE - for cards)
- credit_utilization_pct (NUMERIC, NULLABLE - for cards: balance/limit * 100)
- principal_paid (NUMERIC, NULLABLE - for loans)
- principal_remaining (NUMERIC, NULLABLE - for loans)
- interest_accrued (NUMERIC, NULLABLE)
- month_avg_balance (NUMERIC)
- month_end_balance (NUMERIC)
- total_credits_mtd (NUMERIC - month to date inflows)
- total_debits_mtd (NUMERIC - month to date outflows)
</task>

<task id="3">
Create `schema/fact_interaction.sql` with customer touchpoint data:
- interaction_id (STRING, PRIMARY KEY)
- customer_id (STRING, FOREIGN KEY)
- date_key (INT64, FOREIGN KEY)
- interaction_date (TIMESTAMP)
- channel (STRING: App, Call Center, Branch, Chatbot, Email, SMS)
- reason (STRING: Login, Account Inquiry, Fee Dispute, Card Issue, Loan Application, General Info, Complaint)
- sentiment_score (NUMERIC: 0.0-1.0)
- resolution_status (STRING: Resolved, Pending, Escalated)
- duration_seconds (INT64, NULLABLE)
- agent_id (STRING, NULLABLE)
</task>

<task id="4">
Create `schema/fact_loan_schedule.sql` with repayment tracking:
- schedule_id (STRING, PRIMARY KEY)
- account_id (STRING, FOREIGN KEY)
- customer_id (STRING, FOREIGN KEY)
- date_key (INT64, FOREIGN KEY)
- due_date (DATE)
- payment_due (NUMERIC)
- principal_portion (NUMERIC)
- interest_portion (NUMERIC)
- payment_status (STRING: Scheduled, Paid, Overdue, Partial)
- actual_payment_date (DATE, NULLABLE)
- actual_amount_paid (NUMERIC, NULLABLE)
- days_past_due (INT64, default 0)
</task>

<task id="5">
Create `schema/README.md` documenting the complete data model:
- Overview of star schema design
- Table descriptions and purposes
- Relationship diagram (ASCII or description)
- Key design decisions
- Field naming conventions used
- Data types reference
</task>

## Verification

- [ ] All 4 fact table SQL files created in `schema/` directory
- [ ] README.md documents the complete data model
- [ ] fact_transaction includes is_recurring and counterparty_type for behavioral analysis
- [ ] fact_account_snapshot includes month_avg_balance and month_end_balance for trend charts
- [ ] fact_loan_schedule supports repayment progress calculation
- [ ] All foreign key relationships documented

## Must Haves

1. fact_transaction must have is_recurring flag for subscription detection
2. fact_transaction must have counterparty_type for wallet leakage analysis
3. fact_account_snapshot must have month_avg_balance and month_end_balance for CASA trend chart
4. fact_account_snapshot must have credit_utilization_pct for Cards tab
5. Schema README must document all table relationships
