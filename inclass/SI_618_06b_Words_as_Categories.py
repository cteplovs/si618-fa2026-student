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

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 618 - 06b: words in names as categories

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 12 (Mon Oct 12)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.10.08.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Split a text column into words with pandas string methods, and count the
      words
    - Turn "does this name contain this word?" into a categorical column, and
      explain why a word test is safer than a substring test
    - Use Wednesday's chi-square test and Cramer's V on a word and a grade
    - Explain why testing many things at once produces "significant" results
      by chance, and correct for it

    ## How this notebook works

    **This file is today's session, start to finish**, and it is the second
    half of In-class 06. At the end of today you upload four files: Wednesday's
    two and today's two.

    Each exercise gives each of you a slightly different version of the same
    question. When you have answered yours, a **Reveal the room** button shows
    every version side by side, so that you can see what the whole set of
    answers says, which no single version can.

    ✅ **Before anything else, please type your uniqname below**, because it
    chooses your word in Exercise 1 and your shuffle in Exercise 2.
    """)
    return


@app.cell
def _():
    UNIQNAME = ""
    return (UNIQNAME,)


@app.cell
def _():
    import string
    import zlib

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats

    pd.set_option("display.max_columns", 50)
    pd.set_option("display.max_rows", 30)
    sns.set_theme(style="whitegrid")
    return mo, np, pd, plt, stats, string, zlib


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data is the same as Wednesday's: one row per initial inspection with a
    score and a known borough, from the New York City snapshot in Homework 2.
    `grade_band` is `"A"` for a score of 13 or less and `"not A"` otherwise.
    Today the column of interest is `dba`, the name the restaurant does
    business under.
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
    inspections[["dba", "cuisine_description", "score", "grade_band"]].head()
    return (inspections,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That leaves 46,627 inspections, 60% of which scored in the A range.

    ---
    ## Part 1: From names to words

    A name is a single string, and no test can be run on 46,627 different
    strings. Splitting each name into words turns it into something that can
    be counted. Pandas string methods sit under `.str`, and they apply to every
    row at once: `.str.lower()` makes the case consistent, and `.str.split()`
    splits on spaces and returns a list of words for each name.
    """)
    return


@app.cell
def _(inspections):
    name_lists = inspections["dba"].str.lower().str.split()
    name_lists.head()
    return (name_lists,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To count words across all the names, `.explode()` gives each word in a
    list its own row. Punctuation stuck to a word, as in `"ice-cream,"` or
    `"(soho)"`, would make it a different word, so `.str.strip()` removes
    punctuation characters from both ends. `string.punctuation` is a string of
    every punctuation character, and passing it to `.str.strip()` strips any of
    them, which needs no pattern matching.
    """)
    return


@app.cell
def _(name_lists, string):
    all_words = name_lists.explode().str.strip(string.punctuation)
    all_words = all_words[all_words != ""]
    all_words.value_counts().head(15)
    return (all_words,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some of the most common words, such as `the`, `and` and the Spanish `la`
    and `el`, would be in a name whatever the restaurant was like. Words of
    this kind are called **stop words**, and the usual practice is to set them
    aside before counting. The list below is short and written for these
    names; Wednesday's session on text will use a standard one.
    """)
    return


@app.cell
def _(all_words):
    STOP_WORDS = {"the", "and", "of", "a", "la", "el", "de", "le", "new", "york", "nyc", "ii", "&"}
    word_counts = all_words[~all_words.isin(STOP_WORDS)].value_counts()
    word_counts.head(20)
    return STOP_WORDS, word_counts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For a question about restaurants, what matters is whether a word appears in
    a name, not how many times, so the cell below keeps the **set** of words in
    each name. `name_words` has one entry per inspection, in the same order as
    `inspections`.
    """)
    return


@app.cell
def _(STOP_WORDS, name_lists, string):
    name_words = name_lists.apply(
        lambda _words: {_w.strip(string.punctuation) for _w in _words} - {""} - STOP_WORDS
    )
    name_words.head()
    return (name_words,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Predict, then reveal

    About 60% of all inspections score in the A range. The four words below
    each appear in the names behind 280 to 335 inspections.
    Commit to a prediction before you press the button.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    prediction = mo.ui.radio(
        options=["thai", "golden", "taco", "express"],
        label="**Which word goes with the lowest share of A grades?**",
    )
    reveal_prediction = mo.ui.run_button(label="Reveal the shares")
    mo.vstack([prediction, reveal_prediction])
    return (reveal_prediction,)


@app.cell
def _(inspections, mo, name_words, pd, reveal_prediction):
    mo.stop(not reveal_prediction.value, mo.md("*Press the button once you have predicted.*"))
    _rows = []
    for _word in ["thai", "golden", "taco", "express"]:
        _has = name_words.apply(lambda _ws: _word in _ws)
        _rows.append({
            "word": _word,
            "inspections": int(_has.sum()),
            "share A": round(float((inspections.loc[_has, "grade_band"] == "A").mean()), 3),
        })
    pd.DataFrame(_rows).sort_values("share A")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The shares run from 45% for `thai` to 76% for `taco`, against 60% overall,
    which is a wider spread than Wednesday's boroughs showed. The rest of the
    session asks whether spreads like this could be chance, and what a word in
    a name is really measuring.

    ---
    ## Part 2: A word as a category

    The obvious way to find a word is `.str.contains`, but it finds the letters
    anywhere in the name, including inside other words. Compare the two counts
    below for `tea`.
    """)
    return


