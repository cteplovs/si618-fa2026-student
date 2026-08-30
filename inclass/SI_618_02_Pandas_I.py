# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # SI 618 · 02: pandas I, DataFrames

        Dr. Chris Teplovs, University of Michigan School of Information

        **Fall 2026** · Sessions 3 (Wed Sep 9) and 4 (Mon Sep 14)

        Copyright © 2026. This notebook may not be shared outside of the course
        without permission. Notebook version 2026.08.28.1.CT

        ---

        ## Learning objectives

        By the end of these two sessions you will be able to:

        - Load data into a DataFrame from a file or from a URL
        - Describe the components of a DataFrame, meaning its values, index and
          columns
        - Select columns with `[]`, and rows with `.loc` and `.iloc`
        - Filter rows with boolean masks, combining conditions using `&`, `|` and
          `.isin()`
        - Create derived columns, sort them, and count unique values
        - Convert a string column to `datetime` and pull out its components

        ## Pre-class reading

        Chen, D.Y. (2023). *Pandas for Everyone*, 2nd edition, chapter 1 (Pandas
        DataFrame Basics) and Chapter 2 (Pandas Data Structures).

        ## Structure

        **Session 1, Wednesday.** DataFrame fundamentals and selection, followed by
        Team Challenge 1.

        **Session 2, Monday.** Filtering, operations and dates, followed by Team
        Challenge 2.

        One notebook across two sessions, submitted once, at the end of Monday.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    return mo, np, pd


@app.cell
def _(pd):
    pd.__version__
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 1.1: What is pandas?

        pandas is Python's main data manipulation library, and it gives you two data
        structures to work with. A **Series** is a one-dimensional labelled array,
        and a **DataFrame** is a two-dimensional labelled structure, rather like a
        spreadsheet or a SQL table.

        You can think of a DataFrame as a collection of Series sharing an index, or
        as a NumPy array that happens to know what its rows and columns are called.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 1.2: Creating DataFrames

        There are several ways to build a DataFrame, and these two are the most
        common.

        ### From a dictionary of lists (column-wise)
        """
    )
    return


@app.cell
def _(pd):
    people = {
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "age": [25, 30, 35, 28],
        "city": ["Ann Arbor", "Detroit", "Ann Arbor", "Lansing"],
    }

    df_people = pd.DataFrame(people)
    df_people
    return (df_people,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Key observations:**

        - Each dictionary key becomes a column name
        - Each list becomes the values in that column
        - pandas creates an index for you, running 0, 1, 2, 3 and so on

        ### From a list of dictionaries (row-wise)

        Here each dictionary is a row. This is usually the shape data arrives in from
        an API, and it's the shape you saw in the sensor data last week.
        """
    )
    return


@app.cell
def _(pd):
    students = [
        {"name": "Alice", "age": 25, "gpa": 3.8},
        {"name": "Bob", "age": 30, "gpa": 3.5},
        {"name": "Charlie", "age": 35, "gpa": 3.9},
    ]

    df_students = pd.DataFrame(students)
    df_students
    return (df_students,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 1.3: Loading data from files

        In practice you will load data rather than type it. pandas reads many
        formats:

        | Format | Function |
        |---|---|
        | CSV (most common) | `pd.read_csv()` |
        | Excel | `pd.read_excel()` |
        | JSON | `pd.read_json()` |
        | Parquet | `pd.read_parquet()` |
        | SQL | `pd.read_sql()` |

        All of these will take a URL as readily as a local path, which is how this
        course loads data, since nothing large lives in the course repository.

        ### Example: the Gapminder dataset

        Country-level data on life expectancy, GDP per capita, and population,
        recorded every five years from 1952 to 2007.
        """
    )
    return


@app.cell
def _(pd):
    GAPMINDER_URL = (
        "https://raw.githubusercontent.com/plotly/datasets/master/"
        "gapminderDataFiveYear.csv"
    )
    gapminder = pd.read_csv(GAPMINDER_URL)
    gapminder.head()
    return (gapminder,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 1.4: Basic DataFrame inspection

        When you first load a dataset, inspect it before doing anything else. This
        isn't a formality, it's where you catch the wrong delimiter, or the column
        that quietly loaded as text, or the missing values that will bite you later
        on.
        """
    )
    return


