view: dim_account {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.dim_account` ;;

  # --- Primary Key ---
  dimension: account_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.account_id ;;
  }

  # --- Foreign Key ---
  dimension: customer_id {
    type: string
    hidden: yes
    sql: ${TABLE}.customer_id ;;
  }

  # --- Account Info ---
  dimension: account_type {
    type: string
    sql: ${TABLE}.account_type ;;
  }

  dimension: product_name {
    type: string
    sql: ${TABLE}.product_name ;;
  }

  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }

  dimension: account_number {
    type: string
    sql: ${TABLE}.account_number ;;
    label: "Account Number (Masked)"
  }

  dimension: currency {
    type: string
    sql: ${TABLE}.currency ;;
  }

  # --- Dates ---
  dimension_group: open {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.open_date ;;
  }

  dimension_group: maturity {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.maturity_date ;;
  }

  dimension: account_age_months {
    type: number
    sql: DATE_DIFF(CURRENT_DATE(), ${open_date}, MONTH) ;;
  }

  # --- Balance Fields ---
  dimension: current_balance {
    type: number
    sql: ${TABLE}.current_balance ;;
    value_format_name: usd
  }

  dimension: average_balance {
    type: number
    sql: ${TABLE}.average_balance ;;
    value_format_name: usd
  }

  # --- Credit Card Fields ---
  dimension: credit_limit {
    type: number
    sql: ${TABLE}.credit_limit ;;
    value_format_name: usd
  }

  dimension: available_balance {
    type: number
    sql: ${TABLE}.available_balance ;;
    value_format_name: usd
  }

  dimension: outstanding_balance {
    type: number
    sql: ${TABLE}.outstanding_balance ;;
    value_format_name: usd
  }

  dimension: credit_utilization {
    type: number
    sql: SAFE_DIVIDE(${outstanding_balance}, ${credit_limit}) ;;
    value_format_name: percent_1
  }

  dimension: credit_utilization_tier {
    type: tier
    tiers: [10, 30, 50, 75, 90]
    style: relational
    sql: ${credit_utilization} * 100 ;;
  }

  # --- Loan Fields ---
  dimension: principal_amount {
    type: number
    sql: ${TABLE}.principal_amount ;;
    value_format_name: usd
  }

  dimension: interest_rate {
    type: number
    sql: ${TABLE}.interest_rate ;;
    value_format_name: percent_2
  }

  dimension: loan_term_months {
    type: number
    sql: ${TABLE}.loan_term_months ;;
  }

  dimension: payoff_amount {
    type: number
    sql: ${TABLE}.payoff_amount ;;
    value_format_name: usd
  }

  # --- CD Fields ---
  dimension: cd_term_months {
    type: number
    sql: ${TABLE}.cd_term_months ;;
    label: "CD Term (Months)"
  }

  dimension: annual_yield {
    type: number
    sql: ${TABLE}.annual_yield ;;
    value_format_name: percent_2
    label: "APY"
  }

  # --- Insurance Fields ---
  dimension: coverage_amount {
    type: number
    sql: ${TABLE}.coverage_amount ;;
    value_format_name: usd
  }

  dimension: premium_amount {
    type: number
    sql: ${TABLE}.premium_amount ;;
    value_format_name: usd
  }

  dimension: beneficiary_count {
    type: number
    sql: ${TABLE}.beneficiary_count ;;
  }

  dimension: policy_status {
    type: string
    sql: ${TABLE}.policy_status ;;
  }

  dimension: policy_sub_status {
    type: string
    sql: ${TABLE}.policy_sub_status ;;
  }

  # --- Securities Fields ---
  dimension: security_type {
    type: string
    sql: ${TABLE}.security_type ;;
  }

  dimension: units_held {
    type: number
    sql: ${TABLE}.units_held ;;
  }

  dimension: purchase_price {
    type: number
    sql: ${TABLE}.purchase_price ;;
    value_format_name: usd
  }

  dimension: current_value {
    type: number
    sql: ${TABLE}.current_value ;;
    value_format_name: usd
  }

  dimension: unrealized_gain_loss {
    type: number
    sql: ${current_value} - (${units_held} * ${purchase_price}) ;;
    value_format_name: usd
  }

  # --- Tax Info ---
  dimension: tin_type {
    type: string
    sql: ${TABLE}.tin_type ;;
    label: "TIN Type"
  }

  dimension: tin_number {
    type: string
    sql: ${TABLE}.tin_number ;;
    label: "TIN (Masked)"
  }

  # --- Measures ---
  measure: count {
    type: count
    drill_fields: [account_detail*]
  }

  measure: count_active {
    type: count
    filters: [status: "Active"]
  }

  measure: total_balance {
    type: sum
    sql: ${current_balance} ;;
    value_format_name: usd_0
    drill_fields: [account_detail*]
  }

  measure: total_assets {
    type: sum
    sql: CASE
           WHEN ${account_type} IN ('CASA', 'CD', 'Securities')
           THEN ${current_balance}
           ELSE 0
         END ;;
    value_format_name: usd_0
    label: "Total AUM"
  }

  measure: total_liabilities {
    type: sum
    sql: CASE
           WHEN ${account_type} IN ('Loan', 'Credit Card')
           THEN ${current_balance}
           ELSE 0
         END ;;
    value_format_name: usd_0
    label: "Total LUM"
  }

  measure: total_credit_limit {
    type: sum
    sql: ${credit_limit} ;;
    value_format_name: usd_0
    filters: [account_type: "Credit Card"]
  }

  measure: total_outstanding {
    type: sum
    sql: ${outstanding_balance} ;;
    value_format_name: usd_0
  }

  measure: average_credit_utilization {
    type: average
    sql: ${credit_utilization} ;;
    value_format_name: percent_1
    filters: [account_type: "Credit Card"]
  }

  measure: total_coverage_amount {
    type: sum
    sql: ${coverage_amount} ;;
    value_format_name: usd_0
    filters: [account_type: "Insurance"]
  }

  measure: total_securities_value {
    type: sum
    sql: ${current_value} ;;
    value_format_name: usd_0
    filters: [account_type: "Securities"]
  }

  measure: average_products_per_customer {
    type: number
    sql: ${count} / NULLIF(${dim_customer.count}, 0) ;;
    value_format_name: decimal_2
    label: "Share of Wallet"
  }

  # --- Drill Sets ---
  set: account_detail {
    fields: [
      account_id,
      account_type,
      product_name,
      status,
      current_balance,
      open_date
    ]
  }
}
