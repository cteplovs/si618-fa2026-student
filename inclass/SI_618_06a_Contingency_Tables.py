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
    mo.md(r"""
    # SI 618 - 06a: contingency tables and the chi-square test

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 11 (Wed Oct 7)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.10.06.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Build a contingency table from two categorical columns, and read it as
      counts and as proportions
    - Work out the counts you would expect if the two columns were unrelated,
      and say which cells depart from them most
    - Test whether two categorical columns are related with the chi-square test
      of independence
    - Measure how strong the relationship is with Cramer's V, and show it with a
      mosaic plot

    ## Pre-class reading

    Bruce, P., Bruce, A. and Gedeck, P. (2020). *Practical Statistics for Data
    Scientists*, 2nd edition, the chi-square test section of chapter 3
    (Statistical Experiments and Significance Testing).

    ## How this notebook works

    **This file is today's session, start to finish**, and it is the first half
    of In-class 06. Monday's file will be 06b, and you submit both together at
    the end of Monday's session.

    As in 05a and 05b, each exercise gives each of you a slightly different
    version of the same question, and the room's answers, put together by a show
    of hands, tell you something that no single notebook can. You are welcome to
    compare results with the people around you, although nothing you are graded
    on depends on it.

    ✅ **Before anything else, please type your uniqname below**, because it
    chooses your cuisine in Exercise 1 and your column in Exercise 2.
    """)
    return


@app.cell
def _():
    UNIQNAME = ""
    return (UNIQNAME,)


@app.cell
def _():
    import warnings
    import zlib

    import marimo as mo
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats
    from statsmodels.graphics.mosaicplot import mosaic

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    sns.set_theme(style="whitegrid")

    warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
    return mo, mosaic, np, pd, plt, stats, zlib


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data is the snapshot of New York City restaurant inspections from
    Homework 2. The cell below keeps one row per initial inspection with a score
    and a known borough, and adds four categorical columns: `grade_band`, which
    is `"A"` for a score of 13 or less and `"not A"` otherwise; `cuisine`, with
    everything outside the ten most common cuisines grouped as `"Other"`; and the
    `weekday` and `month` of the inspection.
    """)
    return


@app.cell
def _(np, pd):
    INSPECTIONS_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "nyc_restaurant_inspections_2026-09-28.csv.gz"
    )
    _raw = pd.read_csv(INSPECTIONS_URL)
    inspections = (
        _raw.drop_duplicates(["camis", "inspection_date", "inspection_type"])
        .query('inspection_type == "Cycle Inspection / Initial Inspection" and boro != "0"')
        .dropna(subset=["score"])
        .copy()
    )
    inspections["grade_band"] = np.where(inspections["score"] <= 13, "A", "not A")
    _top10 = inspections["cuisine_description"].value_counts().index[:10]
    inspections["cuisine"] = inspections["cuisine_description"].where(
        inspections["cuisine_description"].isin(_top10), "Other"
    )
    _dates = pd.to_datetime(inspections["inspection_date"])
    inspections["weekday"] = _dates.dt.day_name()
    inspections["month"] = _dates.dt.month_name()
    inspections[["boro", "cuisine_description", "score", "grade_band", "weekday", "month"]].head()
    return (inspections,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That leaves 46,627 inspections.

    ---
    ## Part 1: A contingency table

    A **contingency table** counts how often each combination of two
    categorical columns occurs. `pd.crosstab` builds one, with the first column
    as the rows and the second as the columns.
    """)
    return


