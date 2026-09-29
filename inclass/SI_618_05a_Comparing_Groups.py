# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "matplotlib==3.11.1",
#     "seaborn==0.13.2",
#     "scipy==1.18.1",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 618 - 05a: comparing groups, and what "significant" means

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 9 (Wed Sep 30)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.09.29.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Compare the means of two groups with Welch's t-test, and say what its
      p-value does and does not tell you
    - Explain why the same difference can be significant in a large sample and
      not in a small one
    - Compare three or more groups with a one-way ANOVA, and find which groups
      differ with Tukey's HSD
    - Distinguish a difference that is statistically significant from one that
      is large enough to matter

    ## Pre-class reading

    Bruce, P., Bruce, A. and Gedeck, P. (2020). *Practical Statistics for Data
    Scientists*, 2nd edition, chapter 3 (Statistical Experiments and
    Significance Testing).

    ## How this notebook works

    **This file is today's session, start to finish**, and it is the first half
    of In-class 05. Monday's file will be 05b, and you submit both together at
    the end of Monday's session.

    Both exercises today give each of you a slightly different version of the
    same question, and the room's answers, put together by a show of hands,
    tell you something that no single notebook can. You are welcome to compare
    results with the people around you as you go, although nothing you are
    graded on depends on it.

    ✅ **Before anything else, type your uniqname below**, because it chooses
    your sample in Exercise 1 and your region in Exercise 2.
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

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 20)
    sns.set_theme(style="whitegrid")

    warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
    return mo, np, pd, sns, stats, zlib


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
    Each row is one person with US medical insurance: their age, sex, body mass
    index, number of children, whether they smoke, the region of the country
    they live in, and `charges`, the medical costs billed to their insurer in
    one year, in dollars.

    ---
    ## Part 1: Two groups

    Here are the mean charges for smokers and non-smokers.
    """)
    return


@app.cell
def _(insurance):
    insurance.groupby("smoker")["charges"].agg(["count", "mean", "median", "std"]).round(0)
    return


@app.cell
def _(insurance, sns):
    _ax = sns.boxplot(data=insurance, x="smoker", y="charges")
    _ax.set_xlabel("Smoker")
    _ax.set_ylabel("Annual charges ($)")
    _ax.set_title("Smokers are billed far more than non-smokers")
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Smokers are billed nearly four times as much on average, and the two boxes
    barely overlap. The question a **t-test** answers is narrower than "are
    these different?": it asks how surprising a difference this large would be
    if smoking made no difference at all and the two groups were really one
    population split at random.

    `stats.ttest_ind` takes the two groups as separate arrays. Passing
    `equal_var=False` makes it **Welch's t-test**, which does not assume that
    the two groups have the same spread; since smokers' charges vary much more
    than non-smokers', that is the version to use here, and it is a sensible
    default in general.
    """)
    return


