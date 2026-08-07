import random
from faker import Faker
import pandas as pd

fake = Faker()

# ==========================================================
# CONFIG
# ==========================================================

NUM_USERS = 100000

countries = [
    "United States",
    "India",
    "United Kingdom",
    "Germany",
    "Canada",
    "Australia",
    "Singapore",
    "Japan",
    "France",
    "Brazil"
]

plans = [
    "Free",
    "Basic",
    "Pro",
    "Enterprise"
]

genders = [
    "Male",
    "Female"
]

statuses = [
    "Active",
    "Inactive",
    "Churned"
]

devices = [
    "Desktop",
    "Mobile",
    "Tablet"
]

channels = [
    "Organic Search",
    "Google Ads",
    "LinkedIn",
    "Facebook",
    "Instagram",
    "Referral",
    "Email",
    "Direct"
]

# ==========================================================
# GENERATE USERS
# ==========================================================

users = []

for user_id in range(1, NUM_USERS + 1):

    users.append({

        "user_id": user_id,

        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),

        "country": random.choice(countries),

        "device": random.choice(devices),

        "acquisition_channel": random.choice(channels),

        "plan": random.choice(plans),

        "gender": random.choice(genders),

        "age": random.randint(18,70),

        "status": random.choices(

            statuses,

            weights=[80,10,10]

        )[0]

    })

df = pd.DataFrame(users)

df.to_csv(

    "data/generated/users.csv",

    index=False

)

print("="*50)
print("Users Generated Successfully")
print("="*50)
print(df.head())
print()
print(f"Total Users : {len(df):,}")