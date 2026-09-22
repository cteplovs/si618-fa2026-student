# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "matplotlib==3.11.1",
#     "seaborn==0.13.2",
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
        # SI 618 · 04a: data analysis I, describing one variable

        Dr. Chris Teplovs, University of Michigan School of Information

        **Fall 2026** · Session 7 (Wed Sep 23)

        Copyright © 2026. This notebook may not be shared outside of the course
        without permission. Notebook version 2026.09.22.1.CT

        ---

        ## Learning objectives

        By the end of today you will be able to:

        - Read `.describe()` and say what each of its eight rows means
        - Say what a mean above the median, or below it, tells you about a
          distribution
        - Choose between a histogram, a box plot and a KDE for a single column
        - Build all three with seaborn
        - Apply the 1.5 × IQR rule, and say what an outlier is and is not

        ## Pre-class reading

        McKinney, W. (2022). *Python for Data Analysis*, 3rd edition, chapter 9
        (Plotting and Visualization).

        ## How this notebook works

        **This file is today's session, start to finish.** It is shorter than the
        last three, and it is meant to be done and submitted before you leave.
        Monday is a new file.

        Four times today I will stop before running a cell and ask for a show of
        hands, and four times you will write code on your own. Nothing about a
        prediction is graded.
        """
    )
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

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    sns.set_theme(style="whitegrid")

    # seaborn 0.13 passes an argument matplotlib 3.11 has deprecated. The warning
    # is harmless and appears under every box plot, so it is silenced here.
    warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
    return mo, np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 1: One number cannot describe a distribution

        Notebook 03 ended with a histogram. This one starts by asking why you would
        bother, when `.mean()` is one character shorter to type.

        Here are the minutes a commute took on 24 working days.
        """
    )
    return


@app.cell
def _(pd):
    commute = pd.Series(
        [22, 25, 19, 31, 28, 24, 35, 27, 30, 26, 33, 21, 29, 38,
         23, 32, 26, 27, 34, 20, 95, 110, 28, 25],
        name="minutes",
    )
    commute
    return (commute,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔮 Predict before the next cell runs

        Look at those 24 values. Is the **mean** bigger than the **median**,
        smaller, or about the same? Decide before you scroll.
        """
    )
    return


@app.cell
def _(commute):
    commute.mean(), commute.median()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The mean is 33.7 minutes and the median is 27.5, so they sit more than six
        minutes apart, because two days out of twenty-four dragged the mean past a
        value that twenty of those days beat.

        The mean is not wrong, but it answers a question nobody asked, and the
        histogram below shows why.
        """
    )
    return


@app.cell
def _(commute, plt):
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.hist(commute, bins=12, edgecolor="black")
    _ax.axvline(
        commute.mean(), color="crimson", linestyle="--",
        label=f"mean = {commute.mean():.1f}",
    )
    _ax.axvline(
        commute.median(), color="navy", linestyle="--",
        label=f"median = {commute.median():.1f}",
    )
    _ax.set_xlabel("Commute (minutes)")
    _ax.set_ylabel("Number of days")
    _ax.set_title("Twenty-four commutes, and two of them")
    _ax.legend()
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 2: The data, and `.describe()`

        For the rest of today we use the World Happiness Report for 2019: one row
        per country, a happiness score from a survey, and six columns describing
        what contributes to that score. It is a frozen snapshot of a published
        report rather than a live feed, so these numbers will not move under you.
        """
    )
    return


@app.cell
def _():
    HAPPINESS_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/"
        "refs/heads/main/happiness_2019.csv"
    )
    return (HAPPINESS_URL,)


@app.cell
def _(HAPPINESS_URL, pd):
    happiness = pd.read_csv(HAPPINESS_URL)
    happiness.head()
    return (happiness,)


@app.cell
def _(happiness):
    happiness.shape, happiness.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Each row is one country.

        | Column | What it is |
        |---|---|
        | `rank` | position in the 2019 report, 1 is happiest |
        | `country` | country name |
        | `happiness_score` | the survey score itself, roughly 0–10 |
        | `gdp_per_capita` | how much income **contributes to** that score |
        | `social_support` | how much having someone to count on contributes |
        | `healthy_life_expectancy` | how much healthy life expectancy contributes |
        | `freedom` | how much freedom to make life choices contributes |
        | `generosity` | how much generosity contributes |
        | `corruption` | how much **low** perceived corruption contributes |

        ❗️ **`gdp_per_capita` is not GDP per capita.** The six factor columns are
        each that factor's estimated contribution to the happiness score, in the
        same units as the score, which is why they all sit between 0 and about 1.7.
        A sentence like "countries with a GDP per capita above 1.2" means nothing.
        Read a data dictionary before you write about a column.
        """
    )
    return


