view: fact_interaction {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.fact_interaction` ;;

  dimension: interaction_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.interaction_id ;;
  }

  # --- Foreign Keys ---
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

  # --- Interaction Details ---
  dimension_group: interaction {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.interaction_date ;;
  }

  dimension: channel {
    type: string
    sql: ${TABLE}.channel ;;
  }

  dimension: interaction_type {
    type: string
    sql: ${TABLE}.interaction_type ;;
  }

  dimension: reason {
    type: string
    sql: ${TABLE}.reason ;;
  }

  dimension: sentiment_score {
    type: number
    sql: ${TABLE}.sentiment_score ;;
    value_format_name: decimal_2
  }

  dimension: sentiment_tier {
    type: string
    sql: CASE
           WHEN ${sentiment_score} >= 0.7 THEN 'Positive'
           WHEN ${sentiment_score} >= 0.4 THEN 'Neutral'
           ELSE 'Negative'
         END ;;
  }

  dimension: resolution_status {
    type: string
    sql: ${TABLE}.resolution_status ;;
  }

  dimension: duration_minutes {
    type: number
    sql: ${TABLE}.duration_minutes ;;
  }

  # --- Measures ---
  measure: count {
    type: count
    drill_fields: [interaction_detail*]
  }

  measure: average_sentiment {
    type: average
    sql: ${sentiment_score} ;;
    value_format_name: decimal_2
  }

  measure: average_duration {
    type: average
    sql: ${duration_minutes} ;;
    value_format_name: decimal_1
    label: "Avg Duration (mins)"
  }

  measure: count_negative_sentiment {
    type: count
    filters: [sentiment_tier: "Negative"]
  }

  measure: negative_sentiment_rate {
    type: number
    sql: ${count_negative_sentiment} / NULLIF(${count}, 0) ;;
    value_format_name: percent_1
  }

  measure: count_resolved {
    type: count
    filters: [resolution_status: "Resolved"]
  }

  measure: resolution_rate {
    type: number
    sql: ${count_resolved} / NULLIF(${count}, 0) ;;
    value_format_name: percent_1
  }

  # --- Drill Sets ---
  set: interaction_detail {
    fields: [
      interaction_id,
      interaction_date,
      channel,
      interaction_type,
      reason,
      sentiment_score,
      resolution_status
    ]
  }
}
