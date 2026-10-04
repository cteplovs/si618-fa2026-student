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
    # SI 618 - 05b: correlation and linear regression

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 10 (Mon Oct 5)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.09.29.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Measure the strength of a relationship with Pearson's and Spearman's
      correlation, and say when the two disagree
    - Fit a linear regression with `statsmodels`, and read its slope, intercept
      and R-squared
    - Explain why a slope estimated from a small sample can land far from the
      slope in the population
    - Add predictors to a regression, including categorical ones, and read each
      coefficient as an effect with the other predictors held constant

    ## Pre-class reading

    Bruce, P., Bruce, A. and Gedeck, P. (2020). *Practical Statistics for Data
    Scientists*, 2nd edition, chapter 4 (Regression and Prediction).

    ## How this notebook works

    **This file is today's session, start to finish**, and it is the second half
    of In-class 05. Wednesday's file was 05a, and at the end of today you upload
    both notebooks together.

    As on Wednesday, both exercises give each of you a slightly different
    version of the same question, and the room's answers, put together by a
    show of hands, show something that no single notebook can. You are welcome
    to compare results with the people around you, although nothing you are
    graded on depends on it.

    ✅ **Before anything else, please type your uniqname below**, because it chooses
    your sample in Exercise 1 and your predictor in Exercise 2.
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
    import statsmodels.formula.api as smf

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    sns.set_theme(style="whitegrid")

    warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
    return mo, np, pd, plt, smf, sns, zlib


@app.cell
def _(pd):
    INSURANCE_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/"
        "main/insurance.csv"
    )
    insurance = pd.read_csv(INSURANCE_URL)
    insurance.head()
    return (insurance,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is Wednesday's data: one row per person with US medical insurance, and
    `charges`, the medical costs billed to their insurer in one year, in
    dollars. On Wednesday you compared groups, and today the question is how
    charges change along a numeric column such as age.

    ---
    ## Part 1: Correlation

    The scatterplot comes first, because, as Anscombe's quartet showed in 04b,
    one correlation coefficient can describe very different data.
    """)
    return


@app.cell
def _(insurance, sns):
    _ax = sns.scatterplot(data=insurance, x="age", y="charges", alpha=0.5)
    _ax.set_xlabel("Age")
    _ax.set_ylabel("Annual charges ($)")
    _ax.set_title("Charges rise with age, in three bands")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Charges rise with age, but the points form three separate bands rather than
    one cloud, which is worth remembering for the vote below.

    A **correlation coefficient** summarises how closely two columns move
    together, on a scale from -1 to 1. **Pearson's** correlation, the default in
    pandas, measures how close the points come to a straight line, whereas
    **Spearman's** correlation ranks both columns first and measures how
    consistently one rises with the other, whether or not it does so along a
    straight line.
    """)
    return


@app.cell
def _(insurance, pd):
    _columns = ["age", "bmi", "children", "charges"]
    pd.DataFrame({
        "pearson": insurance[_columns].corr()["charges"],
        "spearman": insurance[_columns].corr(method="spearman")["charges"],
    }).drop("charges").round(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For age, Pearson's correlation is 0.30 and Spearman's is 0.53. The two
    disagree because charges are right-skewed, as they were on Wednesday, and
    the few very large values sit well away from any straight line even though
    they follow the same upward order. When the two coefficients differ this
    much, the relationship is consistent but not linear, or it is being pulled
    by extreme values, and in either case you should look at the scatterplot
    before quoting either number.

    ---
    ## Part 2: Fitting a line

    A **linear regression** finds the straight line that comes closest to the
    points, in the sense of making the squared vertical distances from the
    points to the line as small as possible. `statsmodels` takes the model as
    a formula, with the outcome on the left of the `~` and the predictors on
    the right.
    """)
    return


@app.cell
def _(insurance, smf):
    age_model = smf.ols("charges ~ age", data=insurance).fit()
    age_model.params.round(1)
    return (age_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The line is `charges = 3,166 + 258 * age`. The **slope**, 258, says that
    each additional year of age goes with about $258 more in annual charges,
    and the **intercept**, 3,166, is the line's value at age zero. Since
    nobody in the data is that young, the intercept sets the height of the
    line rather than describing anyone.

    **R-squared** is the share of the variation in charges that the line
    accounts for.
    """)
    return


