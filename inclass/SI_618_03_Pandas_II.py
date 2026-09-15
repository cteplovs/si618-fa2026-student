# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "matplotlib==3.11.1",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 618 · 03: pandas II, combining and reshaping

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** · Sessions 5 (Wed Sep 16) and 6 (Mon Sep 21)

    Copyright © 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.09.14.1.CT

    ---

    ## Learning objectives

    By the end of these two sessions you will be able to:

    - Load data that isn't a tidy comma-separated file: title rows, unusual
      missing-value markers, semicolons, and nested JSON from a web API
    - Clean join keys so that a merge matches the rows it should
    - Stack DataFrames with `pd.concat()` and join them with `pd.merge()`,
      choosing between inner, left, right and outer joins
    - Reshape between wide and long formats with `.melt()`, `.pivot()`,
      `.stack()` and `.unstack()`
    - Summarise groups with `.groupby()` and pivot tables
    - Plot a distribution as a histogram

    ## Pre-class reading

    Chen, D.Y. (2023). *Pandas for Everyone*, 2nd edition, the chapters on tidy
    data and on grouping.

    McKinney, W. (2022). *Python for Data Analysis*, 3rd edition, chapters 7
    (Data Cleaning and Preparation), 8 (Data Wrangling: Join, Combine, and
    Reshape) and 10 (Data Aggregation and Group Operations).

    ## Structure

    **Session 1, Wednesday.** Loading, combining and reshaping, followed by Team
    Challenge 1.

    **Session 2, Monday.** Grouping, pivot tables and histograms, followed by
    Team Challenge 2.

    One notebook across two sessions, submitted at the end of Monday.
    """)
    return


@app.cell
def _():
    import json
    from urllib.request import urlopen

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    return json, mo, np, pd, plt, urlopen


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1.1: CSV files that need a little help

    Notebook 02 loaded clean CSV files, where one call to `pd.read_csv()` was
    enough. Real files are often less cooperative, so here's one that isn't:
    NASA's record of global temperature anomalies, meaning how far each month
    was above or below the 1951–1980 average, in degrees Celsius.
    """)
    return


@app.cell
def _():
    GISTEMP_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    return (GISTEMP_URL,)


@app.cell
def _(GISTEMP_URL, pd):
    # Try the plain call first and look at what comes back.
    pd.read_csv(GISTEMP_URL).columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's a single column, named after a sentence. The first line of the file
    is a title, `Land-Ocean: Global Means`, rather than a header row, so pandas
    took the title as the header and couldn't make sense of the rest.
    `skiprows=1` tells it to ignore that first line.
    """)
    return


@app.cell
def _(GISTEMP_URL, pd):
    temps_raw = pd.read_csv(GISTEMP_URL, skiprows=1)
    temps_raw.tail()
    return (temps_raw,)


@app.cell
def _(temps_raw):
    temps_raw.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the types. Every month is a temperature, but some of them loaded as
    text. Scroll to the last row of `.tail()` above and you'll see why: months
    that haven't been reported yet are written as `***`. A single `***` anywhere
    in a column is enough to make pandas treat the whole column as text.

    This is the same problem as the zip codes in the Chicago data: the file is
    text, and pandas has to guess. `na_values` tells pandas which strings mean
    "missing", so it can stop guessing.
    """)
    return


@app.cell
def _(GISTEMP_URL, pd):
    temps = pd.read_csv(GISTEMP_URL, skiprows=1, na_values="***")
    temps.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every month column is now numeric. The unreported months are `NaN`, which is
    what they actually are.

    ❗️ This file gains a row every year, so don't write code that assumes it
    has a particular number of rows.

    ## Part 1.2: Other delimiters

    Not every "CSV" uses commas. Semicolons are common, especially in files
    from Europe, where the comma is often the decimal point. This is the UCI
    Wine Quality dataset: lab measurements for 1,599 red vinho verde wines from
    Portugal, each one rated for quality by tasters.
    """)
    return


@app.cell
def _():
    WINE_URL = (
        "https://archive.ics.uci.edu/ml/machine-learning-databases/"
        "wine-quality/winequality-red.csv"
    )
    return (WINE_URL,)


@app.cell
def _(WINE_URL, pd):
    # The plain call again. Look at the shape, and at the name of the only column.
    _wine_wrong = pd.read_csv(WINE_URL)
    _wine_wrong.shape, _wine_wrong.columns[0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 1,599 rows, but a single column whose name is the entire header line.
    pandas split each line at the commas, found none, and kept every line
    whole. `sep=";"` tells it what the separator really is.
    """)
    return


@app.cell
def _(WINE_URL, pd):
    wine = pd.read_csv(WINE_URL, sep=";")
    wine.head()
    return (wine,)


@app.cell
def _(wine):
    wine.dtypes
    return


