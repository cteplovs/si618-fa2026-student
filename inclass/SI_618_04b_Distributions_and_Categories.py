# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo>=0.23.3",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
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
    mo.md(r"""
    # SI 618 · 04b: shapes, categories, and the limits of a summary

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** · Session 8 (Mon Sep 28)

    Copyright © 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.09.22.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Name the shape of a distribution from its skewness, and say what the sign
      of that number tells you about the mean and the median
    - Read a Q-Q plot, and say what a curve away from the line means
    - Identify a distribution's shape from its plots rather than from its
      summary statistics
    - Build a categorical column from a numeric one, and compare groups with bar
      charts, including grouped and stacked ones
    - Say what a correlation coefficient does not tell you

    ## Pre-class reading

    McKinney, W. (2022). *Python for Data Analysis*, 3rd edition, chapter 9
    (Plotting and Visualization).

    ## How this notebook works

    **This file is today's session, start to finish**, and it is the second half
    of In-class 04. Wednesday's file was 04a, and you submit both today.

    You do not need 04a open to do this one, though the columns will be familiar.
    There are two exercises, and as on Wednesday the second has more than one
    defensible answer.
    """)
    return


@app.cell
def _():
    import warnings

    import marimo as mo
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    sns.set_theme(style="whitegrid")

    warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
    return mo, np, pd, plt, sns, stats


@app.cell
def _(pd):
    HAPPINESS_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/"
        "refs/heads/main/happiness_2019.csv"
    )
    happiness = pd.read_csv(HAPPINESS_URL)
    happiness.head()
    return (happiness,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Naming the shapes

    On Wednesday two box plots looked nothing like each other. `corruption` had
    fourteen dots above the box and none below, while `social_support` had four
    below and none above. Those are the two shapes worth naming.

    - A **right-skewed** distribution has a long tail on the high side, and its
      mean sits above its median, which is what the commute data did.
    - A **left-skewed** distribution has the long tail on the low side, and its
      mean sits below its median.
    - A **symmetric** distribution has neither, and the two agree.

    `.skew()` puts a number on it: negative for a left tail, positive for a right
    tail, and near zero for symmetry.
    """)
    return


@app.cell
def _(happiness):
    _columns = [
        "social_support", "freedom", "gdp_per_capita",
        "happiness_score", "generosity", "corruption",
    ]
    shape_table = happiness[_columns].agg(["mean", "median", "skew"]).T.round(3)
    shape_table.assign(mean_minus_median=(shape_table["mean"] - shape_table["median"]).round(3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read the two right-hand columns together, because they always agree in sign.
    `social_support` skews −1.14 and its mean sits below its median;
    `corruption` skews +1.65 and its mean sits above; `happiness_score` skews
    0.01 and the two are within a hundredth of each other.

    A rough reading of the number: below about 0.5 in absolute value is nearly
    symmetric, and above 1 is strongly skewed. Those boundaries are conventions
    rather than facts, and the plot is still the thing to look at.

    ---
    ## Part 2: Q-Q plots

    A **Q-Q plot** compares your data against a distribution you name, usually
    the normal. It sorts your values, works out where each one would fall if the
    data were normal, and plots the two against each other. Points on the
    straight line mean your data matches, and points curving away mean it does
    not.

    This matters more than it looks, because several of the tests in notebook 05
    assume a roughly normal distribution.
    """)
    return


@app.cell
def _(happiness, plt, stats):
    _fig, _ax = plt.subplots(figsize=(6, 5))
    stats.probplot(happiness["happiness_score"], dist="norm", plot=_ax)
    _ax.set_title("Happiness score against a normal distribution")
    _ax
    return


