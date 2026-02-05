# Bank Retail Demo Project

## Overview
This project is a demonstration analytics platform for retail banking data. It provides end‑to‑end capabilities including data generation, exploratory data analysis, schema design, and analytical modeling.

## Project Objectives
- Simulate realistic retail banking datasets  
- Perform exploratory and multidimensional analysis  
- Define analytical schemas and metrics  
- Provide visualization layer through LookML  

## Repository Structure

```
bank_retail_demo/
├── .planning/            # Project planning and research notes
├── data/                 # Raw and processed datasets
├── lookml/               # Looker models and views
├── schema/               # Database schema definitions
├── eda_*.py              # Exploratory analysis scripts
├── financial_data_mockup.py  # Data generation utilities
├── PROJECT.md            # Project description
├── REQUIREMENTS.md       # Business and technical requirements
├── ROADMAP.md            # Development roadmap
└── README.md             # This file
```

## Key Components

### Data Generation
- `financial_data_mockup.py` creates synthetic banking transactions, customers, and products
- Configurable parameters for volume and distributions

### Exploratory Data Analysis
- `eda_quick_check.py` – initial data validation  
- `eda_plots.py` – visualization utilities  
- `eda_multidimensional.py` – slice and dice analysis  
- `eda_detailed_analysis.py` – in‑depth statistical review  

### Analytics Layer
- Schema definitions for analytical warehouse  
- LookML models for BI consumption  
- Metrics aligned with business requirements  

## Getting Started

1. Install dependencies  
   ```bash
   pip install -r REQUIREMENTS.md
   ```

2. Generate sample data  
   ```bash
   python financial_data_mockup.py
   ```

3. Run exploratory analysis  
   ```bash
   python eda_quick_check.py
   ```

## Usage Scenarios
- Customer behavior analysis  
- Product performance tracking  
- Risk and churn indicators  
- Revenue and profitability reporting  

## Development Guidelines
- Follow modular script design  
- Store outputs in `/data`  
- Maintain schema changes in `/schema`  
- Document metrics in LookML layer  

## Future Enhancements
- Predictive modeling for churn  
- Real‑time ingestion pipeline  
- Dashboard templates  
- Data quality framework  
