view: dim_product {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.dim_product` ;;

  dimension: product_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.product_id ;;
  }

  dimension: product_name {
    type: string
    sql: ${TABLE}.product_name ;;
  }

  dimension: product_type {
    type: string
    sql: ${TABLE}.product_type ;;
  }

  dimension: product_category {
    type: string
    sql: ${TABLE}.product_category ;;
  }

  dimension: description {
    type: string
    sql: ${TABLE}.description ;;
  }

  dimension: min_balance {
    type: number
    sql: ${TABLE}.min_balance ;;
    value_format_name: usd
  }

  dimension: annual_fee {
    type: number
    sql: ${TABLE}.annual_fee ;;
    value_format_name: usd
  }

  dimension: interest_rate_min {
    type: number
    sql: ${TABLE}.interest_rate_min ;;
    value_format_name: percent_2
  }

  dimension: interest_rate_max {
    type: number
    sql: ${TABLE}.interest_rate_max ;;
    value_format_name: percent_2
  }

  dimension: is_active {
    type: yesno
    sql: ${TABLE}.is_active ;;
  }

  measure: count {
    type: count
    drill_fields: [product_id, product_name, product_category]
  }
}
