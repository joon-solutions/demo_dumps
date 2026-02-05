"""
Customer 360 Dashboard - Mock Data Generator
Generates realistic banking data for 5,000 customers with persona-driven behavior.
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
import os

# --- CONFIGURATION ---
NUM_CUSTOMERS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
OUTPUT_DIR = "data"
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating data for {NUM_CUSTOMERS} customers...")

# --- PERSONA DEFINITIONS ---
# More realistic distributions and constraints
PERSONAS = {
    "Frequent Traveler": {
        "weight": 0.08,  # Rare - requires high income
        "age_range": (32, 58),
        "income_brackets": ["100-250K", "250K+"],
        "segment_weights": {"Affluent": 0.6, "High Net Worth": 0.4},  # No mass market
        "spending_categories": ["Travel", "Dining", "Dining", "Entertainment", "Shopping"],  # More balanced
        "monthly_spend_range": (4000, 12000),
        "card_types": ["Gold Credit Card", "Platinum Credit Card", "Platinum Credit Card"],  # Premium cards
        "preferred_channels": ["App", "App", "App", "App", "Chatbot"],  # 80% app
        "weekend_spending_mult": 1.6,
        "product_count_range": (3, 5),
    },
    "Young Parent": {
        "weight": 0.20,
        "age_range": (28, 42),
        "income_brackets": ["50-100K", "100-250K"],
        "segment_weights": {"Mass Market": 0.55, "Affluent": 0.45},
        "spending_categories": ["Groceries", "Shopping", "Healthcare", "Dining", "Gas"],  # More varied
        "monthly_spend_range": (2500, 6000),
        "card_types": ["Basic Credit Card", "Gold Credit Card", "Gold Credit Card"],
        "preferred_channels": ["App", "App", "App", "Branch", "Chatbot"],  # Mostly app
        "weekend_spending_mult": 1.4,
        "product_count_range": (2, 4),
    },
    "Digital Native": {
        "weight": 0.25,
        "age_range": (23, 35),
        "income_brackets": ["25-50K", "50-100K", "50-100K"],
        "segment_weights": {"Mass Market": 0.7, "Affluent": 0.3},
        "spending_categories": ["Dining", "Entertainment", "Shopping", "Subscriptions", "Groceries"],  # More varied
        "monthly_spend_range": (1200, 3500),
        "card_types": ["Basic Credit Card", "Basic Credit Card", "Gold Credit Card"],  # Mostly basic
        "preferred_channels": ["App", "App", "App", "App", "App", "Chatbot"],  # 83% app
        "weekend_spending_mult": 1.7,
        "product_count_range": (1, 3),
    },
    "College Student": {
        "weight": 0.12,
        "age_range": (18, 24),
        "income_brackets": ["<25K", "<25K", "25-50K"],  # Mostly low income
        "segment_weights": {"Mass Market": 1.0},  # 100% mass market
        "spending_categories": ["Dining", "Entertainment", "Shopping", "Subscriptions", "Groceries"],  # More varied
        "monthly_spend_range": (400, 1200),
        "card_types": ["Basic Credit Card"],  # Only basic cards
        "preferred_channels": ["App", "App", "App", "App", "Chatbot", "Chatbot"],  # Never branch
        "weekend_spending_mult": 2.0,  # Heavy weekend spending
        "product_count_range": (1, 2),  # Minimal products
    },
    "Boomer": {
        "weight": 0.35,  # Largest segment - most banking customers are older
        "age_range": (55, 78),
        "income_brackets": ["50-100K", "100-250K", "100-250K", "250K+"],
        "segment_weights": {"Mass Market": 0.3, "Affluent": 0.5, "High Net Worth": 0.2},
        "spending_categories": ["Healthcare", "Groceries", "Shopping", "Utilities", "Dining"],  # More varied
        "monthly_spend_range": (2000, 7000),
        "card_types": ["Gold Credit Card", "Gold Credit Card", "Platinum Credit Card"],
        "preferred_channels": ["Branch", "Branch", "Branch", "Call Center", "Call Center", "App"],  # 50% branch
        "weekend_spending_mult": 0.6,  # Much less weekend spending
        "product_count_range": (2, 5),
    },
}

# --- PRODUCT CATALOG ---
PRODUCTS = [
    # CASA
    {"product_id": "PROD-001", "product_name": "Savings Account", "product_type": "Savings", "product_category": "CASA", "min_balance": 100, "annual_fee": 0, "interest_rate_min": 0.01, "interest_rate_max": 0.02},
    {"product_id": "PROD-002", "product_name": "Premium Savings", "product_type": "Savings", "product_category": "CASA", "min_balance": 10000, "annual_fee": 0, "interest_rate_min": 0.03, "interest_rate_max": 0.04},
    {"product_id": "PROD-003", "product_name": "Checking Account", "product_type": "Checking", "product_category": "CASA", "min_balance": 0, "annual_fee": 0, "interest_rate_min": 0, "interest_rate_max": 0.005},
    {"product_id": "PROD-004", "product_name": "Money Market", "product_type": "Money Market", "product_category": "CASA", "min_balance": 25000, "annual_fee": 0, "interest_rate_min": 0.04, "interest_rate_max": 0.05},
    # Cards
    {"product_id": "PROD-010", "product_name": "Basic Credit Card", "product_type": "Credit Card", "product_category": "Cards", "min_balance": None, "annual_fee": 0, "interest_rate_min": 0.18, "interest_rate_max": 0.24},
    {"product_id": "PROD-011", "product_name": "Gold Credit Card", "product_type": "Credit Card", "product_category": "Cards", "min_balance": None, "annual_fee": 95, "interest_rate_min": 0.15, "interest_rate_max": 0.21},
    {"product_id": "PROD-012", "product_name": "Platinum Credit Card", "product_type": "Credit Card", "product_category": "Cards", "min_balance": None, "annual_fee": 450, "interest_rate_min": 0.12, "interest_rate_max": 0.18},
    # Loans
    {"product_id": "PROD-020", "product_name": "Personal Loan", "product_type": "Personal Loan", "product_category": "Loans", "min_balance": None, "annual_fee": 0, "interest_rate_min": 0.08, "interest_rate_max": 0.15},
    {"product_id": "PROD-021", "product_name": "Home Mortgage", "product_type": "Mortgage", "product_category": "Loans", "min_balance": None, "annual_fee": 0, "interest_rate_min": 0.05, "interest_rate_max": 0.07},
    {"product_id": "PROD-022", "product_name": "Auto Loan", "product_type": "Auto Loan", "product_category": "Loans", "min_balance": None, "annual_fee": 0, "interest_rate_min": 0.06, "interest_rate_max": 0.10},
    {"product_id": "PROD-023", "product_name": "Education Loan", "product_type": "Education Loan", "product_category": "Loans", "min_balance": None, "annual_fee": 0, "interest_rate_min": 0.04, "interest_rate_max": 0.08},
    # CDs
    {"product_id": "PROD-030", "product_name": "Standard CD", "product_type": "CD", "product_category": "CDs", "min_balance": 1000, "annual_fee": 0, "interest_rate_min": 0.04, "interest_rate_max": 0.045},
    {"product_id": "PROD-031", "product_name": "High-Yield CD", "product_type": "CD", "product_category": "CDs", "min_balance": 10000, "annual_fee": 0, "interest_rate_min": 0.05, "interest_rate_max": 0.055},
    {"product_id": "PROD-032", "product_name": "Jumbo CD", "product_type": "CD", "product_category": "CDs", "min_balance": 100000, "annual_fee": 0, "interest_rate_min": 0.055, "interest_rate_max": 0.06},
    # Insurance
    {"product_id": "PROD-040", "product_name": "Term Life Insurance", "product_type": "Life Insurance", "product_category": "Insurance", "min_balance": None, "annual_fee": None, "interest_rate_min": None, "interest_rate_max": None},
    {"product_id": "PROD-041", "product_name": "Whole Life Insurance", "product_type": "Life Insurance", "product_category": "Insurance", "min_balance": None, "annual_fee": None, "interest_rate_min": None, "interest_rate_max": None},
    {"product_id": "PROD-042", "product_name": "Property Insurance", "product_type": "Property Insurance", "product_category": "Insurance", "min_balance": None, "annual_fee": None, "interest_rate_min": None, "interest_rate_max": None},
    {"product_id": "PROD-043", "product_name": "Travel Insurance", "product_type": "Travel Insurance", "product_category": "Insurance", "min_balance": None, "annual_fee": None, "interest_rate_min": None, "interest_rate_max": None},
    # Securities
    {"product_id": "PROD-050", "product_name": "Equity Fund", "product_type": "Equity", "product_category": "Securities", "min_balance": 500, "annual_fee": 0.005, "interest_rate_min": None, "interest_rate_max": None},
    {"product_id": "PROD-051", "product_name": "Bond Fund", "product_type": "Bond", "product_category": "Securities", "min_balance": 1000, "annual_fee": 0.003, "interest_rate_min": None, "interest_rate_max": None},
    {"product_id": "PROD-052", "product_name": "Mutual Fund", "product_type": "Mutual Fund", "product_category": "Securities", "min_balance": 1000, "annual_fee": 0.01, "interest_rate_min": None, "interest_rate_max": None},
    {"product_id": "PROD-053", "product_name": "SIP Investment", "product_type": "SIP", "product_category": "Securities", "min_balance": 100, "annual_fee": 0.008, "interest_rate_min": None, "interest_rate_max": None},
]

# --- MERCHANT CATALOG ---
MERCHANTS = [
    # Groceries
    {"merchant_id": "MERCH-001", "merchant_name": "Whole Foods", "mcc_code": "5411", "mcc_category": "Groceries", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-002", "merchant_name": "Kroger", "mcc_code": "5411", "mcc_category": "Groceries", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-003", "merchant_name": "Trader Joe's", "mcc_code": "5411", "mcc_category": "Groceries", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-004", "merchant_name": "Costco", "mcc_code": "5411", "mcc_category": "Groceries", "merchant_type": "Retail", "is_subscription_merchant": False},
    # Dining
    {"merchant_id": "MERCH-010", "merchant_name": "Starbucks", "mcc_code": "5814", "mcc_category": "Dining", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-011", "merchant_name": "Chipotle", "mcc_code": "5812", "mcc_category": "Dining", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-012", "merchant_name": "Uber Eats", "mcc_code": "5812", "mcc_category": "Dining", "merchant_type": "Online", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-013", "merchant_name": "DoorDash", "mcc_code": "5812", "mcc_category": "Dining", "merchant_type": "Online", "is_subscription_merchant": False},
    # Travel
    {"merchant_id": "MERCH-020", "merchant_name": "Delta Airlines", "mcc_code": "3058", "mcc_category": "Travel", "merchant_type": "Service", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-021", "merchant_name": "United Airlines", "mcc_code": "3000", "mcc_category": "Travel", "merchant_type": "Service", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-022", "merchant_name": "Marriott Hotels", "mcc_code": "7011", "mcc_category": "Travel", "merchant_type": "Service", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-023", "merchant_name": "Hilton Hotels", "mcc_code": "7011", "mcc_category": "Travel", "merchant_type": "Service", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-024", "merchant_name": "Uber", "mcc_code": "4121", "mcc_category": "Travel", "merchant_type": "Service", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-025", "merchant_name": "Airbnb", "mcc_code": "7011", "mcc_category": "Travel", "merchant_type": "Online", "is_subscription_merchant": False},
    # Utilities
    {"merchant_id": "MERCH-030", "merchant_name": "Verizon", "mcc_code": "4814", "mcc_category": "Utilities", "merchant_type": "Service", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-031", "merchant_name": "AT&T", "mcc_code": "4814", "mcc_category": "Utilities", "merchant_type": "Service", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-032", "merchant_name": "Comcast", "mcc_code": "4899", "mcc_category": "Utilities", "merchant_type": "Service", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-033", "merchant_name": "City Power Co", "mcc_code": "4900", "mcc_category": "Utilities", "merchant_type": "Service", "is_subscription_merchant": True},
    # Entertainment / Subscriptions
    {"merchant_id": "MERCH-040", "merchant_name": "Netflix", "mcc_code": "4899", "mcc_category": "Subscriptions", "merchant_type": "Online", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-041", "merchant_name": "Spotify", "mcc_code": "5968", "mcc_category": "Subscriptions", "merchant_type": "Online", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-042", "merchant_name": "Amazon Prime", "mcc_code": "5968", "mcc_category": "Subscriptions", "merchant_type": "Online", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-043", "merchant_name": "Disney+", "mcc_code": "4899", "mcc_category": "Subscriptions", "merchant_type": "Online", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-044", "merchant_name": "Planet Fitness", "mcc_code": "7941", "mcc_category": "Subscriptions", "merchant_type": "Service", "is_subscription_merchant": True},
    {"merchant_id": "MERCH-045", "merchant_name": "Apple Music", "mcc_code": "5968", "mcc_category": "Subscriptions", "merchant_type": "Online", "is_subscription_merchant": True},
    # Healthcare
    {"merchant_id": "MERCH-050", "merchant_name": "CVS Pharmacy", "mcc_code": "5912", "mcc_category": "Healthcare", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-051", "merchant_name": "Walgreens", "mcc_code": "5912", "mcc_category": "Healthcare", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-052", "merchant_name": "Kaiser Permanente", "mcc_code": "8011", "mcc_category": "Healthcare", "merchant_type": "Service", "is_subscription_merchant": False},
    # Shopping
    {"merchant_id": "MERCH-060", "merchant_name": "Amazon", "mcc_code": "5311", "mcc_category": "Shopping", "merchant_type": "Online", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-061", "merchant_name": "Target", "mcc_code": "5311", "mcc_category": "Shopping", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-062", "merchant_name": "Walmart", "mcc_code": "5311", "mcc_category": "Shopping", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-063", "merchant_name": "Best Buy", "mcc_code": "5732", "mcc_category": "Shopping", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-064", "merchant_name": "Buy Buy Baby", "mcc_code": "5641", "mcc_category": "Shopping", "merchant_type": "Retail", "is_subscription_merchant": False},
    # Gas
    {"merchant_id": "MERCH-070", "merchant_name": "Shell", "mcc_code": "5541", "mcc_category": "Gas", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-071", "merchant_name": "Chevron", "mcc_code": "5541", "mcc_category": "Gas", "merchant_type": "Retail", "is_subscription_merchant": False},
    {"merchant_id": "MERCH-072", "merchant_name": "ExxonMobil", "mcc_code": "5541", "mcc_category": "Gas", "merchant_type": "Retail", "is_subscription_merchant": False},
    # Salary (internal transfers)
    {"merchant_id": "MERCH-100", "merchant_name": "Employer Direct Deposit", "mcc_code": "0000", "mcc_category": "Income", "merchant_type": "Internal", "is_subscription_merchant": False},
]

MERCHANTS_BY_CATEGORY = {}
for m in MERCHANTS:
    cat = m["mcc_category"]
    if cat not in MERCHANTS_BY_CATEGORY:
        MERCHANTS_BY_CATEGORY[cat] = []
    MERCHANTS_BY_CATEGORY[cat].append(m)

# --- HELPER FUNCTIONS ---
def generate_phone():
    return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

def generate_ssn_masked():
    return f"***-**-{random.randint(1000, 9999)}"

def generate_account_number():
    return f"****{random.randint(1000, 9999)}"

def pick_persona():
    personas = list(PERSONAS.keys())
    # Add noise to weights (+/- 15%)
    weights = [PERSONAS[p]["weight"] * random.uniform(0.85, 1.15) for p in personas]
    return random.choices(personas, weights=weights)[0]

def get_customer_spending_profile(cust, persona):
    """
    Generate a unique spending profile for each customer based on multiple factors.
    Returns a dict with multipliers for different aspects of spending.
    This creates realistic variance - not everyone in a persona spends the same way.
    """
    age = cust["age"]
    gender = cust.get("gender", "Other")
    income = cust["income_bracket"]
    segment = cust["segment"]

    # Base spending personality (some people are frugal, some splurge)
    # This is the biggest source of individual variance
    spending_personality = np.random.lognormal(mean=0, sigma=0.35)  # Range ~0.5-2.0
    spending_personality = max(0.4, min(2.5, spending_personality))

    # Age factor - spending patterns change with life stage
    if age < 25:
        age_factor = random.uniform(0.6, 1.0)  # Students/young adults spend less overall
    elif 25 <= age < 35:
        age_factor = random.uniform(0.9, 1.3)  # Peak spending years
    elif 35 <= age < 50:
        age_factor = random.uniform(1.0, 1.4)  # Family years, high expenses
    elif 50 <= age < 65:
        age_factor = random.uniform(0.9, 1.2)  # Kids leaving, stable
    else:
        age_factor = random.uniform(0.6, 1.0)  # Retired, fixed income

    # Income factor - this shifts spending up/down significantly
    income_factors = {
        "<25K": random.uniform(0.5, 0.8),
        "25-50K": random.uniform(0.7, 1.0),
        "50-100K": random.uniform(0.9, 1.3),
        "100-250K": random.uniform(1.2, 1.8),
        "250K+": random.uniform(1.5, 2.5),
    }
    income_factor = income_factors.get(income, 1.0)

    # Gender-based subtle category preferences (not amount, but category mix)
    # These are SUBTLE and based on aggregate consumer data, not stereotypes
    category_preferences = {}
    if gender == "Male":
        category_preferences = {
            "Gas": random.uniform(1.0, 1.3),
            "Dining": random.uniform(1.0, 1.2),
            "Entertainment": random.uniform(1.0, 1.2),
            "Shopping": random.uniform(0.8, 1.0),
            "Healthcare": random.uniform(0.8, 1.0),
        }
    elif gender == "Female":
        category_preferences = {
            "Shopping": random.uniform(1.0, 1.3),
            "Healthcare": random.uniform(1.0, 1.2),
            "Groceries": random.uniform(1.0, 1.2),
            "Gas": random.uniform(0.8, 1.0),
        }

    # Segment affects quality/premium vs budget choices
    segment_quality_mult = {
        "Mass Market": random.uniform(0.7, 1.0),
        "Affluent": random.uniform(1.0, 1.4),
        "High Net Worth": random.uniform(1.3, 2.0),
    }.get(segment, 1.0)

    # Final overall multiplier combines all factors
    overall_mult = spending_personality * age_factor * income_factor * 0.7  # 0.7 to normalize
    overall_mult = max(0.3, min(3.0, overall_mult))  # Clamp to reasonable range

    return {
        "overall_multiplier": overall_mult,
        "spending_personality": spending_personality,
        "age_factor": age_factor,
        "income_factor": income_factor,
        "segment_quality": segment_quality_mult,
        "category_preferences": category_preferences,
    }

def round_to_realistic_amount(amount):
    """Make amounts look more realistic - cluster around round numbers"""
    if amount < 10:
        return round(amount, 2)
    elif amount < 50:
        # Round to nearest $5 with some noise
        base = round(amount / 5) * 5
        return base + random.uniform(-0.99, 0.99)
    elif amount < 200:
        # Cluster around $10 increments
        base = round(amount / 10) * 10
        noise = random.choice([0, 0.49, 0.95, 0.99, -0.01])
        return base + noise
    elif amount < 1000:
        # Cluster around $25 or $50 increments
        increment = random.choice([25, 50])
        base = round(amount / increment) * increment
        noise = random.choice([0, 0.49, 0.95, 0.99, -0.01])
        return base + noise
    else:
        # Large amounts - round to nearest $100
        base = round(amount / 100) * 100
        return base + random.choice([0, 0, 0, 50, -50])

def is_payday(date):
    """Check if date is around typical paydays"""
    day = date.day
    return day in [1, 2, 14, 15, 16, 28, 29, 30, 31]

def get_seasonal_multiplier(date):
    """Spending varies by season/holidays"""
    month = date.month
    day = date.day

    # Black Friday / Holiday shopping (Nov-Dec)
    if month == 11 and day >= 20:
        return random.uniform(1.3, 1.8)
    if month == 12 and day <= 25:
        return random.uniform(1.4, 2.0)

    # Back to school (Aug-Sep)
    if month in [8, 9]:
        return random.uniform(1.1, 1.3)

    # Summer travel (Jun-Jul)
    if month in [6, 7]:
        return random.uniform(1.1, 1.2)

    # Post-holiday slump (Jan-Feb)
    if month in [1, 2]:
        return random.uniform(0.7, 0.9)

    return random.uniform(0.9, 1.1)

# --- 1. GENERATE dim_date ---
print("Generating dim_date...")
dates = []
current = START_DATE
while current <= END_DATE:
    date_key = int(current.strftime("%Y%m%d"))
    dates.append({
        "date_key": date_key,
        "full_date": current.date(),
        "year": current.year,
        "quarter": (current.month - 1) // 3 + 1,
        "month": current.month,
        "month_name": current.strftime("%B"),
        "week_of_year": current.isocalendar()[1],
        "day_of_month": current.day,
        "day_of_week": current.weekday(),
        "day_name": current.strftime("%A"),
        "is_weekend": current.weekday() >= 5,
        "is_holiday": current.month == 12 and current.day == 25,  # Simplified
        "fiscal_year": current.year if current.month >= 7 else current.year - 1,
        "fiscal_quarter": ((current.month - 7) % 12) // 3 + 1,
    })
    current += timedelta(days=1)
df_date = pd.DataFrame(dates)

# --- 2. GENERATE dim_product ---
print("Generating dim_product...")
for p in PRODUCTS:
    p["is_active"] = True
    p["description"] = f"{p['product_name']} - {p['product_category']}"
df_product = pd.DataFrame(PRODUCTS)

# --- 3. GENERATE dim_merchant ---
print("Generating dim_merchant...")
df_merchant = pd.DataFrame(MERCHANTS)

# --- 4. GENERATE dim_customer ---
print("Generating dim_customer...")
customers = []
customer_ids = [f"CUST-{str(i).zfill(6)}" for i in range(1, NUM_CUSTOMERS + 1)]

STATES = ["CA", "TX", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]
CITIES = {
    "CA": ["Los Angeles", "San Francisco", "San Diego"],
    "TX": ["Houston", "Dallas", "Austin"],
    "NY": ["New York", "Buffalo", "Albany"],
    "FL": ["Miami", "Orlando", "Tampa"],
    "IL": ["Chicago", "Springfield"],
    "PA": ["Philadelphia", "Pittsburgh"],
    "OH": ["Columbus", "Cleveland"],
    "GA": ["Atlanta", "Savannah"],
    "NC": ["Charlotte", "Raleigh"],
    "MI": ["Detroit", "Grand Rapids"],
}

for c_id in customer_ids:
    persona = pick_persona()
    p_config = PERSONAS[persona]

    age = random.randint(*p_config["age_range"])
    dob = datetime.now() - timedelta(days=age * 365 + random.randint(0, 364))

    state = random.choice(STATES)
    city = random.choice(CITIES[state])

    join_date = fake.date_between(start_date=START_DATE, end_date=END_DATE - timedelta(days=90))

    # Use segment weights for realistic distribution (need segment first for churn calc)
    segment_weights = p_config.get("segment_weights", {"Mass Market": 0.7, "Affluent": 0.25, "High Net Worth": 0.05})
    segment = random.choices(list(segment_weights.keys()), weights=list(segment_weights.values()))[0]

    # Churn rate based on real industry data:
    # - HNW: ~6-8% (very sticky - dedicated relationship managers, bespoke services)
    # - Affluent/Mass-Affluent: ~15-20% (highest - underserved "no-man's land", looking for personalization)
    # - Mass Market: ~10-15% (transactional, product-centric)
    base_churn = {
        "High Net Worth": 0.07,
        "Affluent": 0.17,
        "Mass Market": 0.12,
    }.get(segment, 0.12)

    # Persona adjustment
    if persona == "Young Parent":
        base_churn *= 0.65  # Very sticky - mortgages, life stage, family accounts
    elif persona == "College Student":
        base_churn *= 1.4  # Higher - life changes, graduating, moving
    elif persona == "Boomer":
        base_churn *= 0.8  # Stickier - inertia, relationship with branch

    # Age adjustment - younger more likely to switch
    age_factor = 1.0 + (35 - age) * 0.01  # Younger = higher churn
    age_factor = max(0.7, min(1.3, age_factor))
    base_churn *= age_factor

    churn_rate = base_churn * random.uniform(0.85, 1.15)
    is_churned = random.random() < churn_rate

    churn_date = None
    if is_churned:
        min_active = join_date + timedelta(days=60)
        if min_active < END_DATE.date():
            churn_date = fake.date_between(start_date=min_active, end_date=END_DATE.date())
        else:
            is_churned = False

    # Segment already assigned above

    # Preferred channel based on persona
    preferred_channel = random.choice(p_config.get("preferred_channels", ["App", "Branch", "Call Center", "Chatbot"]))

    # Employment type
    if persona == "College Student":
        employment_type = "Student"
    elif persona == "Boomer" and age > 62:
        employment_type = random.choices(["Retired", "Salaried", "Self-Employed"], weights=[0.6, 0.25, 0.15])[0]
    else:
        employment_type = random.choices(["Salaried", "Self-Employed", "Retired"], weights=[0.7, 0.2, 0.1])[0]

    # Home ownership based on persona/segment
    if persona == "College Student":
        home_ownership = "Rent"
    elif segment == "High Net Worth":
        home_ownership = random.choices(["Own", "Own", "Own", "Rent"], weights=[0.85, 0.05, 0.05, 0.05])[0]
    elif persona == "Young Parent":
        home_ownership = random.choices(["Own", "Rent"], weights=[0.55, 0.45])[0]
    else:
        home_ownership = random.choices(["Own", "Rent"], weights=[0.5, 0.5])[0]

    # Engagement score varies by persona
    if persona == "Digital Native":
        engagement_score = random.randint(50, 100)  # High engagement
    elif persona == "College Student":
        engagement_score = random.randint(30, 80)
    elif persona == "Boomer":
        engagement_score = random.randint(20, 70)  # Lower digital engagement
    else:
        engagement_score = random.randint(30, 90)

    customers.append({
        "customer_id": c_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": dob.date(),
        "age": age,
        "gender": random.choice(["Male", "Female", "Other"]),
        "email": fake.email(),
        "phone": generate_phone(),
        "address_city": city,
        "address_state": state,
        "address_country": "USA",
        "marital_status": random.choice(["Single", "Married", "Divorced"]) if persona != "College Student" else random.choices(["Single", "Married"], weights=[0.95, 0.05])[0],
        "has_children": persona == "Young Parent" or (persona == "Boomer" and random.random() < 0.7) or (random.random() < 0.2),
        "num_dependents": random.randint(1, 3) if persona == "Young Parent" else (0 if persona == "College Student" else random.randint(0, 2)),
        "occupation": fake.job()[:50],
        "employment_type": employment_type,
        "income_bracket": random.choice(p_config["income_brackets"]),
        "home_ownership": home_ownership,
        "segment": segment,
        "kyc_status": random.choices(["Verified", "Pending", "Expired"], weights=[0.88, 0.08, 0.04])[0],
        "join_date": join_date,
        "preferred_channel": preferred_channel,
        "engagement_score": engagement_score,
        "persona_tag": persona,
        "risk_tolerance": "Low" if persona == "Boomer" else ("High" if persona in ["Digital Native", "Frequent Traveler"] else random.choice(["Low", "Medium", "High"])),
        "churn_status": is_churned,
        "churn_date": churn_date,
    })

df_customer = pd.DataFrame(customers)

# --- 5. GENERATE dim_account ---
print("Generating dim_account...")
accounts = []
account_counter = 1

# Products by category for easy lookup
PRODUCTS_BY_CAT = {}
for p in PRODUCTS:
    cat = p["product_category"]
    if cat not in PRODUCTS_BY_CAT:
        PRODUCTS_BY_CAT[cat] = []
    PRODUCTS_BY_CAT[cat].append(p)

for _, cust in df_customer.iterrows():
    c_id = cust["customer_id"]
    persona = cust["persona_tag"]
    segment = cust["segment"]
    join_date = cust["join_date"]

    # Get persona config for this customer
    p_config = PERSONAS[persona]
    product_count_target = random.randint(*p_config.get("product_count_range", (1, 3)))

    # Everyone gets a CASA account - balance based on segment with realistic variance
    if segment == "Mass Market":
        # Most have low balances, few have moderate savings
        if random.random() < 0.7:
            balance = random.uniform(200, 3000)
        elif random.random() < 0.9:
            balance = random.uniform(3000, 8000)
        else:
            balance = random.uniform(8000, 15000)  # Rare savers
        casa_product = random.choice([p for p in PRODUCTS_BY_CAT["CASA"] if "Premium" not in p["product_name"]])
    elif segment == "Affluent":
        # More variance - some lower, some higher
        balance = np.random.lognormal(mean=10.5, sigma=0.8)  # Median ~36K, long tail
        balance = max(5000, min(balance, 200000))
        casa_product = random.choice(PRODUCTS_BY_CAT["CASA"])
    else:  # High Net Worth
        # High balances with significant variance
        balance = np.random.lognormal(mean=12.5, sigma=0.7)  # Median ~270K, long tail
        balance = max(50000, min(balance, 2000000))
        casa_product = random.choice([p for p in PRODUCTS_BY_CAT["CASA"] if "Premium" in p["product_name"] or "Money Market" in p["product_name"]])

    accounts.append({
        "account_id": f"ACC-{str(account_counter).zfill(8)}",
        "customer_id": c_id,
        "account_type": "CASA",
        "product_name": casa_product["product_name"],
        "status": "Active",
        "open_date": join_date,
        "maturity_date": None,
        "account_number": generate_account_number(),
        "credit_limit": None,
        "available_balance": None,
        "principal_amount": None,
        "interest_rate": random.uniform(casa_product["interest_rate_min"], casa_product["interest_rate_max"]),
        "loan_term_months": None,
        "payoff_amount": None,
        "outstanding_balance": None,
        "cd_term_months": None,
        "annual_yield": None,
        "average_balance": balance * 0.9,
        "tin_type": None,
        "tin_number": None,
        "coverage_amount": None,
        "premium_amount": None,
        "beneficiary_count": None,
        "policy_status": None,
        "policy_sub_status": None,
        "security_type": None,
        "units_held": None,
        "purchase_price": None,
        "current_value": None,
        "current_balance": round(balance, 2),
        "currency": "USD",
    })
    account_counter += 1
    primary_casa_id = accounts[-1]["account_id"]

    # Credit card probability and type based on persona
    card_probability = {
        "College Student": 0.50,  # Many students don't have cards
        "Digital Native": 0.75,
        "Young Parent": 0.85,
        "Frequent Traveler": 0.95,  # Almost all have cards
        "Boomer": 0.80,
    }.get(persona, 0.70)

    current_product_count = 1  # CASA already added

    if random.random() < card_probability and current_product_count < product_count_target + 1:
        # Card type based on multiple factors: persona, age, income, segment
        # This creates more realistic variation (not 100% one type per persona)

        age = cust["age"]
        income = cust["income_bracket"]

        # Base probabilities from persona
        base_probs = {"Basic Credit Card": 0.33, "Gold Credit Card": 0.34, "Platinum Credit Card": 0.33}

        # Adjust by persona preference (shift probabilities, don't set to 100%)
        if persona == "College Student":
            base_probs = {"Basic Credit Card": 0.80, "Gold Credit Card": 0.18, "Platinum Credit Card": 0.02}
        elif persona == "Frequent Traveler":
            base_probs = {"Basic Credit Card": 0.05, "Gold Credit Card": 0.35, "Platinum Credit Card": 0.60}
        elif persona == "Boomer":
            base_probs = {"Basic Credit Card": 0.15, "Gold Credit Card": 0.50, "Platinum Credit Card": 0.35}
        elif persona == "Digital Native":
            base_probs = {"Basic Credit Card": 0.55, "Gold Credit Card": 0.35, "Platinum Credit Card": 0.10}
        elif persona == "Young Parent":
            base_probs = {"Basic Credit Card": 0.30, "Gold Credit Card": 0.50, "Platinum Credit Card": 0.20}

        # Age adjustment (older = more credit history = better cards)
        if age > 45:
            base_probs["Gold Credit Card"] += 0.10
            base_probs["Platinum Credit Card"] += 0.05
            base_probs["Basic Credit Card"] -= 0.15
        elif age < 25:
            base_probs["Basic Credit Card"] += 0.15
            base_probs["Platinum Credit Card"] -= 0.10
            base_probs["Gold Credit Card"] -= 0.05

        # Income adjustment
        if income in ["100-250K", "250K+"]:
            base_probs["Platinum Credit Card"] += 0.15
            base_probs["Gold Credit Card"] += 0.10
            base_probs["Basic Credit Card"] -= 0.25
        elif income == "<25K":
            base_probs["Basic Credit Card"] += 0.20
            base_probs["Platinum Credit Card"] -= 0.15
            base_probs["Gold Credit Card"] -= 0.05

        # Segment adjustment
        if segment == "High Net Worth":
            base_probs["Platinum Credit Card"] += 0.20
            base_probs["Basic Credit Card"] -= 0.20
        elif segment == "Mass Market":
            base_probs["Basic Credit Card"] += 0.15
            base_probs["Platinum Credit Card"] -= 0.15

        # Normalize probabilities
        total = sum(max(0.01, v) for v in base_probs.values())
        base_probs = {k: max(0.01, v) / total for k, v in base_probs.items()}

        # Select card type
        card_type_name = random.choices(list(base_probs.keys()), weights=list(base_probs.values()))[0]
        card_product = next((p for p in PRODUCTS_BY_CAT["Cards"] if p["product_name"] == card_type_name), PRODUCTS_BY_CAT["Cards"][0])

        # Credit limit based on segment and card type
        if card_product["product_name"] == "Basic Credit Card":
            limit = random.choice([1000, 2000, 3000, 5000])
        elif card_product["product_name"] == "Gold Credit Card":
            limit = random.choice([5000, 7500, 10000, 15000])
        else:  # Platinum
            limit = random.choice([15000, 25000, 50000, 75000, 100000])

        # Segment adjustment for limits
        if segment == "High Net Worth":
            limit = int(limit * random.uniform(1.5, 2.5))
        elif segment == "Mass Market":
            limit = int(limit * random.uniform(0.6, 1.0))

        # Utilization varies - some people max out, some barely use
        utilization_pattern = random.random()
        if utilization_pattern < 0.3:
            outstanding = random.uniform(0, limit * 0.1)  # Low users
        elif utilization_pattern < 0.7:
            outstanding = random.uniform(limit * 0.1, limit * 0.4)  # Moderate
        else:
            outstanding = random.uniform(limit * 0.4, limit * 0.8)  # High users

        accounts.append({
            "account_id": f"ACC-{str(account_counter).zfill(8)}",
            "customer_id": c_id,
            "account_type": "Credit Card",
            "product_name": card_product["product_name"],
            "status": "Active",
            "open_date": fake.date_between(start_date=join_date, end_date=END_DATE.date()),
            "maturity_date": None,
            "account_number": generate_account_number(),
            "credit_limit": limit,
            "available_balance": round(limit - outstanding, 2),
            "principal_amount": None,
            "interest_rate": random.uniform(card_product["interest_rate_min"], card_product["interest_rate_max"]),
            "loan_term_months": None,
            "payoff_amount": None,
            "outstanding_balance": round(outstanding, 2),
            "cd_term_months": None,
            "annual_yield": None,
            "average_balance": None,
            "tin_type": None,
            "tin_number": None,
            "coverage_amount": None,
            "premium_amount": None,
            "beneficiary_count": None,
            "policy_status": None,
            "policy_sub_status": None,
            "security_type": None,
            "units_held": None,
            "purchase_price": None,
            "current_value": None,
            "current_balance": round(outstanding, 2),
            "currency": "USD",
        })
        account_counter += 1
        current_product_count += 1

    # Loans - probability based on persona and segment
    loan_chances = {
        "College Student": 0.15,  # Only education loans
        "Digital Native": 0.20,
        "Young Parent": 0.55,  # High - mortgages, auto loans
        "Frequent Traveler": 0.30,
        "Boomer": 0.35,  # Many have paid off, some refinance
    }
    loan_chance = loan_chances.get(persona, 0.25)
    has_mortgage = False

    if random.random() < loan_chance and current_product_count < product_count_target + 2:
        loan_product = random.choice(PRODUCTS_BY_CAT["Loans"])
        if persona == "Young Parent" and random.random() < 0.6:
            loan_product = next(p for p in PRODUCTS_BY_CAT["Loans"] if p["product_name"] == "Home Mortgage")
            has_mortgage = True

        principal = random.choice([10000, 25000, 50000, 100000])
        if loan_product["product_name"] == "Home Mortgage":
            principal = random.choice([200000, 300000, 400000, 500000])

        term = 60 if loan_product["product_name"] != "Home Mortgage" else 360
        rate = random.uniform(loan_product["interest_rate_min"], loan_product["interest_rate_max"])
        months_elapsed = random.randint(6, min(term, 36))
        remaining = principal * (1 - months_elapsed / term * 0.8)

        loan_end = END_DATE.date() - timedelta(days=180)
        if join_date >= loan_end:
            loan_end = join_date + timedelta(days=30)
        open_date = fake.date_between(start_date=join_date, end_date=loan_end)
        maturity = open_date + timedelta(days=term * 30)

        accounts.append({
            "account_id": f"ACC-{str(account_counter).zfill(8)}",
            "customer_id": c_id,
            "account_type": "Loan",
            "product_name": loan_product["product_name"],
            "status": "Active",
            "open_date": open_date,
            "maturity_date": maturity,
            "account_number": generate_account_number(),
            "credit_limit": None,
            "available_balance": None,
            "principal_amount": principal,
            "interest_rate": rate,
            "loan_term_months": term,
            "payoff_amount": round(remaining * 1.02, 2),
            "outstanding_balance": round(remaining, 2),
            "cd_term_months": None,
            "annual_yield": None,
            "average_balance": None,
            "tin_type": None,
            "tin_number": None,
            "coverage_amount": None,
            "premium_amount": None,
            "beneficiary_count": None,
            "policy_status": None,
            "policy_sub_status": None,
            "security_type": None,
            "units_held": None,
            "purchase_price": None,
            "current_value": None,
            "current_balance": round(remaining, 2),
            "currency": "USD",
        })
        account_counter += 1
        current_product_count += 1

    # CDs - mostly for Boomers and HNW, rare for young people
    cd_chances = {
        "College Student": 0.02,  # Almost never
        "Digital Native": 0.05,
        "Young Parent": 0.10,
        "Frequent Traveler": 0.15,
        "Boomer": 0.45,  # Common for retirement savings
    }
    cd_chance = cd_chances.get(persona, 0.10)
    if segment == "High Net Worth":
        cd_chance += 0.20  # HNW more likely to have CDs

    if random.random() < cd_chance and current_product_count < product_count_target + 2:
        cd_product = random.choice(PRODUCTS_BY_CAT["CDs"])
        cd_balance = random.choice([5000, 10000, 25000, 50000, 100000])
        term = random.choice([6, 12, 24, 36, 60])
        rate = random.uniform(cd_product["interest_rate_min"], cd_product["interest_rate_max"])

        open_date = fake.date_between(start_date=join_date, end_date=END_DATE.date())
        maturity = open_date + timedelta(days=term * 30)

        accounts.append({
            "account_id": f"ACC-{str(account_counter).zfill(8)}",
            "customer_id": c_id,
            "account_type": "CD",
            "product_name": cd_product["product_name"],
            "status": "Active",
            "open_date": open_date,
            "maturity_date": maturity,
            "account_number": generate_account_number(),
            "credit_limit": None,
            "available_balance": None,
            "principal_amount": cd_balance,
            "interest_rate": rate,
            "loan_term_months": None,
            "payoff_amount": None,
            "outstanding_balance": None,
            "cd_term_months": term,
            "annual_yield": round(rate * 100, 2),
            "average_balance": cd_balance,
            "tin_type": random.choice(["SSN", "EIN"]),
            "tin_number": generate_ssn_masked(),
            "coverage_amount": None,
            "premium_amount": None,
            "beneficiary_count": None,
            "policy_status": None,
            "policy_sub_status": None,
            "security_type": None,
            "units_held": None,
            "purchase_price": None,
            "current_value": None,
            "current_balance": round(cd_balance * (1 + rate * term / 12 / 2), 2),
            "currency": "USD",
        })
        account_counter += 1
        current_product_count += 1

    # Insurance - varies significantly by life stage
    insurance_chances = {
        "College Student": 0.05,  # Almost never
        "Digital Native": 0.12,
        "Young Parent": 0.50,  # High - protecting family
        "Frequent Traveler": 0.35,  # Travel insurance
        "Boomer": 0.45,  # Life insurance, property
    }
    insurance_chance = insurance_chances.get(persona, 0.20)
    has_life_insurance = False

    if random.random() < insurance_chance and current_product_count < product_count_target + 2:
        ins_product = random.choice(PRODUCTS_BY_CAT["Insurance"])
        coverage = random.choice([100000, 250000, 500000, 1000000])
        premium = coverage * 0.005 / 12

        # Cross-sell signal: 40% of mortgage holders DON'T have life insurance
        if has_mortgage and random.random() < 0.4:
            pass  # Skip insurance - creates cross-sell opportunity
        else:
            has_life_insurance = "Life" in ins_product["product_name"]
            accounts.append({
                "account_id": f"ACC-{str(account_counter).zfill(8)}",
                "customer_id": c_id,
                "account_type": "Insurance",
                "product_name": ins_product["product_name"],
                "status": "Active",
                "open_date": fake.date_between(start_date=join_date, end_date=END_DATE.date()),
                "maturity_date": None,
                "account_number": generate_account_number(),
                "credit_limit": None,
                "available_balance": None,
                "principal_amount": None,
                "interest_rate": None,
                "loan_term_months": None,
                "payoff_amount": None,
                "outstanding_balance": None,
                "cd_term_months": None,
                "annual_yield": None,
                "average_balance": None,
                "tin_type": None,
                "tin_number": None,
                "coverage_amount": coverage,
                "premium_amount": round(premium, 2),
                "beneficiary_count": random.randint(1, 3),
                "policy_status": random.choice(["Active", "Active", "Active", "New Business"]),
                "policy_sub_status": "Premium Paying",
                "security_type": None,
                "units_held": None,
                "purchase_price": None,
                "current_value": None,
                "current_balance": 0,
                "currency": "USD",
            })
            account_counter += 1
            current_product_count += 1

    # Securities - varies by wealth and age
    sec_chances = {
        "College Student": 0.03,  # Almost never
        "Digital Native": 0.15,  # Some into crypto/stocks
        "Young Parent": 0.20,
        "Frequent Traveler": 0.40,  # High income, investing
        "Boomer": 0.50,  # Retirement investments
    }
    sec_chance = sec_chances.get(persona, 0.15)
    if segment == "High Net Worth":
        sec_chance += 0.30  # HNW definitely investing

    if random.random() < sec_chance and current_product_count < product_count_target + 2:
        sec_product = random.choice(PRODUCTS_BY_CAT["Securities"])
        units = random.randint(10, 500)
        purchase_price = random.uniform(20, 200)
        current_price = purchase_price * random.uniform(0.8, 1.4)

        accounts.append({
            "account_id": f"ACC-{str(account_counter).zfill(8)}",
            "customer_id": c_id,
            "account_type": "Securities",
            "product_name": sec_product["product_name"],
            "status": "Active",
            "open_date": fake.date_between(start_date=join_date, end_date=END_DATE.date()),
            "maturity_date": None,
            "account_number": generate_account_number(),
            "credit_limit": None,
            "available_balance": None,
            "principal_amount": None,
            "interest_rate": None,
            "loan_term_months": None,
            "payoff_amount": None,
            "outstanding_balance": None,
            "cd_term_months": None,
            "annual_yield": None,
            "average_balance": None,
            "tin_type": None,
            "tin_number": None,
            "coverage_amount": None,
            "premium_amount": None,
            "beneficiary_count": None,
            "policy_status": None,
            "policy_sub_status": None,
            "security_type": sec_product["product_type"],
            "units_held": units,
            "purchase_price": round(purchase_price, 2),
            "current_value": round(current_price * units, 2),
            "current_balance": round(current_price * units, 2),
            "currency": "USD",
        })
        account_counter += 1

df_account = pd.DataFrame(accounts)

# --- 6. GENERATE fact_transaction ---
print("Generating fact_transaction...")
transactions = []
txn_counter = 1

# Create account lookup
customer_accounts = df_account.groupby("customer_id").apply(lambda x: x.to_dict("records")).to_dict()

for _, cust in df_customer.iterrows():
    c_id = cust["customer_id"]
    persona = cust["persona_tag"]
    p_config = PERSONAS[persona]
    join_date = cust["join_date"]
    churn_date = cust["churn_date"]

    active_end = churn_date if churn_date else END_DATE.date()
    if isinstance(active_end, datetime):
        active_end = active_end.date()

    days_active = (active_end - join_date).days
    if days_active < 1:
        continue

    # Get customer's CASA account for transactions
    cust_accounts = customer_accounts.get(c_id, [])
    casa_accounts = [a for a in cust_accounts if a["account_type"] == "CASA"]
    card_accounts = [a for a in cust_accounts if a["account_type"] == "Credit Card"]

    if not casa_accounts:
        continue

    primary_account = casa_accounts[0]

    # Monthly spend based on persona
    monthly_spend = random.uniform(*p_config["monthly_spend_range"])

    # Generate salary credits (1st or 15th of month)
    if cust["employment_type"] == "Salaried":
        salary_day = random.choice([1, 15])
        salary_amount = {"<25K": 1500, "25-50K": 3000, "50-100K": 6000, "100-250K": 12000, "250K+": 20000}
        salary = salary_amount.get(cust["income_bracket"], 4000)

        current_month = datetime(join_date.year, join_date.month, 1)
        while current_month.date() < active_end:
            pay_date = current_month.replace(day=min(salary_day, 28))
            if join_date <= pay_date.date() < active_end:
                transactions.append({
                    "transaction_id": f"TXN-{str(txn_counter).zfill(10)}",
                    "customer_id": c_id,
                    "account_id": primary_account["account_id"],
                    "merchant_id": "MERCH-100",
                    "date_key": int(pay_date.strftime("%Y%m%d")),
                    "transaction_date": pay_date,
                    "amount": round(salary + random.uniform(-100, 100), 2),
                    "transaction_type": "credit",
                    "payment_method": "Bank Transfer",
                    "mcc_category": "Income",
                    "is_recurring": True,
                    "recurring_frequency": "monthly",
                    "counterparty_type": "external",
                    "counterparty_name": "Employer",
                    "description": "Direct Deposit - Salary",
                    "channel": "Online",
                    "reference_number": f"SAL{txn_counter}",
                })
                txn_counter += 1
            current_month = (current_month.replace(day=1) + timedelta(days=32)).replace(day=1)

    # Generate subscription transactions (monthly recurring)
    subscriptions = random.sample(
        [m for m in MERCHANTS if m["is_subscription_merchant"]],
        k=random.randint(1, 4)
    )
    for sub in subscriptions:
        sub_amount = {"Netflix": 15.99, "Spotify": 9.99, "Amazon Prime": 14.99, "Disney+": 7.99,
                      "Planet Fitness": 24.99, "Apple Music": 10.99, "Verizon": 85, "AT&T": 75,
                      "Comcast": 120, "City Power Co": 150}.get(sub["merchant_name"], 20)

        sub_day = random.randint(1, 28)
        current_month = datetime(join_date.year, join_date.month, 1)
        while current_month.date() < active_end:
            sub_date = current_month.replace(day=sub_day)
            if join_date <= sub_date.date() < active_end:
                use_card = card_accounts and random.random() < 0.6
                account = card_accounts[0] if use_card else primary_account

                transactions.append({
                    "transaction_id": f"TXN-{str(txn_counter).zfill(10)}",
                    "customer_id": c_id,
                    "account_id": account["account_id"],
                    "merchant_id": sub["merchant_id"],
                    "date_key": int(sub_date.strftime("%Y%m%d")),
                    "transaction_date": sub_date,
                    "amount": round(sub_amount, 2),
                    "transaction_type": "debit",
                    "payment_method": "Credit Card" if use_card else "Direct Debit",
                    "mcc_category": sub["mcc_category"],
                    "is_recurring": True,
                    "recurring_frequency": "monthly",
                    "counterparty_type": "external",
                    "counterparty_name": sub["merchant_name"],
                    "description": f"{sub['merchant_name']} Monthly",
                    "channel": "Online",
                    "reference_number": f"SUB{txn_counter}",
                })
                txn_counter += 1
            current_month = (current_month.replace(day=1) + timedelta(days=32)).replace(day=1)

    # Generate regular spending transactions (persona-driven with individual variance)
    # Get unique spending profile for this customer
    spending_profile = get_customer_spending_profile(cust, persona)

    # Variable transaction frequency - not uniform
    # Spending personality affects frequency too (big spenders shop more often)
    base_txns = int(days_active / 2.5)
    freq_mult = 0.7 + (spending_profile["spending_personality"] - 1.0) * 0.3  # personality affects freq
    num_txns = int(base_txns * random.uniform(0.6, 1.5) * freq_mult)
    preferred_categories = p_config["spending_categories"]
    weekend_mult = p_config.get("weekend_spending_mult", 1.0)

    for _ in range(num_txns):
        # Generate date with day-of-week bias based on persona
        for attempt in range(10):  # Try up to 10 times to get right day distribution
            txn_date = fake.date_between(start_date=join_date, end_date=active_end)
            txn_datetime = datetime.combine(txn_date, datetime.min.time())
            is_weekend = txn_datetime.weekday() >= 5

            # Strong day-of-week filtering based on persona
            if weekend_mult > 1.3:  # Weekend-heavy personas (Students, Digital Natives)
                if not is_weekend and random.random() < 0.35:
                    continue  # 35% chance to skip weekday transactions
                break
            elif weekend_mult < 0.9:  # Weekday-heavy personas (Boomers)
                if is_weekend and random.random() < 0.45:
                    continue  # 45% chance to skip weekend transactions
                break
            else:
                break  # Normal personas - accept any day

        # Category selection - mix of persona preference and general spending
        # Everyone travels sometimes (vacations, business), not just Frequent Travelers
        month = txn_datetime.month

        # Seasonal travel boost (summer vacation, holidays, spring break)
        # Much lower rates - travel is occasional, not frequent
        travel_boost = 0.0
        if month in [6, 7, 8]:  # Summer - 1-2 vacation transactions
            travel_boost = 0.03
        elif month in [11, 12]:  # Holiday season
            travel_boost = 0.025
        elif month == 3:  # Spring break
            travel_boost = 0.015

        # Age/wealth affects travel slightly
        age = cust["age"]
        if 25 <= age <= 45:
            travel_boost += 0.01
        if cust["segment"] in ["Affluent", "High Net Worth"]:
            travel_boost += 0.015

        # Random travel decision - only for non-Travelers
        if random.random() < travel_boost and persona != "Frequent Traveler":
            category = "Travel"
        elif random.random() < 0.45 and preferred_categories:  # Reduced to 45% persona preference
            category = random.choice(preferred_categories)
        else:
            # General categories everyone uses, weighted by individual factors
            general_cats = ["Groceries", "Dining", "Shopping", "Gas", "Healthcare", "Entertainment"]
            weights = [1.0, 1.0, 1.0, 0.8, 0.5, 0.7]

            # Age-based adjustments with randomness
            age = cust["age"]
            if age < 30:
                weights[1] *= random.uniform(1.2, 1.8)  # Young people dine out more
                weights[5] *= random.uniform(1.2, 1.7)  # More entertainment
                weights[4] *= random.uniform(0.3, 0.6)  # Less healthcare
            elif age > 55:
                weights[4] *= random.uniform(1.5, 2.5)  # Healthcare increases with age
                weights[1] *= random.uniform(0.6, 0.9)  # Less dining out
                weights[5] *= random.uniform(0.5, 0.8)  # Less entertainment

            # Gender-based category preferences from spending profile
            for cat_idx, cat_name in enumerate(general_cats):
                cat_pref = spending_profile["category_preferences"].get(cat_name, 1.0)
                weights[cat_idx] *= cat_pref

            # Family adjustments
            if cust.get("has_children"):
                weights[0] *= random.uniform(1.2, 1.5)  # More groceries for families
                weights[2] *= random.uniform(1.1, 1.4)  # More shopping (kids stuff)
                weights[5] *= random.uniform(1.0, 1.3)  # Family entertainment

            # Income adjustments - higher income more dining/entertainment
            if cust["income_bracket"] in ["100-250K", "250K+"]:
                weights[1] *= random.uniform(1.1, 1.4)  # More dining
                weights[5] *= random.uniform(1.1, 1.3)  # More entertainment

            # Add random noise to all weights for individual variation
            weights = [w * random.uniform(0.7, 1.3) for w in weights]

            category = random.choices(general_cats, weights=weights)[0]

        merchants_in_cat = MERCHANTS_BY_CATEGORY.get(category, MERCHANTS_BY_CATEGORY["Shopping"])
        merchant = random.choice(merchants_in_cat)

        # Amount based on category - REDUCED Travel, more realistic ranges
        # Travel: Most travel purchases are small (Uber $15-40, meals while traveling $30-80)
        # Big travel purchases (flights, hotels) are occasional, handled separately
        amount_ranges = {
            "Groceries": (20, 180),
            "Dining": (8, 85),
            "Travel": (15, 150),  # Reduced! Most travel txns are small (rideshare, parking, snacks)
            "Utilities": (40, 200),
            "Subscriptions": (5, 50),
            "Healthcare": (15, 350),
            "Shopping": (15, 400),
            "Gas": (25, 75),
            "Entertainment": (8, 100),
        }
        amt_range = amount_ranges.get(category, (10, 100))
        amount = random.uniform(*amt_range)

        # Occasional BIG travel purchases (flights, hotels) - 15% of travel transactions
        if category == "Travel" and random.random() < 0.15:
            # Big travel: flight ($200-800), hotel stay ($150-500)
            amount = random.choice([
                random.uniform(200, 600),   # Domestic flight
                random.uniform(400, 1200),  # International flight
                random.uniform(100, 400),   # Hotel night
                random.uniform(300, 800),   # Weekend getaway package
            ])

        # Apply individual spending profile multiplier
        amount *= spending_profile["overall_multiplier"]

        # Apply category preference if exists
        cat_pref = spending_profile["category_preferences"].get(category, 1.0)
        amount *= cat_pref

        # Apply seasonal multiplier
        amount *= get_seasonal_multiplier(txn_datetime)

        # Weekend effect - but with individual variance
        if is_weekend:
            weekend_effect = weekend_mult * random.uniform(0.8, 1.2)  # Add noise to weekend mult
            amount *= weekend_effect

        # Payday spike - people spend more right after payday
        if is_payday(txn_datetime):
            amount *= random.uniform(1.05, 1.25)  # Reduced from 1.1-1.4

        # Segment quality multiplier (HNW buys premium, Mass Market buys budget)
        amount *= spending_profile["segment_quality"]

        # Round to realistic amount
        amount = round_to_realistic_amount(amount)

        use_card = card_accounts and random.random() < 0.5
        account = card_accounts[0] if use_card else primary_account

        transactions.append({
            "transaction_id": f"TXN-{str(txn_counter).zfill(10)}",
            "customer_id": c_id,
            "account_id": account["account_id"],
            "merchant_id": merchant["merchant_id"],
            "date_key": int(txn_datetime.strftime("%Y%m%d")),
            "transaction_date": txn_datetime,
            "amount": amount,
            "transaction_type": "debit",
            "payment_method": "Credit Card" if use_card else random.choice(["Debit Card", "Bank Transfer"]),
            "mcc_category": merchant["mcc_category"],
            "is_recurring": False,
            "recurring_frequency": None,
            "counterparty_type": "external",
            "counterparty_name": merchant["merchant_name"],
            "description": f"Purchase at {merchant['merchant_name']}",
            "channel": random.choice(["App", "POS", "Online"]),
            "reference_number": f"PUR{txn_counter}",
        })
        txn_counter += 1

df_transaction = pd.DataFrame(transactions)

# --- 7. GENERATE fact_account_snapshot ---
print("Generating fact_account_snapshot...")
snapshots = []
snapshot_counter = 1

for _, acc in df_account.iterrows():
    acc_id = acc["account_id"]
    c_id = acc["customer_id"]
    cust = df_customer[df_customer["customer_id"] == c_id].iloc[0]

    open_date = acc["open_date"]
    if isinstance(open_date, str):
        open_date = datetime.strptime(open_date, "%Y-%m-%d").date()

    churn_date = cust["churn_date"]
    active_end = churn_date if churn_date else END_DATE.date()
    if isinstance(active_end, datetime):
        active_end = active_end.date()

    # Monthly snapshots
    current = datetime(open_date.year, open_date.month, 1)
    balance = acc["current_balance"] or 0

    while current.date() < active_end and current.date() <= END_DATE.date():
        # Simulate balance changes
        if acc["account_type"] == "CASA":
            change = random.uniform(-0.05, 0.08)
            balance = max(0, balance * (1 + change))
        elif acc["account_type"] == "Credit Card":
            balance = random.uniform(0, acc["credit_limit"] * 0.7)
        elif acc["account_type"] == "Loan":
            # Gradual paydown
            balance = max(0, balance * 0.98)

        snapshot_date = current.date()
        date_key = int(current.strftime("%Y%m%d"))

        snapshots.append({
            "snapshot_id": f"SNAP-{str(snapshot_counter).zfill(10)}",
            "account_id": acc_id,
            "customer_id": c_id,
            "date_key": date_key,
            "snapshot_date": snapshot_date,
            "balance": round(balance, 2),
            "month_avg_balance": round(balance * 0.95, 2),
            "month_end_balance": round(balance, 2),
            "available_credit": round(acc["credit_limit"] - balance, 2) if acc["account_type"] == "Credit Card" else None,
            "credit_utilization_pct": round(balance / acc["credit_limit"] * 100, 1) if acc["account_type"] == "Credit Card" and acc["credit_limit"] else None,
            "principal_paid": round((acc["principal_amount"] or 0) - balance, 2) if acc["account_type"] == "Loan" else None,
            "principal_remaining": round(balance, 2) if acc["account_type"] == "Loan" else None,
            "interest_accrued": round(balance * (acc["interest_rate"] or 0) / 12, 2) if acc["account_type"] == "Loan" else None,
            "total_credits_mtd": round(random.uniform(1000, 10000), 2) if acc["account_type"] == "CASA" else None,
            "total_debits_mtd": round(random.uniform(800, 9000), 2) if acc["account_type"] == "CASA" else None,
            "net_cash_flow_mtd": None,
            "customer_product_count": len([a for a in customer_accounts.get(c_id, [])]),
        })
        snapshot_counter += 1

        current = (current + timedelta(days=32)).replace(day=1)

df_snapshot = pd.DataFrame(snapshots)
if not df_snapshot.empty and "total_credits_mtd" in df_snapshot.columns:
    df_snapshot["net_cash_flow_mtd"] = df_snapshot["total_credits_mtd"].fillna(0) - df_snapshot["total_debits_mtd"].fillna(0)

# --- 8. GENERATE fact_interaction ---
print("Generating fact_interaction...")
interactions = []
int_counter = 1

INTERACTION_REASONS = ["Account Inquiry", "Card Issue", "Loan Question", "Fee Dispute", "Password Reset",
                       "Statement Request", "Address Change", "New Product Interest", "Complaint", "General Info"]

for _, cust in df_customer.iterrows():
    c_id = cust["customer_id"]
    join_date = cust["join_date"]
    churn_date = cust["churn_date"]
    persona = cust["persona_tag"]
    p_config = PERSONAS[persona]

    active_end = churn_date if churn_date else END_DATE.date()
    if isinstance(active_end, datetime):
        active_end = active_end.date()

    days_active = (active_end - join_date).days
    if days_active < 1:
        continue

    # Variable interactions based on engagement with noise
    base_interactions = max(1, int(cust["engagement_score"] / 10))
    num_interactions = int(base_interactions * random.uniform(0.6, 1.5))
    num_interactions = max(1, num_interactions)

    # Get persona-specific channel preferences
    preferred_channels = p_config.get("preferred_channels", ["App", "Call Center", "Branch", "Chatbot"])

    for _ in range(num_interactions):
        int_date = fake.date_between(start_date=join_date, end_date=active_end)

        # Sentiment drops before churn - more gradual decline
        sentiment = random.uniform(0.55, 1.0)
        if cust["churn_status"] and churn_date:
            days_to_churn = (churn_date - int_date).days
            if days_to_churn < 14:
                sentiment = random.uniform(0.05, 0.35)
            elif days_to_churn < 30:
                sentiment = random.uniform(0.15, 0.45)
            elif days_to_churn < 60:
                sentiment = random.uniform(0.25, 0.55)
            elif days_to_churn < 90:
                sentiment = random.uniform(0.35, 0.65)

        # Use persona-preferred channels
        channel = random.choice(preferred_channels)

        # Duration varies by channel
        if channel == "Branch":
            duration = random.randint(10, 45)
        elif channel == "Call Center":
            duration = random.randint(5, 30)
        elif channel == "App":
            duration = random.randint(1, 10)
        else:  # Chatbot
            duration = random.randint(2, 15)

        interactions.append({
            "interaction_id": f"INT-{str(int_counter).zfill(10)}",
            "customer_id": c_id,
            "date_key": int(datetime.combine(int_date, datetime.min.time()).strftime("%Y%m%d")),
            "interaction_date": int_date,
            "channel": channel,
            "interaction_type": random.choice(["Inquiry", "Inquiry", "Complaint", "Request", "Feedback"]),
            "reason": random.choice(INTERACTION_REASONS),
            "sentiment_score": round(sentiment, 2),
            "resolution_status": random.choices(["Resolved", "Pending", "Escalated"], weights=[0.75, 0.15, 0.10])[0],
            "duration_minutes": duration,
        })
        int_counter += 1

df_interaction = pd.DataFrame(interactions)

# --- 9. GENERATE fact_loan_schedule ---
print("Generating fact_loan_schedule...")
loan_schedules = []
schedule_counter = 1

loan_accounts = df_account[df_account["account_type"] == "Loan"]

for _, loan in loan_accounts.iterrows():
    acc_id = loan["account_id"]
    c_id = loan["customer_id"]
    principal = loan["principal_amount"]
    rate = loan["interest_rate"]
    term = loan["loan_term_months"]
    open_date = loan["open_date"]

    if not principal or not term:
        continue

    # Calculate monthly payment (simplified)
    monthly_rate = rate / 12
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**term) / ((1 + monthly_rate)**term - 1)
    else:
        monthly_payment = principal / term

    remaining = principal
    current = datetime(open_date.year, open_date.month, 1) + timedelta(days=32)
    current = current.replace(day=1)

    for payment_num in range(1, min(term + 1, 37)):  # Cap at 36 payments for data size
        if current.date() > END_DATE.date():
            break

        interest_portion = remaining * monthly_rate
        principal_portion = monthly_payment - interest_portion
        remaining = max(0, remaining - principal_portion)

        due_date = current.replace(day=min(15, 28))
        date_key = int(due_date.strftime("%Y%m%d"))

        # Payment status
        if due_date.date() < END_DATE.date() - timedelta(days=30):
            status = random.choices(["Paid", "Paid", "Paid", "Paid", "Overdue", "Prepaid"], weights=[0.85, 0.05, 0.03, 0.02, 0.03, 0.02])[0]
        else:
            status = "Scheduled"

        actual_date = None
        actual_amount = None
        extra_principal = 0
        days_past_due = 0

        if status == "Paid":
            actual_date = due_date.date() - timedelta(days=random.randint(0, 5))
            actual_amount = monthly_payment
        elif status == "Overdue":
            days_past_due = random.randint(1, 30)
            actual_date = due_date.date() + timedelta(days=days_past_due)
            actual_amount = monthly_payment
        elif status == "Prepaid":
            actual_date = due_date.date() - timedelta(days=random.randint(5, 15))
            extra_principal = random.uniform(500, 5000)
            actual_amount = monthly_payment + extra_principal
            remaining = max(0, remaining - extra_principal)

        loan_schedules.append({
            "schedule_id": f"SCHED-{str(schedule_counter).zfill(10)}",
            "account_id": acc_id,
            "customer_id": c_id,
            "date_key": date_key,
            "due_date": due_date.date(),
            "payment_number": payment_num,
            "total_payments": term,
            "payment_due": round(monthly_payment, 2),
            "principal_portion": round(principal_portion, 2),
            "interest_portion": round(interest_portion, 2),
            "payment_status": status,
            "actual_payment_date": actual_date,
            "actual_amount_paid": round(actual_amount, 2) if actual_amount else None,
            "extra_principal_paid": round(extra_principal, 2) if extra_principal else 0,
            "days_past_due": days_past_due,
            "late_fee_charged": 25 if days_past_due > 0 else 0,
            "cumulative_principal_paid": round(principal - remaining, 2),
            "remaining_balance": round(remaining, 2),
        })
        schedule_counter += 1

        current = (current + timedelta(days=32)).replace(day=1)

df_loan_schedule = pd.DataFrame(loan_schedules)

# --- EXPORT ---
print("\nExporting to CSV...")
df_date.to_csv(f"{OUTPUT_DIR}/dim_date.csv", index=False)
df_product.to_csv(f"{OUTPUT_DIR}/dim_product.csv", index=False)
df_merchant.to_csv(f"{OUTPUT_DIR}/dim_merchant.csv", index=False)
df_customer.to_csv(f"{OUTPUT_DIR}/dim_customer.csv", index=False)
df_account.to_csv(f"{OUTPUT_DIR}/dim_account.csv", index=False)
df_transaction.to_csv(f"{OUTPUT_DIR}/fact_transaction.csv", index=False)
df_snapshot.to_csv(f"{OUTPUT_DIR}/fact_account_snapshot.csv", index=False)
df_interaction.to_csv(f"{OUTPUT_DIR}/fact_interaction.csv", index=False)
df_loan_schedule.to_csv(f"{OUTPUT_DIR}/fact_loan_schedule.csv", index=False)

print("\n" + "="*60)
print("DATA GENERATION COMPLETE")
print("="*60)
print(f"\nDimension Tables:")
print(f"  dim_date:     {len(df_date):,} rows")
print(f"  dim_product:  {len(df_product):,} rows")
print(f"  dim_merchant: {len(df_merchant):,} rows")
print(f"  dim_customer: {len(df_customer):,} rows")
print(f"  dim_account:  {len(df_account):,} rows")
print(f"\nFact Tables:")
print(f"  fact_transaction:      {len(df_transaction):,} rows")
print(f"  fact_account_snapshot: {len(df_snapshot):,} rows")
print(f"  fact_interaction:      {len(df_interaction):,} rows")
print(f"  fact_loan_schedule:    {len(df_loan_schedule):,} rows")
print(f"\nPersona Distribution:")
for persona in PERSONAS:
    count = len(df_customer[df_customer["persona_tag"] == persona])
    pct = count / len(df_customer) * 100
    print(f"  {persona}: {count:,} ({pct:.1f}%)")
print(f"\nCross-sell Signals:")
mortgage_holders = set(df_account[df_account["product_name"] == "Home Mortgage"]["customer_id"])
life_insurance_holders = set(df_account[df_account["product_name"].str.contains("Life", na=False)]["customer_id"])
mortgage_no_life = mortgage_holders - life_insurance_holders
print(f"  Mortgage holders without life insurance: {len(mortgage_no_life)}")
print(f"\nRecurring Transactions: {len(df_transaction[df_transaction['is_recurring'] == True]):,}")
print(f"\nFiles saved to: {OUTPUT_DIR}/")
