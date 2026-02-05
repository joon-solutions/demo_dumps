"""
EDA Plots for Customer 360 Mock Data
Generates visualizations to verify data quality and realism
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load data
print("Loading data...")
df_customer = pd.read_csv("data/dim_customer.csv")
df_account = pd.read_csv("data/dim_account.csv")
df_transaction = pd.read_csv("data/fact_transaction.csv")
df_interaction = pd.read_csv("data/fact_interaction.csv")

# Convert dates
df_transaction['transaction_date'] = pd.to_datetime(df_transaction['transaction_date'])
df_customer['join_date'] = pd.to_datetime(df_customer['join_date'])

# Create figure with subplots
fig = plt.figure(figsize=(20, 24))

# 1. Persona Distribution
ax1 = fig.add_subplot(4, 3, 1)
persona_counts = df_customer['persona_tag'].value_counts()
colors = sns.color_palette("husl", len(persona_counts))
ax1.pie(persona_counts, labels=persona_counts.index, autopct='%1.1f%%', colors=colors)
ax1.set_title('Customer Persona Distribution', fontsize=12, fontweight='bold')

# 2. Segment Distribution
ax2 = fig.add_subplot(4, 3, 2)
segment_counts = df_customer['segment'].value_counts()
ax2.bar(segment_counts.index, segment_counts.values, color=['#3498db', '#2ecc71', '#e74c3c'])
ax2.set_title('Customer Segment Distribution', fontsize=12, fontweight='bold')
ax2.set_ylabel('Count')
for i, v in enumerate(segment_counts.values):
    ax2.text(i, v + 50, str(v), ha='center')

# 3. Transaction Amount Distribution (log scale)
ax3 = fig.add_subplot(4, 3, 3)
amounts = df_transaction[df_transaction['transaction_type'] == 'debit']['amount']
ax3.hist(amounts, bins=50, color='#9b59b6', edgecolor='white', alpha=0.7)
ax3.set_title('Transaction Amount Distribution (Debits)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Amount ($)')
ax3.set_ylabel('Frequency')
ax3.set_yscale('log')

# 4. Spending by Category
ax4 = fig.add_subplot(4, 3, 4)
category_spend = df_transaction[df_transaction['transaction_type'] == 'debit'].groupby('mcc_category')['amount'].sum().sort_values(ascending=True)
category_spend.plot(kind='barh', ax=ax4, color=sns.color_palette("viridis", len(category_spend)))
ax4.set_title('Total Spending by Category', fontsize=12, fontweight='bold')
ax4.set_xlabel('Total Amount ($)')

# 5. Monthly Transaction Volume
ax5 = fig.add_subplot(4, 3, 5)
df_transaction['month'] = df_transaction['transaction_date'].dt.to_period('M')
monthly_txn = df_transaction.groupby('month').size()
monthly_txn.index = monthly_txn.index.astype(str)
ax5.plot(range(len(monthly_txn)), monthly_txn.values, marker='o', linewidth=2, markersize=3, color='#e74c3c')
ax5.set_title('Monthly Transaction Volume', fontsize=12, fontweight='bold')
ax5.set_xlabel('Month')
ax5.set_ylabel('Number of Transactions')
ax5.set_xticks(range(0, len(monthly_txn), 3))
ax5.set_xticklabels([monthly_txn.index[i] for i in range(0, len(monthly_txn), 3)], rotation=45)

# 6. Recurring vs Non-Recurring
ax6 = fig.add_subplot(4, 3, 6)
recurring_counts = df_transaction['is_recurring'].value_counts()
ax6.pie(recurring_counts, labels=['One-time', 'Recurring'], autopct='%1.1f%%',
        colors=['#3498db', '#e74c3c'], explode=[0, 0.05])
ax6.set_title('Recurring vs One-time Transactions', fontsize=12, fontweight='bold')

# 7. Account Type Distribution
ax7 = fig.add_subplot(4, 3, 7)
account_types = df_account['account_type'].value_counts()
ax7.bar(account_types.index, account_types.values, color=sns.color_palette("Set2", len(account_types)))
ax7.set_title('Account Type Distribution', fontsize=12, fontweight='bold')
ax7.set_ylabel('Count')
ax7.tick_params(axis='x', rotation=45)
for i, v in enumerate(account_types.values):
    ax7.text(i, v + 50, str(v), ha='center', fontsize=9)

# 8. Balance Distribution by Segment (CASA accounts)
ax8 = fig.add_subplot(4, 3, 8)
casa_accounts = df_account[df_account['account_type'] == 'CASA'].merge(
    df_customer[['customer_id', 'segment']], on='customer_id'
)
for segment in ['Mass Market', 'Affluent', 'High Net Worth']:
    data = casa_accounts[casa_accounts['segment'] == segment]['current_balance']
    ax8.hist(data, bins=30, alpha=0.5, label=segment)
ax8.set_title('CASA Balance Distribution by Segment', fontsize=12, fontweight='bold')
ax8.set_xlabel('Balance ($)')
ax8.set_ylabel('Frequency')
ax8.legend()
ax8.set_xscale('log')

# 9. Spending Patterns by Persona
ax9 = fig.add_subplot(4, 3, 9)
txn_with_persona = df_transaction.merge(df_customer[['customer_id', 'persona_tag']], on='customer_id')
persona_category = txn_with_persona[txn_with_persona['transaction_type'] == 'debit'].groupby(
    ['persona_tag', 'mcc_category']
)['amount'].sum().unstack(fill_value=0)
# Normalize to show percentage
persona_category_pct = persona_category.div(persona_category.sum(axis=1), axis=0) * 100
top_categories = ['Travel', 'Groceries', 'Dining', 'Healthcare', 'Shopping', 'Subscriptions']
persona_category_pct[[c for c in top_categories if c in persona_category_pct.columns]].plot(
    kind='bar', ax=ax9, width=0.8
)
ax9.set_title('Spending Pattern by Persona (Top Categories)', fontsize=12, fontweight='bold')
ax9.set_xlabel('Persona')
ax9.set_ylabel('% of Total Spend')
ax9.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
ax9.tick_params(axis='x', rotation=45)

# 10. Customer Age Distribution by Persona
ax10 = fig.add_subplot(4, 3, 10)
for persona in df_customer['persona_tag'].unique():
    ages = df_customer[df_customer['persona_tag'] == persona]['age']
    ax10.hist(ages, bins=20, alpha=0.5, label=persona)
ax10.set_title('Age Distribution by Persona', fontsize=12, fontweight='bold')
ax10.set_xlabel('Age')
ax10.set_ylabel('Frequency')
ax10.legend(fontsize=8)

# 11. Interaction Channel Distribution
ax11 = fig.add_subplot(4, 3, 11)
channel_counts = df_interaction['channel'].value_counts()
ax11.pie(channel_counts, labels=channel_counts.index, autopct='%1.1f%%',
         colors=sns.color_palette("Set3", len(channel_counts)))
ax11.set_title('Customer Interaction Channels', fontsize=12, fontweight='bold')

# 12. Salary Distribution (Income Verification)
ax12 = fig.add_subplot(4, 3, 12)
salary_txn = df_transaction[df_transaction['mcc_category'] == 'Income']['amount']
ax12.hist(salary_txn, bins=30, color='#27ae60', edgecolor='white', alpha=0.7)
ax12.set_title('Salary Credit Distribution', fontsize=12, fontweight='bold')
ax12.set_xlabel('Salary Amount ($)')
ax12.set_ylabel('Frequency')
# Add vertical lines for expected salary ranges
for sal, label in [(1500, '<25K'), (3000, '25-50K'), (6000, '50-100K'), (12000, '100-250K'), (20000, '250K+')]:
    ax12.axvline(x=sal, color='red', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('data/eda_overview.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_overview.png")

# Additional detailed plots
fig2, axes = plt.subplots(2, 2, figsize=(14, 12))

# Credit Card Utilization
ax = axes[0, 0]
cc_accounts = df_account[df_account['account_type'] == 'Credit Card']
cc_util = (cc_accounts['outstanding_balance'] / cc_accounts['credit_limit'] * 100).dropna()
ax.hist(cc_util, bins=30, color='#e74c3c', edgecolor='white', alpha=0.7)
ax.set_title('Credit Card Utilization Distribution', fontsize=12, fontweight='bold')
ax.set_xlabel('Utilization %')
ax.set_ylabel('Frequency')
ax.axvline(x=30, color='green', linestyle='--', label='30% threshold')
ax.axvline(x=50, color='orange', linestyle='--', label='50% threshold')
ax.legend()

# Transaction Frequency by Day of Week
ax = axes[0, 1]
df_transaction['day_of_week'] = df_transaction['transaction_date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = df_transaction['day_of_week'].value_counts().reindex(day_order)
ax.bar(day_order, day_counts.values, color=sns.color_palette("Blues_d", 7))
ax.set_title('Transactions by Day of Week', fontsize=12, fontweight='bold')
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)

# Churn Analysis - Sentiment Before Churn
ax = axes[1, 0]
churned_customers = df_customer[df_customer['churn_status'] == True]['customer_id']
active_customers = df_customer[df_customer['churn_status'] == False]['customer_id'].sample(len(churned_customers))
churned_sentiment = df_interaction[df_interaction['customer_id'].isin(churned_customers)]['sentiment_score']
active_sentiment = df_interaction[df_interaction['customer_id'].isin(active_customers)]['sentiment_score']
ax.hist(active_sentiment, bins=20, alpha=0.5, label='Active Customers', color='green')
ax.hist(churned_sentiment, bins=20, alpha=0.5, label='Churned Customers', color='red')
ax.set_title('Sentiment Score: Active vs Churned', fontsize=12, fontweight='bold')
ax.set_xlabel('Sentiment Score')
ax.set_ylabel('Frequency')
ax.legend()

# Products per Customer
ax = axes[1, 1]
products_per_customer = df_account.groupby('customer_id').size()
ax.hist(products_per_customer, bins=range(1, 10), color='#9b59b6', edgecolor='white', alpha=0.7, align='left')
ax.set_title('Products per Customer (Share of Wallet)', fontsize=12, fontweight='bold')
ax.set_xlabel('Number of Products')
ax.set_ylabel('Number of Customers')
ax.set_xticks(range(1, 9))

plt.tight_layout()
plt.savefig('data/eda_detailed.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_detailed.png")

# Print summary statistics
print("\n" + "="*60)
print("DATA QUALITY SUMMARY")
print("="*60)

print("\n📊 TRANSACTION AMOUNTS:")
print(f"   Mean: ${df_transaction['amount'].mean():,.2f}")
print(f"   Median: ${df_transaction['amount'].median():,.2f}")
print(f"   Min: ${df_transaction['amount'].min():,.2f}")
print(f"   Max: ${df_transaction['amount'].max():,.2f}")

print("\n👥 CUSTOMERS BY SEGMENT:")
for seg, count in df_customer['segment'].value_counts().items():
    avg_balance = casa_accounts[casa_accounts['segment'] == seg]['current_balance'].mean()
    print(f"   {seg}: {count} customers, avg balance ${avg_balance:,.2f}")

print("\n🎯 PERSONA SPENDING PATTERNS (top category):")
for persona in df_customer['persona_tag'].unique():
    cust_ids = df_customer[df_customer['persona_tag'] == persona]['customer_id']
    persona_txn = df_transaction[(df_transaction['customer_id'].isin(cust_ids)) &
                                  (df_transaction['transaction_type'] == 'debit')]
    top_cat = persona_txn.groupby('mcc_category')['amount'].sum().idxmax()
    print(f"   {persona}: {top_cat}")

print("\n💳 CROSS-SELL SIGNALS:")
mortgage_holders = set(df_account[df_account['product_name'] == 'Home Mortgage']['customer_id'])
life_ins = set(df_account[df_account['product_name'].str.contains('Life', na=False)]['customer_id'])
print(f"   Mortgage holders: {len(mortgage_holders)}")
print(f"   Mortgage holders WITHOUT life insurance: {len(mortgage_holders - life_ins)}")

print("\n🔄 RECURRING TRANSACTIONS:")
recurring = df_transaction[df_transaction['is_recurring'] == True]
print(f"   Total recurring: {len(recurring):,}")
print(f"   Salary deposits: {len(recurring[recurring['mcc_category'] == 'Income']):,}")
print(f"   Subscriptions: {len(recurring[recurring['mcc_category'] != 'Income']):,}")

print("\n✅ Plots saved to data/eda_overview.png and data/eda_detailed.png")