@app.cell
def _(inspections, name_words):
    _substring = inspections["dba"].str.lower().str.contains("tea", regex=False)
    _word = name_words.apply(lambda _ws: "tea" in _ws)
    print("Names containing the letters 'tea':", int(_substring.sum()))
    print("Names containing the word 'tea':   ", int(_word.sum()))
    inspections.loc[_substring & ~_word, "dba"].drop_duplicates().head(6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Almost half of the 568 substring matches are names such as `STK
    STEAKHOUSE`, `BATEAUX NEW YORK` and `MOMENTEA KITCHEN`, where the letters
    sit inside another word. For that reason, the rest of this notebook tests
    whether a word is in the set of words for each name.

    The cell below does that for `bar`, which gives a column of `True` and
    `False`, a categorical column with two values. Crossing it with
    `grade_band` gives a 2 by 2 contingency table, and everything from
    Wednesday applies to it.
    """)
    return


@app.cell
def _(inspections, name_words, pd, stats):
    has_bar = name_words.apply(lambda _ws: "bar" in _ws)
    bar_table = pd.crosstab(has_bar, inspections["grade_band"])
    print(bar_table, "\n")
    print(pd.crosstab(has_bar, inspections["grade_band"], normalize="index").round(3), "\n")
    print("p =", stats.chi2_contingency(bar_table).pvalue)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Inspections of places with `bar` in the name scored an A 64% of the time,
    against 60% for the rest, and the p-value is about 0.0001, so by the usual
    convention the difference is significant. The 1,838 inspections are enough
    for a gap of four points to be detected.

    ---
    ### 🚀 Exercise 1: does your word go with the grade?

    Your uniqname has assigned you one of twelve common words, shown below as
    `my_word`.

    ✅ Step 1: Build `my_has_word`, which is `True` for each inspection whose
    name contains `my_word`, using `name_words` as for `bar` above.

    ✅ Step 2: Build `my_word_table`, the contingency table of `my_has_word`
    against `grade_band`, and assign its chi-square p-value to `my_word_p`, as
    a float.

    ✅ Step 3: Assign to `my_share_gap` the share of A grades among inspections
    with your word, minus the share among those without it. For `bar`, it
    would be 0.643 - 0.598, or about 0.045.

    ✅ Step 4: Once the test below passes, press **Reveal the room** to see
    all twelve words, then assign to `word_sentence` two or three sentences.
    Choose one word from the room's table whose result you think says more
    about the kind of restaurant than about the word itself, and say why.
    """)
    return


@app.cell
def _(UNIQNAME, mo, zlib):
    mo.stop(
        not UNIQNAME.strip(),
        mo.md("⚠️ Type your uniqname into `UNIQNAME` at the top of the notebook."),
    )
    EXERCISE_WORDS = [
        "restaurant", "bakery", "pizza", "house", "chicken", "deli",
        "kitchen", "sushi", "cafe", "grill", "shop", "coffee",
    ]
    my_seed = zlib.crc32(UNIQNAME.strip().lower().encode())
    my_word = EXERCISE_WORDS[my_seed % len(EXERCISE_WORDS)]
    my_word
    return EXERCISE_WORDS, my_seed, my_word


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_has_word = None
    my_word_table = None
    my_word_p = None
    my_share_gap = None
    word_sentence = ""
    return my_has_word, my_share_gap, my_word_p, my_word_table, word_sentence


