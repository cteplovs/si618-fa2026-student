# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "matplotlib==3.11.1",
#     "seaborn==0.13.2",
#     "scipy==1.18.1",
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
        # SI 618 · Homework 2: What a restaurant grade hides

        **Name:**
        **Uniqname:**

        Due **Monday, October 5, before class (3:30 PM)**. The full spec is in
        `README.md`, and the rubric is in `RUBRIC.md`. Read both before you start.

        Rename this file `SI618_HW02_<uniqname>.py` before you submit, and upload
        its HTML export alongside it.

        ### Working in marimo

        - A variable can be defined in only one cell, so give each new result a
          new name, such as `inspections_checked`, or prefix a name with `_` to
          keep it inside its cell.
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
    import pandas as pd
    import seaborn as sns
    from scipy import stats

    pd.set_option("display.max_columns", 50)
    sns.set_theme(style="whitegrid")
    return mo, pd, plt, sns, stats


@app.cell
def _():
    DATA_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "nyc_restaurant_inspections_2026-09-28.csv.gz"
    )
    INSPECTION_KEY = ["camis", "inspection_date", "inspection_type"]
    return DATA_URL, INSPECTION_KEY


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 1: From violations to inspections (20 points)

        ### 1.1 Load and inspect (5)
        """
    )
    return


@app.cell
def _():
    # Load the data from DATA_URL into `raw`, then show its shape, its column
    # types, and the missing values in each column.
    raw = None
    return (raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what a single row represents, and the code that
        convinced you.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 1.2 Collapse (7)""")
    return


@app.cell
def _():
    # First check that what you intend to keep is constant within an
    # inspection. Then build `inspections`, with one row per inspection.
    inspections = None
    return (inspections,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: how many rows you started with, how many inspections
        you ended with, and how you know the second number is right.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 1.3 Decide what to keep (8)

        *Your decisions here, written **before** you filter. For each one, give
        the alternative you considered, the reason you rejected it, and how many
        inspections the decision removes.*

        - **Placeholder dates:**
        - **Inspection types:**
        - **Unknown borough:**
        - **Missing scores:**
        """
    )
    return


@app.cell
def _():
    # Filter `inspections` to the ones your analysis will use.
    scored = None
    return (scored,)


@app.cell(hide_code=True)
def _(INSPECTION_KEY, inspections, pd, raw, scored):
    def test_part_1():
        assert isinstance(raw, pd.DataFrame), "Load the data into `raw`."
        assert isinstance(inspections, pd.DataFrame), (
            "`inspections` should be a DataFrame."
        )
        assert len(inspections) < len(raw), (
            "`inspections` has as many rows as `raw`. A row of `raw` is not an "
            "inspection, so collapsing should leave fewer."
        )
        _key = [_c for _c in INSPECTION_KEY if _c in inspections.columns]
        assert not inspections.duplicated(_key).any(), (
            "Some inspections appear more than once in `inspections`. Which "
            "columns together identify a single inspection?"
        )
        assert isinstance(scored, pd.DataFrame), "`scored` should be a DataFrame."
        assert "score" in scored.columns, "`scored` should still have its `score` column."
        assert scored["score"].notna().all(), (
            "`scored` still contains inspections with no score. Decide what to do "
            "with them in 1.3."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 2: Describe the scores (25 points)

        ### 2.1 Summarise (7)
        """
    )
    return


@app.cell
def _():
    # The mean, median and skewness of the scores in `scored`.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what the three numbers together tell you about the
        shape of the distribution.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 2.2 Plot (8)""")
    return


@app.cell
def _():
    # A histogram, a box plot, and a Q-Q plot against a normal distribution.
    # Add cells as you need them.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: why you chose your bin width, and what each plot shows
        that the other two do not.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 2.3 Look closely (10)""")
    return


@app.cell
def _():
    # A histogram with one bar for every possible score from 0 to 50.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: where the histogram differs from a smooth right-skewed
        distribution, with counts, or why you think it does not.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 3: Explain what you found (15 points)
        """
    )
    return


@app.cell
def _():
    # Compare initial inspections and re-inspections around both cutoffs.
    # Add cells as you need them.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what you conclude and why, at least two explanations
        that could produce the pattern, and what further data would tell them
        apart.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 4: Compare groups (30 points)

        ### 4.1 Two cuisines (15)

        *Your answer here: the two cuisines, why you expect them to differ, and
        your hypotheses, written **before** you run the test.*
        """
    )
    return


@app.cell
def _():
    # Run the t-test and assign its result to `cuisine_result`. Report the
    # difference between the two groups in inspection points as well.
    cuisine_result = None
    return (cuisine_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what the result means, whether the assumptions are
        reasonable for these data, and whether the difference would matter to a
        diner.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 4.2 Five boroughs (15)

        *Your answer here: your hypotheses, written **before** you run the
        test.*
        """
    )
    return


@app.cell
def _():
    # The mean, median and number of inspections in each borough, then the
    # one-way ANOVA, with its result assigned to `borough_result`.
    borough_result = None
    return (borough_result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what the test tells you, what it does not, how large
        the differences between boroughs actually are, and whether the
        assumptions are reasonable for these data.*
        """
    )
    return


@app.cell(hide_code=True)
def _(borough_result, cuisine_result):
    def test_part_4():
        for _name, _result in [("cuisine_result", cuisine_result),
                               ("borough_result", borough_result)]:
            assert _result is not None, f"Assign your test's result to `{_name}`."
            assert hasattr(_result, "pvalue"), (
                f"`{_name}` has no p-value. Assign the object that the scipy "
                "test returns, rather than a number taken from it."
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
        2. Rename this file `SI618_HW02_<uniqname>.py`.
        3. Export it:
           ```bash
           uvx marimo export html --sandbox SI618_HW02_<uniqname>.py -o SI618_HW02_<uniqname>.html
           ```
        4. Upload both files to Canvas.
        """
    )
    return


if __name__ == "__main__":
    app.run()
