---
- dashboard: executive_overview
  title: "Executive Overview"
  layout: newspaper
  preferred_viewer: dashboards-next
  description: "Level A - Strategic portfolio health and customer insights"
  filters_location_top: true

  filters:
    - name: date_range
      title: "Date Range"
      type: date_filter
      default_value: "2024"
      allow_multiple_values: false

    - name: segment
      title: "Customer Segment"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.segment
      default_value: ""
      allow_multiple_values: true
      ui_config:
        type: checkboxes

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

    # Row 1: KPI Cards
    - title: "Total Customers"
      name: total_customers
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_customer.count]
      listen:
        segment: dim_customer.segment
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
        segment: dim_customer.segment
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
        segment: dim_customer.segment
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
        segment: dim_customer.segment
      row: 2
      col: 12
      width: 4
      height: 4

    - title: "Churn Rate"
      name: churn_rate
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_customer.churn_rate]
      listen:
        segment: dim_customer.segment
      row: 2
      col: 16
      width: 4
      height: 4

    - title: "Avg Sentiment"
      name: avg_sentiment
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [fact_interaction.average_sentiment]
      listen:
        segment: dim_customer.segment
      row: 2
      col: 20
      width: 4
      height: 4

    # Row 2: Portfolio Health - AUM vs LUM by Segment
    - title: "Portfolio Health: AUM vs LUM by Segment"
      name: portfolio_health
      type: looker_bar
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.segment]
      measures: [dim_account.total_assets, dim_account.total_liabilities]
      listen:
        segment: dim_customer.segment
      sorts: [dim_account.total_assets desc]
      row: 6
      col: 0
      width: 12
      height: 8
      series_colors:
        dim_account.total_assets: "#4285F4"
        dim_account.total_liabilities: "#EA4335"

    # Row 2: Customer Segment Distribution
    - title: "Customer Distribution by Segment"
      name: segment_distribution
      type: looker_pie
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.segment]
      measures: [dim_customer.count]
      listen:
        segment: dim_customer.segment
      row: 6
      col: 12
      width: 12
      height: 8
      series_colors:
        Mass Market: "#34A853"
        Affluent: "#4285F4"
        High Net Worth: "#9334E6"

    # Row 3: Product Holdings by Segment
    - title: "Product Holdings by Segment"
      name: segment_product_heatmap
      type: looker_grid
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.segment, dim_account.account_type]
      measures: [dim_account.count]
      pivots: [dim_account.account_type]
      listen:
        segment: dim_customer.segment
      row: 14
      col: 0
      width: 12
      height: 8

    # Row 3: Churn Rate by Segment
    - title: "Churn Rate by Segment"
      name: churn_by_segment
      type: looker_column
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.segment]
      measures: [dim_customer.churn_rate]
      listen:
        segment: dim_customer.segment
      row: 14
      col: 12
      width: 12
      height: 8
      series_colors:
        dim_customer.churn_rate: "#EA4335"

    # Row 4: Monthly Transaction Volume
    - title: "Monthly Transaction Volume"
      name: monthly_transaction_volume
      type: looker_column
      model: demo_retail_banking
      explore: transactions
      dimensions: [fact_transaction.transaction_month]
      measures: [fact_transaction.count]
      listen:
        segment: dim_customer.segment
      row: 22
      col: 0
      width: 12
      height: 8
      series_colors:
        fact_transaction.count: "#4285F4"

    # Row 4: Product Growth Over Time
    - title: "Product Growth by Type"
      name: product_growth
      type: looker_line
      model: demo_retail_banking
      explore: accounts
      dimensions: [dim_account.open_month]
      measures: [dim_account.count]
      pivots: [dim_account.account_type]
      listen:
        segment: dim_customer.segment
      sorts: [dim_account.open_month]
      row: 22
      col: 12
      width: 12
      height: 8
      series_colors:
        CASA: "#4285F4"
        Credit Card: "#EA4335"
        Loan: "#FBBC04"
        CD: "#34A853"
        Securities: "#9334E6"
        Insurance: "#FF6D01"

    # Row 5: Channel Usage
    - title: "Interaction Channel Mix"
      name: channel_mix
      type: looker_pie
      model: demo_retail_banking
      explore: interactions
      dimensions: [fact_interaction.channel]
      measures: [fact_interaction.count]
      listen:
        segment: dim_customer.segment
      row: 30
      col: 0
      width: 24
      height: 8