@app.cell(hide_code=True)
def _(
    inspections,
    my_has_word,
    my_share_gap,
    my_word,
    my_word_p,
    my_word_table,
    name_words,
    pd,
    stats,
):
    def check_exercise_1():
        _has = name_words.apply(lambda _ws: my_word in _ws)
        _table = pd.crosstab(_has, inspections["grade_band"])
        _shares = pd.crosstab(_has, inspections["grade_band"], normalize="index")["A"]
        assert my_has_word is not None, "Build `my_has_word` from `name_words`."
        assert int(pd.Series(my_has_word).sum()) == int(_has.sum()), (
            f"`my_has_word` is True for {int(pd.Series(my_has_word).sum())} inspections, but "
            f"{int(_has.sum())} names contain the word `{my_word}`. Test membership in "
            "`name_words` rather than using `.str.contains`."
        )
        assert my_word_table is not None, "Build `my_word_table`."
        assert my_word_table.shape == (2, 2), (
            f"`my_word_table` has shape {my_word_table.shape}, where 2 by 2 is expected: "
            "`my_has_word` first and `grade_band` second."
        )
        assert my_word_p is not None, "Assign the chi-square p-value to `my_word_p`."
        assert abs(float(my_word_p) - stats.chi2_contingency(_table).pvalue) < 1e-9, (
            f"`my_word_p` is {my_word_p}. Pass `my_word_table` to "
            "`stats.chi2_contingency` and take `.pvalue`."
        )
        assert my_share_gap is not None, "Assign the gap in shares to `my_share_gap`."
        assert abs(float(my_share_gap) - (_shares[True] - _shares[False])) < 0.001, (
            f"`my_share_gap` is {my_share_gap}. Take the share of A among names with your "
            "word minus the share among names without it; the order matters."
        )

    return (check_exercise_1,)


@app.cell(hide_code=True)
def _(check_exercise_1, word_sentence):
    def test_exercise_1():
        check_exercise_1()

    def test_word_sentence():
        assert len(word_sentence.strip()) >= 100, (
            f"`word_sentence` is {len(word_sentence.strip())} characters, where a word "
            "from the room's table and a reason are expected."
        )

    return


@app.cell(hide_code=True)
def _(check_exercise_1, mo):
    try:
        check_exercise_1()
        _ready = True
    except AssertionError:
        _ready = False
    reveal_words = mo.ui.run_button(label="Reveal the room", disabled=not _ready)
    mo.vstack([
        reveal_words,
        mo.md("" if _ready else "*The button unlocks once Steps 1 to 3 pass their test.*"),
    ])
    return (reveal_words,)