@app.cell
def _(gapminder):
    gapminder.tail()
    return


@app.cell
def _(gapminder):
    # (rows, columns)
    gapminder.shape
    return


@app.cell
def _(gapminder):
    gapminder.columns.tolist()
    return


@app.cell
def _(gapminder):
    gapminder.dtypes
    return


@app.cell
def _(gapminder):
    gapminder.info()
    return


@app.cell
def _(gapminder):
    gapminder.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Question for reflection:** What do you notice in the `.describe()` output?
        What is the range of years? What stands out about life expectancy?

        ## Part 1.5: Understanding DataFrame structure

        A DataFrame has three components. The **values** are the data itself, held as
        a NumPy array, the **index** holds the row labels, and the **columns** hold
        the column labels.

        Almost everything pandas does is some combination of those.
        """
    )
    return


@app.cell
def _(gapminder):
    gapminder.values[:5]
    return


@app.cell
def _(gapminder):
    gapminder.index
    return


@app.cell
def _(gapminder):
    gapminder.columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 1.6: Selecting columns

        A single column comes back as a **Series**, whereas a list of columns comes
        back as a **DataFrame**, and that distinction matters more often than you
        might expect.
        """
    )
    return


@app.cell
def _(gapminder):
    countries = gapminder["country"]
    type(countries), countries.head()
    return


@app.cell
def _(gapminder):
    # Attribute syntax also works, but only when the column name happens to be a
    # valid Python identifier. Prefer the bracket form -- it always works.
    gapminder.lifeExp.head()
    return


@app.cell
def _(gapminder):
    subset = gapminder[["country", "year", "lifeExp"]]
    type(subset), subset.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ❗️ Note the **double brackets** `[[...]]` when selecting multiple columns.
        The outer brackets are the selection, and the inner ones are the list of
        names you're selecting. A single-element list such as `gapminder[["country"]]`
        gives you back a one-column *DataFrame* rather than a Series, which
        occasionally catches people out.

        ## Part 1.7: Selecting rows

        - `.head()` and `.tail()` give you the first or last *n* rows
        - `.loc[]` selects by **label**
        - `.iloc[]` selects by **integer position**
        - boolean indexing selects by **condition**, which we come to in session 2

        ### `.loc[]`, which is label-based
        """
    )
    return


@app.cell
def _(gapminder):
    gapminder.loc[0]
    return


@app.cell
def _(gapminder):
    # Note: .loc slices are INCLUSIVE of the endpoint.
    gapminder.loc[0:4]
    return


@app.cell
def _(gapminder):
    gapminder.loc[0:4, ["country", "year", "lifeExp"]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### `.iloc[]`, which is position-based""")
    return


@app.cell
def _(gapminder):
    gapminder.iloc[0]
    return