@app.cell
def _(wine):
    # Now the data is usable. How generous were the tasters?
    wine["quality"].value_counts().sort_index()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Twelve numeric columns, as there should be. Most wines scored 5 or 6, and
    only 18 of them scored 8.

    If a file also writes decimals with commas, `decimal=","` handles those.
    Whenever a file loads as one wide column, check the separator first.

    ## Part 1.3: JSON from a web API

    JSON is what most web APIs return, and it's rarely a flat table. The US
    Geological Survey publishes every earthquake recorded in the past seven
    days as JSON, updated every minute, so your numbers will differ slightly
    from your neighbour's.
    """)
    return


@app.cell
def _():
    QUAKES_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    return (QUAKES_URL,)


@app.cell
def _(QUAKES_URL, pd):
    # read_json expects a flat list of records. See what it makes of this.
    try:
        _result = pd.read_json(QUAKES_URL)
    except ValueError as _err:
        _result = f"ValueError: {_err}"
    _result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    pandas can't build a table because this file isn't one. So load it as
    ordinary Python instead, and look at how it's organised.
    """)
    return


@app.cell
def _(QUAKES_URL, json, urlopen):
    with urlopen(QUAKES_URL) as _response:
        quakes_json = json.load(_response)
    list(quakes_json.keys()), len(quakes_json["features"])
    return (quakes_json,)


@app.cell
def _(quakes_json):
    # One earthquake, exactly as the API sends it.
    quakes_json["features"][0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's a dictionary. Its `features` key holds a list with one entry per
    earthquake, and each entry has more dictionaries nested inside it. Most of
    what we want sits under `properties`.

    `pd.json_normalize()` flattens that nesting. Each nested key becomes a
    column, named by its path with dots in between, so `properties.mag` is the
    `mag` inside `properties`.
    """)
    return


@app.cell
def _(pd, quakes_json):
    quakes = pd.json_normalize(quakes_json["features"])
    quakes.shape, list(quakes.columns)
    return (quakes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `properties.time` is a very large integer. It counts milliseconds since
    1 January 1970, which is how many APIs send times. Notebook 02's
    `pd.to_datetime()` converts it once you tell it the unit.

    A column name with a dot in it is one more reason to use brackets:
    `quakes.properties.mag` won't work, and `quakes["properties.mag"]` will.
    """)
    return


@app.cell
def _(pd, quakes):
    quakes_dated = quakes.assign(time=pd.to_datetime(quakes["properties.time"], unit="ms"))
    quakes_dated[["time", "properties.place", "properties.mag"]].sort_values(
        "properties.mag", ascending=False
    ).head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1.4: Excel, for reference

    Excel files work the same way, with a few extra parameters. We won't run
    this, since it needs the `openpyxl` package and a file to read, but the
    pattern is worth recognising:

    ```python
    pd.read_excel("file.xlsx", sheet_name="Sheet1")   # one sheet, by name
    pd.read_excel("file.xlsx", sheet_name=0)          # one sheet, by position
    pd.read_excel("file.xlsx", sheet_name=None)       # every sheet, as a dict
    ```

    `header`, `usecols`, `skiprows` and `na_values` all mean the same thing
    they mean for `read_csv`.

    ## Part 1.5: Cleaning keys before you merge

    A merge matches rows whose key values are *exactly* equal. `"A123"` and
    `"A123 "` look identical on screen, but they aren't equal, so they won't
    match.
    """)
    return


@app.cell
def _(pd):
    products_messy = pd.DataFrame(
        {
            "product_id": ["A123 ", "B456", " C789", "D012"],  # note the spaces
            "name": ["Widget", "Gadget", "Doohickey", "Thingamajig"],
        }
    )
    sales_messy = pd.DataFrame(
        {
            "product_id": ["A123", "B456", "C789"],
            "quantity": [10, 5, 8],
        }
    )
    products_messy, sales_messy
    return products_messy, sales_messy


@app.cell
def _(pd, products_messy, sales_messy):
    # Merging before cleaning. We'll cover merge properly in Part 2; for now,
    # watch the quantity column.
    pd.merge(products_messy, sales_messy, on="product_id", how="left")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only the Gadget found its quantity. The stray spaces stopped the other two
    from matching, and pandas didn't raise an error or warning. It filled in
    `NaN` and moved on. A merge that quietly matches fewer rows than it should
    is one of the most common bugs in data analysis, and the only way to catch
    it is to look.
    """)
    return


@app.cell
def _(pd, products_messy, sales_messy):
    products_clean = products_messy.assign(
        product_id=products_messy["product_id"].str.strip()
    )
    pd.merge(products_clean, sales_messy, on="product_id", how="left")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now three products match. The Thingamajig still has no quantity, but that's
    correct this time, because there are no sales for it.

    **String cleaning you'll use all the time:**

    | Expression | Does |
    |---|---|
    | `.str.strip()` | removes leading and trailing whitespace |
    | `.str.lower()`, `.str.upper()` | changes case |
    | `.str.replace("a", "b")` | replaces text |
    | `.astype(str)`, `.astype(int)` | converts the type, so `101` and `"101"` can match |

    ---
    ## Part 2.1: Stacking DataFrames with `concat`

    Use `pd.concat()` when you have several tables with the *same columns*, such
    as the same report for different quarters, and you want one long table.
    """)
    return


@app.cell
def _(pd):
    q1_sales = pd.DataFrame(
        {
            "product": ["Laptop", "Mouse", "Keyboard", "Monitor"],
            "units": [45, 120, 85, 32],
            "quarter": "Q1",
        }
    )
    q2_sales = pd.DataFrame(
        {
            "product": ["Laptop", "Mouse", "Keyboard", "Monitor"],
            "units": [52, 135, 91, 38],
            "quarter": "Q2",
        }
    )
    all_sales = pd.concat([q1_sales, q2_sales], ignore_index=True)
    all_sales
    return q1_sales, q2_sales


@app.cell
def _(pd, q1_sales, q2_sales):
    # Without ignore_index=True, each table keeps its own index, so the labels
    # 0-3 appear twice. .loc[0] would now return two rows.
    pd.concat([q1_sales, q2_sales])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2.2: Joining DataFrames with `merge`

    Use `pd.merge()` when two tables have *different* columns that share a key,
    such as a product catalogue and a list of sales that refer to products by
    ID. If you know SQL, this is a join.
    """)
    return