@app.cell
def _(
    EXERCISE_WORDS,
    inspections,
    mo,
    my_word,
    name_words,
    np,
    pd,
    reveal_words,
    stats,
):
    mo.stop(not reveal_words.value)
    _rows = []
    for _word in EXERCISE_WORDS:
        _has = name_words.apply(lambda _ws: _word in _ws)
        _table = pd.crosstab(_has, inspections["grade_band"])
        _result = stats.chi2_contingency(_table)
        _shares = pd.crosstab(_has, inspections["grade_band"], normalize="index")["A"]
        _rows.append({
            "word": _word + ("  <- yours" if _word == my_word else ""),
            "inspections": int(_has.sum()),
            "share A with": round(float(_shares[True]), 3),
            "share A without": round(float(_shares[False]), 3),
            "gap": round(float(_shares[True] - _shares[False]), 3),
            "p": float(f"{_result.pvalue:.2g}"),
            "V": round(float(np.sqrt(_result.statistic / _table.to_numpy().sum())), 3),
        })
    pd.DataFrame(_rows).sort_values("gap").reset_index(drop=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Eight of the twelve words are significant, and the gaps run in both
    directions. A word in a name is rarely the cause of anything: `pizza` and
    `bakery` stand for kinds of kitchen, and the cuisine column already
    records the kind of kitchen, so the word may be measuring the same thing a
    second time.

    ---
    ## Part 3: Testing many words at once

    There are thousands of words in these names, and nothing stops anyone from
    testing all of them and reporting the ones that come out significant. A
    p-value below 0.05 happens about one time in twenty **when there is no
    relationship at all**, so testing enough words guarantees some
    "discoveries".

    The way to see this is to destroy any real relationship and test anyway.
    Shuffling `grade_band` into a random order keeps the same number of A
    grades but assigns them to inspections at random, so on the shuffled
    grades no word can genuinely go with the grade.

    ### 🚀 Exercise 2: how many discoveries does chance make?

    `TOP_WORDS` below holds the 50 most common words, and `shuffled_grades` is
    `grade_band` shuffled by your uniqname, so each of you has a different
    shuffle.

    ✅ Step 1: Write a function `count_significant(grades)` that runs the
    chi-square test of each word in `TOP_WORDS` against `grades` and returns
    the number of words whose p-value is below 0.05, as an int.

    ✅ Step 2: Assign `count_significant(shuffled_grades)` to `my_false_hits`
    and `count_significant(inspections["grade_band"])` to `real_hits`.

    ✅ Step 3: Press **Reveal the room**, then assign to `many_tests_sentence`
    two or three sentences. Say how many of the 50 words you would expect to
    come out significant by chance, and what that implies about the real
    count.
    """)
    return


@app.cell
def _(inspections, my_seed, np, pd, word_counts):
    TOP_WORDS = word_counts.index[:50].tolist()
    shuffled_grades = pd.Series(
        np.random.default_rng(my_seed).permutation(inspections["grade_band"].to_numpy()),
        index=inspections.index,
    )
    TOP_WORDS[:10]
    return TOP_WORDS, shuffled_grades


@app.cell
def _():
    # Your code here.
    def count_significant(grades) -> int:
        return None

    my_false_hits = None
    real_hits = None
    many_tests_sentence = ""
    return count_significant, many_tests_sentence, my_false_hits, real_hits


@app.cell(hide_code=True)
def _(TOP_WORDS, inspections, name_words, np, stats):
    _has_matrix = np.column_stack(
        [name_words.apply(lambda _ws: _word in _ws).to_numpy() for _word in TOP_WORDS]
    )

    def word_pvalues(grades) -> np.ndarray:
        """P-values of the chi-square test of each word in TOP_WORDS against grades."""
        _is_a = np.asarray(grades) == "A"
        _pvalues = []
        for _j in range(len(TOP_WORDS)):
            _has = _has_matrix[:, _j]
            _table = np.array([
                [np.sum(_has & _is_a), np.sum(_has & ~_is_a)],
                [np.sum(~_has & _is_a), np.sum(~_has & ~_is_a)],
            ])
            _pvalues.append(stats.chi2_contingency(_table).pvalue)
        return np.array(_pvalues)

    real_pvalues = word_pvalues(inspections["grade_band"])
    return real_pvalues, word_pvalues


@app.cell(hide_code=True)
def _(
    my_false_hits,
    np,
    real_hits,
    real_pvalues,
    shuffled_grades,
    word_pvalues,
):
    def check_exercise_2():
        _expected_false = int(np.sum(word_pvalues(shuffled_grades) < 0.05))
        _expected_real = int(np.sum(real_pvalues < 0.05))
        assert my_false_hits is not None, "Assign `count_significant(shuffled_grades)` to `my_false_hits`."
        assert int(my_false_hits) == _expected_false, (
            f"`my_false_hits` is {my_false_hits}, where {_expected_false} is expected. "
            "Use `shuffled_grades`, all 50 words, and a strict `< 0.05`."
        )
        assert real_hits is not None, "Assign the count on the real grades to `real_hits`."
        assert int(real_hits) == _expected_real, (
            f"`real_hits` is {real_hits}, where {_expected_real} is expected. Pass "
            "`inspections['grade_band']` to the same function."
        )

    return (check_exercise_2,)


@app.cell(hide_code=True)
def _(check_exercise_2, many_tests_sentence):
    def test_exercise_2():
        check_exercise_2()

    def test_many_tests_sentence():
        assert len(many_tests_sentence.strip()) >= 100, (
            f"`many_tests_sentence` is {len(many_tests_sentence.strip())} characters, "
            "where an expected number and what it implies are expected."
        )

    return


@app.cell(hide_code=True)
def _(check_exercise_2, mo):
    try:
        check_exercise_2()
        _ready_2 = True
    except AssertionError:
        _ready_2 = False
    reveal_shuffles = mo.ui.run_button(label="Reveal the room", disabled=not _ready_2)
    mo.vstack([
        reveal_shuffles,
        mo.md("" if _ready_2 else "*The button unlocks once Steps 1 and 2 pass their test.*"),
    ])
    return (reveal_shuffles,)


@app.cell
def _(inspections, mo, my_false_hits, np, plt, reveal_shuffles, word_pvalues):
    mo.stop(not reveal_shuffles.value)
    _grades = inspections["grade_band"].to_numpy()
    room_false_hits = [
        int(np.sum(word_pvalues(np.random.default_rng(_seed).permutation(_grades)) < 0.05))
        for _seed in range(40)
    ]
    _fig, _ax = plt.subplots(figsize=(8, 3.5))
    _ax.hist(room_false_hits, bins=range(0, max(room_false_hits) + 2), align="left", rwidth=0.85)
    _ax.axvline(my_false_hits, color="crimson", linestyle="--", label=f"your shuffle: {my_false_hits}")
    _ax.set_xlabel("Words significant at 0.05 on shuffled grades (of 50)")
    _ax.set_ylabel("Shuffles")
    _ax.set_title(f"40 shuffles: mean {np.mean(room_false_hits):.2f} false discoveries")
    _ax.legend()
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Across 40 shuffles, the number of words that came out significant averages
    about 2.5, which is 5% of 50, and some shuffles found six or eight. On the
    real grades, 34 of the 50 words are significant, far more than chance would
    produce, so some words do go with the grade. Chance alone cannot say which
    of the 34 are the real ones, however.

    The simplest correction, named after Bonferroni, divides the threshold by
    the number of tests: with 50 tests, a word counts as significant only if
    its p-value is below 0.05 / 50 = 0.001. Applied to a shuffle, it leaves
    almost nothing, as it should. Applied to the real grades, it leaves the
    words below.
    """)
    return


