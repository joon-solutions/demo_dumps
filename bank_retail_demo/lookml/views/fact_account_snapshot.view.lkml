view: fact_account_snapshot {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.fact_account_snapshot` ;;

  dimension: snapshot_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.snapshot_id ;;
  }

  # --- Foreign Keys ---
  dimension: account_id {
    type: string
    hidden: yes
    sql: ${TABLE}.account_id ;;
  }

  dimension: customer_id {
    type: string
    hidden: yes
    sql: ${TABLE}.customer_id ;;
  }

  dimension: date_key {
    type: number
    hidden: yes
    sql: ${TABLE}.date_key ;;
  }

  # --- Dates ---
  dimension_group: snapshot {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.snapshot_date ;;
  }

  # --- Balance Fields ---
  dimension: balance {
    type: number
    sql: ${TABLE}.balance ;;
    value_format_name: usd
  }

  dimension: month_avg_balance {
    type: number
    sql: ${TABLE}.month_avg_balance ;;
    value_format_name: usd
  }

  dimension: month_end_balance {
    type: number
    sql: ${TABLE}.month_end_balance ;;
    value_format_name: usd
  }

  # --- Credit Card Fields ---
  dimension: available_credit {
    type: number
    sql: ${TABLE}.available_credit ;;
    value_format_name: usd
  }

  dimension: credit_utilization_pct {
    type: number
    sql: ${TABLE}.credit_utilization_pct ;;
    value_format_name: percent_1
  }

  # --- Loan Fields ---
  dimension: principal_paid {
    type: number
    sql: ${TABLE}.principal_paid ;;
    value_format_name: usd
  }

  dimension: principal_remaining {
    type: number
    sql: ${TABLE}.principal_remaining ;;
    value_format_name: usd
  }

  dimension: interest_accrued {
    type: number
    sql: ${TABLE}.interest_accrued ;;
    value_format_name: usd
  }

  # --- Cash Flow ---
  dimension: total_credits_mtd {
    type: number
    sql: ${TABLE}.total_credits_mtd ;;
    value_format_name: usd
    label: "Credits MTD"
  }

  dimension: total_debits_mtd {
    type: number
    sql: ${TABLE}.total_debits_mtd ;;
    value_format_name: usd
    label: "Debits MTD"
  }

  dimension: net_cash_flow_mtd {
    type: number
    sql: ${TABLE}.net_cash_flow_mtd ;;
    value_format_name: usd
    label: "Net Cash Flow MTD"
  }

  # --- Product Count ---
  dimension: customer_product_count {
    type: number
    sql: ${TABLE}.customer_product_count ;;
  }

  # --- Measures ---
  measure: count {
    type: count
  }

  measure: total_balance {
    type: sum
    sql: ${balance} ;;
    value_format_name: usd_0
  }

  measure: average_balance {
    type: average
    sql: ${balance} ;;
    value_format_name: usd_0
  }

  measure: total_principal_remaining {
    type: sum
    sql: ${principal_remaining} ;;
    value_format_name: usd_0
  }

  measure: average_utilization {
    type: average
    sql: ${credit_utilization_pct} ;;
    value_format_name: percent_1
  }
}
