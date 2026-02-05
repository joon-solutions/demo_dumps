view: dim_merchant {
  sql_table_name: `joon-4-joon.retail_banking_demo_duongvt.dim_merchant` ;;

  dimension: merchant_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.merchant_id ;;
  }

  dimension: merchant_name {
    type: string
    sql: ${TABLE}.merchant_name ;;
  }

  dimension: mcc_code {
    type: string
    sql: ${TABLE}.mcc_code ;;
    label: "MCC Code"
  }

  dimension: mcc_category {
    type: string
    sql: ${TABLE}.mcc_category ;;
    label: "Spending Category"
  }

  dimension: merchant_type {
    type: string
    sql: ${TABLE}.merchant_type ;;
  }

  dimension: is_subscription_merchant {
    type: yesno
    sql: ${TABLE}.is_subscription_merchant ;;
  }

  measure: count {
    type: count
    drill_fields: [merchant_id, merchant_name, mcc_category]
  }
}