@app.cell
def _(pd):
    products = pd.DataFrame(
        {
            "product_id": [101, 102, 103, 104, 105],
            "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam"],
            "category": ["Computer", "Accessory", "Accessory", "Display", "Accessory"],
            "price": [899, 25, 75, 299, 89],
        }
    )
    transactions = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3, 4, 5, 6],
            "product_id": [101, 102, 101, 103, 104, 101],
            "quantity": [2, 5, 1, 3, 2, 1],
        }
    )
    products, transactions
    return products, transactions


@app.cell
def _(pd, products, transactions):
    # Inner join, the default: only keys that appear in both tables.
    pd.merge(transactions, products, on="product_id", how="inner")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Six rows, one per transaction. The Webcam (`105`) is missing, because
    nobody bought one, so its key isn't in `transactions`. Whether that's what
    you want depends on the question you're asking. The `how` parameter
    decides.
    """)
    return


@app.cell
def _(pd, products, transactions):
    # Left join: every row of the LEFT table, matched where possible.
    pd.merge(products, transactions, on="product_id", how="left")
    return


@app.cell
def _(pd, products, transactions):
    # Right join: every row of the RIGHT table.
    pd.merge(products, transactions, on="product_id", how="right")
    return


@app.cell
def _(pd, products, transactions):
    # Outer join: every row of both.
    pd.merge(products, transactions, on="product_id", how="outer")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | `how=` | Keeps | Use it when |
    |---|---|---|
    | `"inner"` | keys in both tables | you only care about matches |
    | `"left"` | every row of the left table | the left table is the thing you're describing |
    | `"right"` | every row of the right table | the same thing, the other way round |
    | `"outer"` | every row of both | you need to see what *didn't* match |

    Look at the left join again. The Webcam's `quantity` is `NaN`, and the whole
    column has become `float64`, because missing values force a column of
    integers to float. That's the same effect that turned Chicago's zip codes
    into `60614.0`.

    ## Part 2.3: Keys with different names

    Two tables often name the same key differently. `left_on` and `right_on`
    say which column to use on each side.
    """)
    return


@app.cell
def _(pd):
    customers = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "customer_name": ["Alice Corp", "Bob Industries", "Charlie LLC", "Delta Inc"],
            "region": ["East", "West", "East", "Central"],
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [101, 102, 103, 104, 105],
            "cust_id": [1, 2, 1, 3, 2],
            "amount": [1500, 2300, 800, 4200, 1900],
        }
    )
    customers, orders
    return customers, orders


@app.cell
def _(customers, orders, pd):
    pd.merge(orders, customers, left_on="cust_id", right_on="customer_id", how="left")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both key columns survive the merge, `cust_id` and `customer_id`, holding
    the same values. Drop one with `.drop(columns="cust_id")` if you don't need
    it.

    ### 🚀 Checkpoint 3.1

    ✅ Step 1: Left-merge `products` with `transactions` (products on the left),
    and assign the *number of rows* in the result to `n_left_rows`.

    ✅ Step 2: Merge `customers` and `orders` so that **every customer**
    appears, including any who have never ordered. Assign the result to
    `all_customers_orders`.
    """)
    return


@app.cell
def _():
    # Your code here.
    n_left_rows = None
    all_customers_orders = None
    return all_customers_orders, n_left_rows


@app.cell(hide_code=True)
def _(all_customers_orders, n_left_rows):
    def test_checkpoint_3_1():
        assert n_left_rows is not None, "Assign the row count to `n_left_rows`."
        assert n_left_rows == 7, (
            f"Expected 7 rows, got {n_left_rows}. Six transactions match, and a left "
            "join also keeps the product nobody bought."
        )
        assert all_customers_orders is not None, (
            "Assign your merge to `all_customers_orders`."
        )
        assert len(all_customers_orders) == 6, (
            f"Expected 6 rows, got {len(all_customers_orders)}. Which table has to be "
            "on the left for every customer to survive?"
        )
        assert "Delta Inc" in set(all_customers_orders["customer_name"]), (
            "Delta Inc has no orders but should still appear."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3.1: Wide and long

    The same numbers can be laid out two ways.

    - **Wide:** one row per product, one column per month. Easy to read, and
      it's what a spreadsheet usually looks like.
    - **Long:** one row per product *per month*, with a `month` column. Harder
      to read, but it's what most pandas operations, and most plotting
      libraries, expect.
    """)
    return