@app.cell
def _(age_model):
    round(age_model.rsquared, 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Age accounts for about 9% of the variation in charges, which leaves 91%
    unexplained, despite the upward trend visible in the plot.

    ---
    ### Vote: non-smokers only
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    first_vote = mo.ui.radio(
        options=["Higher than 9%", "About the same", "Lower than 9%"],
        label="**First vote.** If we fit the same line to non-smokers only, will age account for more or less of the variation in their charges?",
    )
    first_vote
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Please vote in the notebook, and with your hand when asked, then take a
    minute to tell the person next to you which way you voted and why, looking
    at the three bands in the scatterplot, and vote again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    second_vote = mo.ui.radio(
        options=["Higher than 9%", "About the same", "Lower than 9%"],
        label="**Second vote**, after talking it over.",
    )
    reveal = mo.ui.run_button(label="Reveal the non-smokers' R-squared")
    mo.vstack([second_vote, reveal])
    return (reveal,)


@app.cell
def _(insurance, mo, reveal, smf):
    mo.stop(not reveal.value, mo.md("*Press the button once you have voted twice.*"))
    _non_smokers = insurance[insurance["smoker"] == "no"]
    _model = smf.ols("charges ~ age", data=_non_smokers).fit()
    {"slope": round(_model.params["age"], 1), "r_squared": round(_model.rsquared, 3)}
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Among non-smokers, age accounts for 39% of the variation rather than 9%,
    with almost the same slope. The bottom band in the scatterplot is the
    non-smokers, and the two upper bands are smokers, whose charges are higher
    by an amount that has nothing to do with age. A single line fitted through
    all three bands mixes a strong relationship with age together with a large
    difference that the model does not include, and Part 3 shows how to add
    that difference as a second predictor.

    ---
    ### 🚀 Exercise 1: the slope in a sample of 40

    As on Wednesday, treat the 1,338 people as a population, from which
    `my_sample(n)` draws `n` people with replacement, seeded by your uniqname.

    ✅ Step 1: Fit `charges ~ age` to `my_sample(40)`, and assign its slope, as
    a float, to `my_slope`.

    ✅ Step 2: When asked, raise your hand if your slope is below $100, and
    then if it is above $400.

    ✅ Step 3: Assign to `slope_sentence` two or three sentences on what the
    hands showed. The full data gives a slope of $258, so say how far a sample
    of 40 can land from it, and what that implies for a slope that somebody
    reports from a small sample.
    """)
    return


@app.cell
def _(UNIQNAME, insurance, mo, zlib):
    mo.stop(
        not UNIQNAME.strip(),
        mo.md("⚠️ Type your uniqname into `UNIQNAME` at the top of the notebook."),
    )
    my_seed = zlib.crc32(UNIQNAME.strip().lower().encode())

    def my_sample(n: int):
        """Draw n people from `insurance`, with replacement, seeded by your uniqname."""
        return insurance.sample(n, replace=True, random_state=my_seed)

    return my_sample, my_seed


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_slope = None
    slope_sentence = ""
    return my_slope, slope_sentence


@app.cell(hide_code=True)
def _(insurance, my_seed, my_slope, slope_sentence, smf):
    def test_exercise_1():
        _df = insurance.sample(40, replace=True, random_state=my_seed)
        _expected = smf.ols("charges ~ age", data=_df).fit().params["age"]
        assert my_slope is not None, "Assign your slope to `my_slope`."
        assert abs(float(my_slope) - _expected) < 1e-6, (
            f"`my_slope` is {my_slope}. Fit `charges ~ age` to `my_sample(40)` "
            "and take `.params['age']`, rather than the intercept or R-squared."
        )
        assert len(slope_sentence.strip()) >= 100, (
            f"`slope_sentence` is {len(slope_sentence.strip())} characters, where "
            "an account of the hands and what they imply is expected."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The regression output measures that spread. The **standard error**
    of the slope estimates how far a slope from a sample this size typically
    lands from the population's, and the confidence interval is roughly the
    slope plus or minus two standard errors.
    """)
    return


@app.cell
def _(age_model, pd):
    pd.DataFrame({
        "slope": age_model.params,
        "std_error": age_model.bse,
        "ci_low": age_model.conf_int()[0],
        "ci_high": age_model.conf_int()[1],
    }).round(1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With all 1,338 people, the standard error of the slope is about $23 and the
    confidence interval runs from about $214 to $302. With 40 people it is
    several times wider, which is what the room's hands showed.

    ---
    ## Part 3: More than one predictor

    A formula can take several predictors, joined by `+`, and the cell below
    adds body mass index to age.
    """)
    return


@app.cell
def _(insurance, smf):
    age_bmi_model = smf.ols("charges ~ age + bmi", data=insurance).fit()
    {
        "params": age_bmi_model.params.round(1).to_dict(),
        "r_squared": round(age_bmi_model.rsquared, 3),
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each coefficient is now read with the other predictor **held constant**.
    The age coefficient, about 242, says that between two people with the same
    BMI, the one a year older is billed about $242 more, and the BMI
    coefficient, about 333, says that between two people of the same age, each
    extra point of BMI goes with about $333 more. Adding BMI raises R-squared
    only from 0.089 to 0.117.

    A categorical predictor such as `sex` goes into the formula the same way.
    `statsmodels` turns it into a 0/1 column for every category except the
    first in alphabetical order, which becomes the **reference**, so the
    coefficient named `sex[T.male]` is the difference between men and women
    with age held constant.
    """)
    return


