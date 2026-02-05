view: dim_date {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.dim_date` ;;

  dimension: date_key {
    primary_key: yes
    type: number
    sql: ${TABLE}.date_key ;;
    hidden: yes
  }

  dimension_group: full {
    type: time
    timeframes: [raw, date, week, month, month_name, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.full_date ;;
    label: ""
  }

  dimension: year {
    type: number
    sql: ${TABLE}.year ;;
  }

  dimension: quarter {
    type: number
    sql: ${TABLE}.quarter ;;
  }

  dimension: month {
    type: number
    sql: ${TABLE}.month ;;
  }

  dimension: month_name {
    type: string
    sql: ${TABLE}.month_name ;;
  }

  dimension: week_of_year {
    type: number
    sql: ${TABLE}.week_of_year ;;
  }

  dimension: day_of_month {
    type: number
    sql: ${TABLE}.day_of_month ;;
  }

  dimension: day_of_week {
    type: number
    sql: ${TABLE}.day_of_week ;;
    description: "0=Monday, 6=Sunday"
  }

  dimension: day_name {
    type: string
    sql: ${TABLE}.day_name ;;
  }

  dimension: is_weekend {
    type: yesno
    sql: ${TABLE}.is_weekend ;;
  }

  dimension: is_holiday {
    type: yesno
    sql: ${TABLE}.is_holiday ;;
  }

  dimension: fiscal_year {
    type: number
    sql: ${TABLE}.fiscal_year ;;
  }

  dimension: fiscal_quarter {
    type: number
    sql: ${TABLE}.fiscal_quarter ;;
  }

  measure: count {
    type: count
    hidden: yes
  }
}