@app.cell
def _(pd):
    revenue_wide = pd.DataFrame(
        {
            "product": ["Laptop", "Monitor", "Keyboard"],
            "Jan": [45000, 18000, 6000],
            "Feb": [48000, 19500, 6300],
            "Mar": [52000, 21000, 6800],
            "Apr": [49000, 19800, 6500],
        }
    )
    revenue_wide
    return (revenue_wide,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3.2: Wide to long with `melt`

    `id_vars` names the columns that identify a row and should stay as they
    are. Every other column is "melted" into two new columns: one holding the
    old column name (`var_name`) and one holding the value (`value_name`).
    """)
    return


@app.cell
def _(revenue_wide):
    revenue_long = revenue_wide.melt(
        id_vars=["product"],
        var_name="month",
        value_name="revenue",
    )
    revenue_long
    return (revenue_long,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three products × four months = twelve rows.

    ## Part 3.3: Long to wide with `pivot`

    `pivot` reverses it. `index` becomes the rows, `columns` becomes the
    columns, and `values` fills the cells.
    """)
    return


@app.cell
def _(revenue_long):
    revenue_back = revenue_long.pivot(index="product", columns="month", values="revenue")
    revenue_back
    return (revenue_back,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The months came back in alphabetical order, Apr, Feb, Jan, Mar, because to
    pandas they're just strings. Selecting the columns with a list puts them
    back in order. Adding a column uses `.assign()`, as in notebook 02, rather
    than modifying `revenue_back` in place.
    """)
    return


@app.cell
def _(revenue_back):
    _months = ["Jan", "Feb", "Mar", "Apr"]
    revenue_ordered = revenue_back[_months]
    revenue_ordered.assign(jan_feb_change=revenue_ordered["Feb"] - revenue_ordered["Jan"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ❗️ `pivot` raises an error if any `index`/`columns` pair appears more than
    once, because it can't put two values in one cell. When your data has
    duplicates you need a *pivot table*, which combines them. That's Monday.

    ## Part 3.4: `stack` and `unstack`

    These do the same kind of reshaping for a DataFrame whose index has more
    than one level, called a MultiIndex. `unstack` moves the innermost index
    level up into the columns, and `stack` moves it back down.
    """)
    return


@app.cell
def _(pd):
    regional = pd.DataFrame(
        {
            "region": ["North", "North", "South", "South"],
            "quarter": ["Q1", "Q2", "Q1", "Q2"],
            "sales": [120, 135, 98, 112],
            "profit": [18, 22, 15, 19],
        }
    ).set_index(["region", "quarter"])
    regional
    return (regional,)


@app.cell
def _(regional):
    regional_wide = regional.unstack()
    regional_wide
    return (regional_wide,)


