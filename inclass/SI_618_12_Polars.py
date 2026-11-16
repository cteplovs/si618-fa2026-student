# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "polars==1.44.1",
#     "pyarrow==25.0.1",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def title(mo):
    mo.md(r"""
    # SI 618 - 12: Polars

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 23 (Mon Nov 23)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.11.16.1.CT

    ---

    ## Today you will be able to

    - Read a file with Polars, and use `select`, `filter`, `with_columns` and
      `group_by` with expressions built from `pl.col`
    - Translate a pandas preparation you already know into Polars
    - Compare the time pandas and Polars take for the same work
    - Build a lazy query with `scan_csv`, read its plan with `explain`, and run it with
      `collect`

    ## Reading

    The [Polars user guide](https://docs.pola.rs/), the getting-started and concepts
    sections.

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Where we left off | 3 |
    | Reading the inspections | 7 |
    | Expressions | 20 |
    | pandas and Polars side by side | 10 |
    | Lazy queries | 15 |
    | Exercise: compute the mean score by cuisine in a borough of your choice | 8 |
    """)
    return


@app.cell
def imports():
    import tempfile
    import time
    import urllib.request
    from pathlib import Path

    import marimo as mo
    import numpy as np
    import pandas as pd
    import polars as pl

    return Path, mo, np, pd, pl, tempfile, time, urllib


@app.cell(hide_code=True)
def recap(mo):
    mo.md(r"""
    ---
    ## Where we left off

    Topics 08 to 11 used scikit-learn on data that fit easily in memory. Today and
    next Monday are about working with larger data. Today's tool, Polars, is a
    DataFrame library like pandas, written in Rust, which uses every core of the
    computer and can optimise a whole query before it reads any data. Its methods have
    different names from pandas', so most of today is about translating operations
    you already know.
    """)
    return


@app.cell(hide_code=True)
def data_intro(mo):
    mo.md(r"""
    ---
    ## Reading the inspections

    We use the New York City restaurant inspections from Homework 2 and notebook 06a.
    `pl.read_csv` reads the compressed file from its URL, as `pd.read_csv` does.
    """)
    return


@app.cell
def read_inspections(pl):
    INSPECTIONS_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "nyc_restaurant_inspections_2026-09-28.csv.gz"
    )
    raw_inspections = pl.read_csv(INSPECTIONS_URL, infer_schema_length=10000)
    raw_inspections.head()
    return INSPECTIONS_URL, raw_inspections


@app.cell(hide_code=True)
def read_reading(mo, raw_inspections):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The file has {raw_inspections.height:,} rows and {raw_inspections.width} columns.
    A Polars DataFrame has no index, so rows are identified only by their values, and
    each column has one type, shown under its name: `i64` is a 64-bit integer and
    `str` a string. `infer_schema_length=10000` makes Polars use the first 10,000
    rows, rather than the default 100, to infer each column's type.
    """)
    return


@app.cell(hide_code=True)
def expressions_intro(mo):
    mo.md(r"""
    ---
    ## Expressions

    In Polars, most work is done by passing *expressions* to a few methods. An
    expression such as `pl.col("score") <= 13` describes a computation on a column
    without running it; the method it is passed to runs it.

    | Method | What it does | pandas equivalent |
    |---|---|---|
    | `select` | Keeps or computes columns | `df[[...]]` |
    | `filter` | Keeps rows for which an expression is true | `df[mask]` or `.query` |
    | `with_columns` | Adds or replaces columns | `df["new"] = ...` or `.assign` |
    | `group_by(...).agg(...)` | Computes one row per group | `.groupby(...).agg(...)` |
    | `unique(subset=...)` | Drops duplicate rows | `.drop_duplicates(...)` |

    Notebook 06a prepared the inspections in pandas: it dropped repeated rows for the
    same inspection, kept initial inspections with a known borough and a score, and
    added `grade_band`, which is `"A"` for a score of 13 or less. Below, we do the same
    in Polars, with one method call for each step and the calls chained together.
    """)
    return


@app.cell
def prepare_inspections(pl, raw_inspections):
    inspections = (
        raw_inspections
        .unique(subset=["camis", "inspection_date", "inspection_type"],
                keep="first", maintain_order=True)
        .filter(
            (pl.col("inspection_type") == "Cycle Inspection / Initial Inspection")
            & (pl.col("boro") != "0")
        )
        .drop_nulls("score")
        .with_columns(
            grade_band=pl.when(pl.col("score") <= 13).then(pl.lit("A")).otherwise(pl.lit("not A"))
        )
    )
    inspections.select("boro", "cuisine_description", "score", "grade_band").head()
    return (inspections,)


@app.cell(hide_code=True)
def prepare_reading(inspections, mo):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    That leaves {inspections.height:,} inspections, the same number as in notebook 06a.
    `pl.when(...).then(...).otherwise(...)` is Polars' equivalent of `np.where`, and
    `pl.lit` marks a value as a constant rather than the name of a column.

    ### Grouping

    `group_by` takes the column to group by, and `agg` takes one expression for each
    column of the result. The share of A grades in each borough is the mean of a
    column of True and False, as it would be in pandas.
    """)
    return