@app.cell
def _(happiness, plt, stats):
    _fig, _ax = plt.subplots(figsize=(6, 5))
    stats.probplot(happiness["corruption"], dist="norm", plot=_ax)
    _ax.set_title("Corruption against a normal distribution")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The happiness score sits close to the line along most of its length, bending
    only at the ends, which is what real data that is roughly normal looks like.
    Corruption curves away sharply at the top, because its long right tail
    produces values far larger than a normal distribution would.

    Reading the curve: points above the line at the right mean the high values
    are more extreme than normal, which is the same right tail you saw as
    fourteen dots on the box plot, drawn a second way.

    ---
    ### 🚀 Exercise 1: identify six distributions

    The file below holds six columns named `v1` to `v6`, with 500 rows each and
    no other clue about what they are. Each one has a different shape.

    ✅ Assign a dictionary to `shapes`, mapping each column name to its shape,
    using exactly these six labels, each of which is used once:

    `"normal"` · `"right-skewed"` · `"left-skewed"` · `"uniform"` ·
    `"bimodal"` · `"normal with outliers"`

    Plot before you compute. A histogram tells you most of it, a box plot settles
    whether the tail is a tail or a handful of separate values, and `.skew()`
    and `.kurtosis()` confirm what you are already looking at.

    Two of the six have a positive skew, and telling them apart is the point of
    the exercise: one has a smooth tail trailing off, while the other is a bell
    with a few values sitting well away from it.
    """)
    return


@app.cell
def _(pd):
    MYSTERY_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/"
        "main/mystery_distributions.csv"
    )
    mystery = pd.read_csv(MYSTERY_URL)
    mystery.describe().round(2)
    return (mystery,)


@app.cell
def _():
    # Your code here. Plot first, then fill in the dictionary.
    shapes = {}
    return (shapes,)


@app.cell(hide_code=True)
def _(shapes):
    def test_exercise_1():
        _answer = {
            "v1": "normal",
            "v2": "right-skewed",
            "v3": "left-skewed",
            "v4": "uniform",
            "v5": "bimodal",
            "v6": "normal with outliers",
        }
        _hints = {
            "v1": "skews 0.18 with kurtosis near zero, and its Q-Q plot is nearly straight.",
            "v2": "skews +1.77, and nothing falls below 20, so the tail runs one way only.",
            "v3": "skews -2.06, with a long tail running down to -9.",
            "v4": "has kurtosis -1.22 and a histogram that is flat from 30 to 70.",
            "v5": "has two separate humps, which no single skew number can tell you about.",
            "v6": "skews +1.60, but its histogram is a bell with 25 values sitting apart from it.",
        }
        assert isinstance(shapes, dict), (
            f"`shapes` should be a dictionary, not a {type(shapes).__name__}."
        )
        _missing = set(_answer) - set(shapes)
        assert not _missing, f"`shapes` is missing {sorted(_missing)}."
        _vocab = set(_answer.values())
        for _col, _given in shapes.items():
            assert _given in _vocab, (
                f"{_col} is labelled {_given!r}, which is not one of the six labels."
            )
        assert len(set(shapes.values())) == 6, (
            "Each label is used exactly once, and yours repeats one. Two of the six "
            "have a positive skew, and they are not the same shape."
        )
        for _col, _want in _answer.items():
            assert shapes[_col] == _want, (
                f"{_col} is labelled {shapes[_col]!r}. Look again: it {_hints[_col]}"
            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Making categories, and comparing them

    Every plot so far has taken a numeric column. To compare groups you need a
    categorical one, and often you have to build it. `pd.qcut` cuts a numeric
    column into equal-sized groups by quantile, which is the same idea as the
    quartiles in `.describe()`.
    """)
    return


@app.cell
def _(happiness, np, pd):
    tiers = pd.qcut(
        happiness["happiness_score"], 4,
        labels=["bottom", "lower-mid", "upper-mid", "top"],
    )
    happiness_tiered = happiness.assign(
        tier=tiers,
        government=np.where(
            happiness["corruption"] >= happiness["corruption"].median(),
            "cleaner", "less clean",
        ),
    )
    happiness_tiered["tier"].value_counts().sort_index()
    return (happiness_tiered,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Thirty-nine countries in each tier, by construction, since `qcut` cuts by
    quantile rather than by value. `pd.cut` is its sibling, cutting at values you
    name and giving groups of unequal size.

    A bar chart of a **mean** within each group is `sns.barplot`, which computes
    the mean for you and draws a confidence interval around it.
    """)
    return


@app.cell
def _(happiness_tiered, sns):
    _ax = sns.barplot(data=happiness_tiered, x="tier", y="gdp_per_capita")
    _ax.set_xlabel("Happiness tier")
    _ax.set_ylabel("Income contribution to the score")
    _ax.set_title("Income contribution rises with happiness tier")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That rises cleanly, 0.47 to 1.31 across the four tiers, and the bars do not
    overlap much, which is worth noticing before Monday's material on whether a
    difference is real.

    To compare **two** categorical columns you need counts rather than a mean,
    and `pd.crosstab` counts every combination.
    """)
    return


