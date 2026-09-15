# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
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
        # SI 618 · Homework 1: Joining the world's data

        **Name:**
        **Uniqname:**
        **Indicator:**

        Due **Monday, September 21, before class (3:30 PM)**. The full spec is in
        `README.md`, and the rubric is in `RUBRIC.md`. Read both before you start.

        Rename this file `SI618_HW01_<uniqname>.py` before you submit, and upload
        its HTML export alongside it.

        ### Working in marimo

        - A variable can be defined in only one cell. Give each new result a new
          name, like `indicator_clean` or `merged_checked`, or prefix a name with
          `_` to keep it inside its cell.
        - Add as many cells as you need, wherever you need them.
        - For written answers, edit the markdown cells marked *Your answer here*.
        - The tests at the end of each part check that your work has the right
          **shape**, not that it's right. A green test doesn't mean a part is
          complete.
        """
    )
    return


@app.cell
def _():
    import json
    from urllib.request import urlopen

    import marimo as mo
    import pandas as pd

    pd.set_option("display.max_columns", 50)
    return json, mo, pd, urlopen


@app.cell
def _():
    COUNTRIES_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"
    INDICATOR_URL = (
        "https://api.worldbank.org/v2/country/all/indicator/{code}"
        "?format=json&per_page=20000&date=2000:2024"
    )
    ALLOWED_CODES = {
        "SP.DYN.LE00.IN",
        "NY.GDP.PCAP.CD",
        "IT.NET.USER.ZS",
        "SP.DYN.TFRT.IN",
        "SP.URB.TOTL.IN.ZS",
        "EG.ELC.ACCS.ZS",
        "SL.TLF.CACT.FE.ZS",
        "EN.GHG.CO2.PC.CE.AR5",
        "SH.DYN.MORT",
    }
    return ALLOWED_CODES, COUNTRIES_URL, INDICATOR_URL


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 1: Load and inspect (15 points)

        ### 1.1 A loading function (5)
        """
    )
    return


@app.cell
def _(INDICATOR_URL, json, pd, urlopen):
    def fetch_indicator(code: str) -> pd.DataFrame:
        """Replace this docstring with one that describes what your function does."""
        # Your code here. INDICATOR_URL.format(code=code) gives you the URL.
        return None
    return (fetch_indicator,)


@app.cell
def _():
    # Your chosen indicator code, from the table in README.md.
    INDICATOR_CODE = ""
    return (INDICATOR_CODE,)


@app.cell
def _():
    # Load the country list, population, and your indicator.
    countries = None
    population = None
    indicator = None
    return countries, indicator, population


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 1.2 Why this indicator (3)

        *Your answer here.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 1.3 Inspect (7)""")
    return


@app.cell
def _():
    # Shape, types and missing values for each of the three tables.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: the columns you'll use, and the type problems you
        noticed.*
        """
    )
    return


@app.cell(hide_code=True)
def _(ALLOWED_CODES, INDICATOR_CODE, countries, fetch_indicator, indicator, pd, population):
    def test_part_1():
        assert INDICATOR_CODE in ALLOWED_CODES, (
            "Set INDICATOR_CODE to one of the codes in the README's table."
        )
        assert fetch_indicator.__doc__ and "Replace this docstring" not in fetch_indicator.__doc__, (
            "Give fetch_indicator a docstring of your own."
        )
        for _name, _frame in [("countries", countries), ("population", population),
                              ("indicator", indicator)]:
            assert isinstance(_frame, pd.DataFrame), f"`{_name}` should be a DataFrame."
        assert "value" in indicator.columns, (
            "`indicator` has no `value` column. Is it still nested? Look at which of "
            "the two items in the response holds the data."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 2: Clean and join (30 points)

        ### 2.1 Find the problems (10)

        For each problem: the code that shows it, and how many rows or values it
        affects.
        """
    )
    return


@app.cell
def _():
    # Your investigation here. Add cells as you need them.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: at least four problems, each with its count.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 2.2 Decide, then merge (15)

        *Your decisions here, written **before** the merge. For each one, the
        alternative you considered and why you didn't choose it.*

        - **Join columns:**
        - **Join type:**
        - **Rows that aren't countries:**
        - **Cleaning first:**
        """
    )
    return


@app.cell
def _():
    # Your merge. Use intermediate cells for any cleaning.
    merged = None
    return (merged,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 2.3 Check the merge (5)""")
    return


@app.cell
def _():
    # Row counts before and after, and a check for unmatched rows.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what you checked, and what you found.*
        """
    )
    return


@app.cell(hide_code=True)
def _(merged, pd):
    def test_part_2():
        assert isinstance(merged, pd.DataFrame), "`merged` should be a DataFrame."
        assert "value" in merged.columns, "`merged` should still have the indicator's `value`."
        assert any("region" in str(_c) for _c in merged.columns), (
            "`merged` has no region column. Did the country list's columns come through?"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 3: Combine and reshape (25 points)

        ### 3.1 Stack (8)
        """
    )
    return


@app.cell
def _():
    # Clean and merge population the same way as your indicator, then stack.
    population_merged = None
    stacked = None
    return population_merged, stacked


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: how many rows `stacked` should have, and how you know.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 3.2 Reshape (10)""")
    return


@app.cell
def _():
    # One row per country, one column per year. Then add the change column,
    # under a new name.
    by_year = None
    return (by_year,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what you did about countries missing one of the years,
        and how many that affected.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 3.3 Rank (7)""")
    return


@app.cell
def _():
    # The ten largest and ten smallest changes, with region and income level.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: who is at each end.*
        """
    )
    return


@app.cell(hide_code=True)
def _(by_year, pd, stacked):
    def test_part_3():
        assert isinstance(stacked, pd.DataFrame), "`stacked` should be a DataFrame."
        assert isinstance(by_year, pd.DataFrame), "`by_year` should be a DataFrame."
        assert by_year.shape[1] >= 20, (
            f"`by_year` has {by_year.shape[1]} columns. It should have one per year, "
            "so it needs to be wide. Which of melt and pivot goes that way?"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 4: Find something interesting (20 points)

        ### 4.1 Ask (4)

        *Your question here.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 4.2 Answer (10)""")
    return


@app.cell
def _():
    # Your analysis. Add cells as you need them.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 4.3 Interpret (6)

        *Your answer here: what you found, whether it surprised you, what might
        explain it, and what you'd check before believing it.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 5: For a reader who doesn't code (10 points)

        **Question:**

        **Finding:**

        **Evidence:**

        -
        -

        **So what:**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## AI attribution

        *If you used generative AI in a substantial way, say what you used and what
        it did. Otherwise, write "None".*

        ---
        ## Before you submit

        1. Restart and run every cell, top to bottom.
        2. Rename this file `SI618_HW01_<uniqname>.py`.
        3. Export it:
           ```bash
           uvx marimo export html --sandbox SI618_HW01_<uniqname>.py -o SI618_HW01_<uniqname>.html
           ```
        4. Upload both files to Canvas.
        """
    )
    return


if __name__ == "__main__":
    app.run()