@app.cell
def borough_shares(inspections, pl):
    borough_table = (
        inspections
        .group_by("boro")
        .agg(
            share_A=(pl.col("grade_band") == "A").mean(),
            inspections=pl.len(),
        )
        .sort("share_A", descending=True)
    )
    borough_table
    return (borough_table,)


@app.cell(hide_code=True)
def borough_reading(borough_table, mo):
    _top = borough_table.row(0, named=True)
    _bottom = borough_table.row(-1, named=True)
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    {_top['boro']} has the highest share of A grades, {_top['share_A']:.1%}, and
    {_bottom['boro']} the lowest, {_bottom['share_A']:.1%}, as in notebook 06a. The
    names given in `agg`, such as `share_A=`, become the names of the columns, and
    `pl.len()` counts the rows in each group.
    """)
    return


@app.cell(hide_code=True)
def timing_intro(mo):
    mo.md(r"""
    ---
    ## pandas and Polars side by side

    Below, we run the same preparation five times in each library, starting from the
    same data in memory, and keep the fastest time of each, which is the least
    affected by whatever else the computer was doing.
    """)
    return


@app.cell
def timing(np, pd, pl, raw_inspections, time):
    raw_pandas = raw_inspections.to_pandas()

    def prepare_with_pandas(df: pd.DataFrame) -> pd.DataFrame:
        """06a's preparation in pandas."""
        out = (
            df.drop_duplicates(["camis", "inspection_date", "inspection_type"])
            .query('inspection_type == "Cycle Inspection / Initial Inspection" and boro != "0"')
            .dropna(subset=["score"])
            .copy()
        )
        out["grade_band"] = np.where(out["score"] <= 13, "A", "not A")
        return out

    def prepare_with_polars(df: pl.DataFrame) -> pl.DataFrame:
        """The same preparation in Polars."""
        return (
            df.unique(subset=["camis", "inspection_date", "inspection_type"],
                      keep="first", maintain_order=True)
            .filter((pl.col("inspection_type") == "Cycle Inspection / Initial Inspection")
                    & (pl.col("boro") != "0"))
            .drop_nulls("score")
            .with_columns(grade_band=pl.when(pl.col("score") <= 13)
                          .then(pl.lit("A")).otherwise(pl.lit("not A")))
        )

    def fastest_ms(function, data) -> float:
        """The fastest of five runs, in milliseconds."""
        _times = []
        for _ in range(5):
            _start = time.perf_counter()
            function(data)
            _times.append(time.perf_counter() - _start)
        return 1000 * min(_times)

    preparation_times = pd.Series({
        "pandas": fastest_ms(prepare_with_pandas, raw_pandas),
        "Polars": fastest_ms(prepare_with_polars, raw_inspections),
    }, name="milliseconds")
    preparation_times.round(1)
    return (preparation_times,)