@app.cell
def _(happiness_tiered, pd):
    tier_government = pd.crosstab(
        happiness_tiered["tier"], happiness_tiered["government"]
    )
    tier_government
    return (tier_government,)


@app.cell
def _(plt, tier_government):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4.5))
    tier_government.plot(kind="bar", ax=_axes[0])
    _axes[0].set_title("Grouped: bars side by side")
    _axes[0].set_xlabel("Happiness tier")
    _axes[0].set_ylabel("Number of countries")
    tier_government.plot(kind="bar", stacked=True, ax=_axes[1])
    _axes[1].set_title("Stacked: bars on top of each other")
    _axes[1].set_xlabel("Happiness tier")
    _axes[1].set_ylabel("Number of countries")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Grouped bars compare the pieces; stacked bars compare the totals.** Here
    the totals are 39 everywhere, so the stacked version is only useful for
    reading the proportion inside each bar, and the grouped version is the one
    that answers the question.

    ---
    ### 🚀 Exercise 2: does a cleaner government track with happiness?

    The two columns you just crossed are `tier`, built from the happiness score,
    and `government`, which splits countries at the median of `corruption`, so
    "cleaner" means a government whose perceived corruption contributes more to
    happiness than the typical country's does.

    ✅ Step 1: Assign the crosstab of `tier` against `government` to
    `tier_counts`, using `happiness_tiered`.

    ✅ Step 2: Assign to `cleaner_share` a Series giving the **proportion** of
    each tier whose government is "cleaner", as a number between 0 and 1.

    *Hint:* dividing the crosstab by its row totals gives proportions, and
    `.sum(axis=1)` produces those totals. `div(..., axis=0)` divides each row.

    ✅ Step 3: Build one labelled bar chart of `cleaner_share`, and assign its
    axes to `ax_share`.

    ✅ Step 4: Look at the four numbers before you write anything, because they
    do not do what the barplot in Part 3 did. Assign to `share_claim` a sentence
    or two saying what the pattern is and what you would need before telling
    somebody that cleaner government makes a country happier.
    """)
    return


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    tier_counts = None
    cleaner_share = None
    ax_share = None
    share_claim = ""
    return ax_share, cleaner_share, share_claim, tier_counts


@app.cell(hide_code=True)
def _(ax_share, cleaner_share, share_claim, tier_counts):
    def test_exercise_2():
        assert tier_counts is not None, "Assign the crosstab to `tier_counts`."
        assert tuple(tier_counts.shape) == (4, 2), (
            f"Expected 4 tiers by 2 government groups, got {tuple(tier_counts.shape)}."
        )
        assert int(tier_counts.to_numpy().sum()) == 156, (
            f"The counts should add to 156 countries, not "
            f"{int(tier_counts.to_numpy().sum())}."
        )
        assert int(tier_counts.loc["top", "cleaner"]) == 28, (
            f"The top tier should have 28 cleaner governments, got "
            f"{tier_counts.loc['top', 'cleaner']}."
        )
        assert cleaner_share is not None, "Assign the proportions to `cleaner_share`."
        assert abs(float(cleaner_share.loc["top"]) - 28 / 39) < 0.01, (
            f"The top tier's share should be 28/39, about 0.72, got "
            f"{cleaner_share.loc['top']}. These are proportions rather than counts."
        )
        assert abs(float(cleaner_share.loc["upper-mid"]) - 14 / 39) < 0.01, (
            f"The upper-mid tier's share should be 14/39, about 0.36, got "
            f"{cleaner_share.loc['upper-mid']}."
        )
        assert ax_share is not None, "Assign your plot's axes to `ax_share`."
        _marks = (
            len(getattr(ax_share, "patches", []))
            + len(getattr(ax_share, "lines", []))
            + len(getattr(ax_share, "collections", []))
        )
        assert _marks > 0, (
            f"`ax_share` is a {type(ax_share).__name__} with nothing drawn on it."
        )
        assert (
            ax_share.get_xlabel().strip() != "" or ax_share.get_ylabel().strip() != ""
        ), "Label the axes in words rather than leaving the column names."
        assert len(share_claim.strip()) >= 80, (
            f"`share_claim` is {len(share_claim.strip())} characters, where the "
            "pattern and what you would still need are both expected."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: What a correlation does not tell you

    One more warning before notebook 05, which is built on correlation and
    regression. These four datasets were written by the statistician Frank
    Anscombe in 1973, and they are the most efficient argument for plotting
    anything before you summarise it.
    """)
    return


