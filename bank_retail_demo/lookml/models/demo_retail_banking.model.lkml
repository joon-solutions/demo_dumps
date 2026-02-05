connection: "joon-4-joon"

# Include all views
include: "/views/*.view.lkml"

# Include all dashboards
include: "/dashboards/*.dashboard.lookml"

# =====================================================
# MAIN EXPLORE: Customer 360
# =====================================================
# This is the primary explore for the Customer 360 dashboard
# It connects all tables with dim_customer at the center

explore: demo_retail_banking {
  label: "demo_retail_banking"
  description: "Complete customer view with accounts, transactions, and interactions"

  from: dim_customer
  view_name: dim_customer

  # --- Accounts ---
  join: dim_account {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_customer.customer_id} = ${dim_account.customer_id} ;;
  }

  # --- Products (via Account) ---
  join: dim_product {
    type: left_outer
    relationship: many_to_one
    sql_on: ${dim_account.product_name} = ${dim_product.product_name} ;;
  }

  # --- Transactions ---
  join: fact_transaction {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_customer.customer_id} = ${fact_transaction.customer_id} ;;
  }

  # --- Merchants (via Transaction) ---
  join: dim_merchant {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_transaction.merchant_id} = ${dim_merchant.merchant_id} ;;
  }

  # --- Interactions ---
  join: fact_interaction {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_customer.customer_id} = ${fact_interaction.customer_id} ;;
  }

  # --- Loan Schedule ---
  join: fact_loan_schedule {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_customer.customer_id} = ${fact_loan_schedule.customer_id} ;;
  }

  # --- Account Snapshots ---
  join: fact_account_snapshot {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_customer.customer_id} = ${fact_account_snapshot.customer_id} ;;
  }
}

# =====================================================
# EXPLORE: Transactions Analysis
# =====================================================
# Optimized for transaction-level analysis and spending patterns

explore: transactions {
  label: "Transaction Analysis"
  description: "Analyze spending patterns, categories, and transaction trends"

  from: fact_transaction
  view_name: fact_transaction

  join: dim_customer {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_transaction.customer_id} = ${dim_customer.customer_id} ;;
  }

  join: dim_account {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_transaction.account_id} = ${dim_account.account_id} ;;
  }

  join: dim_merchant {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_transaction.merchant_id} = ${dim_merchant.merchant_id} ;;
  }

  join: dim_date {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_transaction.date_key} = ${dim_date.date_key} ;;
  }
}

# =====================================================
# EXPLORE: Account Portfolio
# =====================================================
# Account-centric view for portfolio analysis

explore: accounts {
  label: "Account Portfolio"
  description: "Analyze account holdings, balances, and product mix"

  from: dim_account
  view_name: dim_account

  join: dim_customer {
    type: left_outer
    relationship: many_to_one
    sql_on: ${dim_account.customer_id} = ${dim_customer.customer_id} ;;
  }

  join: dim_product {
    type: left_outer
    relationship: many_to_one
    sql_on: ${dim_account.product_name} = ${dim_product.product_name} ;;
  }

  join: fact_account_snapshot {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_account.account_id} = ${fact_account_snapshot.account_id} ;;
  }

  join: fact_loan_schedule {
    type: left_outer
    relationship: one_to_many
    sql_on: ${dim_account.account_id} = ${fact_loan_schedule.account_id} ;;
  }
}

# =====================================================
# EXPLORE: Customer Interactions
# =====================================================
# Interaction-centric view for service analysis

explore: interactions {
  label: "Customer Interactions"
  description: "Analyze customer service interactions, sentiment, and channel usage"

  from: fact_interaction
  view_name: fact_interaction

  join: dim_customer {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_interaction.customer_id} = ${dim_customer.customer_id} ;;
  }

  join: dim_date {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_interaction.date_key} = ${dim_date.date_key} ;;
  }
}

# =====================================================
# EXPLORE: Loan Performance
# =====================================================
# Loan-specific analysis for delinquency and payment tracking

explore: loan_performance {
  label: "Loan Performance"
  description: "Track loan payments, delinquency, and amortization"

  from: fact_loan_schedule
  view_name: fact_loan_schedule

  join: dim_account {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_loan_schedule.account_id} = ${dim_account.account_id} ;;
  }

  join: dim_customer {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_loan_schedule.customer_id} = ${dim_customer.customer_id} ;;
  }

  join: dim_date {
    type: left_outer
    relationship: many_to_one
    sql_on: ${fact_loan_schedule.date_key} = ${dim_date.date_key} ;;
  }
}
