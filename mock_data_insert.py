import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

db_url = "postgresql+psycopg2://example_user:exanmple_pass@localhost:5433/trendyol_db"
engine = create_engine(db_url)

brands = pd.DataFrame({"id": [1, 2], "name": ["BrandA", "BrandB"]})

categories = pd.DataFrame(
    {
        "id": [1, 2],
        "name": ["Clothing", "Electronics"],
        "parent_category_id": [None, None],
    }
)

category_attributes = pd.DataFrame(
    {
        "id": [1, 2, 3],
        "category_id": [1, 1, 2],
        "name": ["Color", "Size", "Warranty"],
        "type": ["string", "string", "string"],
        "required": [True, False, True],
    }
)

products = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "name": ["T-Shirt", "Jeans", "Smartphone", "Laptop", "Jacket"],
        "barcode": [
            "1234567890123",
            "1234567890124",
            "1234567890125",
            "1234567890126",
            "1234567890127",
        ],
        "brand_id": [1, 1, 2, 2, 1],
        "category_id": [1, 1, 2, 2, 1],
        "description": [
            "Comfortable cotton t-shirt",
            "Blue denim jeans",
            "Latest model smartphone",
            "Powerful laptop",
            "Winter jacket",
        ],
    }
)

product_attributes = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5, 7],
        "product_id": [1, 1, 2, 3, 4, 5],
        "attribute_id": [1, 2, 1, 3, 3, 1],
        "value": ["Red", "M", "Blue", "2 Years", "1 Year", "Black"],
    }
)
now = datetime.now()
product_inventory = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "product_id": [1, 2, 3, 4, 5],
        "quantity": [100, 150, 50, 30, 80],
        "list_price": [29.99, 49.99, 699.99, 1199.99, 89.99],
        "sale_price": [24.99, 44.99, 649.99, 1149.99, 79.99],
        "currency": ["TRY"] * 5,
        "created_at": [now] * 5,
        "updated_at": [now] * 5,
    }
)


def insert_df(df, table_name):
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"{table_name} tablosuna veri eklendi.")

insert_df(brands, 'brands')
insert_df(categories, 'categories')
insert_df(category_attributes, 'category_attributes')
insert_df(products, 'products')
insert_df(product_attributes, "product_attributes")
insert_df(product_inventory, "product_inventory")
