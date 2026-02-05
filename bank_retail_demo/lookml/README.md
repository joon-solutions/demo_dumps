

# LookML Analytics Layer

## Overview
This directory contains the Looker modeling layer for the Bank Retail Demo project. It defines the semantic model used by BI users to explore retail banking data in a governed and consistent way.

The LookML layer transforms raw analytical tables into business-friendly dimensions, measures, and dashboards.

## Folder Structure

```
lookml/
├── dashboards/          # Pre-built analytical dashboards
│   ├── executive.dashboard.lookml
│   ├── individual.dashboard.lookml
│   └── segment.dashboard.lookml
├── models/              # Looker model definitions
│   └── demo_retail_banking.model.lookml
├── views/               # Dimension and fact views
│   ├── dim_account.view.lookml
│   ├── dim_customer.view.lookml
│   ├── dim_date.view.lookml
│   ├── dim_merchant.view.lookml
│   ├── dim_product.view.lookml
│   ├── fact_account_snapshot.view.lookml
│   ├── fact_interaction.view.lookml
│   ├── fact_loan_schedule.view.lookml
│   └── fact_transaction.view.lookml
└── manifest.lookml
```

## Modeling Principles

- Star schema approach with clear separation of facts and dimensions  
- Business-friendly naming conventions  
- Reusable measures and dimensions  
- Centralized definitions for KPIs  
- Consistent date and time handling  

## Key Subject Areas

### Customers
- Demographics  
- Segment classification  
- Acquisition channels  
- Lifetime value metrics  

### Accounts & Balances
- Current balance  
- Historical snapshots  
- Product ownership  
- Status lifecycle  

### Transactions
- Revenue measures  
- Channel analysis  
- Merchant categories  
- Behavioral indicators  

### Lending
- Loan schedules  
- Repayment status  
- Risk indicators  
- Interest income  

## Dashboards

- **Executive Dashboard** – high level KPIs, revenue, balances, risk  
- **Individual Dashboard** – single customer 360 view  
- **Segment Dashboard** – cohort and segment comparison  

## Development Guide

1. Add new fields in the appropriate view file  
2. Expose them through the model  
3. Reuse existing dimensions where possible  
4. Follow naming standards:
   - dimensions: snake_case  
   - measures: verb_noun (total_revenue, count_accounts)  

## Testing

- Validate joins through Looker content validator  
- Check aggregate correctness vs source data  
- Ensure symmetric aggregates for ratios  
- Test filters and drill paths  

## Future Extensions

- PDTs for performance  
- Advanced customer scoring  
- Real-time transaction explores  
- Data quality dashboards  
