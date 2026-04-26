import random
from datetime import datetime, timedelta

import pandas as pd


regions = ["East", "West", "South", "North"]

categories = {
    "Furniture": ["Chair", "Table", "Sofa", "Bookshelf", "Cabinet"],
    "Technology": ["Phone", "Laptop", "Tablet", "Monitor", "Printer"],
    "Office Supplies": ["Paper", "Pen", "Notebook", "Binder", "Stapler"],
}

products = {
    "Chair": ["Office Chair", "Dining Chair", "Ergonomic Chair"],
    "Table": ["Study Table", "Coffee Table", "Conference Table"],
    "Sofa": ["Living Room Sofa", "Sectional Sofa"],
    "Bookshelf": ["Wooden Bookshelf", "Metal Bookshelf"],
    "Cabinet": ["File Cabinet", "Storage Cabinet"],

    "Phone": ["iPhone", "Samsung Galaxy", "OnePlus Phone"],
    "Laptop": ["Dell Laptop", "HP Laptop", "MacBook"],
    "Tablet": ["iPad", "Samsung Tab"],
    "Monitor": ["LG Monitor", "Dell Monitor"],
    "Printer": ["HP Printer", "Canon Printer"],

    "Paper": ["A4 Paper Pack", "Legal Paper Pack"],
    "Pen": ["Ball Pen", "Gel Pen"],
    "Notebook": ["Spiral Notebook", "Hardcover Notebook"],
    "Binder": ["Office Binder", "Ring Binder"],
    "Stapler": ["Mini Stapler", "Heavy Duty Stapler"],
}


def generate_sales_data(row_count: int = 2000) -> pd.DataFrame:
    data = []
    start_date = datetime(2025, 1, 1)

    for i in range(row_count):
        category = random.choice(list(categories.keys()))
        sub_category = random.choice(categories[category])
        product = random.choice(products[sub_category])

        order_date = start_date + timedelta(days=random.randint(0, 364))
        sales = round(random.uniform(20, 2500), 2)
        quantity = random.randint(1, 10)
        profit_margin = random.uniform(-0.05, 0.35)
        profit = round(sales * profit_margin, 2)

        data.append(
            [
                1000 + i,
                order_date.strftime("%Y-%m-%d"),
                random.choice(regions),
                category,
                sub_category,
                product,
                sales,
                quantity,
                profit,
            ]
        )

    columns = [
        "order_id",
        "order_date",
        "region",
        "category",
        "sub_category",
        "product_name",
        "sales",
        "quantity",
        "profit",
    ]

    return pd.DataFrame(data, columns=columns)


if __name__ == "__main__":
    df = generate_sales_data(row_count=2000)
    df.to_csv("sales_data.csv", index=False)
    print("Dataset generated: sales_data.csv")