@app.cell
def _(regional_wide):
    regional_wide.stack()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🚀 Team Challenge 1: Build an integrated dataset

    **About 30 minutes, in teams.** Each person keeps their own copy, and
    submission on Monday is individual.

    You work for an e-commerce analytics company, and the data you need is
    spread across four tables:

    - `catalog`: one row per product, keyed by `sku`
    - `sales_wide`: units sold per month, **wide**, keyed by `product_sku`
    - `segments`: customer segments and their discount rates
    - `product_segments`: how much each segment likes each product

    Look at all four before you start.

    ### Milestones

    **Milestone 1, reshape.** Convert `sales_wide` to long format, with the
    columns `product_sku`, `month` and `units_sold`. Assign it to `sales_long`.

    **Milestone 2, add product information.** Merge `sales_long` with
    `catalog`, bearing in mind the keys have different names. Assign it to
    `sales_with_products`.

    **Milestone 3, revenue.** Add a `revenue` column (units sold × price) with
    `.assign()`, and assign the result to `sales_revenue`. Then find the product
    with the most revenue across all four months (`top_product`), and the month
    with the most revenue across all products (`top_month`).

    *Hint:* pivot `sales_revenue` so products are rows and months are columns.
    `.sum(axis=1)` totals each row, `.sum()` totals each column, and `.idxmax()`
    from notebook 02 gives you the label of the largest value.

    **Milestone 4, segments.** Merge `product_segments` with `segments`, and
    then with `catalog`. Add a `discounted_price` column, which is the price
    after that segment's discount. Assign the result to `segment_products`.
    Then assign the product the Business segment prefers most to
    `top_business_product`. Look closely at the scores before you trust your
    answer.

    If you have time to spare: which category earns the most revenue, and which
    segment has the highest average preference score? You can answer both by
    filtering, but on Monday you'll learn a much shorter way.

    Graded complete or incomplete.
    """)
    return


@app.cell
def _(pd):
    catalog = pd.DataFrame(
        {
            "sku": ["LAP-001", "MON-001", "KEY-001", "MOU-001", "WEB-001"],
            "product_name": [
                "ThinkPro Laptop",
                '27" Monitor',
                "Mechanical Keyboard",
                "Wireless Mouse",
                "HD Webcam",
            ],
            "category": ["Computers", "Displays", "Accessories", "Accessories", "Accessories"],
            "price": [1299.99, 389.99, 149.99, 49.99, 79.99],
            "supplier_id": [1, 2, 3, 3, 4],
        }
    )
    sales_wide = pd.DataFrame(
        {
            "product_sku": ["LAP-001", "MON-001", "KEY-001", "MOU-001", "WEB-001"],
            "Jan": [45, 32, 88, 142, 28],
            "Feb": [52, 38, 95, 156, 31],
            "Mar": [48, 41, 102, 168, 35],
            "Apr": [61, 45, 98, 175, 38],
        }
    )
    segments = pd.DataFrame(
        {
            "segment_id": [1, 2, 3],
            "segment_name": ["Consumer", "Business", "Education"],
            "discount_rate": [0.0, 0.15, 0.20],
        }
    )
    product_segments = pd.DataFrame(
        {
            "sku": ["LAP-001", "LAP-001", "MON-001", "KEY-001", "KEY-001", "MOU-001", "WEB-001"],
            "segment_id": [1, 2, 2, 1, 2, 1, 2],
            "preference_score": [8, 9, 7, 6, 8, 7, 9],
        }
    )
    return


@app.cell
def _():
    # Milestone 1.
    sales_long = None
    return (sales_long,)


@app.cell
def _():
    # Milestone 2.
    sales_with_products = None
    return (sales_with_products,)


@app.cell
def _():
    # Milestone 3. Add cells below for the pivot if you need them, using new names.
    sales_revenue = None
    top_product = None
    top_month = None
    return sales_revenue, top_month, top_product


@app.cell
def _():
    # Milestone 4.
    segment_products = None
    top_business_product = None
    return segment_products, top_business_product


@app.cell(hide_code=True)
def _(
    sales_long,
    sales_revenue,
    sales_with_products,
    segment_products,
    top_business_product,
    top_month,
    top_product,
):
    def test_team_challenge_1():
        assert sales_long is not None, "Milestone 1: assign `sales_long`."
        assert set(sales_long.columns) == {"product_sku", "month", "units_sold"}, (
            f"Milestone 1: expected columns product_sku, month, units_sold, got "
            f"{list(sales_long.columns)}. Check var_name and value_name."
        )
        assert sales_long.shape == (20, 3), (
            f"Milestone 1: expected 20 rows (5 products × 4 months), got "
            f"{sales_long.shape[0]}. Is product_sku in id_vars?"
        )
        assert sales_long["units_sold"].sum() == 1518, (
            "Milestone 1: the units don't add up to the wide table's total."
        )

        assert sales_with_products is not None, "Milestone 2: assign `sales_with_products`."
        assert len(sales_with_products) == 20, (
            f"Milestone 2: expected 20 rows, got {len(sales_with_products)}. The keys "
            "have different names, so you need left_on and right_on."
        )
        assert {"product_name", "price"} <= set(sales_with_products.columns), (
            "Milestone 2: the merge should bring in product_name and price from catalog."
        )

        assert sales_revenue is not None, "Milestone 3: assign `sales_revenue`."
        assert "revenue" in sales_revenue.columns, (
            "Milestone 3: add a `revenue` column with .assign()."
        )
        assert top_product == "ThinkPro Laptop", (
            f"Milestone 3: expected 'ThinkPro Laptop', got {top_product!r}. Sum each "
            "product's revenue across the months, then take .idxmax()."
        )
        assert top_month == "Apr", (
            f"Milestone 3: expected 'Apr', got {top_month!r}. This time sum down the "
            "columns rather than across the rows."
        )

        assert segment_products is not None, "Milestone 4: assign `segment_products`."
        assert len(segment_products) == 7, (
            f"Milestone 4: expected 7 rows, one per row of product_segments, got "
            f"{len(segment_products)}."
        )
        assert {"segment_name", "product_name", "discounted_price"} <= set(
            segment_products.columns
        ), "Milestone 4: you need segment_name, product_name and discounted_price."
        _laptop_business = segment_products[
            (segment_products["product_name"] == "ThinkPro Laptop")
            & (segment_products["segment_name"] == "Business")
        ]
        assert round(float(_laptop_business["discounted_price"].iloc[0]), 2) == 1104.99, (
            "Milestone 4: a 15% discount should take the laptop from 1299.99 to "
            "1104.99. Is it price × (1 − discount_rate)?"
        )
        assert top_business_product in {"ThinkPro Laptop", "HD Webcam"}, (
            f"Milestone 4: got {top_business_product!r}. Filter to Business first, "
            "then look at preference_score."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Debrief, about 8 minutes

    - Two products tie for the Business segment's favourite. Which one did your
      code pick, and why that one?
    - The Education segment has no products. Is it in `segment_products`? Which
      join would keep it, and would you want it?
    - When would you reach for `concat` rather than `merge`?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ## 📌 Homework 1 stops here

            Homework 1 uses the material **above this line** and nothing below it.
            Grouping, pivot tables and histograms come on Monday, and you don't need
            them for Homework 1.
            """
        ),
        kind="warn",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## ⏸️ END OF SESSION 1 — pick up here next class
    ---

    Nothing to submit today. We carry on in this same file on Monday, and you'll
    submit it at the end of that session.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4.1: `groupby`

    Most questions about data are really questions about groups. Which branch
    is busiest? Which month is wettest? In each case you **split** the rows
    into groups, **apply** a calculation to each group, and **combine** the
    results into one table. `groupby` does all three.
    """)
    return


@app.cell
def _(pd):
    weather = pd.DataFrame(
        {
            "city": ["Seattle", "Seattle", "Seattle", "Portland", "Portland", "Portland",
                     "Vancouver", "Vancouver", "Vancouver", "Seattle", "Portland", "Vancouver"],
            "month": ["Jan", "Feb", "Mar", "Jan", "Feb", "Mar",
                      "Jan", "Feb", "Mar", "Apr", "Apr", "Apr"],
            "rainfall_mm": [140, 108, 95, 135, 102, 88, 168, 125, 110, 78, 65, 92],
            "avg_temp_c": [5, 7, 9, 6, 8, 10, 4, 6, 8, 11, 12, 10],
            "sunny_days": [8, 10, 12, 9, 11, 13, 7, 9, 11, 15, 16, 14],
        }
    )
    weather
    return (weather,)


@app.cell
def _(weather):
    # Split by city, take the rainfall column, apply the mean.
    weather.groupby("city")["rainfall_mm"].mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read that line in three parts: **what to group by**, **which column**, and
    **what to calculate**. Nearly every `groupby` you'll write has that shape.
    The result is indexed by the groups, which is why the cities are the index
    rather than a column.

    `.agg()` applies several calculations at once.
    """)
    return


