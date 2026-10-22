# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "matplotlib==3.11.1",
#     "scipy==1.18.1",
#     "scikit-learn==1.9.0",
#     "opencc-python-reimplemented==0.1.7",
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
        # SI 618 - Homework 4: Who wrote the last forty chapters?

        **Name:**
        **Uniqname:**

        Due **Wednesday, October 28, before class (3:30 PM)**. The full spec is in
        `README.md`, and the rubric is in `RUBRIC.md`. Read both before you start;
        the spec's table of function characters gives the meaning of every
        character you will count, and you do not need to read Chinese.

        Rename this file `SI618_HW04_<uniqname>.py` before you submit, and upload
        its HTML export alongside it.

        ### Working in marimo

        - A variable can be defined in only one cell, so give each new result a
          new name, such as `chapters_checked`, or prefix a name with `_` to keep
          it inside its cell.
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
    import re
    import urllib.request

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from opencc import OpenCC
    from scipy import stats
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

    # Chinese characters need a font that has them; the first one found is used.
    plt.rcParams["font.sans-serif"] = [
        "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "SimHei", "DejaVu Sans",
    ]
    t2s = OpenCC("t2s")
    return CountVectorizer, OpenCC, TfidfVectorizer, mo, np, pd, plt, re, stats, t2s, urllib


@app.cell
def _():
    DATA_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "hongloumeng_pg24264.txt"
    )
    FUNCTION_CHARS = list("之其亦乃而矣焉了的着呢吗么罢便就也又都还只这那")
    # A regular expression matching one Chinese character, for counting with
    # `re` or with pandas' `.str.count()`. It is an ordinary string rather than
    # r"...", so Python turns the escapes into the characters themselves, which
    # every regex engine pandas might use understands.
    CHINESE_CHAR = "[\u4e00-\u9fff]"
    return CHINESE_CHAR, DATA_URL, FUNCTION_CHARS


@app.cell
def _(DATA_URL, urllib):
    # The whole file as one string, Gutenberg's licence text included.
    raw_text = urllib.request.urlopen(DATA_URL).read().decode("utf-8")
    len(raw_text)
    return (raw_text,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 1: Get the chapters (15 points)

        ### 1.1 Load and strip (5)
        """
    )
    return


@app.cell
def _():
    # Remove Gutenberg's text from both ends of `raw_text`, leaving the novel in
    # `novel`. Then show its length and its first and last 200 characters.
    novel = None
    return (novel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 1.2 Split (10)""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The cell below is written for you. It finds every line of `novel` that
        begins with a chapter heading, 第N回, and shows each match in
        `heading_matches`: where it starts in `novel`, the numeral, the chapter
        number as an integer, and the whole line. You do not need to change it,
        and you do not need to write a pattern of your own.
        """
    )
    return