@app.cell
def _(gapminder):
    # Note: .iloc slices are EXCLUSIVE of the endpoint, like ordinary Python
    # slicing. This asymmetry with .loc is a common source of off-by-one bugs.
    gapminder.iloc[0:5, 0:3]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🚀 Checkpoint 2.1

        A quick self-check before we get to the team challenge.

        ✅ Step 1: Using `.loc`, select rows 10 through 15 inclusive, along with the
        columns `country` and `pop`, in that order, and assign the result to
        `checkpoint_rows`.

        ✅ Step 2: Assign the number of unique countries in `gapminder` to
        `n_countries`, for which `.nunique()` will help.
        """
    )
    return


@app.cell
def _():
    # Your code here.
    checkpoint_rows = None
    n_countries = None
    return checkpoint_rows, n_countries


@app.cell(hide_code=True)
def _(checkpoint_rows, n_countries):
    def test_checkpoint_2_1():
        assert checkpoint_rows is not None, "Assign your selection to `checkpoint_rows`."
        assert checkpoint_rows.shape == (6, 2), (
            f"Expected 6 rows and 2 columns, got {checkpoint_rows.shape}. "
            "Remember that .loc slices include the endpoint."
        )
        assert list(checkpoint_rows.columns) == ["country", "pop"], (
            f"Expected columns ['country', 'pop'], got {list(checkpoint_rows.columns)}."
        )
        assert n_countries == 142, (
            f"Expected 142 unique countries, got {n_countries}."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🚀 Team Challenge 1: Load and explore data

        **30 minutes, in teams.**

        You'll be working with health inspection results for food establishments in
        Chicago, which is a real municipal dataset and correspondingly messy.

        The URL below asks the City of Chicago's API for inspections during 2024 and
        2025 only, since the full dataset is far too large to download in class. It's
        pinned to a fixed window so that everyone in the room is looking at the same
        data. Expect the load to take somewhere between ten and twenty seconds.

        ### Milestones

        **Milestone 1, load the data.** Load the CSV at `INSPECTIONS_URL` into a
        DataFrame called `inspections`, display the first ten rows, and work out how
        many rows and columns there are.

        **Milestone 2, understand the structure.** What are the column names, what
        type is each column, and are there missing values? `.info()` will answer all
        three at once.

        **Milestone 3, explore the numeric columns.** Use `.describe()`, and consider
        which columns are actually numeric, and whether that's what you expected.

        **Milestone 4, initial questions.** Write two or three questions you could
        answer with this data, in `tc1_questions`.

        **Milestone 5, team summary.** Fill in `tc1_summary` with what the dataset
        contains, one interesting pattern you noticed, and what you'd explore next.

        This is graded complete or incomplete, so submit whatever you finish. It
        isn't homework.
        """
    )
    return


@app.cell
def _():
    INSPECTIONS_URL = (
        "https://data.cityofchicago.org/resource/4ijn-s7e5.csv"
        "?$limit=100000"
        "&$where=inspection_date%20between%20%272024-01-01T00%3A00%3A00%27"
        "%20and%20%272025-12-31T23%3A59%3A59%27"
    )
    return (INSPECTIONS_URL,)


@app.cell
def _():
    # Milestone 1: load the data into `inspections`, then look at it.
    inspections = None
    return (inspections,)


@app.cell
def _():
    # Milestone 2: understand the structure.
    return


@app.cell
def _():
    # Milestone 3: explore the numeric columns.
    return


@app.cell
def _():
    # Milestone 4: two or three questions, one per line, each ending in "?"
    tc1_questions = """
    1.
    2.
    3.
    """
    return (tc1_questions,)


@app.cell
def _():
    # Milestone 5: your team's summary.
    tc1_summary = {
        "contains": "",
        "pattern": "",
        "next": "",
    }
    return (tc1_summary,)


@app.cell(hide_code=True)
def _(inspections, tc1_questions, tc1_summary):
    def test_team_challenge_1():
        assert inspections is not None, (
            "Milestone 1: load INSPECTIONS_URL into `inspections`."
        )
        assert inspections.shape[1] == 17, (
            f"Expected 17 columns, got {inspections.shape[1]}. "
            "Did you use INSPECTIONS_URL as given?"
        )
        assert len(inspections) > 30_000, (
            f"Expected roughly 38,000 rows, got {len(inspections)}. "
            "Check that the $limit in the URL survived copy-paste."
        )

        _qs = [ln.strip() for ln in tc1_questions.strip().splitlines() if ln.strip()]
        assert len(_qs) >= 2, "Milestone 4: write at least two questions."
        assert sum(q.endswith("?") for q in _qs) >= 2, (
            "Milestone 4: each line should be a question ending in '?'."
        )

        for _key in ("contains", "pattern", "next"):
            assert tc1_summary[_key].strip(), (
                f"Milestone 5: `tc1_summary['{_key}']` is still empty."
            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Debrief, about 8 minutes

        - What did teams find surprising in `.info()`?
        - Which columns loaded as the wrong type, and why might that have happened?

        ---
        ## ⏸️ END OF SESSION 1 — pick up here next class
        ---

        Nothing to submit today. We carry on in this same file on Monday, and you'll
        submit it at the end of that session.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 2.1: Boolean indexing (filtering)

        Filtering is probably the operation you'll reach for most often. It works in
        two steps, and it's worth seeing them separately once before you start
        writing them as a single line.
        """
    )
    return


@app.cell
def _(gapminder):
    # Step one: a boolean mask -- a Series of True/False, one per row.
    is_usa = gapminder["country"] == "United States"
    type(is_usa), is_usa.head(10)
    return (is_usa,)


@app.cell
def _(gapminder, is_usa):
    # Step two: index with the mask. Rows where the mask is True are kept.
    gapminder[is_usa]
    return


@app.cell
def _(gapminder):
    # In practice you write it as one line.
    gapminder[gapminder["country"] == "Canada"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Multiple conditions

        Use `&` for AND and `|` for OR, rather than `and` and `or`, which can't
        operate elementwise on a Series. Do wrap each condition in parentheses, since
        `&` binds more tightly than `==`, and without them Python will parse the
        expression differently from how you intended while the error message says
        nothing helpful about it.
        """
    )
    return


