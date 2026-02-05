

# Data Directory

## Overview
This folder contains all datasets and analytical outputs used in the Bank Retail Demo project. It includes both structured CSV data that feeds the LookML semantic layer and generated artifacts from exploratory data analysis.

The data represents a realistic synthetic retail banking environment covering customers, accounts, transactions, loans, and interactions.

---

## Core Data Tables

### Dimension Tables

#### dim_customer.csv
- One row per customer  
- Demographics: age, gender, income bracket, state  
- Segmentation: persona and wealth segment  
- Engagement indicators and churn flag  

#### dim_account.csv
- One row per account  
- Account type (CASA, Credit Card, Loan, CD, Insurance, Securities)  
- Status, open date, credit limit, balance  

#### dim_product.csv
- Product catalog and hierarchy  
- Product family and pricing attributes  

#### dim_merchant.csv
- Merchant category codes  
- Geography and industry classification  

#### dim_date.csv
- Calendar attributes  
- Fiscal periods and holiday flags  

### Fact Tables

#### fact_transaction.csv
- Customer spending activity  
- Amount, category, channel, timestamp  
- Links to customer, account, merchant  

#### fact_account_snapshot.csv
- Daily/monthly balance snapshots  
- Product holdings over time  

#### fact_loan_schedule.csv
- Loan principal and repayment schedule  
- Interest and remaining balance  

#### fact_interaction.csv
- Customer touchpoints  
- App, branch, call center, chatbot events  

---

## Generated Analysis Files

The following images are outputs from the EDA scripts and illustrate key insights:

- **eda_products.png** – product holdings by persona and segment  
- **eda_by_income.png** – behavior across income brackets  
- **eda_time_based.png** – seasonal and cohort trends  
- **eda_by_segment.png** – segment performance and churn  
- **eda_churn.png** – churn drivers  
- **eda_accounts_products.png** – product mix analysis  
- **eda_variance_check.png** – distribution validation  
- **eda_accounts.png** – account structure  
- **eda_by_geography.png** – state level analysis  

These files are reproducible via the scripts in the project root.

---

## Usage Guidelines

- Do not edit CSV files manually – regenerate via `financial_data_mockup.py`  
- Use date dimension for all time joins  
- Transaction amounts are in USD  
- Income brackets are categorical, not exact salary  
- Churn flag represents 6‑month inactivity  

---