@app.cell
def _(insurance, stats):
    _smokers = insurance.loc[insurance["smoker"] == "yes", "charges"]
    _non_smokers = insurance.loc[insurance["smoker"] == "no", "charges"]
    stats.ttest_ind(_smokers, _non_smokers, equal_var=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result has two numbers that matter. The **statistic**, about 32.8, is
    the difference in means measured in units of its own uncertainty, so a
    value that far from zero says the difference is many times larger than
    sampling noise would produce. The **p-value**, about `6e-103`, is the
    probability of seeing a difference at least this large if there were no
    real difference, and a value that small means that chance is not a
    plausible explanation.

    A p-value below 0.05 is conventionally called **statistically
    significant**. That threshold is a convention, like the skewness cut-offs
    on Monday, and a p-value is not the probability that the groups are the
    same.

    You may remember from 04b that charges are right-skewed, which a t-test is
    supposed to mind. With samples in the hundreds, the mean of each group is
    close to normally distributed even when the individual values are not, and
    that is what the test relies on. With a dozen people per group, the skew
    would matter more.

    ---
    ### Vote: men and women

    The next comparison is less obvious.
    """)
    return


@app.cell
def _(insurance):
    insurance.groupby("sex")["charges"].agg(["count", "mean", "std"]).round(0)
    return


@app.cell(hide_code=True)
def _(mo):
    first_vote = mo.ui.radio(
        options=["Yes, p < 0.05", "No, p >= 0.05", "Not sure"],
        label="**First vote.** Men are billed about $1,390 more than women on average. Is that difference statistically significant?",
    )
    first_vote
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vote in the notebook and with your hand when asked. Then take a minute to
    tell the person next to you which way you voted and why, and vote again.
    Nothing here is graded, and changing your mind is the point of the second
    vote.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    second_vote = mo.ui.radio(
        options=["Yes, p < 0.05", "No, p >= 0.05", "Not sure"],
        label="**Second vote**, after talking it over.",
    )
    reveal = mo.ui.run_button(label="Reveal the t-test")
    mo.vstack([second_vote, reveal])
    return (reveal,)


@app.cell
def _(insurance, mo, reveal, stats):
    mo.stop(not reveal.value, mo.md("*Press the button once you have voted twice.*"))
    _men = insurance.loc[insurance["sex"] == "male", "charges"]
    _women = insurance.loc[insurance["sex"] == "female", "charges"]
    stats.ttest_ind(_men, _women, equal_var=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The p-value is about 0.036, which is below 0.05, so by the convention the
    difference is significant. Whether it is **large** is a separate question,
    and the standard deviations in the table above answer it: charges vary by
    between $11,000 and $13,000 from person to person within each sex, so a
    difference of $1,390 between the averages is roughly a tenth of that
    spread.

    Dividing the difference in means by the typical spread gives a measure of
    size called **Cohen's d**, which, unlike a p-value, does not grow with the
    number of people you have.
    """)
    return


@app.cell
def _(insurance, np):
    def cohens_d(a, b) -> float:
        """Difference in means divided by the pooled standard deviation."""
        _pooled = np.sqrt((a.var() * (len(a) - 1) + b.var() * (len(b) - 1)) / (len(a) + len(b) - 2))
        return (a.mean() - b.mean()) / _pooled

    _by_smoking = cohens_d(
        insurance.loc[insurance["smoker"] == "yes", "charges"],
        insurance.loc[insurance["smoker"] == "no", "charges"],
    )
    _by_sex = cohens_d(
        insurance.loc[insurance["sex"] == "male", "charges"],
        insurance.loc[insurance["sex"] == "female", "charges"],
    )
    {"smoking": round(_by_smoking, 2), "sex": round(_by_sex, 2)}
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Smoking separates the groups by more than three standard deviations, and
    sex by about a tenth of one. Both differences are significant, but only one
    of them is large, and a p-value alone could not have told you which.

    ---
    ### 🚀 Exercise 1: the same question in samples of different sizes

    Treat the 1,338 people in the file as a whole population, and draw samples
    from it. `my_sample(n)`, defined below, draws `n` people **with
    replacement**, which lets a sample be larger than the file, and your
    uniqname sets the random seed, so your samples differ from everyone else's
    while staying the same each time you run the notebook.

    ✅ Step 1: Write a function `sex_p_value(df)` that takes a DataFrame shaped
    like `insurance` and returns the p-value of Welch's t-test comparing men's
    and women's charges, as a float. Run on the full `insurance` table, it
    should give the 0.036 you saw above.

    ✅ Step 2: Assign to `p_by_size` a dictionary mapping each of the sample
    sizes 60, 600 and 6000 to the p-value of `sex_p_value(my_sample(n))`.

    ✅ Step 3: When asked, raise your hand for each sample size at which your
    p-value came out below 0.05, and note roughly how much of the room did the
    same.

    ✅ Step 4: Assign to `size_sentence` two or three sentences on what the
    hands showed. Everyone sampled the same population, with the same
    difference between men and women in it, so explain why some people's
    samples found that difference and others' did not, and what that implies
    for a p-value you get from a single sample.
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

    return (my_seed,)


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    def sex_p_value(df) -> float:
        return None

    p_by_size = {}
    size_sentence = ""
    return p_by_size, sex_p_value, size_sentence


