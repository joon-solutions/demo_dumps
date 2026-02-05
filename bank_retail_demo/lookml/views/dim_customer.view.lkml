view: dim_customer {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.dim_customer` ;;

  # --- Primary Key ---
  dimension: customer_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.customer_id ;;
  }

  # --- Demographics ---
  dimension: first_name {
    type: string
    sql: ${TABLE}.first_name ;;
  }

  dimension: last_name {
    type: string
    sql: ${TABLE}.last_name ;;
  }

  dimension: full_name {
    type: string
    sql: CONCAT(${first_name}, ' ', ${last_name}) ;;
  }

  dimension_group: date_of_birth {
    type: time
    timeframes: [raw, date, month, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.date_of_birth ;;
  }

  dimension: age {
    type: number
    sql: ${TABLE}.age ;;
  }

  dimension: age_group {
    type: tier
    tiers: [18, 25, 35, 45, 55, 65]
    style: integer
    sql: ${age} ;;
  }

  dimension: gender {
    type: string
    sql: ${TABLE}.gender ;;
  }

  dimension: email {
    type: string
    sql: ${TABLE}.email ;;
  }

  dimension: phone {
    type: string
    sql: ${TABLE}.phone ;;
  }

  # --- Address ---
  dimension: address_city {
    type: string
    sql: ${TABLE}.address_city ;;
  }

  dimension: address_state {
    type: string
    sql: ${TABLE}.address_state ;;
    map_layer_name: us_states
  }

  dimension: address_country {
    type: string
    sql: ${TABLE}.address_country ;;
  }

  dimension: full_address {
    type: string
    sql: CONCAT(${address_city}, ', ', ${address_state}) ;;
  }

  # --- Family ---
  dimension: marital_status {
    type: string
    sql: ${TABLE}.marital_status ;;
  }

  dimension: has_children {
    type: yesno
    sql: ${TABLE}.has_children ;;
  }

  dimension: num_dependents {
    type: number
    sql: ${TABLE}.num_dependents ;;
  }

  # --- Employment ---
  dimension: occupation {
    type: string
    sql: ${TABLE}.occupation ;;
  }

  dimension: employment_type {
    type: string
    sql: ${TABLE}.employment_type ;;
  }

  dimension: income_bracket {
    type: string
    sql: ${TABLE}.income_bracket ;;
    order_by_field: income_bracket_sort
  }

  dimension: income_bracket_sort {
    hidden: yes
    type: number
    sql: CASE ${income_bracket}
           WHEN '<25K' THEN 1
           WHEN '25-50K' THEN 2
           WHEN '50-100K' THEN 3
           WHEN '100-250K' THEN 4
           WHEN '250K+' THEN 5
           ELSE 6
         END ;;
  }

  dimension: home_ownership {
    type: string
    sql: ${TABLE}.home_ownership ;;
  }

  # --- Segmentation ---
  dimension: segment {
    type: string
    sql: ${TABLE}.segment ;;
  }

  dimension: persona_tag {
    type: string
    sql: ${TABLE}.persona_tag ;;
    label: "Persona"
  }

  dimension: risk_tolerance {
    type: string
    sql: ${TABLE}.risk_tolerance ;;
  }

  # --- Account Status ---
  dimension: kyc_status {
    type: string
    sql: ${TABLE}.kyc_status ;;
    label: "KYC Status"
  }

  dimension_group: join {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.join_date ;;
  }

  dimension: customer_tenure_months {
    type: number
    sql: DATE_DIFF(CURRENT_DATE(), ${join_date}, MONTH) ;;
  }

  dimension: preferred_channel {
    type: string
    sql: ${TABLE}.preferred_channel ;;
  }

  dimension: engagement_score {
    type: number
    sql: ${TABLE}.engagement_score ;;
  }

  dimension: engagement_tier {
    type: tier
    tiers: [25, 50, 75]
    style: integer
    sql: ${engagement_score} ;;
  }

  # --- Churn ---
  dimension: churn_status {
    type: yesno
    sql: ${TABLE}.churn_status ;;
    label: "Is Churned"
  }

  dimension_group: churn {
    type: time
    timeframes: [raw, date, month, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.churn_date ;;
  }

  # --- Measures ---
  measure: count {
    type: count
    drill_fields: [customer_detail*]
  }

  measure: count_churned {
    type: count
    filters: [churn_status: "yes"]
    drill_fields: [customer_detail*]
  }

  measure: churn_rate {
    type: number
    sql: ${count_churned} / NULLIF(${count}, 0) ;;
    value_format_name: percent_1
  }

  measure: average_age {
    type: average
    sql: ${age} ;;
    value_format_name: decimal_1
  }

  measure: average_engagement_score {
    type: average
    sql: ${engagement_score} ;;
    value_format_name: decimal_1
  }

  measure: average_tenure_months {
    type: average
    sql: ${customer_tenure_months} ;;
    value_format_name: decimal_1
  }

  # --- Drill Sets ---
  set: customer_detail {
    fields: [
      customer_id,
      full_name,
      segment,
      persona_tag,
      income_bracket,
      join_date
    ]
  }
}
