---
- dashboard: customer_360_individual
  title: "Customer 360 - Individual View"
  layout: newspaper
  preferred_viewer: dashboards-next
  description: "Level C - Complete individual customer profile with portfolio details"
  filters_location_top: true

  filters:
    - name: customer_id
      title: "Customer ID"
      type: field_filter
      explore: demo_retail_banking
      field: dim_customer.customer_id
      default_value: ""
      allow_multiple_values: false
      required: true
      ui_config:
        type: advanced
        display: popover

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
    # PROFILE HEADER
    # =====================================================
    - title: "Customer Name"
      name: customer_name
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.full_name]
      listen:
        customer_id: dim_customer.customer_id
      row: 2
      col: 0
      width: 6
      height: 3

    - title: "Segment"
      name: customer_segment
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.segment]
      listen:
        customer_id: dim_customer.customer_id
      row: 2
      col: 6
      width: 3
      height: 3

    - title: "Persona"
      name: customer_persona
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.persona_tag]
      listen:
        customer_id: dim_customer.customer_id
      row: 2
      col: 9
      width: 3
      height: 3

    - title: "Total Balance"
      name: total_balance
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_account.total_balance]
      listen:
        customer_id: dim_customer.customer_id
      row: 2
      col: 12
      width: 4
      height: 3

    - title: "Products Held"
      name: products_held
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      measures: [dim_account.count]
      listen:
        customer_id: dim_customer.customer_id
      row: 2
      col: 16
      width: 4
      height: 3

    - title: "KYC Status"
      name: kyc_status
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.kyc_status]
      listen:
        customer_id: dim_customer.customer_id
      row: 2
      col: 20
      width: 4
      height: 3

    # Profile Details Row
    - title: "Customer Details"
      name: customer_details
      type: looker_single_record
      model: demo_retail_banking
      explore: demo_retail_banking
      fields: [
        dim_customer.customer_id,
        dim_customer.email,
        dim_customer.phone,
        dim_customer.full_address,
        dim_customer.occupation,
        dim_customer.employment_type,
        dim_customer.income_bracket,
        dim_customer.join_date,
        dim_customer.preferred_channel,
        dim_customer.risk_tolerance
      ]
      listen:
        customer_id: dim_customer.customer_id
      row: 5
      col: 0
      width: 12
      height: 6

    - title: "Engagement Score"
      name: engagement_score
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.engagement_score]
      listen:
        customer_id: dim_customer.customer_id
      row: 5
      col: 12
      width: 4
      height: 3

    - title: "Tenure (Months)"
      name: tenure
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.customer_tenure_months]
      listen:
        customer_id: dim_customer.customer_id
      row: 5
      col: 16
      width: 4
      height: 3

    - title: "Churn Risk"
      name: churn_risk
      type: single_value
      model: demo_retail_banking
      explore: demo_retail_banking
      dimensions: [dim_customer.churn_status]
      listen:
        customer_id: dim_customer.customer_id
      row: 5
      col: 20
      width: 4
      height: 3

    # =====================================================
    # OVERVIEW TAB - Asset/Liability Donuts
    # =====================================================
    - title: "Assets by Type"
      name: assets_donut
      type: looker_pie
      model: demo_retail_banking
      explore: accounts
      dimensions: [dim_account.account_type]
      measures: [dim_account.total_balance]
      filters:
        dim_account.account_type: "CASA,CD,Securities"
      listen:
        customer_id: dim_customer.customer_id
      row: 11
      col: 0
      width: 8
      height: 8

    - title: "Liabilities by Type"
      name: liabilities_donut
      type: looker_pie
      model: demo_retail_banking
      explore: accounts
      dimensions: [dim_account.account_type]
      measures: [dim_account.total_balance]
      filters:
        dim_account.account_type: "Loan,Credit Card"
      listen:
        customer_id: dim_customer.customer_id
      row: 11
      col: 8
      width: 8
      height: 8

    - title: "Total AUM vs LUM"
      name: aum_lum_comparison
      type: looker_bar
      model: demo_retail_banking
      explore: accounts
      measures: [dim_account.total_assets, dim_account.total_liabilities]
      listen:
        customer_id: dim_customer.customer_id
      row: 11
      col: 16
      width: 8
      height: 8
      series_colors:
        dim_account.total_assets: "#34A853"
        dim_account.total_liabilities: "#EA4335"

    # =====================================================
    # CASA TAB
    # =====================================================
    - title: "CASA Accounts"
      name: casa_table
      type: looker_grid
      model: demo_retail_banking
      explore: accounts
      dimensions: [
        dim_account.account_id,
        dim_account.product_name,
        dim_account.status,
        dim_account.open_date
      ]
      measures: [dim_account.total_balance]
      filters:
        dim_account.account_type: "CASA"
      listen:
        customer_id: dim_customer.customer_id
      row: 19
      col: 0
      width: 12
      height: 6

    - title: "Spending by Category"
      name: casa_spending_donut
      type: looker_pie
      model: demo_retail_banking
      explore: transactions
      dimensions: [fact_transaction.mcc_category]
      measures: [fact_transaction.total_debits]
      filters:
        fact_transaction.transaction_type: "debit"
        fact_transaction.mcc_category: "-Income"
      listen:
        customer_id: dim_customer.customer_id
      sorts: [fact_transaction.total_debits desc]
      limit: 8
      row: 19
      col: 12
      width: 12
      height: 6

    # =====================================================
    # CARDS TAB
    # =====================================================
    - title: "Credit Cards"
      name: cards_table
      type: looker_grid
      model: demo_retail_banking
      explore: accounts
      dimensions: [
        dim_account.account_id,
        dim_account.product_name,
        dim_account.credit_limit,
        dim_account.outstanding_balance,
        dim_account.available_balance,
        dim_account.interest_rate
      ]
      filters:
        dim_account.account_type: "Credit Card"
      listen:
        customer_id: dim_customer.customer_id
      row: 25
      col: 0
      width: 16
      height: 6

    - title: "Credit Utilization"
      name: credit_utilization_gauge
      type: single_value
      model: demo_retail_banking
      explore: accounts
      measures: [dim_account.average_credit_utilization]
      filters:
        dim_account.account_type: "Credit Card"
      listen:
        customer_id: dim_customer.customer_id
      row: 25
      col: 16
      width: 8
      height: 6

    # =====================================================
    # LOANS TAB
    # =====================================================
    - title: "Loan Accounts"
      name: loans_table
      type: looker_grid
      model: demo_retail_banking
      explore: accounts
      dimensions: [
        dim_account.account_id,
        dim_account.product_name,
        dim_account.principal_amount,
        dim_account.outstanding_balance,
        dim_account.interest_rate,
        dim_account.loan_term_months,
        dim_account.maturity_date
      ]
      filters:
        dim_account.account_type: "Loan"
      listen:
        customer_id: dim_customer.customer_id
      row: 31
      col: 0
      width: 24
      height: 6

    # =====================================================
    # CDs TAB
    # =====================================================
    - title: "CD Accounts"
      name: cd_table
      type: looker_grid
      model: demo_retail_banking
      explore: accounts
      dimensions: [
        dim_account.account_id,
        dim_account.product_name,
        dim_account.current_balance,
        dim_account.annual_yield,
        dim_account.cd_term_months,
        dim_account.maturity_date
      ]
      filters:
        dim_account.account_type: "CD"
      listen:
        customer_id: dim_customer.customer_id
      row: 37
      col: 0
      width: 24
      height: 6

    # =====================================================
    # INSURANCE TAB
    # =====================================================
    - title: "Insurance Policies"
      name: insurance_table
      type: looker_grid
      model: demo_retail_banking
      explore: accounts
      dimensions: [
        dim_account.account_id,
        dim_account.product_name,
        dim_account.coverage_amount,
        dim_account.premium_amount,
        dim_account.beneficiary_count,
        dim_account.policy_status
      ]
      filters:
        dim_account.account_type: "Insurance"
      listen:
        customer_id: dim_customer.customer_id
      row: 43
      col: 0
      width: 24
      height: 6

    # =====================================================
    # SECURITIES TAB
    # =====================================================
    - title: "Securities Holdings"
      name: securities_table
      type: looker_grid
      model: demo_retail_banking
      explore: accounts
      dimensions: [
        dim_account.account_id,
        dim_account.product_name,
        dim_account.security_type,
        dim_account.units_held,
        dim_account.purchase_price,
        dim_account.current_value,
        dim_account.unrealized_gain_loss
      ]
      filters:
        dim_account.account_type: "Securities"
      listen:
        customer_id: dim_customer.customer_id
      row: 49
      col: 0
      width: 24
      height: 6

    # =====================================================
    # TRANSACTIONS & INTERACTIONS
    # =====================================================
    - title: "Recent Transactions"
      name: recent_transactions
      type: looker_grid
      model: demo_retail_banking
      explore: transactions
      dimensions: [
        fact_transaction.transaction_date,
        fact_transaction.description,
        fact_transaction.mcc_category,
        fact_transaction.amount,
        fact_transaction.transaction_type,
        fact_transaction.channel
      ]
      listen:
        customer_id: dim_customer.customer_id
      sorts: [fact_transaction.transaction_date desc]
      limit: 20
      row: 55
      col: 0
      width: 12
      height: 10

    - title: "Recent Interactions"
      name: recent_interactions
      type: looker_grid
      model: demo_retail_banking
      explore: interactions
      dimensions: [
        fact_interaction.interaction_date,
        fact_interaction.channel,
        fact_interaction.interaction_type,
        fact_interaction.reason,
        fact_interaction.sentiment_score,
        fact_interaction.resolution_status
      ]
      listen:
        customer_id: dim_customer.customer_id
      sorts: [fact_interaction.interaction_date desc]
      limit: 10
      row: 55
      col: 12
      width: 12
      height: 10

    # Monthly Spending Trend
    - title: "Monthly Spending Trend"
      name: monthly_spending_trend
      type: looker_line
      model: demo_retail_banking
      explore: transactions
      dimensions: [fact_transaction.transaction_month]
      measures: [fact_transaction.total_debits, fact_transaction.total_credits]
      listen:
        customer_id: dim_customer.customer_id
      row: 65
      col: 0
      width: 24
      height: 8
      series_colors:
        fact_transaction.total_debits: "#EA4335"
        fact_transaction.total_credits: "#34A853"