@app.cell
def _(happiness):
    happiness.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Those eight rows are worth knowing by name.

        - **`count`** is non-null values, not rows. If it differs between columns
          you have missing data, and you want to know that before you average
          anything.
        - **`mean`** and **`std`**: the average, and the typical distance from it.
        - **`min`** and **`max`**: the range.
        - **`25%`, `50%`, `75%`**: the quartiles. A quarter of the values fall
          below the first, half below the second, three quarters below the third.
          **`50%` is the median.**

        Four of those rows are quartiles, which is the shape of the distribution
        written as numbers and most of what a box plot draws.
        """
    )
    return


@app.cell
def _(happiness):
    score = happiness["happiness_score"]
    score.mean(), score.median()
    return (score,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The two numbers are 5.41 and 5.38, which is nearly identical and the
        opposite of what the commute data did.

        Here is a small function for the five numbers we keep coming back to,
        since we want them again four more times today.
        """
    )
    return


@app.cell
def _(pd, score):
    def summarise(s: "pd.Series") -> "pd.Series":
        """Return the five summary numbers this session keeps coming back to."""
        return pd.Series(
            {
                "mean": s.mean(),
                "median": s.median(),
                "std": s.std(),
                "min": s.min(),
                "max": s.max(),
            }
        ).round(3)

    summarise(score)
    return (summarise,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🚀 Exercise 1: read the summary

        The `freedom` column is how much freedom to make life choices contributes
        to each country's happiness score.

        ✅ Step 1: Assign its mean to `mean_freedom` and its median to
        `median_freedom`.

        ✅ Step 2: Assign its interquartile range, the 75th percentile minus the
        25th, to `iqr_freedom`.

        ✅ Step 3: Assign `True` or `False` to `mean_below_median`: is the mean the
        smaller of the two?
        """
    )
    return


@app.cell
def _():
    # Your code here.
    mean_freedom = None
    median_freedom = None
    iqr_freedom = None
    mean_below_median = None
    return iqr_freedom, mean_below_median, mean_freedom, median_freedom


@app.cell(hide_code=True)
def _(iqr_freedom, mean_below_median, mean_freedom, median_freedom):
    def test_exercise_1():
        assert mean_freedom is not None, "Assign the mean to `mean_freedom`."
        assert round(float(mean_freedom), 3) == 0.393, (
            f"Expected 0.393, got {mean_freedom}. Take the mean of the `freedom` "
            "column on its own, not of the whole DataFrame."
        )
        assert median_freedom is not None, "Assign the median to `median_freedom`."
        assert round(float(median_freedom), 3) == 0.417, (
            f"Expected 0.417, got {median_freedom}. `.median()`, or `.quantile(0.5)`."
        )
        assert iqr_freedom is not None, "Assign the range to `iqr_freedom`."
        assert round(float(iqr_freedom), 3) == 0.199, (
            f"Expected 0.199, got {iqr_freedom}. That is .quantile(0.75) minus "
            ".quantile(0.25), not max minus min."
        )
        assert mean_below_median is True, (
            f"Got {mean_below_median!r}. Compare the two numbers you just computed. "
            "This column leans the opposite way from the commute data."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The commute's mean sat **above** its median, and `freedom`'s sits
        **below**. That one comparison tells you which way a distribution leans,
        and on Monday it gets a name.

        ---
        ## Part 3: Histograms, and the bins argument

        A histogram cuts the range into bins and counts what lands in each.
        Notebook 03 said too few bins hides the shape and too many turns it into
        noise. Drag the slider and watch what that costs you.
        """
    )
    return


@app.cell
def _(mo):
    bins_slider = mo.ui.slider(4, 60, value=20, step=2, label="Number of bins")
    bins_slider
    return (bins_slider,)


