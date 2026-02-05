# Plan 01: Dimension Tables Schema

## Frontmatter

```yaml
wave: 1
depends_on: []
files_modified:
  - schema/dim_customer.sql
  - schema/dim_account.sql
  - schema/dim_product.sql
  - schema/dim_merchant.sql
  - schema/dim_date.sql
autonomous: true
```

## Objective

Create BigQuery-compatible SQL DDL schema definitions for all dimension tables in the Customer 360 data model.

## Context

The PROJECT.md defines the required fields for each dimension table. This plan creates the actual SQL schema files that will be used to create tables in BigQuery.

## Tasks

<task id="1">
Create `schema/` directory structure
</task>

<task id="2">
Create `schema/dim_customer.sql` with all customer fields:
- customer_id (STRING, PRIMARY KEY)
- first_name, last_name (STRING)
- date_of_birth (DATE), age (INT64), gender (STRING)
- email, phone (STRING)
- address_city, address_state, address_country (STRING)
- marital_status (STRING: Single, Married, Divorced, Widowed)
- has_children (BOOLEAN), num_dependents (INT64)
- occupation, employment_type (STRING: Salaried, Self-Employed, Retired, Student)
- income_bracket (STRING: <25K, 25-50K, 50-100K, 100-250K, 250K+)
- home_ownership (STRING: Own, Rent, Other)
- segment (STRING: Mass Market, Affluent, High Net Worth)
- kyc_status (STRING: Verified, Pending, Expired)
- join_date (DATE)
- preferred_channel (STRING: App, Branch, Call Center, Chatbot)
- engagement_score (INT64: 0-100)
- persona_tag (STRING: Frequent Traveler, Young Parent, Digital Native, College Student, Boomer)
- risk_tolerance (STRING: Low, Medium, High)
- churn_status (BOOLEAN), churn_date (DATE, NULLABLE)
</task>

<task id="3">
Create `schema/dim_account.sql` with account fields supporting all product types:
- account_id (STRING, PRIMARY KEY)
- customer_id (STRING, FOREIGN KEY)
- account_type (STRING: CASA, Credit Card, Loan, CD, Insurance, Securities)
- product_name (STRING)
- status (STRING: Active, Dormant, Closed)
- open_date (DATE), maturity_date (DATE, NULLABLE)
- credit_limit (NUMERIC, NULLABLE - for cards)
- interest_rate (NUMERIC, NULLABLE)
- coverage_amount (NUMERIC, NULLABLE - for insurance)
- beneficiary_count (INT64, NULLABLE - for insurance)
- principal_amount (NUMERIC, NULLABLE - for loans)
- current_balance (NUMERIC)
- account_number (STRING - masked display)
- currency (STRING, default 'USD')
</task>

<task id="4">
Create `schema/dim_product.sql` with product catalog fields:
- product_id (STRING, PRIMARY KEY)
- product_name (STRING)
- product_type (STRING: Savings, Checking, Credit Card, Personal Loan, Mortgage, CD, Life Insurance, Property Insurance, Equity, Mutual Fund, SIP)
- product_category (STRING: CASA, Cards, Loans, CDs, Insurance, Securities)
- min_balance (NUMERIC, NULLABLE)
- annual_fee (NUMERIC, NULLABLE)
- interest_rate_min (NUMERIC, NULLABLE)
- interest_rate_max (NUMERIC, NULLABLE)
- description (STRING)
</task>

<task id="5">
Create `schema/dim_merchant.sql` with merchant fields:
- merchant_id (STRING, PRIMARY KEY)
- merchant_name (STRING)
- mcc_code (STRING - 4-digit Merchant Category Code)
- mcc_category (STRING: Groceries, Dining, Travel, Utilities, Entertainment, Healthcare, Shopping, Subscriptions, Other)
- merchant_type (STRING: Retail, Online, Subscription, Service)
- is_subscription_merchant (BOOLEAN)
</task>

<task id="6">
Create `schema/dim_date.sql` with standard date dimension:
- date_key (INT64, PRIMARY KEY - YYYYMMDD format)
- full_date (DATE)
- day_of_week (INT64: 1-7)
- day_name (STRING: Monday-Sunday)
- day_of_month (INT64: 1-31)
- day_of_year (INT64: 1-366)
- week_of_year (INT64: 1-53)
- month (INT64: 1-12)
- month_name (STRING: January-December)
- quarter (INT64: 1-4)
- year (INT64)
- is_weekend (BOOLEAN)
- is_month_end (BOOLEAN)
- is_salary_day (BOOLEAN - 1st or 15th)
</task>

## Verification

- [ ] All 5 dimension table SQL files created in `schema/` directory
- [ ] Each file contains valid BigQuery DDL syntax
- [ ] All fields from PROJECT.md data model are included
- [ ] Data types are appropriate for BigQuery
- [ ] Comments/descriptions added for non-obvious fields

## Must Haves

1. dim_customer must include all persona-related fields (persona_tag, segment, engagement_score)
2. dim_account must support all 6 product types (CASA, Cards, Loans, CDs, Insurance, Securities)
3. dim_merchant must include mcc_code and is_subscription_merchant for transaction categorization
4. dim_date must include is_salary_day for salary detection logic
