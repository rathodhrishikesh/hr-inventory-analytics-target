import pandas as pd
import numpy as np

np.random.seed(42)

stores = ["Minneapolis", "Chicago", "Dallas", "Atlanta"]
categories = ["Electronics", "Home", "Grocery", "Apparel"]
products = [f"P{i}" for i in range(1, 21)]

rows = []
for store in stores:
    for product in products:
        for day in pd.date_range("2024-01-01", "2025-12-31"):
            demand = max(0, int(np.random.normal(20, 5)))
            price = np.random.uniform(10, 100)
            cost = price * 0.6
            rows.append([day, store, product, np.random.choice(categories), demand, price, cost])

df = pd.DataFrame(rows, columns=["Date","Store","Product","Category","Units_Sold","Price","Cost"])
df["Revenue"] = df["Units_Sold"] * df["Price"]
df.to_csv("sales_data.csv", index=False)
print("sales_data.csv generated")