@app.cell
def _(inspections, pd):
    boro_table = pd.crosstab(inspections["boro"], inspections["grade_band"])
    boro_table
    return (boro_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counts are hard to compare when the boroughs differ this much in size, since
    Manhattan has ten times as many inspections as Staten Island.
    `normalize="index"` divides each row by its total, so each row shows the
    share of that borough's inspections in each column.
    """)
    return


@app.cell
def _(inspections, pd):
    pd.crosstab(inspections["boro"], inspections["grade_band"], normalize="index").round(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Manhattan has the highest share of A grades, at 62%, and Staten Island the
    lowest, at 55%. The question for the rest of the session is whether a spread
    of seven points across boroughs says anything about the boroughs, and if so,
    how much.

    ---
    ### Vote: which borough is most out of line?

    If borough made no difference to grades, every borough would have the
    city-wide share of A grades, which is 60%, and its counts would follow from
    that. Look at the counts in `boro_table` and the shares above.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    first_vote = mo.ui.radio(
        options=["Bronx", "Manhattan", "Queens", "Staten Island"],
        label="**First vote.** Which borough's counts are furthest from what you would expect if borough made no difference?",
    )
    first_vote
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Please vote in the notebook and with your hand when asked, then take a
    minute to tell the person next to you which way you voted and why, and vote
    again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    second_vote = mo.ui.radio(
        options=["Bronx", "Manhattan", "Queens", "Staten Island"],
        label="**Second vote**, after talking it over.",
    )
    reveal = mo.ui.run_button(label="Reveal the expected counts")
    mo.vstack([second_vote, reveal])
    return (reveal,)


@app.cell
def _(boro_table, mo, np, pd, reveal):
    mo.stop(not reveal.value, mo.md("*Press the button once you have voted twice.*"))
    _n = boro_table.to_numpy().sum()
    boro_expected = pd.DataFrame(
        np.outer(boro_table.sum(axis=1), boro_table.sum(axis=0)) / _n,
        index=boro_table.index,
        columns=boro_table.columns,
    )
    boro_residuals = (boro_table - boro_expected) / np.sqrt(boro_expected)
    mo.vstack([
        mo.md("**Expected counts**, if borough made no difference:"),
        boro_expected.round(0),
        mo.md("**Standardised residuals**, (observed - expected) / sqrt(expected):"),
        boro_residuals.round(2),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each **expected count** is the row total times the column total, divided by
    the number of inspections. For the Bronx, that is 4,419 inspections times
    the city-wide share of A grades, which gives 2,652 A grades, against the
    2,569 it received.

    A **standardised residual** divides the gap between the observed and
    expected counts by the square root of the expected count, so that gaps in
    large and small cells can be compared. Queens, whose not-A count is 4.8
    standardised units above what independence predicts, is furthest out of
    line, even though Staten Island has the lower share of A grades. Staten
    Island is small, so its shortfall of about five points below the city-wide
    60% amounts to fewer inspections than Queens's shortfall of three points.

    ---
    ## Part 2: The chi-square test

    Squaring the standardised residuals and adding them up gives the
    **chi-square statistic**, which is zero when every count matches its
    expected value and grows as the table moves further from independence.
    `stats.chi2_contingency` computes it, together with its p-value, its
    degrees of freedom and the table of expected counts.
    """)
    return