@app.cell
def _(gapminder):
    recent_usa = gapminder[
        (gapminder["country"] == "United States") & (gapminder["year"] >= 2000)
    ]
    recent_usa
    return


@app.cell
def _(gapminder):
    usa_or_canada = gapminder[
        (gapminder["country"] == "United States") | (gapminder["country"] == "Canada")
    ]
    len(usa_or_canada), usa_or_canada.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### `.isin()` for multiple values

        Chaining `|` gets unwieldy once you're past two or three values, whereas
        `.isin()` will simply take a list.
        """
    )
    return


@app.cell
def _(gapminder):
    countries_of_interest = ["United States", "Canada", "Mexico"]
    north_america = gapminder[gapminder["country"].isin(countries_of_interest)]
    north_america.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 2.2: Basic operations

        ### Creating columns

        ❗️ Note the idiom here. `.assign()` returns a new DataFrame rather than
        modifying `gapminder` in place, and in marimo that isn't really optional,
        since `gapminder` is defined in one cell and read by several others, so
        mutating it here would make the results depend on which cells you happened to
        run. It's a good habit everywhere else too.
        """
    )
    return


@app.cell
def _(gapminder):
    gapminder_plus = gapminder.assign(
        pop_millions=gapminder["pop"] / 1_000_000,
        total_gdp=gapminder["gdpPercap"] * gapminder["pop"],
    )
    gapminder_plus[["country", "year", "pop", "pop_millions", "total_gdp"]].head()
    return (gapminder_plus,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Sorting""")
    return


@app.cell
def _(gapminder):
    gapminder.sort_values("lifeExp", ascending=False).head(10)
    return


@app.cell
def _(gapminder):
    # Sorting by several columns: country first, then year within each country.
    gapminder.sort_values(["country", "year"]).head(15)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Unique values and value counts""")
    return


@app.cell
def _(gapminder):
    gapminder["country"].nunique(), gapminder["country"].unique()[:10]
    return


@app.cell
def _(gapminder):
    gapminder["year"].value_counts().sort_index()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🚀 Checkpoint 2.2

        ✅ Step 1: Filter `gapminder` down to rows from 2007 in Africa, and assign
        the mean life expectancy of those rows, rounded to two decimal places, to
        `africa_2007_life_exp`.

        ✅ Step 2: Using `gapminder_plus`, find the country with the largest
        `total_gdp` in 2007, and assign its name to `top_gdp_2007`.
        """
    )
    return


@app.cell
def _():
    # Your code here.
    africa_2007_life_exp = None
    top_gdp_2007 = None
    return africa_2007_life_exp, top_gdp_2007


@app.cell(hide_code=True)
def _(africa_2007_life_exp, top_gdp_2007):
    def test_checkpoint_2_2():
        assert africa_2007_life_exp is not None, (
            "Assign the mean to `africa_2007_life_exp`."
        )
        assert round(float(africa_2007_life_exp), 2) == 54.81, (
            f"Expected 54.81, got {africa_2007_life_exp}. Both conditions apply at "
            "once -- year 2007 AND continent Africa -- so combine them with &."
        )
        assert top_gdp_2007 == "United States", (
            f"Expected 'United States', got {top_gdp_2007!r}. `.idxmax()` gives you "
            "the index label of the largest value, which you can pass to `.loc`."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part 2.3: Working with dates

        Dates are among the most common things people get wrong when loading data, so
        they're worth a short preview now. We'll return to them properly later in the
        term.

        ### Why datetime matters

        When pandas reads a CSV, it loads dates as **strings**.
        """
    )
    return


