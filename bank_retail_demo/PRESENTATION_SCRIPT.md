# Customer 360 Dashboard - Presentation Script
**Duration: 10-15 minutes**

---

## Opening (1 minute)

> "Today I'll walk you through our Customer 360 Dashboard solution for retail banking. This solution provides a complete view of your customer portfolio across three levels of analysis - from executive-level portfolio health down to individual customer profiles."

**Key Value Proposition:**
- Single source of truth for customer insights
- Three interconnected dashboards for different user personas
- Real-time visibility into AUM, LUM, churn risk, and customer behavior

---

## Dashboard Overview (30 seconds)

> "We've built three dashboards that work together as a drill-down system:"

| Dashboard | Audience | Question It Answers |
|-----------|----------|---------------------|
| **Executive Overview** | C-Suite, Board | "How is our portfolio performing?" |
| **Demographic & Segment** | Marketing, Operations | "Who are our customers and how do they behave?" |
| **Customer 360** | Relationship Managers | "What does this specific customer look like?" |

> "Notice the navigation bar at the top - users can seamlessly move between dashboards to drill deeper into the data."

---

## Dashboard 1: Executive Overview (3-4 minutes)

### Opening
> "Let's start where executives start - the big picture."

### KPIs Row (Point to each)
- **Total Customers** - "5,000 customers in our portfolio"
- **Total AUM** - "Assets Under Management - what customers have deposited with us"
- **Total LUM** - "Liabilities Under Management - what we've lent out"
- **Share of Wallet** - "Average products per customer - higher means stickier customers"
- **Churn Rate** - "Percentage of customers we've lost - a key health metric"
- **Avg Sentiment** - "Customer satisfaction from interaction data"

### Key Visualizations

**Portfolio Health (AUM vs LUM by Segment)**
> "This shows the balance between deposits and loans across our three segments. High Net Worth brings the most AUM, while Mass Market drives loan volume."

**Customer Distribution**
> "Our customer base breakdown - about 50% Mass Market, 39% Affluent, and 10% High Net Worth."

**Product Holdings by Segment**
> "A heatmap showing which products each segment uses. Notice High Net Worth customers have more Securities and CDs, while Mass Market focuses on basic CASA and Credit Cards."

**Monthly Transaction Volume & Product Growth**
> "These trend charts show activity over time - transaction volumes and new account openings by product type."

**Churn Rate by Segment**
> "Critical insight - which segments are we losing? This helps prioritize retention efforts."

### Demo the Filter
> "Watch what happens when I filter to just 'High Net Worth' customers..."
*(Apply filter, show numbers change)*
> "Every chart updates instantly. Now we're seeing only our most valuable segment."

---

## Dashboard 2: Demographic & Segment Analysis (4-5 minutes)

### Transition
> "Now let's drill deeper. Click 'Demographic & Segment' to understand WHO our customers are."

### Filters (Point out)
> "Notice we have much more filtering capability here - Gender, Age Group, Income Bracket, Occupation, Segment, and Persona. This is for analysts who need to slice and dice."

### KPIs Row
> "Same core KPIs for consistency, but now they respond to all our demographic filters."

### Demographics Section
> "Four views of our customer composition:"
- **Gender** - "Fairly balanced male/female split"
- **Age Group** - "Our largest cohort is 45-54, typical for banking"
- **Income Bracket** - "Distribution across income levels"
- **Top Occupations** - "Who our customers are professionally"

### Spending Behavior
**Spending by Category Over Time**
> "This is powerful - we can see spending patterns across categories like Shopping, Healthcare, Groceries. Notice the upward trend in Shopping."

**Top 10 Merchants**
> "Which merchants get the most of our customers' wallet share. Best Buy, Walmart, Target lead."

### Customer Acquisition
> "New customer growth over time - are we acquiring consistently or in bursts?"

### Spending by Demographics
> "How spending differs by Gender, Age, and Income. Higher income = higher spend, but Age shows interesting patterns."

### Products & Banking Relationship
- **Product Mix** - "What products are popular"
- **AUM by Income** - "Higher earners have more assets (as expected)"
- **LUM by Age** - "Middle-aged customers carry more debt"

