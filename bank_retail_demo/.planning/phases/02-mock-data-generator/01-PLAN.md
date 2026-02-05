# Plan 02-01: Mock Data Generator

## Metadata
- **Wave:** 1
- **Autonomous:** true
- **Files Modified:** financial_data_mockup.py, data/*.csv

## Objective

Enhance the mock data generator to produce realistic banking data aligned with Phase 1 schemas.

## Tasks

### Task 1: Refactor customer generation with personas
- Add 5 persona types: Frequent Traveler, Young Parent, Digital Native, College Student, Boomer
- Add all dim_customer fields (contact info, demographics, employment, etc.)
- Distribute personas with realistic weights

### Task 2: Generate dim_product catalog
- Create product catalog with all types: CASA, Cards, Loans, CDs, Insurance, Securities
- Include product details (rates, fees, terms)

### Task 3: Generate dim_merchant with MCC codes
- Create merchants by category (Groceries, Dining, Travel, etc.)
- Flag subscription merchants (Netflix, Spotify, etc.)

### Task 4: Generate dim_date table
- Standard date dimension for 2023-2025
- Include fiscal periods, holidays

### Task 5: Generate dim_account for all product types
- CASA accounts (Savings, Checking)
- Credit Cards with limits
- Loans with terms and rates
- CDs with maturity dates
- Insurance policies
- Securities holdings

### Task 6: Generate fact_transaction with persona patterns
- Persona-driven merchant selection (Traveler → airlines/hotels, Parent → baby stores)
- Recurring transactions (salary on 1st/15th, subscriptions monthly)
- Realistic amount distributions (not uniform random)

### Task 7: Generate fact_account_snapshot
- Monthly balance snapshots
- Credit utilization for cards
- Cash flow metrics

### Task 8: Generate fact_interaction
- Customer service interactions
- Channel distribution (App, Branch, Call Center, Chatbot)

### Task 9: Generate fact_loan_schedule
- Payment schedules for loan accounts
- Include some overdue/prepaid patterns

### Task 10: Add cross-sell signals
- Insurance gaps (mortgage holders without life insurance)
- Pre-payment potential (high savings vs loan balance)

## Verification
- [ ] 5,000 customers generated
- [ ] All 5 personas represented
- [ ] 9 CSV files created matching schemas
- [ ] Recurring transactions detectable (is_recurring flag)
- [ ] Cross-sell opportunities exist in data

## Output
- `data/` directory with all CSV files
