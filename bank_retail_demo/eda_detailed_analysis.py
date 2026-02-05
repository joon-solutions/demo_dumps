"""
Extended EDA for Customer 360 Mock Data
More detailed visualizations to understand data patterns
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
df_product = pd.read_csv("data/dim_product.csv")

# Convert dates
df_transaction['transaction_date'] = pd.to_datetime(df_transaction['transaction_date'])
df_customer['join_date'] = pd.to_datetime(df_customer['join_date'])

# Merge for analysis
df_txn_full = df_transaction.merge(df_customer[['customer_id', 'persona_tag', 'segment', 'age']], on='customer_id')
df_acc_full = df_account.merge(df_customer[['customer_id', 'persona_tag', 'segment', 'age']], on='customer_id')

# ============================================================
# FIGURE 1: Credit Card Analysis
# ============================================================
fig1, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1a. Card Type by Persona
ax = axes[0, 0]
cards = df_acc_full[df_acc_full['account_type'] == 'Credit Card']
card_persona = pd.crosstab(cards['persona_tag'], cards['product_name'], normalize='index') * 100
card_persona.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Credit Card Type Distribution by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Persona')
ax.set_ylabel('% of Cardholders')
ax.legend(title='Card Type', bbox_to_anchor=(1.02, 1))
ax.tick_params(axis='x', rotation=45)

# 1b. Card Type by Segment
ax = axes[0, 1]
card_segment = pd.crosstab(cards['segment'], cards['product_name'], normalize='index') * 100
card_segment.plot(kind='bar', ax=ax, width=0.8, color=['#3498db', '#f39c12', '#9b59b6'])
ax.set_title('Credit Card Type Distribution by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Segment')
ax.set_ylabel('% of Cardholders')
ax.legend(title='Card Type')
ax.tick_params(axis='x', rotation=0)

# 1c. Credit Limit by Segment
ax = axes[1, 0]
for segment in ['Mass Market', 'Affluent', 'High Net Worth']:
    data = cards[cards['segment'] == segment]['credit_limit'].dropna()
    ax.hist(data, bins=20, alpha=0.5, label=f'{segment} (n={len(data)})')
ax.set_title('Credit Limit Distribution by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Credit Limit ($)')
ax.set_ylabel('Frequency')
ax.legend()

# 1d. Average Credit Limit by Persona & Card Type
ax = axes[1, 1]
avg_limit = cards.groupby(['persona_tag', 'product_name'])['credit_limit'].mean().unstack()
avg_limit.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Average Credit Limit by Persona & Card Type', fontsize=12, fontweight='bold')
ax.set_xlabel('Persona')
ax.set_ylabel('Average Credit Limit ($)')
ax.legend(title='Card Type', bbox_to_anchor=(1.02, 1))
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('data/eda_credit_cards.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_credit_cards.png")

# ============================================================
# FIGURE 2: Products & Cross-sell Analysis
# ============================================================
fig2, axes = plt.subplots(2, 2, figsize=(14, 12))

# 2a. Products per Customer by Persona
ax = axes[0, 0]
products_per_cust = df_account.groupby('customer_id').size().reset_index(name='product_count')
products_per_cust = products_per_cust.merge(df_customer[['customer_id', 'persona_tag']], on='customer_id')
sns.boxplot(data=products_per_cust, x='persona_tag', y='product_count', ax=ax,
            order=['College Student', 'Digital Native', 'Young Parent', 'Frequent Traveler', 'Boomer'])
ax.set_title('Products per Customer by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Persona')
ax.set_ylabel('Number of Products')
ax.tick_params(axis='x', rotation=45)

# 2b. Products per Customer by Segment
ax = axes[0, 1]
products_per_cust_seg = products_per_cust.merge(df_customer[['customer_id', 'segment']], on='customer_id')
sns.boxplot(data=products_per_cust_seg, x='segment', y='product_count', ax=ax,
            order=['Mass Market', 'Affluent', 'High Net Worth'])
ax.set_title('Products per Customer by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Segment')
ax.set_ylabel('Number of Products')

# 2c. Product Mix by Segment (what types of accounts)
ax = axes[1, 0]
product_mix = pd.crosstab(df_acc_full['segment'], df_acc_full['account_type'], normalize='index') * 100
product_mix[['CASA', 'Credit Card', 'Loan', 'CD', 'Insurance', 'Securities']].plot(
    kind='bar', ax=ax, stacked=True, width=0.8
)
ax.set_title('Product Mix by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Segment')
ax.set_ylabel('% of Accounts')
ax.legend(title='Account Type', bbox_to_anchor=(1.02, 1))
ax.tick_params(axis='x', rotation=0)

# 2d. Cross-sell Opportunity: Mortgage holders without Life Insurance
ax = axes[1, 1]
mortgage_holders = set(df_account[df_account['product_name'] == 'Home Mortgage']['customer_id'])
life_ins_holders = set(df_account[df_account['product_name'].str.contains('Life', na=False)]['customer_id'])
mortgage_with_life = mortgage_holders & life_ins_holders
mortgage_without_life = mortgage_holders - life_ins_holders

# Get their segments
mortgage_cust = df_customer[df_customer['customer_id'].isin(mortgage_holders)]
cross_sell_data = {
    'Has Life Insurance': len(mortgage_with_life),
    'No Life Insurance\n(Cross-sell Opportunity)': len(mortgage_without_life)
}
colors = ['#27ae60', '#e74c3c']
ax.pie(cross_sell_data.values(), labels=cross_sell_data.keys(), autopct='%1.1f%%', colors=colors,
       explode=[0, 0.1])
ax.set_title(f'Mortgage Holders: Life Insurance Cross-sell\n(n={len(mortgage_holders)} mortgage holders)',
             fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('data/eda_products.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_products.png")

# ============================================================
# FIGURE 3: Spending Patterns Deep Dive
# ============================================================
fig3, axes = plt.subplots(2, 2, figsize=(14, 12))

# 3a. Monthly Spending by Persona
ax = axes[0, 0]
df_txn_full['month'] = df_txn_full['transaction_date'].dt.to_period('M')
monthly_persona = df_txn_full[df_txn_full['transaction_type'] == 'debit'].groupby(
    ['month', 'persona_tag']
)['amount'].sum().unstack()
monthly_persona.index = monthly_persona.index.astype(str)
# Sample every 3rd month for readability
monthly_persona.iloc[::3].plot(ax=ax, marker='o', linewidth=2, markersize=4)
ax.set_title('Monthly Spending by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Total Spending ($)')
ax.legend(title='Persona', bbox_to_anchor=(1.02, 1))
ax.tick_params(axis='x', rotation=45)

# 3b. Transaction Amount Distribution by Persona
ax = axes[0, 1]
debit_txns = df_txn_full[df_txn_full['transaction_type'] == 'debit']
for persona in ['College Student', 'Digital Native', 'Boomer', 'Frequent Traveler']:
    data = debit_txns[debit_txns['persona_tag'] == persona]['amount']
    ax.hist(data[data < 500], bins=50, alpha=0.4, label=persona)  # Cap at 500 for visibility
ax.set_title('Transaction Amount Distribution by Persona (< $500)', fontsize=12, fontweight='bold')
ax.set_xlabel('Amount ($)')
ax.set_ylabel('Frequency')
ax.legend()

# 3c. Average Transaction by Category & Persona
ax = axes[1, 0]
avg_by_cat_persona = debit_txns.groupby(['mcc_category', 'persona_tag'])['amount'].mean().unstack()
top_cats = ['Travel', 'Groceries', 'Dining', 'Healthcare', 'Shopping']
avg_by_cat_persona.loc[top_cats].plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Average Transaction Amount by Category & Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Category')
ax.set_ylabel('Average Amount ($)')
ax.legend(title='Persona', bbox_to_anchor=(1.02, 1), fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 3d. Spending by Day of Month (Payday Effect)
ax = axes[1, 1]
debit_txns = debit_txns.copy()
debit_txns['day_of_month'] = debit_txns['transaction_date'].dt.day
daily_spend = debit_txns.groupby('day_of_month')['amount'].sum()
ax.bar(daily_spend.index, daily_spend.values, color='#3498db', alpha=0.7)
ax.axvline(x=1, color='red', linestyle='--', alpha=0.7, label='1st (Payday)')
ax.axvline(x=15, color='red', linestyle='--', alpha=0.7, label='15th (Payday)')
ax.set_title('Total Spending by Day of Month', fontsize=12, fontweight='bold')
ax.set_xlabel('Day of Month')
ax.set_ylabel('Total Spending ($)')
ax.legend()

plt.tight_layout()
plt.savefig('data/eda_spending.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_spending.png")

# ============================================================
# FIGURE 4: Customer Demographics & Behavior
# ============================================================
fig4, axes = plt.subplots(2, 2, figsize=(14, 12))

# 4a. Age vs Total Balance (scatter)
ax = axes[0, 0]
cust_balance = df_acc_full.groupby('customer_id').agg({
    'current_balance': 'sum',
    'age': 'first',
    'segment': 'first'
}).reset_index()
for segment in ['Mass Market', 'Affluent', 'High Net Worth']:
    data = cust_balance[cust_balance['segment'] == segment]
    ax.scatter(data['age'], data['current_balance'], alpha=0.3, label=segment, s=10)
ax.set_title('Age vs Total Balance by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Age')
ax.set_ylabel('Total Balance ($)')
ax.set_yscale('log')
ax.legend()

# 4b. Channel Usage by Persona (Heatmap)
ax = axes[0, 1]
channel_persona = pd.crosstab(df_interaction['customer_id'], df_interaction['channel'])
channel_persona = channel_persona.merge(df_customer[['customer_id', 'persona_tag']],
                                         left_index=True, right_on='customer_id')
channel_by_persona = channel_persona.groupby('persona_tag')[['App', 'Branch', 'Call Center', 'Chatbot']].mean()
sns.heatmap(channel_by_persona, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax)
ax.set_title('Average Interactions per Channel by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Channel')
ax.set_ylabel('Persona')

# 4c. Income Bracket Distribution by Persona
ax = axes[1, 0]
income_order = ['<25K', '25-50K', '50-100K', '100-250K', '250K+']
income_persona = pd.crosstab(df_customer['persona_tag'], df_customer['income_bracket'], normalize='index') * 100
income_persona = income_persona[[c for c in income_order if c in income_persona.columns]]
income_persona.plot(kind='bar', ax=ax, stacked=True, width=0.8,
                    color=['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60'])
ax.set_title('Income Distribution by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Persona')
ax.set_ylabel('% of Customers')
ax.legend(title='Income Bracket', bbox_to_anchor=(1.02, 1))
ax.tick_params(axis='x', rotation=45)

# 4d. Geographic Distribution
ax = axes[1, 1]
state_counts = df_customer['address_state'].value_counts()
state_counts.plot(kind='bar', ax=ax, color=sns.color_palette("viridis", len(state_counts)))
ax.set_title('Customer Distribution by State', fontsize=12, fontweight='bold')
ax.set_xlabel('State')
ax.set_ylabel('Number of Customers')
for i, v in enumerate(state_counts.values):
    ax.text(i, v + 10, str(v), ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('data/eda_demographics.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_demographics.png")

# ============================================================
# FIGURE 5: Churn Analysis
# ============================================================
fig5, axes = plt.subplots(2, 2, figsize=(14, 12))

churned = df_customer[df_customer['churn_status'] == True]
active = df_customer[df_customer['churn_status'] == False]

# 5a. Churn Rate by Persona
ax = axes[0, 0]
churn_by_persona = df_customer.groupby('persona_tag')['churn_status'].mean() * 100
churn_by_persona.sort_values().plot(kind='barh', ax=ax, color='#e74c3c')
ax.set_title('Churn Rate by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Churn Rate (%)')
ax.set_ylabel('Persona')
for i, v in enumerate(churn_by_persona.sort_values().values):
    ax.text(v + 0.3, i, f'{v:.1f}%', va='center')

# 5b. Churn Rate by Segment
ax = axes[0, 1]
churn_by_segment = df_customer.groupby('segment')['churn_status'].mean() * 100
churn_by_segment.plot(kind='bar', ax=ax, color=['#3498db', '#f39c12', '#27ae60'])
ax.set_title('Churn Rate by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Segment')
ax.set_ylabel('Churn Rate (%)')
ax.tick_params(axis='x', rotation=0)
for i, v in enumerate(churn_by_segment.values):
    ax.text(i, v + 0.3, f'{v:.1f}%', ha='center')

# 5c. Engagement Score: Churned vs Active
ax = axes[1, 0]
ax.hist(active['engagement_score'], bins=20, alpha=0.5, label=f'Active (n={len(active)})', color='green')
ax.hist(churned['engagement_score'], bins=20, alpha=0.5, label=f'Churned (n={len(churned)})', color='red')
ax.set_title('Engagement Score: Active vs Churned', fontsize=12, fontweight='bold')
ax.set_xlabel('Engagement Score')
ax.set_ylabel('Frequency')
ax.legend()

# 5d. Products Held: Churned vs Active
ax = axes[1, 1]
churned_products = df_account[df_account['customer_id'].isin(churned['customer_id'])].groupby('customer_id').size()
active_products = df_account[df_account['customer_id'].isin(active['customer_id'])].groupby('customer_id').size()
ax.hist(active_products, bins=range(1, 10), alpha=0.5, label=f'Active (avg={active_products.mean():.1f})',
        color='green', align='left')
ax.hist(churned_products, bins=range(1, 10), alpha=0.5, label=f'Churned (avg={churned_products.mean():.1f})',
        color='red', align='left')
ax.set_title('Products Held: Active vs Churned', fontsize=12, fontweight='bold')
ax.set_xlabel('Number of Products')
ax.set_ylabel('Frequency')
ax.legend()

plt.tight_layout()
plt.savefig('data/eda_churn.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_churn.png")

# ============================================================
# FIGURE 6: Account & Balance Analysis
# ============================================================
fig6, axes = plt.subplots(2, 2, figsize=(14, 12))

# 6a. Loan Amount Distribution by Type
ax = axes[0, 0]
loans = df_account[df_account['account_type'] == 'Loan']
for loan_type in loans['product_name'].unique():
    data = loans[loans['product_name'] == loan_type]['principal_amount'].dropna()
    if len(data) > 0:
        ax.hist(data, bins=20, alpha=0.5, label=f'{loan_type} (n={len(data)})')
ax.set_title('Loan Principal Distribution by Type', fontsize=12, fontweight='bold')
ax.set_xlabel('Principal Amount ($)')
ax.set_ylabel('Frequency')
ax.legend()

# 6b. CD Term Distribution
ax = axes[1, 0]
cds = df_account[df_account['account_type'] == 'CD']
cd_terms = cds['cd_term_months'].value_counts().sort_index()
ax.bar(cd_terms.index.astype(str), cd_terms.values, color='#9b59b6')
ax.set_title('CD Term Distribution', fontsize=12, fontweight='bold')
ax.set_xlabel('Term (Months)')
ax.set_ylabel('Number of CDs')
for i, v in enumerate(cd_terms.values):
    ax.text(i, v + 2, str(v), ha='center')

# 6c. Insurance Coverage by Persona
ax = axes[0, 1]
insurance = df_acc_full[df_acc_full['account_type'] == 'Insurance']
ins_by_persona = insurance.groupby('persona_tag')['coverage_amount'].mean() / 1000  # in thousands
ins_by_persona.sort_values().plot(kind='barh', ax=ax, color='#27ae60')
ax.set_title('Average Insurance Coverage by Persona', fontsize=12, fontweight='bold')
ax.set_xlabel('Average Coverage ($K)')
ax.set_ylabel('Persona')

# 6d. Securities Value by Segment
ax = axes[1, 1]
securities = df_acc_full[df_acc_full['account_type'] == 'Securities']
sec_by_segment = securities.groupby('segment')['current_value'].agg(['mean', 'median', 'count'])
x = range(len(sec_by_segment))
width = 0.35
ax.bar([i - width/2 for i in x], sec_by_segment['mean'], width, label='Mean', color='#3498db')
ax.bar([i + width/2 for i in x], sec_by_segment['median'], width, label='Median', color='#e74c3c')
ax.set_xticks(x)
ax.set_xticklabels(sec_by_segment.index)
ax.set_title('Securities Value by Segment', fontsize=12, fontweight='bold')
ax.set_xlabel('Segment')
ax.set_ylabel('Value ($)')
ax.legend()

plt.tight_layout()
plt.savefig('data/eda_accounts.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_accounts.png")

# ============================================================
# Print Summary Statistics
# ============================================================
print("\n" + "="*70)
print("DETAILED DATA SUMMARY")
print("="*70)

print("\n📊 CREDIT CARD ANALYSIS:")
print(f"   Total cardholders: {len(cards['customer_id'].unique()):,}")
card_type_dist = cards['product_name'].value_counts()
for card, count in card_type_dist.items():
    print(f"   {card}: {count:,} ({count/len(cards)*100:.1f}%)")

print("\n🏦 ACCOUNT BALANCES BY SEGMENT (CASA):")
casa = df_acc_full[df_acc_full['account_type'] == 'CASA']
for segment in ['Mass Market', 'Affluent', 'High Net Worth']:
    data = casa[casa['segment'] == segment]['current_balance']
    print(f"   {segment}:")
    print(f"      Mean: ${data.mean():,.0f}, Median: ${data.median():,.0f}")
    print(f"      Min: ${data.min():,.0f}, Max: ${data.max():,.0f}")

print("\n📈 PRODUCTS PER CUSTOMER:")
ppc = df_account.groupby('customer_id').size()
for persona in df_customer['persona_tag'].unique():
    cust_ids = df_customer[df_customer['persona_tag'] == persona]['customer_id']
    persona_ppc = ppc[ppc.index.isin(cust_ids)]
    print(f"   {persona}: avg={persona_ppc.mean():.1f}, min={persona_ppc.min()}, max={persona_ppc.max()}")

print("\n💳 CHURN ANALYSIS:")
print(f"   Overall churn rate: {df_customer['churn_status'].mean()*100:.1f}%")
print(f"   Churned customers: {churned.shape[0]:,}")
print(f"   Active customers: {active.shape[0]:,}")

print("\n✅ All detailed EDA plots saved to data/")