@app.cell
def _(pd):
    df_dates_raw = pd.DataFrame(
        {
            "date": ["2023-01-15", "2023-06-20", "2024-03-10"],
            "sales": [100, 150, 200],
        }
    )
    df_dates_raw.dtypes
    return (df_dates_raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        `date` has type `object`, which is to say text. While it's text you can't
        extract the year, work out the difference between two dates, filter a range,
        or sort chronologically. Sorting text sorts alphabetically, which happens to
        look right for `YYYY-MM-DD` and goes badly wrong for almost every other
        format.

        ### Converting, and extracting components

        `pd.to_datetime()` does the conversion, and afterwards the `.dt` accessor
        gives you access to the parts.
        """
    )
    return


@app.cell
def _(df_dates_raw, pd):
    df_dates = df_dates_raw.assign(date=pd.to_datetime(df_dates_raw["date"]))
    df_dates = df_dates.assign(
        year=df_dates["date"].dt.year,
        month=df_dates["date"].dt.month,
        day=df_dates["date"].dt.day,
        day_of_week=df_dates["date"].dt.day_name(),
    )
    df_dates
    return (df_dates,)


@app.cell
def _(df_dates):
    df_dates.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **The `.dt` accessor:**

        | Expression | Gives you |
        |---|---|
        | `.dt.year` | year |
        | `.dt.month` | month, 1–12 |
        | `.dt.day` | day of month, 1–31 |
        | `.dt.day_name()` | `"Monday"`, `"Tuesday"`, … |
        | `.dt.quarter` | quarter, 1–4 |
        | `.dt.date` | the date part, dropping the time |

        **Quick reference:**

        ```python
        df = df.assign(when=pd.to_datetime(df["when"]))   # convert
        df = df.assign(year=df["when"].dt.year)           # extract
        df_2025 = df[df["year"] == 2025]                  # filter
        ```

        It's worth converting when you need to extract components, filter by a range,
        work out differences, or group by time period. If the date is only ever a
        label that you won't analyse, you can leave it alone.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🚀 Team Challenge 2: Selection and filtering

        **35 minutes, in teams.** Carry on with the `inspections` DataFrame you
        loaded back in Challenge 1.

        ### Milestones

        **Milestone 1, column selection.** Assign the number of unique values in
        `dba_name` to `n_facilities`, and the set of distinct values in `results` to
        `possible_results`.

        **Milestone 2, filtering.** Build `failed_2025`, containing the inspections
        whose `results` is exactly `"Fail"` and whose `inspection_date` falls in 2025.
        You'll need to convert `inspection_date` first, and call the converted frame
        `inspections_dated`.

        **Milestone 3, new columns.** Add a `year` column to `inspections_dated`
        using `.assign()`, along with any other derived column your team finds useful.

        **Milestone 4, find something interesting.** Use sorting and `.value_counts()`
        to answer one of the questions you posed in Challenge 1, and record what you
        found in `tc2_findings`.

        If you have time to spare: which facility has the most inspections, what's the
        most common inspection type, and do failures vary across the year?

        Graded complete or incomplete.
        """
    )
    return


@app.cell
def _():
    # Milestone 1.
    n_facilities = None
    possible_results = None
    return n_facilities, possible_results


@app.cell
def _():
    # Milestones 2 and 3: convert the date, add a `year` column, then filter.
    inspections_dated = None
    failed_2025 = None
    return failed_2025, inspections_dated


@app.cell
def _():
    # Milestone 4: your exploration. Add cells below as you need them.
    tc2_findings = """
    1.
    2.
    3.
    """
    return (tc2_findings,)