@app.cell
def _(pd):
    _x_common = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
    anscombe = pd.concat([
        pd.DataFrame({"dataset": "I", "x": _x_common,
                      "y": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]}),
        pd.DataFrame({"dataset": "II", "x": _x_common,
                      "y": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]}),
        pd.DataFrame({"dataset": "III", "x": _x_common,
                      "y": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]}),
        pd.DataFrame({"dataset": "IV", "x": [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
                      "y": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]}),
    ], ignore_index=True)
    anscombe.groupby("dataset").apply(
        lambda g: pd.Series({
            "mean_x": g["x"].mean(), "mean_y": g["y"].mean(),
            "std_x": g["x"].std(), "std_y": g["y"].std(),
            "correlation": g["x"].corr(g["y"]),
        }),
        include_groups=False,
    ).round(3)
    return (anscombe,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four datasets, and every summary statistic agrees: the same mean in x and y,
    the same standard deviations, and a correlation of 0.82 in all four. A report
    quoting those numbers would describe them as the same data.
    """)
    return


@app.cell
def _(anscombe, sns):
    _grid = sns.lmplot(
        data=anscombe, x="x", y="y", col="dataset", col_wrap=2,
        height=3, ci=None, line_kws={"color": "crimson"},
    )
    _grid.figure.suptitle("Anscombe's quartet, with the same fitted line on each", y=1.02)
    _grid.figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first is what the summary suggests. The second is a curve, so a straight
    line is the wrong model rather than a weak one. The third is a tight line
    with one point dragging the fit away from it. The fourth has no relationship
    at all, and its correlation comes entirely from a single point at x = 19.

    The correlation coefficient is the subject of notebook 05, and this is what
    to remember when you meet it: **it answers one narrow question about a
    straight line, and it cannot tell you whether a straight line was ever the
    right thing to fit.**

    ## Summary

    - skewness is negative for a left tail and positive for a right one, and its
      sign agrees with whether the mean sits below or above the median
    - a Q-Q plot compares your data against a normal distribution, and a curve
      away from the line at one end is a tail
    - a histogram distinguishes a smooth tail from a bell with a few far values,
      which no single number does
    - `pd.qcut` builds equal-sized groups from a numeric column, and `pd.cut`
      cuts at values you choose
    - grouped bars compare the pieces and stacked bars compare the totals
    - identical summary statistics can describe completely different data

    ## Next class

    **Notebook 05, data analysis II:** correlation properly, t-tests, ANOVA and
    linear models. Reading: Bruce, Bruce and Gedeck on statistical experiments
    and significance testing.

    ## Additional resources

    - [seaborn's categorical plots](https://seaborn.pydata.org/tutorial/categorical.html)
    - [scipy.stats.probplot](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html)
    - [The Datasaurus Dozen](https://www.research.autodesk.com/publications/same-stats-different-graphs/),
      which is Anscombe's point made thirteen times over
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded.

    **Try the quartet yourself.** Compute the mean of `y` for each dataset to
    three decimal places and see how far the agreement goes.

    **Build the shape table for the mystery data**, the way Part 1 did for the
    happiness columns, and see which of the six shapes the skew number alone
    would have let you name.

    **Re-cut the tiers with `pd.cut` instead of `pd.qcut`**, at scores of 4, 5
    and 6, and notice that the groups are no longer the same size, which changes
    what a proportion within each one means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Before you leave today.** In-class 04 is one deliverable covering both
    sessions, so upload **four files** in a single submission:

    1. `SI618_04a_<uniqname>.py` and `SI618_04a_<uniqname>.html` from Wednesday
    2. This notebook, renamed `SI618_04b_<uniqname>.py`, and its export:
       ```bash
       uvx marimo export html --sandbox SI618_04b_<uniqname>.py -o SI618_04b_<uniqname>.html
       ```

    ❗️ Late in-class work is not accepted for credit.
    """)
    return


if __name__ == "__main__":
    app.run()