@app.cell(hide_code=True)
def _(insurance, my_seed, p_by_size, sex_p_value, size_sentence, stats):
    def test_exercise_1():
        def _expected(n):
            _df = insurance.sample(n, replace=True, random_state=my_seed)
            return stats.ttest_ind(
                _df.loc[_df["sex"] == "male", "charges"],
                _df.loc[_df["sex"] == "female", "charges"],
                equal_var=False,
            ).pvalue

        _full = sex_p_value(insurance)
        assert _full is not None, "`sex_p_value` should return the p-value."
        assert abs(float(_full) - 0.0358) < 0.001, (
            f"On the full table `sex_p_value` gives {_full}, where 0.036 is expected. "
            "Check that you passed equal_var=False and returned `.pvalue`."
        )
        assert set(p_by_size) == {60, 600, 6000}, (
            f"`p_by_size` should have the keys 60, 600 and 6000 (as integers), "
            f"not {sorted(p_by_size)}."
        )
        for _n in (60, 600, 6000):
            assert abs(float(p_by_size[_n]) - _expected(_n)) < 1e-9, (
                f"Your p-value for n = {_n} does not match `my_sample({_n})`. "
                "Draw each sample with `my_sample` rather than `insurance.sample`."
            )
        assert len(size_sentence.strip()) >= 100, (
            f"`size_sentence` is {len(size_sentence.strip())} characters, where an "
            "explanation of the hands and what they imply is expected."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: More than two groups

    To compare more than two groups, you could run a t-test on every pair, but
    with four groups that is six tests, and each one carries a 5% chance of a
    false alarm, so the chance that at least one of them goes off by accident
    is far higher than 5%. The simplest remedy, the
    [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction),
    divides the threshold by the number of tests, so that each of six tests
    has to reach p < 0.05 / 6, or about 0.008, to count as significant.

    A **one-way ANOVA** avoids the problem by asking a single question of all
    the groups at once: is the variation between the group means larger than
    the variation within the groups would lead you to expect?

    Here is body mass index across the four regions.
    """)
    return


@app.cell
def _(insurance, sns):
    _ax = sns.boxplot(data=insurance, x="region", y="bmi")
    _ax.set_xlabel("Region")
    _ax.set_ylabel("Body mass index")
    _ax.set_title("BMI by region")
    _ax
    return


@app.cell
def _(insurance, stats):
    _groups = [_g["bmi"] for _, _g in insurance.groupby("region")]
    stats.f_oneway(*_groups)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The F statistic is 39.5 and the p-value is about `2e-24`, which is how
    Python writes `2 * 10**-24`, or 0.000000000000000000000002, with the 2 in the
    twenty-fourth decimal place. Together they say that the four regions do
    not share one mean BMI, although the ANOVA stops there and does not say
    which regions differ. **Tukey's HSD** compares every pair while adjusting
    for the number of comparisons, so that the six tests together keep a 5%
    false-alarm rate.
    """)
    return