@app.cell(hide_code=True)
def _(
    failed_2025,
    inspections,
    inspections_dated,
    n_facilities,
    possible_results,
    tc2_findings,
):
    def test_team_challenge_2():
        # These check the shape of your answer against the data you actually
        # loaded, rather than against fixed numbers, because the City of Chicago
        # amends old records and the counts drift over time.
        assert n_facilities is not None, "Milestone 1: assign `n_facilities`."
        assert n_facilities == inspections["dba_name"].nunique(), (
            f"`n_facilities` is {n_facilities}, but dba_name has "
            f"{inspections['dba_name'].nunique()} unique values."
        )
        assert possible_results is not None, "Milestone 1: assign `possible_results`."
        assert set(possible_results) == set(inspections["results"].dropna()), (
            "`possible_results` does not match the distinct values in `results`."
        )

        assert inspections_dated is not None, (
            "Milestone 2: assign the date-converted frame to `inspections_dated`."
        )
        assert "datetime" in str(inspections_dated["inspection_date"].dtype), (
            "`inspection_date` is still text. Convert it with pd.to_datetime()."
        )
        assert "year" in inspections_dated.columns, (
            "Milestone 3: add a `year` column with .assign()."
        )

        assert failed_2025 is not None, "Milestone 2: assign `failed_2025`."
        assert len(failed_2025) > 0, (
            "`failed_2025` is empty. Check the spelling of 'Fail', bearing in mind "
            "the column also contains 'Pass w/ Conditions' and 'Not Ready'."
        )
        assert set(failed_2025["results"].unique()) == {"Fail"}, (
            "`failed_2025` contains results other than 'Fail'."
        )
        assert set(failed_2025["inspection_date"].dt.year.unique()) == {2025}, (
            "`failed_2025` contains inspections from outside 2025."
        )

        _fs = [ln.strip() for ln in tc2_findings.strip().splitlines() if ln.strip()]
        assert len(_fs) >= 1 and len(_fs[0]) > 20, (
            "Milestone 4: record at least one finding in `tc2_findings`."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Presentations and debrief, about 10 minutes

        Two or three teams share their most interesting finding, and we talk about
        what turned out to be hardest.

        ---
        ## Summary

        **Session 1, DataFrame fundamentals**

        - Creating DataFrames from dictionaries (column-wise) and from lists of
          dictionaries (row-wise)
        - Loading from a file or a URL with `pd.read_csv()`
        - Inspecting with `.head()`, `.tail()`, `.shape`, `.dtypes`, `.info()` and
          `.describe()`
        - The structure, meaning values, index and columns
        - Selecting columns, where one name gives a Series and a list gives a
          DataFrame
        - Selecting rows with `.loc`, which is label-based and endpoint inclusive,
          and `.iloc`, which is position-based and endpoint exclusive

        **Session 2, filtering and operations**

        - Boolean masks, and combining conditions with `&`, `|`, and parentheses
        - `.isin()` for a list of values
        - Deriving columns with `.assign()` rather than mutating in place
        - `.sort_values()`, `.nunique()`, `.unique()`, `.value_counts()`
        - `pd.to_datetime()` and the `.dt` accessor

        ## Next class

        **03, pandas II.** Groupby, aggregation and transformation, merging and
        joining, pivot tables and reshaping, and handling missing data.

        Readings: Chen chapters 5–8; McKinney chapters 7, 8, 10.

        ## Additional resources

        - [pandas documentation](https://pandas.pydata.org/docs/)
        - [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
        - [pandas cheat sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
        - [Practice exercises](https://github.com/guipsamora/pandas_exercises)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🏁 END OF NOTEBOOK

        **Submit by the end of today's session.** Two files, both to Canvas:

        1. This notebook, renamed `SI618_02_<uniqname>.py`
        2. An HTML export of it:
           ```bash
           uvx marimo export html --sandbox SI618_02_<uniqname>.py -o SI618_02_<uniqname>.html
           ```

        ❗️ Late in-class work is not accepted for credit.
        """
    )
    return


if __name__ == "__main__":
    app.run()