@app.cell
def _(TOP_WORDS, real_pvalues):
    [_w for _w, _p in zip(TOP_WORDS, real_pvalues) if _p < 0.05 / len(TOP_WORDS)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Twenty-five words survive. Most are chain names, such as `dunkin`,
    `starbucks` and `popeyes`, or name a kind of food, such as `pizza`,
    `thai` and `taco`, which supports the point from Exercise 1 that a word
    often stands for the kind of restaurant.

    ## Summary

    - `.str.lower()`, `.str.split()`, `.explode()` and `.str.strip()` turn a
      column of names into words that can be counted, with no pattern
      matching
    - test whether a word is in a name's set of words, because `.str.contains`
      also finds the letters inside other words
    - a word's presence is a categorical column, so Wednesday's chi-square test
      and Cramer's V apply to it unchanged
    - when no relationship exists, about one test in twenty is significant at
      0.05, so testing many things guarantees false discoveries, and the
      Bonferroni correction divides the threshold by the number of tests

    ## Next class

    **Notebook 07a** begins text analysis: tokenising whole documents rather
    than names, with a standard stop-word list.

    ## Additional resources

    - [pandas: working with text data](https://pandas.pydata.org/docs/user_guide/text.html)
    - [pandas.Series.explode](https://pandas.pydata.org/docs/reference/api/pandas.Series.explode.html)
    - [Multiple comparisons problem](https://en.wikipedia.org/wiki/Multiple_comparisons_problem)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded. It is for anyone who finishes early or wants more
    afterwards.

    **Control for cuisine.** Repeat Exercise 1 for `pizza`, but only within
    inspections whose `cuisine_description` is `"Pizza"`. If the word still
    goes with the grade among pizza places, it is saying something the
    cuisine does not.

    **Count each restaurant once.** Many restaurants have several initial
    inspections. Keep each `camis` once and rerun the test for your word, and
    compare the p-value.

    **Find the strongest word.** Compute Cramer's V for every word in
    `TOP_WORDS` and sort them. Compare the top of that list with the words
    that survive the Bonferroni correction.
    """)
    return


@app.cell(hide_code=True)
def _(UNIQNAME, mo):
    _name = UNIQNAME.strip().lower() or "<uniqname>"
    mo.md(rf"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Before you leave today.** In-class 06 is one deliverable covering both
    sessions, so upload **four files** in a single submission:

    1. `SI618_06a_{_name}.py` and `SI618_06a_{_name}.html` from Wednesday
    2. This notebook, renamed `SI618_06b_{_name}.py`, and its export:
       ```bash
       uvx marimo export html --sandbox SI618_06b_{_name}.py -o SI618_06b_{_name}.html
       ```

    ❗️ Late in-class work is not accepted for credit.
    """)
    return


if __name__ == "__main__":
    app.run()