@app.cell
def _(bins_slider, plt, score):
    _fig, _ax = plt.subplots(figsize=(9, 5))
    _ax.hist(score, bins=bins_slider.value, edgecolor="black")
    _ax.set_xlabel("Happiness score")
    _ax.set_ylabel("Number of countries")
    _ax.set_title(f"World happiness, 2019 — {bins_slider.value} bins")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        At four bins it is a featureless mound, at twenty a single broad hump a
        little above 5, and past about forty-four it breaks into teeth that are
        sampling noise from 156 rows rather than anything about the world.

        No number of bins is correct, though some show the shape without inventing
        detail, and you find those by looking. Twenty to thirty is sensible for 156
        rows.

        ---
        ## Part 4: The same plot, in seaborn

        matplotlib will draw anything, given enough lines. **seaborn** sits on top
        of it, already knows what a distribution plot looks like, and reads columns
        out of a DataFrame by name.

        It is the same figure underneath: `sns.histplot` returns a matplotlib axes,
        which is why the cell still ends the same way.
        """
    )
    return


@app.cell
def _(happiness, sns):
    _ax = sns.histplot(data=happiness, x="happiness_score", bins=20, kde=True)
    _ax.set_xlabel("Happiness score")
    _ax.set_ylabel("Number of countries")
    _ax.set_title("World happiness, 2019")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Two things to take from that cell.

        **`data=` and `x=` is the seaborn habit.** You name the frame and the
        column rather than pulling out a Series. Every seaborn call today looks
        like that.

        **The smooth curve is a KDE**, which is a smoothed version of the same
        histogram without the bin edges. Part 6 uses it properly.

        ### 🚀 Exercise 2: plot a different column

        `social_support` is how much having someone to count on contributes to a
        country's happiness score.

        ✅ Step 1: Build a seaborn histogram of `social_support` with **20 bins**,
        and assign the axes it returns to `ax_hist`.

        ✅ Step 2: Give it an x-axis label and a title, in words a reader would
        understand. End the cell with `ax_hist` so marimo draws it.
        """
    )
    return


@app.cell
def _():
    # Your code here. End the cell with `ax_hist`.
    ax_hist = None
    return (ax_hist,)


@app.cell(hide_code=True)
def _(ax_hist):
    def test_exercise_2():
        assert ax_hist is not None, (
            "Assign the result of your seaborn call to `ax_hist`."
        )
        assert hasattr(ax_hist, "patches"), (
            f"`ax_hist` is a {type(ax_hist).__name__}. sns.histplot returns the "
            "axes, so assign that rather than the DataFrame or the figure."
        )
        assert len(ax_hist.patches) == 20, (
            f"Expected 20 bars, found {len(ax_hist.patches)}. Pass bins=20."
        )
        assert ax_hist.get_xlabel().strip() != "", (
            "The x-axis has no label. `ax_hist.set_xlabel(...)`, in words rather "
            "than the column name."
        )
        assert ax_hist.get_title().strip() != "", (
            "No title. `ax_hist.set_title(...)` — a reader should know what they "
            "are looking at without asking you."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 5: Box plots, and the 1.5 × IQR rule

        A box plot draws four of the eight rows of `.describe()` and adds a rule
        about what counts as unusual.

        - the **box** spans the 25th to the 75th percentile
        - the **line** inside it is the median
        - the **whiskers** reach the furthest point within 1.5 × IQR of the box
        - anything past a whisker is drawn as **its own dot**

        ### 🔮 Predict before the next cell runs

        It box-plots the happiness score for all 156 countries. How many dots will
        there be? **A.** none **B.** two or three **C.** ten or more
        """
    )
    return


@app.cell
def _(happiness, sns):
    _ax = sns.boxplot(data=happiness, y="happiness_score")
    _ax.set_ylabel("Happiness score")
    _ax.set_title("Happiness scores, all 156 countries")
    _ax
    return


@app.cell
def _(score):
    q1_score = score.quantile(0.25)
    q3_score = score.quantile(0.75)
    iqr_score = q3_score - q1_score
    lower_fence = q1_score - 1.5 * iqr_score
    upper_fence = q3_score + 1.5 * iqr_score
    q1_score, q3_score, iqr_score, lower_fence, upper_fence
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        There are no dots at all, because the fences sit at 2.08 and 8.64 while
        the data runs from 2.853 to 7.769, so South Sudan at the bottom and Finland
        at the top both fall comfortably inside.

        **Finland is not an outlier**, but the highest value in a distribution wide
        enough to accommodate it, since the word describes the output of one
        subtraction and one multiplication rather than a judgement about a
        country.

        ### 🔮 Predict before the next cell runs

        Now `corruption`, which is how much **low** perceived corruption
        contributes to happiness, so a high value means a cleaner government. This
        column does have outliers. Are they at the **low** end or the **high** end?
        """
    )
    return


