# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "matplotlib==3.11.1",
#     "seaborn==0.13.2",
#     "scipy==1.18.1",
#     "statsmodels==0.14.6",
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
        # SI 618 - Homework 3: What a neighbourhood's jobs say about its income

        **Name:**
        **Uniqname:**

        Due **Monday, October 12, before class (3:30 PM)**. The full spec is in
        `README.md`, and the rubric is in `RUBRIC.md`. Read both before you start.

        Rename this file `SI618_HW03_<uniqname>.py` before you submit, and upload
        its HTML export alongside it.

        ### Working in marimo

        - A variable can be defined in only one cell, so give each new result a
          new name, such as `tracts_checked`, or prefix a name with `_` to keep it
          inside its cell.
        - Add as many cells as you need, wherever you need them.
        - For written answers, edit the markdown cells marked *Your answer here*.
        - The tests at the end of each part check that your work has the right
          **shape**, not that it is right, so a green test does not mean that a
          part is complete.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import statsmodels.formula.api as smf

    pd.set_option("display.max_columns", 50)
    sns.set_theme(style="whitegrid")
    return mo, np, pd, plt, smf, sns


@app.cell
def _():
    DATA_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "mi_tracts_acs2024.csv"
    )
    OCCUPATIONS = ["management", "service", "sales_office", "construction", "production"]
    return DATA_URL, OCCUPATIONS


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 1: Load and clean (20 points)

        ### 1.1 Load and inspect (5)
        """
    )
    return


@app.cell
def _():
    # Load the data from DATA_URL into `raw`, then show its shape, its column
    # types, the missing values in each column, and the mean, median, minimum
    # and maximum of `median_income`.
    raw = None
    return (raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what those four numbers tell you before you have looked
        any further.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 1.2 Find the problems (7)""")
    return


@app.cell
def _():
    # One cell per problem: the code that demonstrates it, and the number of
    # tracts affected. Add cells as you need them.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: for each problem, one sentence on what it would do to a
        correlation or a fitted line if you ignored it.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 1.3 Decide and clean (8)

        *Your decisions here, written **before** you clean. For each problem from
        1.2, give the alternative you considered and the reason you rejected it.*

        -
        -
        -
        """
    )
    return


@app.cell
def _():
    # Build `tracts`: apply your decisions, add a `county` column, and add one
    # share column per occupation group, as a proportion between 0 and 1.
    tracts = None
    return (tracts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: how many tracts remain, and how many each decision
        removed.*
        """
    )
    return


@app.cell(hide_code=True)
def _(pd, raw, tracts):
    def test_part_1():
        assert isinstance(raw, pd.DataFrame), "Load the data into `raw`."
        assert isinstance(tracts, pd.DataFrame), "`tracts` should be a DataFrame."
        assert "county" in tracts.columns, "Add a `county` column to `tracts`."
        assert len(tracts) < len(raw), (
            "`tracts` has as many rows as `raw`. Did any of your 1.3 decisions "
            "remove tracts?"
        )
        assert (tracts["median_income"] > 0).all(), (
            "`tracts` still has incomes of zero or less. What do the very large "
            "negative values in `median_income` mean?"
        )
        _shares = [_c for _c in tracts.columns if "share" in _c]
        assert len(_shares) >= 5, (
            f"`tracts` has {len(_shares)} columns with 'share' in the name, where "
            "one per occupation group is expected."
        )
        for _c in _shares:
            assert tracts[_c].between(0, 1).all(), (
                f"`{_c}` has values outside 0 to 1. Divide by `employed`, and "
                "check what happens in tracts where `employed` is 0."
            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 2: Plot before you fit (20 points)

        ### 2.1 The scatterplot (8)
        """
    )
    return


@app.cell
def _():
    # Plot `median_income` against the management share.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: the shape of the relationship, how the spread changes
        along it, and the points that stand apart, naming at least one.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 2.2 Five correlations (12)""")
    return


@app.cell
def _():
    # One table with Pearson's and Spearman's correlation between
    # `median_income` and each of the five shares.
    return


@app.cell
def _():
    # The share whose two coefficients differ most, plotted against income.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: which share goes most strongly with income, in which
        direction, and whether the gap between the two coefficients matters.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 3: Fit a line (25 points)

        ### 3.1 Fit (10)
        """
    )
    return


@app.cell
def _():
    # Fit median_income against the management share, and assign the fitted
    # model to `line_model`.
    line_model = None
    return (line_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: the slope in dollars for 10 percentage points, whether
        the intercept describes a real tract, and what R-squared leaves
        unexplained.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 3.2 The tracts the line fits worst (15)""")
    return


@app.cell
def _():
    # The ten tracts furthest below the line and the ten furthest above it,
    # with their county, management share, median income and margin of error.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what the tracts at each end have in common, why the
        line misses them, what further data would check that, and whether the
        margin of error could account for any of them.*
        """
    )
    return


@app.cell(hide_code=True)
def _(line_model):
    def test_part_3():
        assert line_model is not None, "Assign your fitted model to `line_model`."
        assert hasattr(line_model, "rsquared"), (
            "`line_model` has no R-squared. Assign the result of `.fit()`, rather "
            "than the formula or the unfitted model."
        )
        assert len(line_model.params) == 2, (
            f"`line_model` has {len(line_model.params)} coefficients, where an "
            "intercept and one slope are expected."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 4: Add a predictor (25 points)

        ### 4.1 Choose (5)

        *Your answer here, written **before** you fit: the predictor you chose,
        why, and what you expect it to do to the management share's coefficient.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 4.2 Fit and interpret (12)""")
    return


@app.cell
def _():
    # Fit the model with both predictors, and assign it to `two_model`.
    two_model = None
    return (two_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what your predictor's coefficient means with the
        management share held constant, and how the management share's
        coefficient and R-squared compare with 3.1.*
        """
    )
    return


@app.cell(hide_code=True)
def _(line_model, two_model):
    def test_part_4():
        assert two_model is not None, "Assign your fitted model to `two_model`."
        assert hasattr(two_model, "rsquared"), (
            "`two_model` has no R-squared. Assign the result of `.fit()`."
        )
        assert len(two_model.params) > len(line_model.params), (
            "`two_model` has no more coefficients than `line_model`. Add your "
            "predictor to the formula."
        )
        assert any("management" in str(_p) for _p in two_model.params.index), (
            "`two_model` has no management share coefficient. Keep it in the "
            "formula alongside your new predictor."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 4.3 Judge (8)

        *Your answer here: whether your predictor changed what Part 3 appeared to
        show, what someone would have to assume before reading either model as
        cause and effect, and why a relationship between tracts may not hold for
        the people living in them.*
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
        2. Rename this file `SI618_HW03_<uniqname>.py`.
        3. Export it:
           ```bash
           uvx marimo export html --sandbox SI618_HW03_<uniqname>.py -o SI618_HW03_<uniqname>.html
           ```
        4. Upload both files to Canvas.
        """
    )
    return


if __name__ == "__main__":
    app.run()