@app.cell
def _(boro_table, stats):
    stats.chi2_contingency(boro_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The statistic is 94.9, with 4 **degrees of freedom**, which for a table is
    (rows - 1) times (columns - 1). The p-value, about `1e-19`, is the
    probability of a table at least this far from independence if borough made
    no difference to grades, so by the convention from 05a the relationship
    between borough and grade is significant.

    The test requires every **expected** count to be at least 5. The smallest
    here is 682, but cutting a table into small groups, as you will in Exercise
    1, can bring expected counts below that.

    ---
    ### 🚀 Exercise 1: does the borough pattern hold within one cuisine?

    The table above mixes every kind of restaurant together. Your uniqname has
    assigned you one of the eight most common cuisines, shown below as
    `my_cuisine`.

    ✅ Step 1: Build `my_table`, a contingency table of `boro` against
    `grade_band` for the inspections of your cuisine only.

    ✅ Step 2: Assign to `my_p` the p-value of the chi-square test on
    `my_table`, as a float.

    ✅ Step 3: When asked, raise your hand if your p-value is below 0.05.

    ✅ Step 4: Assign to `cuisine_sentence` two or three sentences on what the
    hands showed. Say whether the borough pattern holds within every cuisine,
    and look at the shares of A grades by borough for your own cuisine to say
    whether it runs in the same direction as the city-wide pattern.
    """)
    return


@app.cell
def _(UNIQNAME, inspections, mo, zlib):
    mo.stop(
        not UNIQNAME.strip(),
        mo.md("⚠️ Type your uniqname into `UNIQNAME` at the top of the notebook."),
    )
    my_seed = zlib.crc32(UNIQNAME.strip().lower().encode())
    my_cuisine = inspections["cuisine_description"].value_counts().index[:8][my_seed % 8]
    my_cuisine
    return my_cuisine, my_seed


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_table = None
    my_p = None
    cuisine_sentence = ""
    return cuisine_sentence, my_p, my_table


@app.cell(hide_code=True)
def _(cuisine_sentence, inspections, my_cuisine, my_p, my_table, pd, stats):
    def test_exercise_1():
        _mine = inspections[inspections["cuisine_description"] == my_cuisine]
        _expected = pd.crosstab(_mine["boro"], _mine["grade_band"])
        assert my_table is not None, "Build your contingency table and assign it to `my_table`."
        assert my_table.shape == (5, 2), (
            f"`my_table` has shape {my_table.shape}, where 5 boroughs by 2 grade bands "
            "is expected. Put `boro` first and `grade_band` second."
        )
        assert int(my_table.to_numpy().sum()) == len(_mine), (
            f"`my_table` counts {int(my_table.to_numpy().sum())} inspections, but "
            f"{my_cuisine} has {len(_mine)}. Filter on `cuisine_description` first."
        )
        _p = stats.chi2_contingency(_expected).pvalue
        assert my_p is not None, "Assign the chi-square p-value to `my_p`."
        assert abs(float(my_p) - _p) < 1e-9, (
            f"`my_p` is {my_p}. Pass `my_table` to `stats.chi2_contingency` and "
            "take `.pvalue`."
        )
        assert len(cuisine_sentence.strip()) >= 100, (
            f"`cuisine_sentence` is {len(cuisine_sentence.strip())} characters, where "
            "an account of the hands and of your own cuisine is expected."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: How strong is the relationship?

    A p-value of `1e-19` says that the relationship between borough and grade is
    very unlikely to be chance, but with 46,627 inspections even a weak
    relationship produces a tiny p-value, as 05a showed for differences in
    means. **Cramer's V** measures strength instead, by rescaling the chi-square
    statistic so that it runs from 0, for no relationship, to 1, for a perfect
    one, whatever the size of the table:

    V = sqrt(chi-square / (n * (k - 1))), where n is the number of observations
    and k is the smaller of the number of rows and the number of columns.
    """)
    return


@app.cell
def _(boro_table, np, stats):
    _chi2 = stats.chi2_contingency(boro_table).statistic
    _n = boro_table.to_numpy().sum()
    _k = min(boro_table.shape)
    round(float(np.sqrt(_chi2 / (_n * (_k - 1)))), 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A V of 0.045 is very weak: a common rough guide calls 0.1 weak, 0.3
    moderate and 0.5 strong, so borough is related to grade beyond reasonable
    doubt, but only slightly.

    A **mosaic plot** shows the same table as tiles whose widths are each
    borough's share of the inspections and whose heights are the share of each
    grade band within the borough. When two columns are unrelated, the
    horizontal divisions line up across the plot.
    """)
    return


@app.cell
def _(inspections, mosaic, plt):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    mosaic(inspections, ["boro", "grade_band"], ax=_ax, labelizer=lambda _key: "")
    _ax.set_title("Grade band within each borough")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The divisions are nearly level, which is what a V of 0.045 looks like.

    ---
    ### 🚀 Exercise 2: which column goes with the grade most strongly?

    Your uniqname has assigned you one column of `inspections`, shown below as
    `my_column`: one of `boro`, `cuisine`, `weekday` or `month`.

    ✅ Step 1: Write a function `cramers_v(table)` that takes a contingency
    table and returns Cramer's V as a float. On `boro_table` it should give
    0.045.

    ✅ Step 2: Build the contingency table of `my_column` against `grade_band`,
    and assign its chi-square p-value to `my_column_p` and its Cramer's V to
    `my_v`.

    ✅ Step 3: When asked, the room will raise hands by column, and then
    everyone whose p-value is below 0.05 will keep a hand up. After that, only
    those whose V is above 0.1 will keep a hand up.

    ✅ Step 4: Assign to `column_sentence` two or three sentences saying which
    column the hands showed to go with the grade most strongly, and what the two
    rounds of hands together say about reading a p-value on its own.
    """)
    return