@app.cell
def _(happiness, sns):
    _ax = sns.boxplot(data=happiness, y="corruption")
    _ax.set_ylabel("Corruption (contribution to happiness score)")
    _ax.set_title("Perceived corruption — same plot, different shape")
    _ax
    return


@app.cell
def _(happiness):
    happiness.nlargest(6, "corruption")[["country", "corruption"]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Fourteen countries sit above the upper fence and none below, because most
        of the world clusters near zero on this measure while a handful of
        unusually clean governments trail off above it.

        The plot and the code are the same as the previous one, and an outlier here
        means *notably good*. On Monday this shape gets its name.

        ### 🚀 Exercise 3: which commutes were the unusual ones?

        Back to `commute`, the 24 days from Part 1. Do by hand what the box plot
        does for you.

        ✅ Step 1: Assign the 25th and 75th percentiles to `q1_commute` and
        `q3_commute`, and their difference to `iqr_commute`.

        ✅ Step 2: Assign the upper fence, Q3 + 1.5 × IQR, to `commute_upper`.

        ✅ Step 3: Assign how many days lie above that fence to
        `n_commute_outliers`.
        """
    )
    return


@app.cell
def _():
    # Your code here.
    q1_commute = None
    q3_commute = None
    iqr_commute = None
    commute_upper = None
    n_commute_outliers = None
    return commute_upper, iqr_commute, n_commute_outliers, q1_commute, q3_commute


@app.cell(hide_code=True)
def _(commute_upper, iqr_commute, n_commute_outliers, q1_commute, q3_commute):
    def test_exercise_3():
        assert q1_commute is not None, "Assign the 25th percentile to `q1_commute`."
        assert float(q1_commute) == 24.75, (
            f"Expected 24.75, got {q1_commute}. `.quantile(0.25)` — a quantile "
            "takes a fraction, not 25."
        )
        assert q3_commute is not None, "Assign the 75th percentile to `q3_commute`."
        assert float(q3_commute) == 32.25, (
            f"Expected 32.25, got {q3_commute}. `.quantile(0.75)`."
        )
        assert iqr_commute is not None, "Assign the difference to `iqr_commute`."
        assert float(iqr_commute) == 7.5, (
            f"Expected 7.5, got {iqr_commute}. Q3 minus Q1."
        )
        assert commute_upper is not None, "Assign the upper fence to `commute_upper`."
        assert float(commute_upper) == 43.5, (
            f"Expected 43.5, got {commute_upper}. Q3 + 1.5 * IQR — the 1.5 "
            "multiplies the IQR, not Q3."
        )
        assert n_commute_outliers is not None, (
            "Assign the count to `n_commute_outliers`."
        )
        assert int(n_commute_outliers) == 2, (
            f"Expected 2, got {n_commute_outliers}. Compare the Series to the "
            "fence and sum the result: a boolean Series sums to its number of Trues."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The fence lands at 43.5 minutes, so a 44-minute commute would have been
        flagged even though nothing unusual happened that day, which makes the rule
        a convention rather than a verdict.

        ---
        ## Part 6: KDE, and comparing two groups

        A KDE replaces each observation with a small bump and adds them up, giving
        a smooth curve with no bin edges to argue about. The height is density
        rather than count, and the area under the whole curve is 1.

        It is most useful when you want two distributions on one pair of axes,
        since two histograms drawn on top of each other are hard to read while two
        KDEs are not.
        """
    )
    return