@app.cell
def _(mo, novel, pd, re):
    mo.stop(novel is None, mo.md("⚠️ Build `novel` in 1.1 first."))

    def chinese_number(numeral: str) -> int:
        """Convert a chapter numeral as this edition writes it to an integer.

        Chapters 1 to 99 use 十 for tens (十二 = 12, 四十五 = 45); from 100 on,
        the edition writes digit by digit (一零零 = 100, 一一七 = 117).
        """
        digits = dict(zip("零〇一二三四五六七八九", [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        if "百" in numeral:
            hundreds, rest = numeral.split("百")
            return 100 * (digits[hundreds] if hundreds else 1) + (chinese_number(rest) if rest else 0)
        if "十" in numeral:
            tens, units = numeral.split("十")
            return 10 * (digits[tens] if tens else 1) + (digits[units] if units else 0)
        return int("".join(str(digits[ch]) for ch in numeral))

    HEADING_PATTERN = r"^第([一二三四五六七八九十百零〇]+)回"
    heading_matches = pd.DataFrame(
        [
            {
                "start": _m.start(),
                "numeral": _m.group(1),
                "chapter": chinese_number(_m.group(1)),
                "line": novel[_m.start():novel.find("\n", _m.start())],
            }
            for _m in re.finditer(HEADING_PATTERN, novel, flags=re.M)
        ]
    )
    print(len(heading_matches), "matches")
    heading_matches.head()
    return (heading_matches,)


@app.cell
def _():
    # Look at `heading_matches` with pandas. Show each problem you find, and
    # how you fixed it, in as many cells as you need, before building `chapters`.
    return


@app.cell
def _():
    # Build `chapters`: one row per chapter, with `chapter` (an integer from 1 to
    # 120), `text`, and `n_chars` (Chinese characters only). A chapter's text runs
    # from its heading's `start` to the next heading's `start`. Finish with a
    # check that `chapter` runs from 1 to 120 with no gaps or repeats.
    chapters = None
    return (chapters,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what went wrong at each step, how you found it, and what
        you changed.*
        """
    )
    return


@app.cell(hide_code=True)
def _(chapters, novel, pd):
    def test_part_1():
        assert isinstance(novel, str), "Store the stripped novel in `novel`, as a string."
        assert "PROJECT GUTENBERG" not in novel.upper(), (
            "`novel` still contains Project Gutenberg's text. Check both ends."
        )
        assert isinstance(chapters, pd.DataFrame), "`chapters` should be a DataFrame."
        for _c in ["chapter", "text", "n_chars"]:
            assert _c in chapters.columns, f"`chapters` needs a `{_c}` column."
        assert len(chapters) == 120, (
            f"`chapters` has {len(chapters)} rows, not 120. Look at the `line` column "
            "of `heading_matches`: is every match a chapter heading, and is any "
            "chapter counted twice?"
        )
        assert sorted(chapters["chapter"]) == list(range(1, 121)), (
            "`chapter` should hold each number from 1 to 120 exactly once. Which "
            "numbers are missing or repeated?"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 2: Normalise (10 points)

        ### 2.1 Show the problem (4)
        """
    )
    return


@app.cell
def _():
    # One table: for each character in FUNCTION_CHARS that has a traditional
    # form, its count in `novel` in each form. OpenCC("s2t") converts the other
    # way, which gives you the traditional forms.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what the table means for a count made from the file as it
        stands, and what unequal mixing between the two halves would do.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 2.2 Convert (6)""")
    return


@app.cell
def _():
    # Add a `simplified` column to a copy of `chapters`, then check that every
    # character in FUNCTION_CHARS occurs in it.
    chapters_simplified = None
    return (chapters_simplified,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: which character never occurs, why, and how you fixed it.*
        """
    )
    return


@app.cell(hide_code=True)
def _(FUNCTION_CHARS, chapters_simplified, pd):
    def test_part_2():
        assert isinstance(chapters_simplified, pd.DataFrame), (
            "`chapters_simplified` should be a DataFrame."
        )
        assert "simplified" in chapters_simplified.columns, (
            "Add a `simplified` column holding each converted chapter."
        )
        _all = "".join(chapters_simplified["simplified"])
        _missing = [_c for _c in FUNCTION_CHARS if _c not in _all]
        assert not _missing, (
            f"These never occur in the converted text: {''.join(_missing)}. "
            "What does the original file write in their place?"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 3: Count (20 points)

        ### 3.1 The table (12)
        """
    )
    return


@app.cell
def _():
    # Count FUNCTION_CHARS in every chapter with CountVectorizer, then build
    # `rates`: indexed by chapter number, one column per character, per 1,000
    # Chinese characters.
    rates = None
    return (rates,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: why `analyzer="char"` is the right choice for Chinese.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 3.2 Look first (8)""")
    return


@app.cell
def _():
    # Plot the rates of 之 and 么 across all 120 chapters, with a vertical line
    # between chapters 80 and 81.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what you see, including whether the first 80 chapters are
        uniform.*
        """
    )
    return


@app.cell(hide_code=True)
def _(FUNCTION_CHARS, pd, rates):
    def test_part_3():
        assert isinstance(rates, pd.DataFrame), "`rates` should be a DataFrame."
        assert rates.shape == (120, len(FUNCTION_CHARS)), (
            f"`rates` is {rates.shape}; expected 120 rows and one column per "
            "function character."
        )
        assert list(rates.columns) == FUNCTION_CHARS, (
            "Use FUNCTION_CHARS, in order, as the columns of `rates`."
        )
        assert list(rates.index) == list(range(1, 121)), (
            "Index `rates` by chapter number, 1 to 120."
        )
        assert rates["了"].between(5, 100).all(), (
            "了 should occur several dozen times per 1,000 characters. Are these "
            "rates per 1,000, divided by each chapter's own length?"
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 4: Compare the two parts (30 points)

        ### 4.1 Test (14)
        """
    )
    return


@app.cell
def _():
    # Build `comparison`: one row per character, with both means, the
    # difference, Cohen's d and Welch's p-value, sorted by p-value. Then apply
    # the Bonferroni correction.
    comparison = None
    return (comparison,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: the Bonferroni threshold you used, and how many
        characters still differ.*

        ### 4.2 Read the table (8)

        *Your answer here.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 4.3 Where does the change happen? (8)""")
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""*Your answer here.*""")
    return


@app.cell(hide_code=True)
def _(FUNCTION_CHARS, comparison, pd):
    def test_part_4():
        assert isinstance(comparison, pd.DataFrame), "`comparison` should be a DataFrame."
        assert len(comparison) == len(FUNCTION_CHARS), (
            "`comparison` should have one row per function character."
        )
        _p = [_c for _c in comparison.columns if "p" == _c.lower() or "pval" in _c.lower() or "p_value" in _c.lower()]
        assert _p, "Name the p-value column `p`, `pvalue` or `p_value`."
        _vals = comparison[_p[0]].dropna()
        assert _vals.is_monotonic_increasing, "Sort `comparison` by p-value."
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 5: Content against style (10 points)
        """
    )
    return


@app.cell
def _():
    # TfidfVectorizer with analyzer="char", one document per converted chapter.
    # The fifteen characters whose mean TF-IDF rises most from chapters 1-80 to
    # 81-120, marked as in FUNCTION_CHARS or not.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        *Your answer here: what the characters not on the function list are, and why
        a study of authorship counts function characters instead.*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## Part 6: For a reader who doesn't code (15 points)

        - **Question:**
        - **Finding:**
        - **Evidence:**
            -
            -
        - **So what:**
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
        2. Rename this file `SI618_HW04_<uniqname>.py`.
        3. Export it:
           ```bash
           uvx marimo export html --sandbox SI618_HW04_<uniqname>.py -o SI618_HW04_<uniqname>.html
           ```
        4. Upload both files to Canvas.
        """
    )
    return


if __name__ == "__main__":
    app.run()
