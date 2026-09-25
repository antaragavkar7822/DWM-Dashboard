import pandas as pd


def load_data():

    df_date = pd.read_csv("data/dim_date_rows.csv")
    df_store = pd.read_csv("data/dim_store_rows.csv")
    df_product = pd.read_csv("data/dim_product_rows.csv")
    df_customer = pd.read_csv("data/dim_customer_rows.csv")
    df_sales = pd.read_csv("data/fact_sales_rows.csv")

    return (
        df_date,
        df_store,
        df_product,
        df_customer,
        df_sales
    )


def prepare_olap_data():

    (
        df_date,
        df_store,
        df_product,
        df_customer,
        df_sales
    ) = load_data()

    # Make sure keys have correct type
    df_date["date_key"] = df_date["date_key"].astype(int)
    df_sales["date_key"] = df_sales["date_key"].astype(int)

    df_store["store_key"] = df_store["store_key"].astype(int)
    df_sales["store_key"] = df_sales["store_key"].astype(int)

    df_product["product_key"] = df_product["product_key"].astype(int)
    df_sales["product_key"] = df_sales["product_key"].astype(int)

    df_customer["customer_key"] = df_customer["customer_key"].astype(int)
    df_sales["customer_key"] = df_sales["customer_key"].astype(int)

    # ============================================================
    # QUERY 1 - TOTAL SALES
    # ============================================================

    total_sales = df_sales["line_total"].sum()

    # ============================================================
    # QUERY 2 - ROLL-UP
    # Store → Region
    # ============================================================

    region_sales = (
        df_sales
        .merge(
            df_store[["store_key", "region"]],
            on="store_key"
        )
        .groupby("region")["line_total"]
        .sum()
        .sort_values(ascending=False)
    )

    # ============================================================
    # QUERY 3 - DRILL-DOWN
    # Monthly Sales
    # ============================================================

    monthly_sales = (
        df_sales
        .merge(
            df_date[["date_key", "month"]],
            on="date_key"
        )
        .groupby("month")["line_total"]
        .sum()
        .sort_index()
    )

    # ============================================================
    # QUERY 4 - SLICE
    # North Region
    # ============================================================

    north_data = (
        df_sales
        .merge(
            df_store[["store_key", "region"]],
            on="store_key"
        )
        .merge(
            df_date[["date_key", "month"]],
            on="date_key"
        )
    )

    north_data = north_data[
        north_data["region"] == "North"
    ]

    north_monthly_sales = (
        north_data
        .groupby("month")["line_total"]
        .sum()
        .sort_index()
    )

    # ============================================================
    # QUERY 5 - DICE
    # North + South
    # Electronics + Clothing + Groceries
    # ============================================================

    dice_data = (
        df_sales
        .merge(
            df_store[["store_key", "region"]],
            on="store_key"
        )
        .merge(
            df_product[["product_key", "category_name"]],
            on="product_key"
        )
    )

    dice_data = dice_data[
        dice_data["region"].isin(["North", "South"])
        &
        dice_data["category_name"].isin(
            ["Electronics", "Clothing", "Groceries"]
        )
    ]

    dice_sales = (
        dice_data
        .groupby(
            ["region", "category_name"]
        )["line_total"]
        .sum()
        .unstack()
    )

    # ============================================================
    # QUERY 6 - PIVOT
    # Region × Category
    # ============================================================

    pivot_data = (
        df_sales
        .merge(
            df_store[["store_key", "region"]],
            on="store_key"
        )
        .merge(
            df_product[["product_key", "category_name"]],
            on="product_key"
        )
    )

    pivot_sales = pd.pivot_table(
        pivot_data,
        values="line_total",
        index="region",
        columns="category_name",
        aggfunc="sum"
    )

    # ============================================================
    # QUERY 7 - CATEGORY SALES
    # ============================================================

    category_sales = (
        df_sales
        .merge(
            df_product[
                ["product_key", "category_name"]
            ],
            on="product_key"
        )
        .groupby("category_name")["line_total"]
        .sum()
        .sort_values(ascending=False)
    )

    # ============================================================
    # QUERY 8 - BRAND SALES
    # ============================================================

    brand_sales = (
        df_sales
        .merge(
            df_product[
                ["product_key", "brand"]
            ],
            on="product_key"
        )
        .groupby("brand")["line_total"]
        .sum()
        .sort_values(ascending=True)
    )

    # ============================================================
    # QUERY 9 - STORE TYPE SALES
    # ============================================================

    store_type_sales = (
        df_sales
        .merge(
            df_store[
                ["store_key", "store_type"]
            ],
            on="store_key"
        )
        .groupby("store_type")["line_total"]
        .sum()
        .sort_values(ascending=False)
    )

    # ============================================================
    # QUERY 10 - LOYALTY SALES
    # ============================================================

    loyalty_sales = (
        df_sales
        .merge(
            df_customer[
                ["customer_key", "loyalty_member"]
            ],
            on="customer_key"
        )
        .groupby("loyalty_member")["line_total"]
        .sum()
    )

    return {
        "df_date": df_date,
        "df_store": df_store,
        "df_product": df_product,
        "df_customer": df_customer,
        "df_sales": df_sales,

        "total_sales": total_sales,
        "region_sales": region_sales,
        "monthly_sales": monthly_sales,
        "north_monthly_sales": north_monthly_sales,
        "dice_sales": dice_sales,
        "pivot_sales": pivot_sales,
        "category_sales": category_sales,
        "brand_sales": brand_sales,
        "store_type_sales": store_type_sales,
        "loyalty_sales": loyalty_sales
    }