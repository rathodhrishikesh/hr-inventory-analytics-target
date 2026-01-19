import pandas as pd
import numpy as np

np.random.seed(42)

stores = ["Minneapolis", "Chicago", "Dallas", "Atlanta"]
store_multipliers = {"Minneapolis": 0.9, "Chicago": 1.2, "Dallas": 1.1, "Atlanta": 0.8}

categories = ["Electronics", "Home", "Grocery", "Apparel"]
category_demand = {"Electronics": 15, "Home": 18, "Grocery": 35, "Apparel": 20}

# Create product profile with varying demand levels
products = [f"P{i}" for i in range(1, 21)]
product_profiles = {
    p: {
        "base_demand": np.random.choice([5, 10, 15, 20, 30, 40]),  # Fast vs slow movers
        "price": np.random.uniform(15, 150),
        "cost_margin": np.random.uniform(0.55, 0.65),
        "category": np.random.choice(categories)
    }
    for p in products
}

rows = []
date_range = pd.date_range("2024-01-01", "2025-12-31")

for store in stores:
    for product in products:
        profile = product_profiles[product]
        store_mult = store_multipliers[store]
        
        for day in date_range:
            # Base demand from product profile
            base = profile["base_demand"]
            
            # Add seasonality (higher in Q4)
            month = day.month
            seasonality = 1.0 + 0.3 * np.sin(2 * np.pi * month / 12)
            
            # Add weekly pattern (lower on weekends)
            weekday = day.weekday()
            weekly_factor = 0.7 if weekday >= 5 else 1.1
            
            # Add random noise
            noise = np.random.normal(1.0, 0.15)
            
            # Calculate demand
            demand = max(0, int(base * seasonality * weekly_factor * store_mult * noise))
            
            # Consistent pricing per product
            price = profile["price"]
            
            # Realistic cost margin per product
            cost = price * profile["cost_margin"]
            
            rows.append([
                day,
                store,
                product,
                profile["category"],
                demand,
                price,
                cost
            ])

df = pd.DataFrame(rows, columns=["Date","Store","Product","Category","Units_Sold","Price","Cost"])
df["Revenue"] = df["Units_Sold"] * df["Price"]
df.to_csv("sales_data.csv", index=False)
print("sales_data.csv generated with realistic variation")