### Customer Health
> "Finally, sentiment and churn broken down by demographics. This tells us WHERE to focus retention."

### Demo: Cross-filtering
> "Let me show you the power of cross-filtering. Let's look at just Female customers, aged 35-44, in the 100-250K income bracket..."
*(Apply filters)*
> "Instantly we see the profile of this micro-segment - their spending patterns, products, churn risk."

---

## Dashboard 3: Customer 360 Individual (3-4 minutes)

### Transition
> "Finally, let's look at a single customer. This is what a Relationship Manager sees when preparing for a client call."

### Customer Selection
> "I'll select a customer ID..."
*(Select a customer)*

### Profile Header
> "Immediately we see who this is - their name, segment, persona, total balance, products held, and KYC status."

### Customer Details Card
> "All the key information - contact details, occupation, income bracket, join date, preferred channel, risk tolerance."

### Health Indicators
- **Engagement Score** - "How active is this customer?"
- **Tenure** - "How long have they been with us?"
- **Churn Risk** - "Are they at risk of leaving?"

### Portfolio View
**Assets vs Liabilities**
> "Visual breakdown of what they have with us - Assets on one side, Liabilities on the other, plus a comparison bar."

### Account Details
> "Scrolling down, we see detailed tables for each product type:"
- CASA Accounts
- Credit Cards (with utilization)
- Loans (with terms and maturity)
- CDs
- Insurance Policies
- Securities Holdings

> "This is everything a banker needs to have an informed conversation."

### Spending & Interactions
**Spending by Category**
> "Where does this customer spend their money?"

**Recent Transactions**
> "Last 20 transactions - date, description, amount, category"

**Recent Interactions**
> "Every touchpoint with us - calls, branch visits, app usage, with sentiment scores"

**Monthly Spending Trend**
> "Spending vs Income over time - is this customer financially healthy?"

---

## Wrap-Up: The Connected Story (1 minute)

> "Let me show you how these dashboards connect:"

1. **Start at Executive** - "See churn rate is high in Mass Market"
2. **Drill to Segment** - "Filter to Mass Market, find it's driven by 25-34 age group"
3. **Drill to Individual** - "Look at specific at-risk customers to understand why"

> "This is the power of Customer 360 - from portfolio-level decisions down to individual customer actions, all connected."

---

## Key Takeaways

1. **Three Levels of Insight** - Executive, Segment, Individual
2. **Consistent Metrics** - Same KPIs across dashboards for alignment
3. **Powerful Filtering** - Slice data any way you need
4. **Connected Navigation** - Seamless drill-down between views
5. **Actionable Data** - From strategy to customer conversation

---

## Q&A Prep - Anticipated Questions

**Q: What data sources feed this?**
> "BigQuery data warehouse with tables for customers, accounts, transactions, and interactions. Updated [daily/real-time]."

**Q: Can we add more filters/metrics?**
> "Absolutely. LookML is modular - we can add dimensions, measures, or entirely new views."

**Q: How do the segments get defined?**
> "Currently based on AUM thresholds. Mass Market < $X, Affluent $X-$Y, High Net Worth > $Y. This is configurable."

**Q: What's the data freshness?**
> "Depends on your ETL pipeline. Can be daily batch or near real-time with streaming."

**Q: Can users create their own views?**
> "Yes, they can explore the data in Looker and save their own Looks and dashboards."

---

## Demo Flow Checklist

- [ ] Start on Executive Overview
- [ ] Point out navigation bar
- [ ] Walk through KPIs
- [ ] Show key charts
- [ ] Demo segment filter
- [ ] Navigate to Demographic & Segment
- [ ] Show expanded filters
- [ ] Demo cross-filtering (pick a specific demo persona)
- [ ] Navigate to Customer 360
- [ ] Select a pre-chosen customer ID
- [ ] Walk through profile
- [ ] Show account details
- [ ] Show transaction history
- [ ] Circle back to connected story
- [ ] Open for questions

---

**Pro Tips:**
- Have a specific customer ID ready that has interesting data
- Practice the filter transitions so they're smooth
- Keep a "reset filters" mental note so you don't get stuck
- If something doesn't load, move on - "Let me show you the next section while that loads"