@app.cell
def _(my_seed):
    my_column = ["boro", "cuisine", "weekday", "month"][(my_seed // 8) % 4]
    my_column
    return (my_column,)


@app.cell
def _():
    # Your code here.
    def cramers_v(table) -> float:
        return None

    my_column_p = None
    my_v = None
    column_sentence = ""
    return column_sentence, cramers_v, my_column_p, my_v


@app.cell(hide_code=True)
def _(
    boro_table,
    column_sentence,
    cramers_v,
    inspections,
    my_column,
    my_column_p,
    my_v,
    np,
    pd,
    stats,
):
    def test_exercise_2():
        _boro_v = cramers_v(boro_table)
        assert _boro_v is not None, "`cramers_v` should return Cramer's V."
        assert abs(float(_boro_v) - 0.0451) < 0.001, (
            f"On `boro_table`, `cramers_v` gives {_boro_v}, where 0.045 is expected. "
            "Use the smaller of rows and columns for k, and take the square root."
        )
        _table = pd.crosstab(inspections[my_column], inspections["grade_band"])
        _result = stats.chi2_contingency(_table)
        _v = np.sqrt(_result.statistic / (_table.to_numpy().sum() * (min(_table.shape) - 1)))
        assert my_column_p is not None, "Assign the chi-square p-value to `my_column_p`."
        assert abs(float(my_column_p) - _result.pvalue) < 1e-9, (
            f"`my_column_p` is {my_column_p}. Cross `{my_column}` with `grade_band` "
            "and take the p-value of `stats.chi2_contingency`."
        )
        assert my_v is not None, "Assign Cramer's V for your column to `my_v`."
        assert abs(float(my_v) - _v) < 1e-6, (
            f"`my_v` is {my_v}. Apply `cramers_v` to the table of `{my_column}` "
            "against `grade_band`."
        )
        assert len(column_sentence.strip()) >= 100, (
            f"`column_sentence` is {len(column_sentence.strip())} characters, where "
            "the room's answer and what it says about p-values are expected."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - `pd.crosstab(a, b)` builds a contingency table, and `normalize="index"`
      turns each row into shares
    - the expected count for a cell is its row total times its column total,
      divided by the number of observations, and standardised residuals show
      which cells depart from independence most
    - `stats.chi2_contingency(table)` gives the chi-square statistic, its
      p-value, its degrees of freedom and the expected counts, and it needs
      every expected count to be at least 5
    - a relationship can hold overall and fail, or reverse, within a subgroup
    - Cramer's V measures the strength of a relationship from 0 to 1, which a
      p-value does not, and a mosaic plot shows it

    ## Next class

    **Notebook 06b** turns text into categories. You will split restaurant
    names into words, count them, and use today's test to ask whether a word in
    a restaurant's name goes with its grade.

    ## Additional resources

    - [scipy.stats.chi2_contingency](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)
    - [pandas.crosstab](https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html)
    - [statsmodels mosaic plots](https://www.statsmodels.org/stable/generated/statsmodels.graphics.mosaicplot.mosaic.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded; it is for anyone who finishes early or wants more
    afterwards.

    **Look at the residuals for your cuisine** in Exercise 1, and find the
    borough that departs most from independence. Compare it with the city-wide
    residuals in Part 1.

    **Use the score instead of the band.** Run a one-way ANOVA of `score` across
    boroughs, as in Homework 2, and compare its verdict with the chi-square
    test's. Cutting a score into "A" and "not A" throws information away, so
    think about when that is worth doing.

    **Try a smaller sample.** Draw 300 inspections with
    `inspections.sample(300, random_state=0)`, run the borough test again, and
    check the smallest expected count and what happens to the p-value.
    """)
    return


@app.cell(hide_code=True)
def _(UNIQNAME, mo):
    _name = UNIQNAME.strip().lower() or "<uniqname>"
    mo.md(rf"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Before you leave today.** Please save two files:

    1. This notebook, renamed `SI618_06a_{_name}.py`
    2. An HTML export of it:
       ```bash
       uvx marimo export html --sandbox SI618_06a_{_name}.py -o SI618_06a_{_name}.html
       ```

    ❗️ **Keep both files.** In-class 06 is one deliverable covering today and
    Monday, and at the end of Monday's session you will upload all four files,
    today's two and Monday's two, in a single submission.
    """)
    return


if __name__ == "__main__":
    app.run()