@app.cell
def _(weather):
    weather.groupby("city")["rainfall_mm"].agg(["mean", "min", "max", "sum"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4.2: Grouping by more than one column

    Pass a list, and each *combination* becomes a group. The result has a
    MultiIndex, like `regional` on Wednesday.
    """)
    return


@app.cell
def _(weather):
    city_month = weather.groupby(["city", "month"])["rainfall_mm"].mean()
    city_month
    return (city_month,)


@app.cell
def _(city_month):
    # One value out of a MultiIndex: a tuple, one entry per level.
    city_month.loc[("Seattle", "Jan")]
    return


@app.cell
def _(city_month):
    # And Wednesday's unstack turns it into a city × month table.
    city_month.unstack()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4.3: A different calculation for each column

    **Named aggregation** gives each result column a name and says where it
    comes from: `new_name=("source_column", "function")`.
    """)
    return


@app.cell
def _(weather):
    city_summary = weather.groupby("city").agg(
        total_rain_mm=("rainfall_mm", "sum"),
        mean_temp_c=("avg_temp_c", "mean"),
        sunny_days=("sunny_days", "sum"),
    )
    city_summary
    return (city_summary,)


@app.cell
def _(city_summary):
    # .reset_index() turns the group labels back into an ordinary column,
    # which is what you want before merging the summary with another table.
    city_summary.reset_index()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5.1: Pivot tables

    On Wednesday, `pivot` reshaped data but refused to handle duplicates. A
    **pivot table** handles duplicates by aggregating them. It's a `groupby`
    and an `unstack` in a single call, and the result is the city × month table
    from Part 4.2.
    """)
    return


@app.cell
def _(weather):
    weather.pivot_table(index="city", columns="month", values="rainfall_mm", aggfunc="sum")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Argument | Means |
    |---|---|
    | `index` | what goes down the side |
    | `columns` | what goes across the top |
    | `values` | what fills the cells |
    | `aggfunc` | how to combine several rows that land in the same cell |

    ## Part 5.2: Totals with `margins`

    `margins=True` adds a total row and a total column. The bottom-right cell
    is the grand total.
    """)
    return


@app.cell
def _(weather):
    weather.pivot_table(
        index="city",
        columns="month",
        values="rainfall_mm",
        aggfunc="sum",
        margins=True,
        margins_name="Total",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5.3: Several index levels, and empty cells

    `index` takes a list too. With more groups there are more combinations
    that never occur, and those cells come back as `NaN`. When a missing
    combination really means zero, as with sales, `fill_value=0` says so.
    """)
    return


@app.cell
def _(np, pd):
    _rng = np.random.default_rng(42)
    stores = pd.DataFrame(
        {
            "region": _rng.choice(["North", "South", "East", "West"], 40),
            "store_type": _rng.choice(["Mall", "Street", "Online"], 40),
            "product_category": _rng.choice(["Electronics", "Clothing", "Food"], 40),
            "sales": _rng.integers(1000, 10000, 40),
        }
    )
    stores.head(10)
    return (stores,)


@app.cell
def _(stores):
    stores.pivot_table(
        index=["region", "store_type"],
        columns="product_category",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`groupby` or `pivot_table`?** They compute the same numbers. Use
    `groupby` when you want a list of results, especially one you'll sort or
    merge. Use `pivot_table` when you want to compare two groupings side by
    side in a grid.

    ### 🚀 Checkpoint 3.2

    ✅ Step 1: Assign the city with the highest mean `avg_temp_c` to
    `warmest_city`.

    ✅ Step 2: Build a pivot table of **total** `sunny_days`, with cities as
    rows, months as columns, and totals on both. Assign it to `sunny_pivot`.
    """)
    return