@app.cell
def _(insurance, smf):
    smf.ols("charges ~ age + sex", data=insurance).fit().params.round(1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Men are billed about $1,539 more than women of the same age, which is close
    to the $1,390 difference you tested on Wednesday.

    ---
    ### 🚀 Exercise 2: which predictor matters most?

    Your uniqname has assigned you one predictor to add to age, shown below as
    `my_predictor`: one of `bmi`, `children`, `sex` or `smoker`.

    ✅ Step 1: Fit `charges ~ age + <your predictor>` to the full `insurance`
    table, and assign its R-squared to `my_r_squared`.

    ✅ Step 2: Assign to `my_coefficient` the coefficient of your predictor, as
    a float. For `sex` and `smoker`, its name in `.params` ends in a
    `[T.<category>]` suffix like the one above, so look at `.params` before you
    pick it out.

    ✅ Step 3: When asked, the room will raise hands by predictor, and then
    everyone whose R-squared is above 0.5 will keep a hand up.

    ✅ Step 4: Assign to `predictor_sentence` two or three sentences saying what
    your coefficient means, with age held constant, and which predictor the
    room's hands showed to matter most, and relate that to the three bands in
    the scatterplot.
    """)
    return


@app.cell
def _(my_seed):
    my_predictor = ["bmi", "children", "sex", "smoker"][(my_seed // 4) % 4]
    my_predictor
    return (my_predictor,)


@app.cell
def _():
    # Your code here.
    my_r_squared = None
    my_coefficient = None
    predictor_sentence = ""
    return my_coefficient, my_r_squared, predictor_sentence


@app.cell(hide_code=True)
def _(
    insurance,
    my_coefficient,
    my_predictor,
    my_r_squared,
    predictor_sentence,
    smf,
):
    def test_exercise_2():
        _model = smf.ols(f"charges ~ age + {my_predictor}", data=insurance).fit()
        _name = [_p for _p in _model.params.index if _p.startswith(my_predictor)][0]
        assert my_r_squared is not None, "Assign the model's R-squared to `my_r_squared`."
        assert abs(float(my_r_squared) - _model.rsquared) < 1e-6, (
            f"`my_r_squared` is {my_r_squared}. Fit `charges ~ age + {my_predictor}` "
            "to the full `insurance` table and take `.rsquared`."
        )
        assert my_coefficient is not None, "Assign your predictor's coefficient to `my_coefficient`."
        assert abs(float(my_coefficient) - _model.params[_name]) < 1e-6, (
            f"`my_coefficient` is {my_coefficient}. Your predictor's coefficient is "
            f"the one named {_name!r} in `.params`, not the one for age."
        )
        assert len(predictor_sentence.strip()) >= 100, (
            f"`predictor_sentence` is {len(predictor_sentence.strip())} characters, "
            "where the coefficient, the room's answer and the bands are expected."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - Pearson's correlation measures closeness to a straight line and
      Spearman's measures consistent order, so a large gap between them points
      to skew, extreme values or a curve
    - `smf.ols("y ~ x", data=df).fit()` fits a linear regression, and
      `.params`, `.rsquared` and `.bse` give its coefficients, its R-squared and
      the standard errors of its coefficients
    - a slope from a small sample can land a long way from the population's,
      and its standard error says how far
    - with several predictors, each coefficient is an effect with the others
      held constant, and a categorical predictor's coefficient is a difference
      from its reference category
    - one missing predictor can hide a strong relationship, as smoking hid most
      of age's

    ## Next class

    **Notebook 06a, data analysis III:** contingency tables and the chi-square
    test. The reading is the chi-square section of chapter 3 of Bruce, Bruce
    and Gedeck.

    ## Additional resources

    - [statsmodels formulas](https://www.statsmodels.org/stable/example_formulas.html)
    - [Seeing Theory: regression](https://seeing-theory.brown.edu/regression-analysis/index.html),
      an interactive visual introduction
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded, and it is meant for anyone who finishes early or
    wants more afterwards.

    **Separate the two smoker bands.** Fit `charges ~ age + bmi * smoker`,
    where `*` adds both predictors and their **interaction**, which lets the
    effect of BMI differ between smokers and non-smokers. R-squared rises to
    about 0.84, and the interaction coefficient says how much more each point
    of BMI costs a smoker than a non-smoker.

    **Plot the residuals** of `age_model` against age, using `.resid`. If the
    line were a good model, they would form a formless band around zero, and
    the three bands you will see instead are the same ones as in the first
    scatterplot.

    **Repeat Exercise 1 a thousand times** with seeds 0 to 999, and compare the
    standard deviation of the thousand slopes with the standard error that
    `statsmodels` reports for a single sample of 40.
    """)
    return


@app.cell(hide_code=True)
def _(UNIQNAME, mo):
    _name = UNIQNAME.strip().lower() or "<uniqname>"
    mo.md(rf"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Before you leave today.** In-class 05 is one deliverable covering both
    sessions, so upload **four files** in a single submission:

    1. `SI618_05a_{_name}.py` and `SI618_05a_{_name}.html` from Wednesday
    2. This notebook, renamed `SI618_05b_{_name}.py`, and its export:
       ```bash
       uvx marimo export html --sandbox SI618_05b_{_name}.py -o SI618_05b_{_name}.html
       ```

    ❗️ Late in-class work is not accepted for credit.
    """)
    return


if __name__ == "__main__":
    app.run()