@app.cell(hide_code=True)
def timing_reading(mo, preparation_times):
    _ratio = preparation_times["pandas"] / preparation_times["Polars"]
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    On this computer, Polars took {preparation_times['Polars']:.0f} milliseconds and
    pandas {preparation_times['pandas']:.0f}, so Polars was {_ratio:.1f} times as
    fast. The times will differ on your computer. With about 300,000 rows, both are fast
    enough that the difference does not matter; it starts to matter with tens of
    millions of rows, or when the same work is repeated many times.
    """)
    return


@app.cell(hide_code=True)
def lazy_intro(mo):
    mo.md(r"""
    ---
    ## Lazy queries

    Everything so far was *eager*: each method ran as soon as it was called.
    `pl.scan_csv` instead returns a `LazyFrame`, which records the steps of a query
    without reading the file. When the query is run with `collect`, Polars first
    rearranges the steps, for example so that it reads only the columns and rows the
    query needs, and then runs them.

    `scan_csv` reads from a file on disk, so we first save a copy of the inspections
    file in a temporary folder.
    """)
    return


@app.cell
def download_copy(INSPECTIONS_URL, Path, tempfile, urllib):
    inspections_path = Path(tempfile.gettempdir()) / "nyc_restaurant_inspections.csv.gz"
    if not inspections_path.exists():
        urllib.request.urlretrieve(INSPECTIONS_URL, inspections_path)
    inspections_path
    return (inspections_path,)


@app.cell
def lazy_query(inspections_path, pl):
    queens_query = (
        pl.scan_csv(inspections_path, infer_schema_length=10000)
        .filter(pl.col("boro") == "Queens")
        .group_by("cuisine_description")
        .agg(mean_score=pl.col("score").mean(), inspections=pl.len())
        .sort("inspections", descending=True)
    )
    print(queens_query.explain())
    return (queens_query,)


@app.cell(hide_code=True)
def plan_reading(mo):
    mo.md(r"""
    The plan is read from the bottom up. The bottom lines show that the scan of the
    file reads only 3 of its 11 columns (`PROJECT 3/11 COLUMNS`) and applies the
    filter on the borough as it reads (`SELECTION`), although the query names the
    filter as a separate step. Nothing has been read yet; `collect` runs the plan.
    """)
    return


@app.cell
def collect_query(queens_query):
    queens_cuisines = queens_query.collect()
    queens_cuisines.head()
    return


@app.cell(hide_code=True)
def cuisine_exercise_intro(mo):
    mo.md(r"""
    ### 🚀 Exercise: compute the mean score by cuisine in a borough of your choice

    ✅ Step 1: In the cell below, set `my_boro` to one of `"Bronx"`, `"Brooklyn"`,
    `"Manhattan"` or `"Staten Island"`. Then, starting from `inspections`, use
    `filter`, `group_by` and `agg` to compute each cuisine's mean score and number of
    inspections in that borough, with the columns `cuisine_description`, `mean_score`
    and `inspections`, sorted by `inspections` from most to fewest. Store the result in
    `my_cuisine_scores`.

    ✅ Step 2: In the markdown cell after it, say in a sentence which of the five most
    inspected cuisines in your borough has the lowest mean score. A lower score means
    fewer violations.
    """)
    return


@app.cell
def my_cuisines():
    # Choose a borough, and compute the mean score by cuisine there with Polars.
    my_boro = None
    my_cuisine_scores = None
    return my_boro, my_cuisine_scores


@app.cell(hide_code=True)
def cuisine_answer(mo):
    mo.md(r"""
    *Your answer here: which of the five most inspected cuisines in your borough has
    the lowest mean score.*
    """)
    return


@app.cell(hide_code=True)
def check_cuisine_exercise(my_boro, my_cuisine_scores, pl):
    def test_my_cuisines():
        assert my_boro in ["Bronx", "Brooklyn", "Manhattan", "Staten Island"], (
            'Set `my_boro` to one of "Bronx", "Brooklyn", "Manhattan" or "Staten Island".'
        )
        assert isinstance(my_cuisine_scores, pl.DataFrame), (
            "`my_cuisine_scores` should be a Polars DataFrame. If you built a lazy "
            "query, call `.collect()` on it."
        )
        assert {"cuisine_description", "mean_score", "inspections"} <= set(my_cuisine_scores.columns), (
            "Name the columns in `agg`, for example `mean_score=pl.col(\"score\").mean()`."
        )
        assert my_cuisine_scores["inspections"].is_sorted(descending=True), (
            "Sort by `inspections` with `descending=True`."
        )
    return


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - Polars does most of its work through expressions built from `pl.col`, passed to
      `select`, `filter`, `with_columns` and `group_by(...).agg(...)`.
    - A Polars DataFrame has no index, and each column has one type.
    - For the same preparation, Polars was faster than pandas; the difference matters
      with large data or repeated work.
    - `scan_csv` builds a lazy query, `explain` shows the plan Polars will run, and
      `collect` runs it, reading only the columns and rows the query needs.

    ## Next class

    Wednesday, November 25, is Thanksgiving, with no class. On Monday, November 30,
    notebook 13 will introduce PySpark.
    """)
    return


@app.cell(hide_code=True)
def end_of_notebook(mo):
    mo.md(r"""
    ---
    ## 🏁 END OF NOTEBOOK

    In-class 12 is a one-line answer to the question on Canvas under *In-class 12*,
    which you should submit before the end of the session. There is nothing to upload
    from this notebook.
    """)
    return


if __name__ == "__main__":
    app.run()
