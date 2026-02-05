view: fact_loan_schedule {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.fact_loan_schedule` ;;

  dimension: schedule_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.schedule_id ;;
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

  # --- Payment Schedule ---
  dimension_group: due {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.due_date ;;
  }

  dimension: payment_number {
    type: number
    sql: ${TABLE}.payment_number ;;
  }

  dimension: total_payments {
    type: number
    sql: ${TABLE}.total_payments ;;
  }

  dimension: payment_progress {
    type: number
    sql: ${payment_number} / NULLIF(${total_payments}, 0) ;;
    value_format_name: percent_0
  }

  # --- Payment Amounts ---
  dimension: payment_due {
    type: number
    sql: ${TABLE}.payment_due ;;
    value_format_name: usd
  }

  dimension: principal_portion {
    type: number
    sql: ${TABLE}.principal_portion ;;
    value_format_name: usd
  }

  dimension: interest_portion {
    type: number
    sql: ${TABLE}.interest_portion ;;
    value_format_name: usd
  }

  # --- Payment Status ---
  dimension: payment_status {
    type: string
    sql: ${TABLE}.payment_status ;;
  }

  dimension_group: actual_payment {
    type: time
    timeframes: [raw, date]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.actual_payment_date ;;
  }

  dimension: actual_amount_paid {
    type: number
    sql: ${TABLE}.actual_amount_paid ;;
    value_format_name: usd
  }

  dimension: extra_principal_paid {
    type: number
    sql: ${TABLE}.extra_principal_paid ;;
    value_format_name: usd
  }

  # --- Delinquency ---
  dimension: days_past_due {
    type: number
    sql: ${TABLE}.days_past_due ;;
  }

  dimension: is_overdue {
    type: yesno
    sql: ${days_past_due} > 0 ;;
  }

  dimension: delinquency_bucket {
    type: string
    sql: CASE
           WHEN ${days_past_due} = 0 THEN 'Current'
           WHEN ${days_past_due} <= 30 THEN '1-30 DPD'
           WHEN ${days_past_due} <= 60 THEN '31-60 DPD'
           WHEN ${days_past_due} <= 90 THEN '61-90 DPD'
           ELSE '90+ DPD'
         END ;;
    label: "Days Past Due Bucket"
  }

  dimension: late_fee_charged {
    type: number
    sql: ${TABLE}.late_fee_charged ;;
    value_format_name: usd
  }

  # --- Balance Tracking ---
  dimension: cumulative_principal_paid {
    type: number
    sql: ${TABLE}.cumulative_principal_paid ;;
    value_format_name: usd
  }

  dimension: remaining_balance {
    type: number
    sql: ${TABLE}.remaining_balance ;;
    value_format_name: usd
  }

  # --- Measures ---
  measure: count {
    type: count
  }

  measure: count_scheduled {
    type: count
    filters: [payment_status: "Scheduled"]
  }

  measure: count_paid {
    type: count
    filters: [payment_status: "Paid"]
  }

  measure: count_overdue {
    type: count
    filters: [payment_status: "Overdue"]
  }

  measure: total_payment_due {
    type: sum
    sql: ${payment_due} ;;
    value_format_name: usd_0
  }

  measure: total_principal_paid {
    type: sum
    sql: ${principal_portion} ;;
    filters: [payment_status: "Paid"]
    value_format_name: usd_0
  }

  measure: total_interest_paid {
    type: sum
    sql: ${interest_portion} ;;
    filters: [payment_status: "Paid"]
    value_format_name: usd_0
  }

  measure: total_late_fees {
    type: sum
    sql: ${late_fee_charged} ;;
    value_format_name: usd_0
  }

  measure: overdue_rate {
    type: number
    sql: ${count_overdue} / NULLIF(${count}, 0) ;;
    value_format_name: percent_1
  }

  measure: average_days_past_due {
    type: average
    sql: ${days_past_due} ;;
    filters: [is_overdue: "yes"]
    value_format_name: decimal_1
  }
}
