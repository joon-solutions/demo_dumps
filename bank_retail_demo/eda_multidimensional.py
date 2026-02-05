"""
Multi-dimensional EDA for Customer 360 Mock Data
Views by: Age, Income, Segment, Persona, Gender, Channel, Geography, etc.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')

# Load data
print("Loading data...")
df_customer = pd.read_csv("data/dim_customer.csv")
df_account = pd.read_csv("data/dim_account.csv")
df_transaction = pd.read_csv("data/fact_transaction.csv")
df_interaction = pd.read_csv("data/fact_interaction.csv")

# Convert dates
df_transaction['transaction_date'] = pd.to_datetime(df_transaction['transaction_date'])
df_customer['join_date'] = pd.to_datetime(df_customer['join_date'])

# Create age groups
df_customer['age_group'] = pd.cut(df_customer['age'],
                                   bins=[0, 25, 35, 45, 55, 65, 100],
                                   labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])

# Merge for analysis
df_txn = df_transaction.merge(df_customer[['customer_id', 'persona_tag', 'segment', 'age', 'age_group',
                                            'income_bracket', 'gender', 'address_state']], on='customer_id')
df_acc = df_account.merge(df_customer[['customer_id', 'persona_tag', 'segment', 'age', 'age_group',
                                        'income_bracket', 'gender']], on='customer_id')
df_int = df_interaction.merge(df_customer[['customer_id', 'persona_tag', 'segment', 'age_group',
                                            'income_bracket', 'gender']], on='customer_id')

# ============================================================
# FIGURE 1: BY AGE GROUP
# ============================================================
print("Creating Age Group analysis...")
fig1, axes = plt.subplots(2, 3, figsize=(18, 12))
fig1.suptitle('Analysis by AGE GROUP', fontsize=16, fontweight='bold')

# 1a. Spending by Age Group
ax = axes[0, 0]
debit_txn = df_txn[df_txn['transaction_type'] == 'debit']
age_spend = debit_txn.groupby('age_group')['amount'].agg(['mean', 'sum', 'count'])
ax.bar(age_spend.index.astype(str), age_spend['mean'], color=sns.color_palette("Blues_d", len(age_spend)))
ax.set_title('Average Transaction Amount by Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('Avg Amount ($)')
for i, v in enumerate(age_spend['mean']):
    ax.text(i, v + 5, f'${v:.0f}', ha='center', fontsize=9)

# 1b. Spending Category by Age
ax = axes[0, 1]
age_cat = pd.crosstab(debit_txn['age_group'], debit_txn['mcc_category'], normalize='index') * 100
top_cats = ['Travel', 'Groceries', 'Dining', 'Healthcare', 'Shopping']
age_cat[[c for c in top_cats if c in age_cat.columns]].plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Spending Categories by Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('% of Transactions')
ax.legend(title='Category', bbox_to_anchor=(1.02, 1), fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 1c. Products per Customer by Age
ax = axes[0, 2]
products_by_age = df_acc.groupby(['customer_id', 'age_group']).size().reset_index(name='products')
products_by_age = products_by_age.groupby('age_group')['products'].mean()
ax.bar(products_by_age.index.astype(str), products_by_age.values, color=sns.color_palette("Greens_d", len(products_by_age)))
ax.set_title('Avg Products per Customer by Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('Avg Products')
for i, v in enumerate(products_by_age.values):
    ax.text(i, v + 0.05, f'{v:.1f}', ha='center', fontsize=9)

# 1d. Channel Usage by Age
ax = axes[1, 0]
channel_age = pd.crosstab(df_int['age_group'], df_int['channel'], normalize='index') * 100
channel_age.plot(kind='bar', ax=ax, width=0.8, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
ax.set_title('Channel Preference by Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('% of Interactions')
ax.legend(title='Channel')
ax.tick_params(axis='x', rotation=45)

# 1e. Churn Rate by Age
ax = axes[1, 1]
churn_age = df_customer.groupby('age_group')['churn_status'].mean() * 100
ax.bar(churn_age.index.astype(str), churn_age.values, color='#e74c3c')
ax.set_title('Churn Rate by Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('Churn Rate (%)')
for i, v in enumerate(churn_age.values):
    ax.text(i, v + 0.3, f'{v:.1f}%', ha='center', fontsize=9)

# 1f. Balance by Age
ax = axes[1, 2]
casa_bal = df_acc[df_acc['account_type'] == 'CASA'].groupby('age_group')['current_balance'].agg(['mean', 'median'])
x = np.arange(len(casa_bal))
width = 0.35
ax.bar(x - width/2, casa_bal['mean']/1000, width, label='Mean', color='#3498db')
ax.bar(x + width/2, casa_bal['median']/1000, width, label='Median', color='#e74c3c')
ax.set_xticks(x)
ax.set_xticklabels(casa_bal.index.astype(str))
ax.set_title('CASA Balance by Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('Balance ($K)')
ax.legend()

plt.tight_layout()
plt.savefig('data/eda_by_age.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_by_age.png")

# ============================================================
# FIGURE 2: BY INCOME BRACKET
# ============================================================
print("Creating Income analysis...")
fig2, axes = plt.subplots(2, 3, figsize=(18, 12))
fig2.suptitle('Analysis by INCOME BRACKET', fontsize=16, fontweight='bold')

income_order = ['<25K', '25-50K', '50-100K', '100-250K', '250K+']

# 2a. Spending by Income
ax = axes[0, 0]
income_spend = debit_txn.groupby('income_bracket')['amount'].mean()
income_spend = income_spend.reindex([i for i in income_order if i in income_spend.index])
ax.bar(income_spend.index, income_spend.values, color=sns.color_palette("Oranges_d", len(income_spend)))
ax.set_title('Average Transaction by Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('Avg Amount ($)')
ax.tick_params(axis='x', rotation=45)

# 2b. Spending Category by Income
ax = axes[0, 1]
inc_cat = pd.crosstab(debit_txn['income_bracket'], debit_txn['mcc_category'], normalize='index') * 100
inc_cat = inc_cat.reindex([i for i in income_order if i in inc_cat.index])
inc_cat[[c for c in top_cats if c in inc_cat.columns]].plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Spending Categories by Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('% of Transactions')
ax.legend(title='Category', bbox_to_anchor=(1.02, 1), fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 2c. Card Type by Income
ax = axes[0, 2]
cards = df_acc[df_acc['account_type'] == 'Credit Card']
card_income = pd.crosstab(cards['income_bracket'], cards['product_name'], normalize='index') * 100
card_income = card_income.reindex([i for i in income_order if i in card_income.index])
card_income.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Credit Card Type by Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('% of Cards')
ax.legend(title='Card Type', fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 2d. Channel by Income
ax = axes[1, 0]
ch_inc = pd.crosstab(df_int['income_bracket'], df_int['channel'], normalize='index') * 100
ch_inc = ch_inc.reindex([i for i in income_order if i in ch_inc.index])
ch_inc.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Channel Preference by Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('% of Interactions')
ax.legend(title='Channel')
ax.tick_params(axis='x', rotation=45)

# 2e. Churn by Income
ax = axes[1, 1]
churn_inc = df_customer.groupby('income_bracket')['churn_status'].mean() * 100
churn_inc = churn_inc.reindex([i for i in income_order if i in churn_inc.index])
ax.bar(churn_inc.index, churn_inc.values, color='#9b59b6')
ax.set_title('Churn Rate by Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('Churn Rate (%)')
ax.tick_params(axis='x', rotation=45)
for i, v in enumerate(churn_inc.values):
    ax.text(i, v + 0.3, f'{v:.1f}%', ha='center', fontsize=9)

# 2f. Products by Income
ax = axes[1, 2]
prod_inc = df_acc.groupby(['customer_id', 'income_bracket']).size().reset_index(name='products')
prod_inc = prod_inc.groupby('income_bracket')['products'].mean()
prod_inc = prod_inc.reindex([i for i in income_order if i in prod_inc.index])
ax.bar(prod_inc.index, prod_inc.values, color='#1abc9c')
ax.set_title('Avg Products by Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('Avg Products')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('data/eda_by_income.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_by_income.png")

# ============================================================
# FIGURE 3: BY SEGMENT
# ============================================================
print("Creating Segment analysis...")
fig3, axes = plt.subplots(2, 3, figsize=(18, 12))
fig3.suptitle('Analysis by SEGMENT', fontsize=16, fontweight='bold')

segment_order = ['Mass Market', 'Affluent', 'High Net Worth']
colors_seg = ['#3498db', '#f39c12', '#27ae60']

# 3a. Customer Count & Balance by Segment
ax = axes[0, 0]
seg_stats = df_customer.groupby('segment').agg({'customer_id': 'count'}).rename(columns={'customer_id': 'count'})
seg_stats = seg_stats.reindex(segment_order)
casa_seg = df_acc[df_acc['account_type'] == 'CASA'].groupby('segment')['current_balance'].mean()
ax2 = ax.twinx()
ax.bar(seg_stats.index, seg_stats['count'], color=colors_seg, alpha=0.7, label='Customers')
ax2.plot(seg_stats.index, casa_seg.reindex(segment_order)/1000, 'ro-', linewidth=2, markersize=8, label='Avg Balance')
ax.set_title('Customers & Avg Balance by Segment', fontsize=11)
ax.set_ylabel('Customer Count')
ax2.set_ylabel('Avg Balance ($K)', color='red')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# 3b. Spending Category by Segment
ax = axes[0, 1]
seg_cat = pd.crosstab(debit_txn['segment'], debit_txn['mcc_category'], normalize='index') * 100
seg_cat = seg_cat.reindex(segment_order)
seg_cat[[c for c in top_cats if c in seg_cat.columns]].plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Spending Categories by Segment', fontsize=11)
ax.set_xlabel('Segment')
ax.set_ylabel('% of Transactions')
ax.legend(title='Category', fontsize=8)
ax.tick_params(axis='x', rotation=0)

# 3c. Transaction Amounts by Segment (box plot)
ax = axes[0, 2]
seg_amounts = [debit_txn[debit_txn['segment'] == s]['amount'].values for s in segment_order]
# Cap at 2000 for visibility
seg_amounts_capped = [[min(x, 2000) for x in arr] for arr in seg_amounts]
bp = ax.boxplot(seg_amounts_capped, labels=segment_order, patch_artist=True)
for patch, color in zip(bp['boxes'], colors_seg):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_title('Transaction Amount Distribution by Segment', fontsize=11)
ax.set_ylabel('Amount ($) - capped at $2K')

# 3d. Account Types by Segment
ax = axes[1, 0]
acc_seg = pd.crosstab(df_acc['segment'], df_acc['account_type'], normalize='index') * 100
acc_seg = acc_seg.reindex(segment_order)
acc_seg.plot(kind='bar', ax=ax, stacked=True, width=0.8)
ax.set_title('Account Type Mix by Segment', fontsize=11)
ax.set_xlabel('Segment')
ax.set_ylabel('% of Accounts')
ax.legend(title='Account Type', bbox_to_anchor=(1.02, 1), fontsize=8)
ax.tick_params(axis='x', rotation=0)

# 3e. Churn & Sentiment by Segment
ax = axes[1, 1]
churn_seg = df_customer.groupby('segment')['churn_status'].mean() * 100
churn_seg = churn_seg.reindex(segment_order)
sent_seg = df_int.groupby('segment')['sentiment_score'].mean()
sent_seg = sent_seg.reindex(segment_order)
x = np.arange(len(segment_order))
width = 0.35
ax.bar(x - width/2, churn_seg.values, width, label='Churn Rate %', color='#e74c3c')
ax2 = ax.twinx()
ax2.bar(x + width/2, sent_seg.values * 100, width, label='Sentiment (x100)', color='#2ecc71')
ax.set_xticks(x)
ax.set_xticklabels(segment_order)
ax.set_title('Churn Rate & Sentiment by Segment', fontsize=11)
ax.set_ylabel('Churn Rate (%)', color='#e74c3c')
ax2.set_ylabel('Sentiment Score (x100)', color='#2ecc71')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# 3f. Channel by Segment
ax = axes[1, 2]
ch_seg = pd.crosstab(df_int['segment'], df_int['channel'], normalize='index') * 100
ch_seg = ch_seg.reindex(segment_order)
ch_seg.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Channel Preference by Segment', fontsize=11)
ax.set_xlabel('Segment')
ax.set_ylabel('% of Interactions')
ax.legend(title='Channel')
ax.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('data/eda_by_segment.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_by_segment.png")

# ============================================================
# FIGURE 4: BY GENDER
# ============================================================
print("Creating Gender analysis...")
fig4, axes = plt.subplots(2, 3, figsize=(18, 12))
fig4.suptitle('Analysis by GENDER', fontsize=16, fontweight='bold')

# 4a. Spending by Gender
ax = axes[0, 0]
gender_spend = debit_txn.groupby('gender')['amount'].agg(['mean', 'count'])
ax.bar(gender_spend.index, gender_spend['mean'], color=['#3498db', '#e74c3c', '#2ecc71'])
ax.set_title('Average Transaction by Gender', fontsize=11)
ax.set_ylabel('Avg Amount ($)')

# 4b. Category by Gender
ax = axes[0, 1]
gen_cat = pd.crosstab(debit_txn['gender'], debit_txn['mcc_category'], normalize='index') * 100
gen_cat[[c for c in top_cats if c in gen_cat.columns]].plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Spending Categories by Gender', fontsize=11)
ax.set_ylabel('% of Transactions')
ax.legend(title='Category', fontsize=8)
ax.tick_params(axis='x', rotation=0)

# 4c. Channel by Gender
ax = axes[0, 2]
ch_gen = pd.crosstab(df_int['gender'], df_int['channel'], normalize='index') * 100
ch_gen.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Channel Preference by Gender', fontsize=11)
ax.set_ylabel('% of Interactions')
ax.legend(title='Channel')
ax.tick_params(axis='x', rotation=0)

# 4d. Segment Distribution by Gender
ax = axes[1, 0]
seg_gen = pd.crosstab(df_customer['gender'], df_customer['segment'], normalize='index') * 100
seg_gen[segment_order].plot(kind='bar', ax=ax, width=0.8, color=colors_seg)
ax.set_title('Segment Distribution by Gender', fontsize=11)
ax.set_ylabel('% of Customers')
ax.legend(title='Segment')
ax.tick_params(axis='x', rotation=0)

# 4e. Churn by Gender
ax = axes[1, 1]
churn_gen = df_customer.groupby('gender')['churn_status'].mean() * 100
ax.bar(churn_gen.index, churn_gen.values, color=['#3498db', '#e74c3c', '#2ecc71'])
ax.set_title('Churn Rate by Gender', fontsize=11)
ax.set_ylabel('Churn Rate (%)')
for i, v in enumerate(churn_gen.values):
    ax.text(i, v + 0.3, f'{v:.1f}%', ha='center')

# 4f. Products by Gender
ax = axes[1, 2]
prod_gen = df_acc.groupby(['customer_id', 'gender']).size().reset_index(name='products')
prod_gen = prod_gen.groupby('gender')['products'].mean()
ax.bar(prod_gen.index, prod_gen.values, color=['#3498db', '#e74c3c', '#2ecc71'])
ax.set_title('Avg Products by Gender', fontsize=11)
ax.set_ylabel('Avg Products')

plt.tight_layout()
plt.savefig('data/eda_by_gender.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_by_gender.png")

# ============================================================
# FIGURE 5: BY GEOGRAPHY (State)
# ============================================================
print("Creating Geography analysis...")
fig5, axes = plt.subplots(2, 2, figsize=(16, 12))
fig5.suptitle('Analysis by GEOGRAPHY (State)', fontsize=16, fontweight='bold')

# 5a. Customers by State
ax = axes[0, 0]
state_counts = df_customer['address_state'].value_counts()
ax.bar(state_counts.index, state_counts.values, color=sns.color_palette("viridis", len(state_counts)))
ax.set_title('Customer Distribution by State', fontsize=11)
ax.set_ylabel('Customer Count')
ax.tick_params(axis='x', rotation=45)

# 5b. Avg Spending by State
ax = axes[0, 1]
state_spend = debit_txn.groupby('address_state')['amount'].mean().sort_values(ascending=False)
ax.bar(state_spend.index, state_spend.values, color=sns.color_palette("plasma", len(state_spend)))
ax.set_title('Average Transaction by State', fontsize=11)
ax.set_ylabel('Avg Amount ($)')
ax.tick_params(axis='x', rotation=45)

# 5c. Segment Mix by State
ax = axes[1, 0]
seg_state = pd.crosstab(df_customer['address_state'], df_customer['segment'], normalize='index') * 100
seg_state[segment_order].plot(kind='bar', ax=ax, stacked=True, width=0.8, color=colors_seg)
ax.set_title('Segment Mix by State', fontsize=11)
ax.set_ylabel('% of Customers')
ax.legend(title='Segment')
ax.tick_params(axis='x', rotation=45)

# 5d. Churn by State
ax = axes[1, 1]
churn_state = df_customer.groupby('address_state')['churn_status'].mean() * 100
churn_state = churn_state.sort_values(ascending=False)
ax.bar(churn_state.index, churn_state.values, color='#e74c3c')
ax.set_title('Churn Rate by State', fontsize=11)
ax.set_ylabel('Churn Rate (%)')
ax.tick_params(axis='x', rotation=45)
ax.axhline(y=churn_state.mean(), color='blue', linestyle='--', label=f'Avg: {churn_state.mean():.1f}%')
ax.legend()

plt.tight_layout()
plt.savefig('data/eda_by_geography.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_by_geography.png")

# ============================================================
# FIGURE 6: CROSS-DIMENSIONAL HEATMAPS
# ============================================================
print("Creating Cross-dimensional analysis...")
fig6, axes = plt.subplots(2, 2, figsize=(16, 14))
fig6.suptitle('CROSS-DIMENSIONAL Analysis (Heatmaps)', fontsize=16, fontweight='bold')

# 6a. Avg Spending: Age x Income
ax = axes[0, 0]
spend_age_inc = debit_txn.groupby(['age_group', 'income_bracket'])['amount'].mean().unstack()
spend_age_inc = spend_age_inc[[c for c in income_order if c in spend_age_inc.columns]]
sns.heatmap(spend_age_inc, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax)
ax.set_title('Avg Transaction: Age Group × Income', fontsize=11)
ax.set_xlabel('Income Bracket')
ax.set_ylabel('Age Group')

# 6b. Churn Rate: Persona x Segment
ax = axes[0, 1]
churn_ps = df_customer.groupby(['persona_tag', 'segment'])['churn_status'].mean().unstack() * 100
churn_ps = churn_ps[[c for c in segment_order if c in churn_ps.columns]]
sns.heatmap(churn_ps, annot=True, fmt='.1f', cmap='RdYlGn_r', ax=ax)
ax.set_title('Churn Rate %: Persona × Segment', fontsize=11)
ax.set_xlabel('Segment')
ax.set_ylabel('Persona')

# 6c. Products: Age x Segment
ax = axes[1, 0]
prod_as = df_acc.groupby(['customer_id', 'age_group', 'segment']).size().reset_index(name='products')
prod_as = prod_as.groupby(['age_group', 'segment'])['products'].mean().unstack()
prod_as = prod_as[[c for c in segment_order if c in prod_as.columns]]
sns.heatmap(prod_as, annot=True, fmt='.1f', cmap='Blues', ax=ax)
ax.set_title('Avg Products: Age Group × Segment', fontsize=11)
ax.set_xlabel('Segment')
ax.set_ylabel('Age Group')

# 6d. Channel App Usage: Persona x Age
ax = axes[1, 1]
app_usage = df_int[df_int['channel'] == 'App'].groupby(['persona_tag', 'age_group']).size()
total_int = df_int.groupby(['persona_tag', 'age_group']).size()
app_pct = (app_usage / total_int * 100).unstack()
sns.heatmap(app_pct, annot=True, fmt='.0f', cmap='Greens', ax=ax)
ax.set_title('App Channel Usage %: Persona × Age', fontsize=11)
ax.set_xlabel('Age Group')
ax.set_ylabel('Persona')

plt.tight_layout()
plt.savefig('data/eda_cross_dimensional.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_cross_dimensional.png")

# ============================================================
# FIGURE 7: TIME-BASED ANALYSIS
# ============================================================
print("Creating Time-based analysis...")
fig7, axes = plt.subplots(2, 2, figsize=(16, 12))
fig7.suptitle('TIME-BASED Analysis', fontsize=16, fontweight='bold')

debit_txn = debit_txn.copy()
debit_txn['month'] = debit_txn['transaction_date'].dt.to_period('M')
debit_txn['quarter'] = debit_txn['transaction_date'].dt.to_period('Q')
debit_txn['day_of_week'] = debit_txn['transaction_date'].dt.day_name()

# 7a. Monthly Spending by Segment
ax = axes[0, 0]
monthly_seg = debit_txn.groupby(['month', 'segment'])['amount'].sum().unstack() / 1e6
monthly_seg.index = monthly_seg.index.astype(str)
monthly_seg[segment_order].iloc[::3].plot(ax=ax, marker='o', linewidth=2)  # Every 3rd month
ax.set_title('Monthly Spending by Segment ($M)', fontsize=11)
ax.set_xlabel('Month')
ax.set_ylabel('Total Spending ($M)')
ax.legend(title='Segment')
ax.tick_params(axis='x', rotation=45)

# 7b. Day of Week by Age Group
ax = axes[0, 1]
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_age = pd.crosstab(debit_txn['day_of_week'], debit_txn['age_group'], normalize='columns') * 100
dow_age = dow_age.reindex(day_order)
dow_age.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Day of Week Pattern by Age', fontsize=11)
ax.set_xlabel('Day of Week')
ax.set_ylabel('% of Transactions')
ax.legend(title='Age Group', fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 7c. Customer Acquisition over Time by Segment
ax = axes[1, 0]
df_customer['join_month'] = df_customer['join_date'].dt.to_period('M')
acq_seg = df_customer.groupby(['join_month', 'segment']).size().unstack(fill_value=0)
acq_seg.index = acq_seg.index.astype(str)
acq_seg[segment_order].cumsum().iloc[::3].plot(ax=ax, linewidth=2)
ax.set_title('Cumulative Customer Acquisition by Segment', fontsize=11)
ax.set_xlabel('Month')
ax.set_ylabel('Cumulative Customers')
ax.legend(title='Segment')
ax.tick_params(axis='x', rotation=45)

# 7d. Spending Seasonality by Persona
ax = axes[1, 1]
debit_txn['month_num'] = debit_txn['transaction_date'].dt.month
monthly_persona = debit_txn.groupby(['month_num', 'persona_tag'])['amount'].mean().unstack()
monthly_persona.plot(ax=ax, marker='o', linewidth=2)
ax.set_title('Monthly Spending Pattern by Persona', fontsize=11)
ax.set_xlabel('Month')
ax.set_ylabel('Avg Transaction ($)')
ax.legend(title='Persona', fontsize=8)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.tight_layout()
plt.savefig('data/eda_time_based.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_time_based.png")

# ============================================================
# FIGURE 8: ACCOUNT & PRODUCT ANALYSIS
# ============================================================
print("Creating Account/Product analysis...")
fig8, axes = plt.subplots(2, 3, figsize=(18, 12))
fig8.suptitle('ACCOUNT & PRODUCT Analysis', fontsize=16, fontweight='bold')

# 8a. Account Type by Age
ax = axes[0, 0]
acc_age = pd.crosstab(df_acc['age_group'], df_acc['account_type'], normalize='index') * 100
acc_age.plot(kind='bar', ax=ax, stacked=True, width=0.8)
ax.set_title('Account Type Mix by Age', fontsize=11)
ax.set_ylabel('% of Accounts')
ax.legend(title='Account Type', bbox_to_anchor=(1.02, 1), fontsize=8)
ax.tick_params(axis='x', rotation=45)

# 8b. Credit Limit by Age & Segment
ax = axes[0, 1]
# cards already has age_group from df_acc merge
cl_age_seg = cards.groupby(['age_group', 'segment'])['credit_limit'].mean().unstack() / 1000
cl_age_seg[[c for c in segment_order if c in cl_age_seg.columns]].plot(kind='bar', ax=ax, width=0.8, color=colors_seg)
ax.set_title('Avg Credit Limit by Age & Segment ($K)', fontsize=11)
ax.set_ylabel('Credit Limit ($K)')
ax.legend(title='Segment')
ax.tick_params(axis='x', rotation=45)

# 8c. Loan Amount by Age
ax = axes[0, 2]
loans = df_acc[df_acc['account_type'] == 'Loan']
loan_age = loans.groupby('age_group')['principal_amount'].mean() / 1000
ax.bar(loan_age.index.astype(str), loan_age.values, color='#9b59b6')
ax.set_title('Avg Loan Principal by Age ($K)', fontsize=11)
ax.set_ylabel('Principal ($K)')

# 8d. Insurance Coverage by Segment
ax = axes[1, 0]
insurance = df_acc[df_acc['account_type'] == 'Insurance']
ins_seg = insurance.groupby('segment')['coverage_amount'].agg(['mean', 'median']) / 1000
ins_seg = ins_seg.reindex(segment_order)
x = np.arange(len(ins_seg))
width = 0.35
ax.bar(x - width/2, ins_seg['mean'], width, label='Mean', color='#3498db')
ax.bar(x + width/2, ins_seg['median'], width, label='Median', color='#e74c3c')
ax.set_xticks(x)
ax.set_xticklabels(ins_seg.index)
ax.set_title('Insurance Coverage by Segment ($K)', fontsize=11)
ax.set_ylabel('Coverage ($K)')
ax.legend()

# 8e. Securities Value by Income
ax = axes[1, 1]
securities = df_acc[df_acc['account_type'] == 'Securities']
sec_inc = securities.groupby('income_bracket')['current_value'].mean() / 1000
sec_inc = sec_inc.reindex([i for i in income_order if i in sec_inc.index])
ax.bar(sec_inc.index, sec_inc.values, color='#27ae60')
ax.set_title('Avg Securities Value by Income ($K)', fontsize=11)
ax.set_ylabel('Value ($K)')
ax.tick_params(axis='x', rotation=45)

# 8f. CD Holdings by Age
ax = axes[1, 2]
cds = df_acc[df_acc['account_type'] == 'CD']
cd_age = cds.groupby('age_group').agg({'customer_id': 'count', 'principal_amount': 'mean'})
cd_age.columns = ['count', 'avg_amount']
ax2 = ax.twinx()
ax.bar(cd_age.index.astype(str), cd_age['count'], color='#f39c12', alpha=0.7, label='Count')
ax2.plot(cd_age.index.astype(str), cd_age['avg_amount']/1000, 'bo-', linewidth=2, label='Avg Amount')
ax.set_title('CD Holdings by Age', fontsize=11)
ax.set_ylabel('Number of CDs', color='#f39c12')
ax2.set_ylabel('Avg Amount ($K)', color='blue')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig('data/eda_accounts_products.png', dpi=150, bbox_inches='tight')
print("Saved: data/eda_accounts_products.png")

print("\n" + "="*70)
print("ALL MULTI-DIMENSIONAL EDA COMPLETE")
print("="*70)
print("\nFiles saved:")
print("  - data/eda_by_age.png")
print("  - data/eda_by_income.png")
print("  - data/eda_by_segment.png")
print("  - data/eda_by_gender.png")
print("  - data/eda_by_geography.png")
print("  - data/eda_cross_dimensional.png")
print("  - data/eda_time_based.png")
print("  - data/eda_accounts_products.png")
