"""
Quick EDA to verify spending variance improvements
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')

# Load data
df_customer = pd.read_csv("data/dim_customer.csv")
df_transaction = pd.read_csv("data/fact_transaction.csv")
df_transaction['transaction_date'] = pd.to_datetime(df_transaction['transaction_date'])

# Merge to get persona and other dimensions
txn_with_cust = df_transaction.merge(
    df_customer[['customer_id', 'persona_tag', 'age', 'gender', 'income_bracket', 'segment']],
    on='customer_id'
)

# Filter to debits only
debit_txn = txn_with_cust[txn_with_cust['transaction_type'] == 'debit'].copy()

# Create figure
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Monthly AVERAGE Spending per Customer by Persona
# (Average is more meaningful than total since customer count grows over time)
ax = axes[0, 0]
debit_txn['month'] = debit_txn['transaction_date'].dt.to_period('M')

# Calculate average spending per customer per month
monthly_customer_spend = debit_txn.groupby(['month', 'customer_id', 'persona_tag'])['amount'].sum().reset_index()
monthly_avg = monthly_customer_spend.groupby(['month', 'persona_tag'])['amount'].mean().unstack()
monthly_avg.plot(ax=ax, marker='o', linewidth=2, markersize=4)
ax.set_title('Avg Monthly Spending per Customer by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Avg Spending per Customer ($)')
ax.legend(title='Persona', bbox_to_anchor=(1.02, 1), fontsize=8)

# 2. Average Transaction by Category & Persona - Travel should be smaller
ax = axes[0, 1]
cat_persona_avg = debit_txn.groupby(['mcc_category', 'persona_tag'])['amount'].mean().unstack()
# Get top categories that actually exist in data
available_cats = cat_persona_avg.index.tolist()
top_cats = [c for c in ['Travel', 'Groceries', 'Dining', 'Healthcare', 'Shopping', 'Subscriptions', 'Gas'] if c in available_cats][:6]
cat_persona_avg.loc[top_cats].plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Avg Transaction Amount by Category & Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Category')
ax.set_ylabel('Average Amount ($)')
ax.legend(title='Persona', fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 3. Spending Distribution by Age Group - should show variation
ax = axes[0, 2]
debit_txn['age_group'] = pd.cut(debit_txn['age'], bins=[0, 25, 35, 45, 55, 65, 100],
                                 labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
age_spending = debit_txn.groupby(['customer_id', 'age_group'])['amount'].sum().reset_index()
age_spending_agg = age_spending.groupby('age_group')['amount'].agg(['mean', 'std'])
ax.bar(age_spending_agg.index, age_spending_agg['mean'],
       yerr=age_spending_agg['std'], capsize=5, color=sns.color_palette("viridis", 6))
ax.set_title('Avg Customer Spending by Age Group', fontsize=12, fontweight='bold')
ax.set_xlabel('Age Group')
ax.set_ylabel('Total Spending ($)')

# 4. Spending Variance within Personas (box plot)
ax = axes[1, 0]
customer_spending = debit_txn.groupby(['customer_id', 'persona_tag'])['amount'].sum().reset_index()
customer_spending.boxplot(column='amount', by='persona_tag', ax=ax)
ax.set_title('Spending Variance Within Personas', fontsize=12, fontweight='bold')
ax.set_xlabel('Persona')
ax.set_ylabel('Total Customer Spending ($)')
plt.suptitle('')  # Remove default title

# 5. Spending by Income Bracket
ax = axes[1, 1]
income_order = ['<25K', '25-50K', '50-100K', '100-250K', '250K+']
customer_income_spending = debit_txn.groupby(['customer_id', 'income_bracket'])['amount'].sum().reset_index()
income_spending = customer_income_spending.groupby('income_bracket')['amount'].agg(['mean', 'std']).reindex(income_order)
ax.bar(income_spending.index, income_spending['mean'],
       yerr=income_spending['std'], capsize=5, color=sns.color_palette("rocket", 5))
ax.set_title('Avg Customer Spending by Income', fontsize=12, fontweight='bold')
ax.set_xlabel('Income Bracket')
ax.set_ylabel('Total Spending ($)')
ax.tick_params(axis='x', rotation=45)

# 6. Category Mix by Persona (percentage)
ax = axes[1, 2]
cat_persona_total = debit_txn.groupby(['persona_tag', 'mcc_category'])['amount'].sum().unstack(fill_value=0)
cat_persona_pct = cat_persona_total.div(cat_persona_total.sum(axis=1), axis=0) * 100
top_cats = cat_persona_pct.sum().nlargest(6).index.tolist()
cat_persona_pct[top_cats].plot(kind='bar', ax=ax, stacked=True, width=0.8)
ax.set_title('Spending Category Mix by Persona (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('Persona')
ax.set_ylabel('% of Total Spend')
ax.legend(title='Category', bbox_to_anchor=(1.02, 1), fontsize=8)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('data/eda_variance_check.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_variance_check.png")

# Print summary stats
print("\n" + "="*60)
print("VARIANCE CHECK SUMMARY")
print("="*60)

print("\n📊 AVERAGE TRANSACTION BY CATEGORY:")
for cat in ['Travel', 'Groceries', 'Dining', 'Shopping', 'Healthcare']:
    cat_txns = debit_txn[debit_txn['mcc_category'] == cat]
    print(f"   {cat}: ${cat_txns['amount'].mean():.2f} (median: ${cat_txns['amount'].median():.2f})")

print("\n📊 SPENDING VARIANCE BY PERSONA (std/mean ratio):")
for persona in df_customer['persona_tag'].unique():
    cust_ids = df_customer[df_customer['persona_tag'] == persona]['customer_id']
    persona_spending = debit_txn[debit_txn['customer_id'].isin(cust_ids)].groupby('customer_id')['amount'].sum()
    cv = persona_spending.std() / persona_spending.mean()  # Coefficient of variation
    print(f"   {persona}: CV={cv:.2f} (higher = more variance)")

print("\n📊 TRAVEL SPENDING CHECK:")
travel_txns = debit_txn[debit_txn['mcc_category'] == 'Travel']
print(f"   Count: {len(travel_txns):,}")
print(f"   Mean: ${travel_txns['amount'].mean():.2f}")
print(f"   Median: ${travel_txns['amount'].median():.2f}")
print(f"   Max: ${travel_txns['amount'].max():.2f}")
print(f"   % of total spend: {travel_txns['amount'].sum() / debit_txn['amount'].sum() * 100:.1f}%")