@app.cell
def _(happiness, np):
    gdp_median = happiness["gdp_per_capita"].median()
    happiness_groups = happiness.assign(
        gdp_group=np.where(
            happiness["gdp_per_capita"] >= gdp_median, "Higher GDP", "Lower GDP"
        )
    )
    gdp_median, happiness_groups["gdp_group"].value_counts()
    return (happiness_groups,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Splitting at the median guarantees two groups of roughly equal size, 80 and
        76 here, which makes the comparison fair, since neither group is a handful
        of countries someone picked.

        ### 🔮 Predict before the next cell runs

        Two curves, the richer half and the poorer half. Will they be **A.** almost
        entirely separate, **B.** overlapping but clearly shifted, or **C.** more
        or less on top of each other?
        """
    )
    return


@app.cell
def _(happiness_groups, sns):
    _ax = sns.kdeplot(
        data=happiness_groups,
        x="happiness_score",
        hue="gdp_group",
        fill=True,
        alpha=0.4,
        linewidth=2,
    )
    _ax.set_xlabel("Happiness score")
    _ax.set_ylabel("Density")
    _ax.set_title("Happiness by GDP contribution, split at the median")
    _ax
    return


@app.cell
def _(happiness_groups):
    happiness_groups.groupby("gdp_group")["happiness_score"].agg(
        ["count", "mean", "median"]
    ).round(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The means differ by 1.46, and the curves still overlap across most of
        their width.

        The means alone would let you write "richer countries are happier" and
        stop, whereas the picture makes you add "on average, with plenty of
        exceptions in both directions", which is a different and more honest
        claim.

        ---
        ## Part 7: Three views of one column

        Each of these hides what the others show: the histogram gives shape and
        count without a summary, the box plot gives the summary without telling you
        whether the distribution has one hump or two, and the strip plot gives
        every country and nothing else.
        """
    )
    return


@app.cell
def _(happiness, plt, sns):
    _fig, _axes = plt.subplots(1, 3, figsize=(15, 4.5))
    sns.histplot(data=happiness, x="happiness_score", bins=20, ax=_axes[0])
    _axes[0].set_title("Histogram: shape")
    sns.boxplot(data=happiness, y="happiness_score", ax=_axes[1])
    _axes[1].set_title("Box plot: summary")
    sns.stripplot(data=happiness, y="happiness_score", size=3, jitter=0.25, ax=_axes[2])
    _axes[2].set_title("Strip plot: every country")
    _fig.suptitle("One column, three views", fontweight="bold")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        A short decision list, for the rest of the term:

        | You want to see | Reach for |
        |---|---|
        | the shape of one column | a histogram |
        | quartiles and outliers | a box plot |
        | two or more groups on one pair of axes | a KDE |
        | small data where every point matters | a strip plot |

        ### 🚀 Exercise 4: one sentence

        Scroll back to any plot in this notebook and write one sentence about what
        it shows that its summary statistics do not. Assign it to `observation`,
        as a string.

        Full marks for a real sentence in your own words. There is no correct
        answer here.
        """
    )
    return


@app.cell
def _():
    observation = ""
    return (observation,)


@app.cell(hide_code=True)
def _(observation):
    def test_exercise_4():
        assert isinstance(observation, str), (
            "`observation` should be a string, in quotes."
        )
        assert len(observation.strip()) >= 40, (
            f"That is {len(observation.strip())} characters. One full sentence in "
            "your own words — this is read for a real attempt, not a right answer."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Summary

        - `.describe()` is eight numbers, four of which are quartiles, and `50%`
          is the median
        - a mean above the median, or below it, tells you which way a distribution
          leans
        - the number of histogram bins is a choice you make by looking
        - the 1.5 × IQR rule is arithmetic rather than judgement, and an outlier
          can be notably good
        - `data=` and `x=` is how seaborn is called
        - a KDE puts two groups on one pair of axes

        ## Next class

        **04b, on Monday.** The name for the shapes we kept pointing at, Q-Q plots,
        comparing categories with bar charts, and a first look at two variables at
        once. It is a **new file**, and this one is finished today.

        ## Additional resources

        - [seaborn tutorial](https://seaborn.pydata.org/tutorial.html)
        - [Distribution plots in seaborn](https://seaborn.pydata.org/tutorial/distributions.html)
        - [From Data to Viz](https://www.data-to-viz.com), for choosing a plot
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🏁 END OF NOTEBOOK

        **Before you leave today.** Two files, both to Canvas, under **In-class 04**:

        1. This notebook, renamed `SI618_04a_<uniqname>.py`
        2. An HTML export of it:
           ```bash
           uvx marimo export html --sandbox SI618_04a_<uniqname>.py -o SI618_04a_<uniqname>.html
           ```

        ❗️ **Keep both files.** In-class 04 is one deliverable covering today and
        Monday. On Monday you will upload all four files together, today's two and
        Monday's two, in a single submission.
        """
    )
    return


if __name__ == "__main__":
    app.run()
