---
- dashboard: segment_analysis
  title: "Demographic & Segment Analysis"
  layout: newspaper
  preferred_viewer: dashboards-next
  description: "Level B - Deep dive into customer demographics, spending habits, and segment health"
  filters_location_top: true

  filters:
    # Primary Demographic Filters
    - name: gender
      title: "Gender"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.gender
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: button_toggles

    - name: age_group
      title: "Age Group"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.age_group
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: checkboxes

    - name: income_bracket
      title: "Income Bracket"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.income_bracket
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: checkboxes

    - name: occupation
      title: "Occupation"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.occupation
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: tag_list

    - name: segment
      title: "Segment"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.segment
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: button_toggles

    - name: persona
      title: "Persona"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.persona_tag
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: checkboxes

    - name: date_range
      title: "Date Range"
      type: date_filter
      default_value: "2024"

  elements:
    # Navigation Bar
    - name: navigation
      type: text
      title_text: ""
      body_text: "
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; text-align: center;'>
          <a style='color: white; background-color: #4285F4; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; margin: 0 10px; font-family: sans-serif;'
             href='/dashboards/demo_retail_banking::executive_overview'>Executive Overview</a>
          <a style='color: white; background-color: #4285F4; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; margin: 0 10px; font-family: sans-serif;'
             href='/dashboards/demo_retail_banking::segment_analysis'>Demographic & Segment</a>
          <a style='color: white; background-color: #4285F4; padding: 10px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; margin: 0 10px; font-family: sans-serif;'
             href='/dashboards/demo_retail_banking::customer_360_individual'>Customer 360</a>
        </div>"
      row: 0
      col: 0
      width: 24
      height: 2

    # =====================================================
    # ROW 1: KEY METRICS (6 KPIs)
    # =====================================================
    - title: "Total Customers"
      name: total_customers
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_customer.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 2
      col: 0
      width: 4
      height: 4

    - title: "Total AUM"
      name: total_aum
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_account.total_assets]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 2
      col: 4
      width: 4
      height: 4

    - title: "Total LUM"
      name: total_lum
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_account.total_liabilities]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 2
      col: 8
      width: 4
      height: 4

    - title: "Share of Wallet"
      name: share_of_wallet
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_account.average_products_per_customer]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 2
      col: 12
      width: 4
      height: 4

    - title: "Avg Sentiment"
      name: avg_sentiment
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [fact_interaction.average_sentiment]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 2
      col: 16
      width: 4
      height: 4

    - title: "Churn Rate"
      name: churn_rate
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_customer.churn_rate]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 2
      col: 20
      width: 4
      height: 4

    # =====================================================
    # ROW 2: DEMOGRAPHIC BREAKDOWN
    # =====================================================
    - title: "Customers by Gender"
      name: gender_distribution
      type: looker_pie
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.gender]
      measures: [dim_customer.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 6
      col: 0
      width: 6
      height: 6
      series_colors:
        Male: "#4285F4"
        Female: "#EA4335"

    - title: "Customers by Age Group"
      name: age_distribution
      type: looker_column
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.age_group]
      measures: [dim_customer.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 6
      col: 6
      width: 6
      height: 6
      series_colors:
        dim_customer.count: "#4285F4"

    - title: "Customers by Income Bracket"
      name: income_distribution
      type: looker_bar
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.income_bracket]
      measures: [dim_customer.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 6
      col: 12
      width: 6
      height: 6
      series_colors:
        dim_customer.count: "#34A853"

    - title: "Top Occupations"
      name: occupation_distribution
      type: looker_bar
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.occupation]
      measures: [dim_customer.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      sorts: [dim_customer.count desc]
      limit: 10
      row: 6
      col: 18
      width: 6
      height: 6
      series_colors:
        dim_customer.count: "#9334E6"

    # =====================================================
    # ROW 3: SPENDING TRENDS OVER TIME
    # =====================================================
    - title: "Spending by Category Over Time"
      name: spending_category_trend
      type: looker_line
      model: demo_retail_banking
      explore: transactions
      dimensions: [fact_transaction.transaction_month]
      measures: [fact_transaction.total_debits]
      pivots: [fact_transaction.mcc_category]
      filters:
        fact_transaction.mcc_category: "-Income"
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      sorts: [fact_transaction.transaction_month]
      row: 12
      col: 0
      width: 12
      height: 8

    - title: "Top 10 Merchants - Avg Spend per Customer"
      name: merchant_avg_per_customer
      type: looker_line
      model: demo_retail_banking
      explore: transactions
      dimensions: [fact_transaction.transaction_month]
      measures: [fact_transaction.average_spend_per_customer]
      pivots: [dim_merchant.merchant_name]
      filters:
        fact_transaction.mcc_category: "-Income"
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      sorts: [fact_transaction.average_spend_per_customer desc 0]
      limit: 500
      column_limit: 10
      row: 12
      col: 12
      width: 12
      height: 8

    # =====================================================
    # ROW 4: CUSTOMER ACQUISITION
    # =====================================================
    - title: "Customer Acquisition Over Time"
      name: customer_acquisition
      type: looker_column
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.join_month]
      measures: [dim_customer.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      sorts: [dim_customer.join_month]
      row: 20
      col: 0
      width: 24
      height: 8
      series_colors:
        dim_customer.count: "#4285F4"

    # =====================================================
    # ROW 5: SPENDING BY DEMOGRAPHICS
    # =====================================================
    - title: "Spending by Gender"
      name: spending_by_gender
      type: looker_bar
      model: demo_retail_banking
      explore: transactions
      dimensions: [dim_customer.gender]
      measures: [fact_transaction.total_debits, fact_transaction.average_amount]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 28
      col: 0
      width: 8
      height: 8
      series_colors:
        fact_transaction.total_debits: "#4285F4"
        fact_transaction.average_amount: "#34A853"

    - title: "Spending by Age Group"
      name: spending_by_age
      type: looker_column
      model: demo_retail_banking
      explore: transactions
      dimensions: [dim_customer.age_group]
      measures: [fact_transaction.total_debits]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 28
      col: 8
      width: 8
      height: 8
      series_colors:
        fact_transaction.total_debits: "#FBBC04"

    - title: "Spending by Income Bracket"
      name: spending_by_income
      type: looker_bar
      model: demo_retail_banking
      explore: transactions
      dimensions: [dim_customer.income_bracket]
      measures: [fact_transaction.total_debits]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 28
      col: 16
      width: 8
      height: 8
      series_colors:
        fact_transaction.total_debits: "#9334E6"

    # =====================================================
    # ROW 6: PRODUCT & BANKING RELATIONSHIP
    # =====================================================
    - title: "Product Mix"
      name: product_mix
      type: looker_pie
      model: demo_retail_banking
      explore: accounts
      dimensions: [dim_account.account_type]
      measures: [dim_account.count]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 36
      col: 0
      width: 8
      height: 8
      series_colors:
        CASA: "#4285F4"
        Credit Card: "#EA4335"
        Loan: "#FBBC04"
        CD: "#34A853"
        Securities: "#9334E6"
        Insurance: "#FF6D01"

    - title: "AUM by Income Bracket"
      name: aum_by_income
      type: looker_bar
      model: demo_retail_banking
      explore: accounts
      dimensions: [dim_customer.income_bracket]
      measures: [dim_account.total_assets]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 36
      col: 8
      width: 8
      height: 8
      series_colors:
        dim_account.total_assets: "#34A853"

    - title: "LUM by Age Group"
      name: lum_by_age
      type: looker_column
      model: demo_retail_banking
      explore: accounts
      dimensions: [dim_customer.age_group]
      measures: [dim_account.total_liabilities]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 36
      col: 16
      width: 8
      height: 8
      series_colors:
        dim_account.total_liabilities: "#EA4335"

    # =====================================================
    # ROW 7: CUSTOMER HEALTH - SENTIMENT & CHURN
    # =====================================================
    - title: "Sentiment by Age Group"
      name: sentiment_by_age
      type: looker_column
      model: demo_retail_banking
      explore: interactions
      dimensions: [dim_customer.age_group]
      measures: [fact_interaction.average_sentiment]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 44
      col: 0
      width: 8
      height: 8
      series_colors:
        fact_interaction.average_sentiment: "#34A853"

    - title: "Churn Rate by Income"
      name: churn_by_income
      type: looker_bar
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.income_bracket]
      measures: [dim_customer.churn_rate]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 44
      col: 8
      width: 8
      height: 8
      series_colors:
        dim_customer.churn_rate: "#EA4335"

    - title: "Churn Rate by Age Group"
      name: churn_by_age
      type: looker_column
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.age_group]
      measures: [dim_customer.churn_rate]
      listen:
        gender: dim_customer.gender
        age_group: dim_customer.age_group
        income_bracket: dim_customer.income_bracket
        occupation: dim_customer.occupation
        segment: dim_customer.segment
        persona: dim_customer.persona_tag
      row: 44
      col: 16
      width: 8
      height: 8
      series_colors:
        dim_customer.churn_rate: "#EA4335"


