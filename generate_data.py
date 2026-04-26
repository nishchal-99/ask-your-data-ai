import pandas as pd
import random
from datetime import datetime, timedelta

regions = ["East", "West", "South", "North"]
categories = {
    "Furniture": ["Chair", "Table", "Sofa"],
    "Technology": ["Phone", "Laptop", "Tablet"],
    "Office Supplies": ["Paper", "Pen", "Notebook"]
}

products = {
    "Chair": ["Office Chair", "Dining Chair"],
    "Table": ["Study Table", "Coffee Table"],
    "Sofa": ["Living Room Sofa"],
    "Phone": ["iPhone", "Samsung Galaxy"],
    "Laptop": ["Dell Laptop", "HP Laptop"],
    "Tablet": ["iPad"],
    "Paper": ["A4 Paper Pack"],
    "Pen": ["Ball Pen"],
    "Notebook": ["Spiral Notebook"]
}

data = []

start_date = datetime(2025, 1, 1)

for i in range(1000):  # change to 2000 if you want more
    category = random.choice(list(categories.keys()))
    sub_category = random.choice(categories[category])
    product = random.choice(products[sub_category])

    order_date = start_date + timedelta(days=random.randint(0, 90))

    sales = random.randint(20, 1500)
    quantity = random.randint(1, 10)
    profit = round(sales * random.uniform(0.1, 0.3), 2)

    data.append([
        1000 + i,
        order_date.strftime("%Y-%m-%d"),
        random.choice(regions),
        category,
        sub_category,
        product,
        sales,
        quantity,
        profit
    ])

df = pd.DataFrame(data, columns=[
    "order_id", "order_date", "region", "category",
    "sub_category", "product_name", "sales",
    "quantity", "profit"
])

df.to_csv("sales_data.csv", index=False)

print("Dataset generated: sales_data.csv")