@app.cell
def _(insurance, pd, stats):
    _names = sorted(insurance["region"].unique())
    _tukey = stats.tukey_hsd(*[insurance.loc[insurance["region"] == _r, "bmi"] for _r in _names])
    pd.DataFrame(
        [
            {
                "pair": f"{_names[_i]} vs {_names[_j]}",
                "difference": round(_tukey.statistic[_i, _j], 2),
                "p_value": round(_tukey.pvalue[_i, _j], 4),
            }
            for _i in range(4)
            for _j in range(_i + 1, 4)
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every pair that includes the southeast has a p-value near zero, with the
    southeast's mean BMI between 2.8 and 4.2 points higher than each of the
    others. The southwest also differs from both northern regions, by about 1.4
    points, while the northeast and northwest are indistinguishable, so behind
    the ANOVA's single verdict there are three levels rather than one region
    out of line.

    ---
    ### 🚀 Exercise 2: which region drives the difference in charges?

    Charges also differ by region, less dramatically. Your uniqname has
    assigned you one of the four regions, shown below as `my_region`.

    ✅ Step 1: Assign to `p_all_regions` the p-value of a one-way ANOVA of
    `charges` across all four regions.

    ✅ Step 2: Assign to `p_without_mine` the p-value of the same ANOVA with
    your region left out, so that it compares the other three.

    ✅ Step 3: When asked, the room will raise hands by region, and then
    everyone whose `p_without_mine` is still below 0.05 will keep a hand up.
    Look at which group of hands goes down.

    ✅ Step 4: Assign to `region_sentence` two or three sentences saying which
    region the room's hands point to, and whether the group means (from a
    `groupby` of your own) agree. Then say whether a significant ANOVA on its
    own would have told you that.
    """)
    return


@app.cell
def _(insurance, my_seed):
    my_region = sorted(insurance["region"].unique())[my_seed % 4]
    my_region
    return (my_region,)


@app.cell
def _():
    # Your code here.
    p_all_regions = None
    p_without_mine = None
    region_sentence = ""
    return p_all_regions, p_without_mine, region_sentence


@app.cell(hide_code=True)
def _(
    insurance,
    my_region,
    p_all_regions,
    p_without_mine,
    region_sentence,
    stats,
):
    def test_exercise_2():
        assert p_all_regions is not None, "Assign the four-region p-value to `p_all_regions`."
        assert abs(float(p_all_regions) - 0.0309) < 0.001, (
            f"`p_all_regions` is {p_all_regions}, where about 0.031 is expected. "
            "Pass one array of charges per region to `stats.f_oneway`."
        )
        _others = insurance[insurance["region"] != my_region]
        _expected = stats.f_oneway(
            *[_g["charges"] for _, _g in _others.groupby("region")]
        ).pvalue
        assert p_without_mine is not None, "Assign the three-region p-value to `p_without_mine`."
        assert abs(float(p_without_mine) - _expected) < 1e-6, (
            f"`p_without_mine` is {p_without_mine}. Leave out {my_region!r} and "
            "compare the other three regions."
        )
        assert len(region_sentence.strip()) >= 100, (
            f"`region_sentence` is {len(region_sentence.strip())} characters, where "
            "the region, the means and a word on the ANOVA are expected."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - Welch's t-test (`stats.ttest_ind(a, b, equal_var=False)`) compares two
      means without assuming equal spread
    - a p-value is the probability of a difference at least this large if
      there were no real difference, and below 0.05 is called significant by
      convention
    - the same real difference can fail to reach significance in a small sample
      and reach it easily in a large one, so significance depends on sample
      size as well as on the difference
    - an effect size such as Cohen's d says how large a difference is, which a
      p-value does not
    - a one-way ANOVA (`stats.f_oneway`) tests whether several group means are
      all equal, and Tukey's HSD (`stats.tukey_hsd`) says which pairs differ

    ## Next class

    **Notebook 05b:** correlation and linear regression, using the same
    insurance data. Reading: Bruce, Bruce and Gedeck, chapter 4 (Regression and
    Prediction).

    ## Additional resources

    - [scipy.stats.ttest_ind](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
    - [scipy.stats.tukey_hsd](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.tukey_hsd.html)
    - The American Statistical Association's
      [statement on p-values](https://doi.org/10.1080/00031305.2016.1154108)
      (2016), which is short and readable
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded. It is for anyone who finishes early or wants more
    afterwards.

    **Repeat Exercise 1 a thousand times.** Replace your seed with the numbers
    0 to 999, and count what fraction of samples at each size gives p < 0.05.
    That fraction is the test's **power** at that sample size, and you can
    compare it with what the room's hands suggested.

    **Try the t-test with `equal_var=True`** on smokers and non-smokers, and
    see how much the statistic and its degrees of freedom change when the test
    assumes equal spread.

    **Run Tukey's HSD on charges by region**, and compare what it says with
    what the room's hands said in Exercise 2.
    """)
    return


@app.cell(hide_code=True)
def _(UNIQNAME, mo):
    _name = UNIQNAME.strip().lower() or "<uniqname>"
    mo.md(rf"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Before you leave today.** Save two files:

    1. This notebook, renamed `SI618_05a_{_name}.py`
    2. An HTML export of it:
       ```bash
       uvx marimo export html --sandbox SI618_05a_{_name}.py -o SI618_05a_{_name}.html
       ```

    ❗️ **Keep both files.** In-class 05 is one deliverable covering today and
    Monday, and at the end of Monday's session you will upload all four files,
    today's two and Monday's two, in a single submission.
    """)
    return


if __name__ == "__main__":
    app.run()
