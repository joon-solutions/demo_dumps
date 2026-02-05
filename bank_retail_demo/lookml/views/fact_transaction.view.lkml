view: fact_transaction {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.fact_transaction` ;;

  # --- Primary Key ---
  dimension: transaction_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.transaction_id ;;
  }

  # --- Foreign Keys ---
  dimension: customer_id {
    type: string
    hidden: yes
    sql: ${TABLE}.customer_id ;;
  }

  dimension: account_id {
    type: string
    hidden: yes
    sql: ${TABLE}.account_id ;;
  }

  dimension: merchant_id {
    type: string
    hidden: yes
    sql: ${TABLE}.merchant_id ;;
  }

  dimension: date_key {
    type: number
    hidden: yes
    sql: ${TABLE}.date_key ;;
  }

  # --- Transaction Details ---
  dimension_group: transaction {
    type: time
    timeframes: [raw, date, week, month, month_name, quarter, year, day_of_week]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.transaction_date ;;
  }

  dimension: amount {
    type: number
    sql: ${TABLE}.amount ;;
    value_format_name: usd
  }

  dimension: amount_tier {
    type: tier
    tiers: [10, 50, 100, 250, 500, 1000]
    style: relational
    sql: ${amount} ;;
    value_format_name: usd
  }

  dimension: transaction_type {
    type: string
    sql: ${TABLE}.transaction_type ;;
  }

  dimension: is_debit {
    type: yesno
    sql: ${transaction_type} = 'debit' ;;
  }

  dimension: is_credit {
    type: yesno
    sql: ${transaction_type} = 'credit' ;;
  }

  dimension: payment_method {
    type: string
    sql: ${TABLE}.payment_method ;;
  }

  dimension: mcc_category {
    type: string
    sql: ${TABLE}.mcc_category ;;
    label: "Spending Category"
  }

  # --- Recurring Flags ---
  dimension: is_recurring {
    type: yesno
    sql: ${TABLE}.is_recurring ;;
  }

  dimension: recurring_frequency {
    type: string
    sql: ${TABLE}.recurring_frequency ;;
  }

  # --- Counterparty ---
  dimension: counterparty_type {
    type: string
    sql: ${TABLE}.counterparty_type ;;
  }

  dimension: counterparty_name {
    type: string
    sql: ${TABLE}.counterparty_name ;;
  }

  dimension: description {
    type: string
    sql: ${TABLE}.description ;;
  }

  # --- Channel ---
  dimension: channel {
    type: string
    sql: ${TABLE}.channel ;;
  }

  dimension: reference_number {
    type: string
    sql: ${TABLE}.reference_number ;;
  }

  # --- Measures ---
  measure: count {
    type: count
    drill_fields: [transaction_detail*]
  }

  measure: total_amount {
    type: sum
    sql: ${amount} ;;
    value_format_name: usd_0
    drill_fields: [transaction_detail*]
  }

  measure: average_amount {
    type: average
    sql: ${amount} ;;
    value_format_name: usd
  }

  measure: total_debits {
    type: sum
    sql: ${amount} ;;
    filters: [transaction_type: "debit"]
    value_format_name: usd_0
    label: "Total Spending"
  }

  measure: total_credits {
    type: sum
    sql: ${amount} ;;
    filters: [transaction_type: "credit"]
    value_format_name: usd_0
    label: "Total Income"
  }

  measure: net_cash_flow {
    type: number
    sql: ${total_credits} - ${total_debits} ;;
    value_format_name: usd_0
  }

  measure: count_recurring {
    type: count
    filters: [is_recurring: "yes"]
  }

  measure: recurring_spend {
    type: sum
    sql: ${amount} ;;
    filters: [is_recurring: "yes", transaction_type: "debit"]
    value_format_name: usd_0
  }

  measure: average_transaction_per_customer {
    type: number
    sql: ${count} / NULLIF(${dim_customer.count}, 0) ;;
    value_format_name: decimal_1
    label: "Avg Transactions per Customer"
  }

  measure: average_spend_per_customer {
    type: number
    sql: ${total_debits} / NULLIF(${dim_customer.count}, 0) ;;
    value_format_name: usd_0
    label: "Avg Spend per Customer"
  }

  # --- Drill Sets ---
  set: transaction_detail {
    fields: [
      transaction_id,
      transaction_date,
      amount,
      transaction_type,
      mcc_category,
      counterparty_name
    ]
  }
}