@app.cell
def _():
    # Your code here.
    warmest_city = None
    sunny_pivot = None
    return sunny_pivot, warmest_city


@app.cell(hide_code=True)
def _(sunny_pivot, warmest_city):
    def test_checkpoint_3_2():
        assert warmest_city is not None, "Assign the city's name to `warmest_city`."
        assert warmest_city == "Portland", (
            f"Expected 'Portland', got {warmest_city!r}. Group by city, take the mean "
            "of avg_temp_c, and .idxmax() gives you the label."
        )
        assert sunny_pivot is not None, "Assign your pivot table to `sunny_pivot`."
        assert sunny_pivot.iloc[-1, -1] == 135, (
            f"The bottom-right cell should be the grand total, 135, but it's "
            f"{sunny_pivot.iloc[-1, -1]}. Check aggfunc='sum' and margins=True."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 6.1: Histograms

    A histogram shows how a column's values are distributed. It divides the
    range into **bins** and counts how many values fall in each one. It's the
    first plot to make with any numeric column, and notebook 04 builds on it.

    marimo displays a matplotlib plot when the axes object is the last
    expression in the cell.
    """)
    return


@app.cell
def _(pd):
    prices = pd.Series(
        [10, 15, 12, 25, 30, 22, 18, 45, 50, 35, 28, 32, 19, 21, 38,
         42, 16, 14, 27, 33, 48, 52, 29, 31, 24, 26, 20, 23, 36, 40],
        name="price",
    )
    return (prices,)


@app.cell
def _(plt, prices):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.hist(prices, bins=10, edgecolor="black")
    _ax.set_xlabel("Price ($)")
    _ax.set_ylabel("Number of products")
    _ax.set_title("Distribution of product prices")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 6.2: Bins and range

    The number of bins changes the picture. Too few hides the shape, and too
    many turns it into noise. `range` restricts the plot to an interval, which
    is useful when a handful of extreme values squash everything else into one
    bar.
    """)
    return


@app.cell
def _(plt, prices):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.hist(prices, bins=15, range=(10, 55), edgecolor="black")
    _ax.set_xlabel("Price ($)")
    _ax.set_ylabel("Number of products")
    _ax.set_title("Distribution of product prices, 15 bins")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 6.3: Let the numbers choose the range

    Rather than guessing a range, look at the distribution first. The 5th and
    95th percentiles make a sensible default window that ignores the most
    extreme 10% of values.
    """)
    return


@app.cell
def _(prices):
    prices.describe(), prices.quantile(0.05), prices.quantile(0.95)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🚀 Team Challenge 2: Library checkouts

    **About 25 minutes, in teams.**

    A library system has five branches. `checkouts` holds 200 records, each
    one a branch, genre and month with its number of checkouts, new members
    and late returns. `branch_info` describes each branch.

    ### Milestones

    **Milestone 1, groupby.** Assign the total checkouts for each branch to
    `branch_totals`, the branch with the most checkouts to `top_branch`, and
    the genre with the highest *mean* checkouts to `top_genre_mean`.

    **Milestone 2, pivot tables.** Build a pivot table of total checkouts with
    branches as rows and genres as columns, and no margins, and assign it to
    `branch_genre`. Then find the branch–genre combination with the most
    checkouts and assign it to `top_combo` as a `(branch, genre)` tuple.
    Finally, assign the busiest month overall to `busiest_month`.

    *Hint:* Wednesday's `.stack()` turns the grid back into one long Series
    indexed by `(branch, genre)`, and `.idxmax()` gives you that tuple.

    **Milestone 3, combine.** Merge `branch_totals` with `branch_info` and work
    out checkouts per square foot. Assign the branch with the most to
    `top_per_sqft_branch`. Assign the branch that recruited the most new
    members to `top_recruiting_branch`.

    **Milestone 4, late returns.** Add a `late_rate` column, which is late
    returns divided by checkouts, for each record. Build a pivot table of the
    mean late rate by branch and genre, and assign it to `late_rate_pivot`.
    Assign the worst `(branch, genre)` combination to `worst_late_combo`.

    If you have time to spare: is there a relationship between a branch's size
    and its total checkouts? How confident can you be, with only five branches?

    Graded complete or incomplete.
    """)
    return


@app.cell
def _(np, pd):
    _rng = np.random.default_rng(618)
    _branches = ["Downtown", "Westside", "Eastside", "Northgate", "Central"]
    checkouts = pd.DataFrame(
        {
            "branch": _rng.choice(_branches, 200),
            "genre": _rng.choice(
                ["Fiction", "Non-Fiction", "Mystery", "Science", "Biography", "Children"], 200
            ),
            "month": _rng.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], 200),
            "checkouts": _rng.integers(5, 150, 200),
            "new_members": _rng.integers(0, 30, 200),
            "late_returns": _rng.integers(0, 20, 200),
        }
    )
    branch_info = pd.DataFrame(
        {
            "branch": _branches,
            "size_sqft": [15000, 12000, 8000, 10000, 18000],
            "staff_count": [25, 18, 12, 15, 30],
            "computers": [40, 30, 20, 25, 50],
        }
    )
    checkouts.head(10), branch_info
    return


@app.cell
def _():
    # Milestone 1.
    branch_totals = None
    top_branch = None
    top_genre_mean = None
    return branch_totals, top_branch, top_genre_mean


@app.cell
def _():
    # Milestone 2.
    branch_genre = None
    top_combo = None
    busiest_month = None
    return branch_genre, busiest_month, top_combo


@app.cell
def _():
    # Milestone 3. Add cells above this one if you need them, using new names.
    top_per_sqft_branch = None
    top_recruiting_branch = None
    return top_per_sqft_branch, top_recruiting_branch


@app.cell
def _():
    # Milestone 4.
    late_rate_pivot = None
    worst_late_combo = None
    return late_rate_pivot, worst_late_combo


@app.cell(hide_code=True)
def _(
    branch_genre,
    branch_totals,
    busiest_month,
    late_rate_pivot,
    top_branch,
    top_combo,
    top_genre_mean,
    top_per_sqft_branch,
    top_recruiting_branch,
    worst_late_combo,
):
    def test_team_challenge_2():
        assert branch_totals is not None, "Milestone 1: assign `branch_totals`."
        assert len(branch_totals) == 5, (
            f"Milestone 1: expected one total per branch, 5, got {len(branch_totals)}."
        )
        assert top_branch == "Central", (
            f"Milestone 1: expected 'Central', got {top_branch!r}. Northgate is close "
            "behind, so make sure you summed rather than counted."
        )
        assert top_genre_mean == "Non-Fiction", (
            f"Milestone 1: expected 'Non-Fiction', got {top_genre_mean!r}. This one "
            "asks for the mean, not the sum."
        )

        assert branch_genre is not None, "Milestone 2: assign `branch_genre`."
        assert branch_genre.shape == (5, 6), (
            f"Milestone 2: expected 5 branches × 6 genres, got {branch_genre.shape}. "
            "Leave margins off for this one."
        )
        assert top_combo is not None, "Milestone 2: assign `top_combo`."
        assert tuple(top_combo) == ("Downtown", "Science"), (
            f"Milestone 2: expected ('Downtown', 'Science'), got {top_combo!r}. Try "
            "branch_genre.stack().idxmax()."
        )
        assert busiest_month == "Jan", (
            f"Milestone 2: expected 'Jan', got {busiest_month!r}."
        )

        assert top_per_sqft_branch == "Eastside", (
            f"Milestone 3: expected 'Eastside', got {top_per_sqft_branch!r}. Divide "
            "each branch's total checkouts by its size_sqft."
        )
        assert top_recruiting_branch == "Northgate", (
            f"Milestone 3: expected 'Northgate', got {top_recruiting_branch!r}. Sum "
            "new_members by branch."
        )

        assert late_rate_pivot is not None, "Milestone 4: assign `late_rate_pivot`."
        assert worst_late_combo is not None, "Milestone 4: assign `worst_late_combo`."
        assert tuple(worst_late_combo) == ("Northgate", "Children"), (
            f"Milestone 4: expected ('Northgate', 'Children'), got {worst_late_combo!r}. "
            "Compute the rate for each record first, then take the mean in the pivot."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Debrief, about 5 minutes

    - What's the relationship between `groupby` and pivot tables?
    - Did anyone find a relationship between branch size and checkouts? What
      would you need before you'd believe one?

    ---
    ## Summary

    **Session 1, loading, combining and reshaping**

    - `skiprows` and `na_values` for files with title lines and odd missing
      markers; `sep` for files that don't use commas
    - `pd.json_normalize()` to flatten nested JSON, and
      `pd.to_datetime(..., unit="ms")` for the timestamps APIs send
    - Cleaning keys with `.str.strip()` before a merge, and checking that the
      merge matched what it should
    - `pd.concat()` to stack tables with the same columns
    - `pd.merge()` with `how=` inner, left, right or outer, and `left_on` /
      `right_on` when keys are named differently
    - `.melt()` from wide to long, `.pivot()` from long to wide, and
      `.stack()` / `.unstack()` for a MultiIndex

    **Session 2, grouping, pivot tables and histograms**

    - `groupby`: what to group by, which column, what to calculate
    - `.agg()` for several calculations, and named aggregation for a different
      one per column
    - `.pivot_table()` with `index`, `columns`, `values`, `aggfunc`, `margins`
      and `fill_value`
    - Histograms with matplotlib, choosing `bins` and `range`

    ## Next class

    **04, data analysis I.** Univariate statistics, visualization with seaborn,
    and an introduction to correlation.

    Reading: McKinney, chapter 9 (Plotting and Visualization).

    ## Additional resources

    - [pandas merge, join, concatenate](https://pandas.pydata.org/docs/user_guide/merging.html)
    - [Reshaping and pivot tables](https://pandas.pydata.org/docs/user_guide/reshaping.html)
    - [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Submit by the end of today's session.** Two files, both to Canvas:

    1. This notebook, renamed `SI618_03_<uniqname>.py`
    2. An HTML export of it:
       ```bash
       uvx marimo export html --sandbox SI618_03_<uniqname>.py -o SI618_03_<uniqname>.html
       ```

    ❗️ Late in-class work is not accepted for credit.
    """)
    return


if __name__ == "__main__":
    app.run()
