# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
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
        # SI 618 · 01: Introduction

        Dr. Chris Teplovs, University of Michigan School of Information

        **Fall 2026** · Sessions 1 (Mon Aug 31) and 2 (Wed Sep 2)

        Copyright © 2026. This notebook may not be shared outside of the course
        without permission. Notebook version 2026.08.28.1.CT

        ---

        This notebook introduces marimo, which is the notebook environment we'll be
        using all term, alongside pandas, which is the library we'll lean on for data
        manipulation in most of the sessions that follow.

        ## Learning objectives

        By the end of these two sessions you will be able to:

        - Open, edit and export a marimo notebook, and say something about how its
          reactive execution model differs from a more traditional notebook
        - Explain why a purpose-built data library tends to beat hand-written loops
          over lists of dictionaries
        - Create a `DataFrame`, inspect it with `.head()`, `.info()` and
          `.describe()`, and select from it using `[]` and `.loc`
        - Filter rows with a boolean mask or with `.query()`, compute basic
          aggregations, and carry out a simple `.groupby()`
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Outline

        **Session 1, Monday**

        * 🚩 Block 0: Introduction (25 minutes)
        * 🚩 Block 1: Motivating pandas (30 minutes)

        **Session 2, Wednesday**

        * 🚩 Block 2: Core pandas concepts (40 minutes)
        * 🚩 Block 3: Applied practice (30 minutes)

        One notebook across two sessions, and you submit it once, at the end of
        Wednesday's session.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🚩 Block 0: Introduction

        ### Welcome!

        * Lead Instructor: Dr. Chris Teplovs
        * GSIs: *(see Canvas)*

        The course overview, the policies and the full schedule all live on
        [Canvas](https://canvas.umich.edu/). We won't be reading the syllabus aloud,
        so please have a look at it before Wednesday, and bring any questions.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### How did we get here?

        * **Python**, conceived in the late 1980s and named after Monty Python's
          Flying Circus. First release 1991; version 2.0 in 2000; version 3.0 in
          2008. We will use 3.12 or 3.13.
        * **IPython**, or interactive Python. *"In scientific computing, we typically
          don't know what we're doing."* (IPython tutorial, PyCon 2012.) Scientific
          computing is exploratory computing, and IPython was built for exploring.
          It still provides the kernel underneath most notebook tools.
        * **Jupyter**, which gives you interactive, usually web-based notebooks running
          on IPython kernels. Jupyter notebooks are JSON documents. They became the default
          environment for data work, and
          [not everyone is happy about that](https://www.youtube.com/watch?v=7jiPeIFXb6U).
        * **marimo**, which is what we'll be using. It's a notebook that is a plain
          Python file, and that re-runs the affected cells by itself. More on this in
          a moment.

        ---

        That covers how we got to notebooks. The other half of the story is how the
        tools inside them changed, which matters because a fair amount of advice you
        will find online is describing a Python that no longer exists.

        Jake VanderPlas gave a
        [keynote in 2017](https://pyvideo.org/pydata-seattle-2017/pydata-101.html) laying
        out the PyData stack as it stood then. It's a good hour if you ever want the
        prehistory, and it's on Canvas, though nothing today depends on your having seen
        it. What's more useful is what has happened since, because most of it lands
        somewhere in this course:

        1. **Type hints and static analysis.** Type hints (3.5) matured, with mypy,
           Pyright and Pydantic becoming standard, which addressed a traditional
           Python weakness in larger codebases.
        2. **A performance revolution.** **Polars** emerged as a faster alternative
           to pandas with a more consistent API. **DuckDB** brought fast analytical
           SQL directly into Python. Numba and JAX made JIT compilation accessible.
           CPython itself got 10–60% faster from 3.11 on, and free-threaded Python
           (PEP 703, 3.13) offers true parallelism. *We will use Polars and DuckDB
           later in the term.*
        3. **LLMs.** Transformers and HuggingFace became central; entirely new
           ecosystems grew around LangChain, LlamaIndex, and vector databases.
           Python became *the* language for AI application development, not just ML
           research. This is probably the biggest shift of the lot, since it changed
           *what* data scientists actually do.
        4. **Modern dataframes and Arrow.** Apache Arrow standardization enabled
           zero-copy data sharing, and moved thinking away from pandas'
           index-centric design toward something more SQL-like.
        5. **Notebook evolution.** Quarto for reproducible publishing; growing
           critique of notebook-first development; more tooling for `.py`
           workflows. *marimo is a direct product of this critique.*
        6. **Packaging and environments.** Poetry, uv, and rye addressing decades of
           pip/conda pain. *We use `uv`.*
        7. **Cloud-native data science.** Dask, Ray, and the Databricks/Snowflake
           Python integrations.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Your learning environment

        You're reading this inside marimo, and everything you need in order to run it
        is a single command, which works from anywhere on your machine once you've
        installed `uv`. The setup document on Canvas has the instructions for that.

        ```bash
        uvx marimo edit --sandbox SI_618_01_Introduction.py
        ```

        That one command downloads marimo, builds a throwaway environment containing
        the packages this notebook declares at the top of the file, and opens it, so
        there shouldn't be a virtual environment for you to create or accidentally
        break.

        If installing things locally isn't an option, every notebook is also
        available on [molab](https://molab.marimo.io/), which runs marimo in a browser
        tab without installing anything. You do have to sign in before it will run a
        notebook, and a Google account is the quickest way, and the links are on
        Canvas. It's worth reaching for if your laptop is fighting you, and then
        sorting out the local setup afterwards rather than during class.

        ### If you have never used a notebook before

        Plenty of you have only written Python as `.py` files in VS Code, run start to
        finish, printing things out to see what happened. That is a perfectly good way
        to write software, and it is a slightly awkward way to *explore data*, because
        you end up re-running the whole script every time you want to look at one more
        thing.

        A notebook splits a file into **cells**, which are chunks of code you can run
        one at a time, with the result shown underneath. Load a large dataset once,
        then poke at it twenty different ways without re-loading it. That is the whole
        idea, and it is why data work tends to happen in notebooks.

        The good news if plain `.py` files are where you're comfortable: **a marimo
        notebook is still a `.py` file.** Each cell is a function, and if you ever open
        one in a text editor it's ordinary Python, with nothing hidden in a format you
        can't read. You won't need to do that in this course, since marimo runs in your
        browser and that's where the work happens, but it's worth knowing that nothing
        is being kept from you.

        ### What makes marimo different

        **It's a Python file, not a special document.** What you're reading is valid
        Python, with no separate wrapper format and no saved outputs buried in it. It
        diffs cleanly in git, and `pytest` will run it directly, which is what lets the
        exercises below check themselves as you type.

        **Execution is reactive.** Change a cell, and every cell that depends on it
        re-runs straight away. You never have to remember which cells you have run, or
        in what order, and you can't end up looking at a number that was computed from
        data you have since changed.

        **A variable may only be defined in one cell.** This is the rule most likely to
        catch you out early on, and it follows from the previous one: if two cells both
        defined `df`, marimo would have no way to know which one is current. So it
        insists on one. When you run into it, you can prefix the name with an
        underscore, as in `_tmp`, which makes it local to that cell, or give it a
        distinct name such as `df_sensor`, or wrap the work in a function and return
        the result.

        *(If you have used Jupyter, this is the difference that matters most. There,
        you can define `df` in fifteen cells and whichever you ran last silently wins,
        which is the usual reason a notebook produces results nobody can reproduce.)*

        Have a play with the slider below. There's nothing to submit, it's just there
        so you can watch what happens downstream when you move it.
        """
    )
    return


@app.cell
def _(mo):
    demo_threshold = mo.ui.slider(400, 600, value=500, step=10, label="CO₂ threshold (ppm)")
    demo_threshold
    return (demo_threshold,)


@app.cell
def _(demo_threshold, mo):
    mo.md(
        f"""
        This cell didn't re-run itself. marimo re-ran it *for* you, because it reads
        `demo_threshold`, which you just changed.

        Current threshold: **{demo_threshold.value} ppm**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🚩 Block 1: Motivating pandas

        Before looking at what pandas does, it's worth feeling the problem it solves.
        Below is a small slice of readings from an [Aranet4](https://aranet.com/)
        sensor, recording carbon dioxide, temperature, humidity and atmospheric
        pressure every couple of minutes.

        It's stored the way data often arrives from an API, as a list of
        dictionaries with one per reading.
        """
    )
    return


@app.cell
def _():
    sensor_data = [
        {"Time": "1/19/2022 6:02:13 AM", "Carbon dioxide(ppm)": 490,
         "Temperature(C)": 16.2, "Relative humidity(%)": 32,
         "Atmospheric pressure(hPa)": 986},
        {"Time": "1/19/2022 6:04:13 AM", "Carbon dioxide(ppm)": 498,
         "Temperature(C)": 16.3, "Relative humidity(%)": 32,
         "Atmospheric pressure(hPa)": 986},
        {"Time": "1/19/2022 6:06:13 AM", "Carbon dioxide(ppm)": 491,
         "Temperature(C)": 16.4, "Relative humidity(%)": 32,
         "Atmospheric pressure(hPa)": 986},
        {"Time": "1/19/2022 6:08:13 AM", "Carbon dioxide(ppm)": 506,
         "Temperature(C)": 16.4, "Relative humidity(%)": 32,
         "Atmospheric pressure(hPa)": 986},
        {"Time": "1/19/2022 6:10:13 AM", "Carbon dioxide(ppm)": 501,
         "Temperature(C)": 16.5, "Relative humidity(%)": 32,
         "Atmospheric pressure(hPa)": 986},
        {"Time": "1/19/2022 6:12:13 AM", "Carbon dioxide(ppm)": 489,
         "Temperature(C)": 16.6, "Relative humidity(%)": 32,
         "Atmospheric pressure(hPa)": 986},
    ]
    return (sensor_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🚀 Challenge 1.1.1

        #### ✅ Task 1.1.1.1

        Have a look at the sample sensor data above, and list three questions you
        could ask about it. Write one per line in the string below, ending each with
        a question mark.
        """
    )
    return


@app.cell
def _():
    my_questions = """
    1.
    2.
    3.
    """
    return (my_questions,)


@app.cell(hide_code=True)
def _(my_questions):
    def test_task_1_1_1_1():
        _lines = [ln.strip() for ln in my_questions.strip().splitlines() if ln.strip()]
        assert len(_lines) >= 3, (
            "Write three questions in `my_questions`, one per line."
        )
        assert all(ln.endswith("?") for ln in _lines[:3]), (
            "Each line should be a question ending in '?'. "
            "Statements are hard to answer with data."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### ✅ Task 1.1.1.2

        Write a function that works out the mean carbon dioxide concentration, in
        parts per million, from `sensor_data`, rounding your answer to the nearest
        whole number.
        """
    )
    return


@app.cell
def _(sensor_data):
    def calculate_mean_co2(data: list[dict]) -> float:
        """Return the mean CO2 reading in ppm, rounded to the nearest whole number."""
        pass  # TODO: implement this

    calculate_mean_co2(sensor_data)
    return (calculate_mean_co2,)


@app.cell(hide_code=True)
def _(calculate_mean_co2, sensor_data):
    def test_task_1_1_1_2():
        _result = calculate_mean_co2(sensor_data)
        assert _result is not None, (
            "`calculate_mean_co2` returns None. Did you forget to `return`?"
        )
        assert _result == 496.0, (
            f"Expected 496.0, got {_result}. The raw mean is 495.83..., "
            "so this one hinges on the rounding."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🚀 Challenge 1.1.2

        #### ✅ Task 1.1.2.1

        Write a function that returns only the readings whose carbon dioxide
        concentration is greater than a `threshold` passed in as a parameter.
        """
    )
    return


@app.cell
def _():
    def filter_high_co2(data: list[dict], threshold: float) -> list[dict]:
        """Return the readings whose CO2 value is strictly greater than `threshold`."""
        pass  # TODO: implement this
    return (filter_high_co2,)


@app.cell(hide_code=True)
def _(filter_high_co2, sensor_data):
    def test_task_1_1_2_1():
        _high = filter_high_co2(sensor_data, 500)
        assert _high is not None, (
            "`filter_high_co2` returns None. Did you forget to `return`?"
        )
        assert isinstance(_high, list), (
            f"Expected a list of readings, got {type(_high).__name__}."
        )
        assert {r["Carbon dioxide(ppm)"] for r in _high} == {501, 506}, (
            f"Above 500 ppm there are two readings (501 and 506); you returned "
            f"{[r['Carbon dioxide(ppm)'] for r in _high]}."
        )
        assert len(filter_high_co2(sensor_data, 0)) == 6, (
            "A threshold of 0 should keep every reading."
        )
        assert len(filter_high_co2(sensor_data, 506)) == 0, (
            "The comparison should be strictly greater than, not >=."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### The same thing, in pandas

        You've just written a dozen or so lines of Python. Here's the equivalent work,
        once the data is sitting in a `DataFrame`.
        """
    )
    return


@app.cell
def _(pd, sensor_data):
    df = pd.DataFrame(sensor_data)
    df
    return (df,)


@app.cell
def _(df):
    df["Carbon dioxide(ppm)"].mean()
    return


@app.cell
def _(df):
    df[df["Carbon dioxide(ppm)"] > 500]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Two lines, no loops, and, rather more importantly, they read a lot like the
        question you were asking in the first place. That readability is most of the
        reason pandas ended up winning.

        ---
        ## ⏸️ END OF SESSION 1 — pick up here next class
        ---

        Nothing to submit today. Do leave the notebook somewhere you'll find it
        again, since we carry on in this same file on Wednesday, and you'll submit it
        at the end of that session.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 🚩 Block 2: Core pandas concepts

        ### What is pandas?

        pandas is a data manipulation library built on top of NumPy, offering fast
        and reasonably ergonomic data structures designed specifically for structured
        tabular data. It remains the default tool for data analysis in Python.

        There are two structures worth knowing about. A **DataFrame** is a
        two-dimensional table with labelled rows and columns, rather like a
        spreadsheet, except that each column can hold a different type and operations
        across whole rows or columns are fast. A **Series** is a one-dimensional
        labelled array, and a single column of a DataFrame is a Series, so you can
        think of a DataFrame as several Series sharing an index.

        What that buys you is fast operations over large datasets, built-in tools for
        cleaning data and handling missing values, grouping and aggregation that
        would otherwise be tedious, decent integration with the visualization
        libraries, and readers and writers for CSV, Excel, JSON, Parquet and SQL
        among others.

        A few terms that will keep coming up: the *index* holds the row labels,
        *columns* the column labels, *loc* and *iloc* do selection, *groupby* splits
        data into groups, *aggregation* produces summary statistics, and *filtering*
        selects rows by condition.

        ❗️ The goal here isn't to memorise the pandas API, which is enormous. It's to
        understand the core concepts well enough that you can find the tool you need
        for whatever task is in front of you.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### DataFrame basics

        #### Creating DataFrames

        A DataFrame can be built from all sorts of Python structures, though in
        practice you'll usually be reading one from a file.

        Here are two ways of creating the *same* DataFrame. The first treats the data
        row-wise, as a list of dictionaries with each dictionary a row, while the
        second treats it column-wise, as a dictionary of lists with each list a
        column.
        """
    )
    return


@app.cell
def _(pd):
    df1 = pd.DataFrame([{"A": 1, "B": 2}, {"A": 2, "B": 3}, {"A": 3, "B": 4}])
    df2 = pd.DataFrame({"A": [1, 2, 3], "B": [2, 3, 4]})
    assert df1.equals(df2), "DataFrames are not equal"
    df1
    return (df1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Basic selection: `df['column']`

        Select a column with subscript notation. The result is a Series.
        """
    )
    return


@app.cell
def _(df1):
    df1["A"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        That's terse and convenient, though it's worth getting comfortable with
        `.loc` as well. Note that `.loc` is an *attribute* rather than a method, so it
        takes square brackets rather than parentheses. Its first argument specifies
        the rows, where a bare `:` acts as a wildcard meaning all of them, and the
        second specifies the columns.
        """
    )
    return


@app.cell
def _(df1):
    df1.loc[:, "A"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Viewing data: `.head()`, `.info()`, `.describe()`

        Let's make a slightly larger demo DataFrame. Whenever you get hold of data,
        the first thing to do is look at it.
        """
    )
    return


@app.cell
def _(pd):
    df3 = pd.DataFrame({"A": [1, 2, 3] * 4, "B": [2, 3, 4] * 4})
    df3
    return (df3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        `.head()` shows the first few rows and `.tail()` the last few, while
        `.sample()` takes a random selection. The first two default to five rows and
        `.sample()` to one, and you can pass a number to change that.
        """
    )
    return


@app.cell
def _(df3):
    df3.head(3)
    return


@app.cell
def _(df3):
    df3.sample(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""`.info()` reports the structure, meaning column names, types and non-null counts:""")
    return


@app.cell
def _(df3):
    df3.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""`.describe()` generates descriptive statistics:""")
    return


@app.cell
def _(df3):
    df3.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ❗️ By default `.describe()` only covers the numeric columns, and you can pass
        `include="all"` to cover every column instead. It returns a DataFrame, which
        is handy when you want to pull a value back out programmatically.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Essential operations

        #### Filtering with boolean masks

        Filtering is among the most common things you'll be doing. Back to the small
        sensor DataFrame, `df`:
        """
    )
    return


@app.cell
def _(df):
    df[df["Carbon dioxide(ppm)"] > 500]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The expression inside the brackets, `df["Carbon dioxide(ppm)"] > 500`, is
        itself a Series of booleans, one per row, and indexing with it keeps the rows
        where the value came out `True`. We'll go into this in more depth next class.

        The `.query()` method does much the same thing in a more SQL-like style, and
        note the backticks around a column name containing special characters:
        """
    )
    return


@app.cell
def _(df):
    df.query("`Carbon dioxide(ppm)` > 500")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Basic aggregations

        `.describe()` gives you a batch of statistics all at once, but often you want
        to ask for exactly one, and `.min()`, `.max()`, `.median()`, `.mean()`,
        `.std()`, `.var()` and the rest all follow the same form.
        """
    )
    return


@app.cell
def _(df):
    df["Carbon dioxide(ppm)"].median()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Simple `groupby` operations

        It's often useful to split data into groups and summarise each one. Grouping
        is normally done on a categorical variable rather than a continuous one, so
        the data we've used so far doesn't make much of a demonstration. Let's add a
        categorical column to `df3`.

        ❗️ Note the marimo idiom here. Rather than mutating `df3` in place with
        `df3["C"] = ...`, we use `.assign()` to produce a new DataFrame called `df4`.
        Mutating a value in one cell that another cell also reads is exactly the
        hidden-state problem marimo exists to prevent, and `.assign()` steps neatly
        around it. It's a good habit in Jupyter too, it just isn't enforced there.
        """
    )
    return


@app.cell
def _(df3):
    df4 = df3.assign(C=["maize", "blue"] * 6)
    df4
    return (df4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now group by that new column and look at the group means:""")
    return


@app.cell
def _(df4):
    df4.groupby("C").mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🚩 Block 3: Applied practice

        ### 🚀 Challenge 1.3.1

        So far you've seen six readings, whereas the full sensor file covers about a
        week. We load it straight from a URL, so there's nothing to download and no
        file paths to get wrong.

        This is how data works throughout the course, with notebooks fetching
        whatever they need, and nothing large stored in the course repository.
        """
    )
    return


@app.cell
def _(pd):
    SENSOR_URL = "https://raw.githubusercontent.com/umsi-data-science/data/main/aranet4.csv"
    sensor_full = pd.read_csv(SENSOR_URL)
    sensor_full
    return (sensor_full,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### ✅ Task 1.3.1.1

        Have a look at the first few rows of `sensor_full`. Does everything seem all
        right with the data? Write what you notice in `data_check` below, in at least
        one full sentence.

        Two things worth checking in particular: what type is the `Time` column, and
        does the temperature column have the name you were expecting?
        """
    )
    return


@app.cell
def _():
    data_check = ""
    return (data_check,)


@app.cell(hide_code=True)
def _(data_check):
    def test_task_1_3_1_1():
        assert data_check.strip(), (
            "Write your observations in `data_check`."
        )
        assert len(data_check.strip()) >= 40, (
            "Say a bit more, ideally a full sentence about what you noticed."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### ✅ Task 1.3.1.2

        Now that you can see the whole dataset rather than six rows of it, come up
        with three questions you think would be interesting to ask, one per line, each
        ending in a question mark.
        """
    )
    return


@app.cell
def _():
    my_questions_full = """
    1.
    2.
    3.
    """
    return (my_questions_full,)


@app.cell(hide_code=True)
def _(my_questions_full):
    def test_task_1_3_1_2():
        _lines = [ln.strip() for ln in my_questions_full.strip().splitlines() if ln.strip()]
        assert len(_lines) >= 3, (
            "Write three questions in `my_questions_full`, one per line."
        )
        assert all(ln.endswith("?") for ln in _lines[:3]), (
            "Each line should be a question ending in '?'."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### ✅ Task 1.3.1.3

        What was the maximum temperature, and when did it occur?

        Assign the temperature to `max_temp`, and the time at which it occurred to
        `max_temp_time`. Then, in the markdown cell that follows, state your result in
        a sentence. Use that cell to explain the *result* rather than the code.

        💡 `.idxmax()` gives you the index label of the largest value, which you can
        then feed to `.loc`. You'll also need to convert `Time` from strings into real
        timestamps, which is what `pd.to_datetime()` is for.
        """
    )
    return


@app.cell
def _():
    # Your code here.
    max_temp = None
    max_temp_time = None
    return max_temp, max_temp_time


@app.cell(hide_code=True)
def _(max_temp, max_temp_time, pd):
    def test_task_1_3_1_3():
        assert max_temp is not None, "Assign the maximum temperature to `max_temp`."
        assert max_temp_time is not None, (
            "Assign the time of the maximum to `max_temp_time`."
        )
        assert round(float(max_temp), 1) == 22.2, (
            f"Expected a maximum of 22.2 °C, got {max_temp}. Check the column name, "
            "which contains a degree symbol."
        )
        assert pd.Timestamp(max_temp_time) == pd.Timestamp("2022-01-21 12:51:13"), (
            f"Expected 2022-01-21 12:51:13, got {max_temp_time}. Did you convert "
            "`Time` with pd.to_datetime()?"
        )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        *(Replace this text with a sentence stating the maximum temperature and
        when it occurred.)*
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### ✅ Task 1.3.1.4

        Which day had the highest mean carbon dioxide concentration, and what was
        that mean?

        Assign the date to `highest_co2_day`, and the mean to `highest_co2_mean`.

        💡 You can group by the *date part* of a datetime column using `.dt.date`, and
        then apply what you learned about `groupby` back in Block 2.
        """
    )
    return


@app.cell
def _():
    # Your code here.
    highest_co2_day = None
    highest_co2_mean = None
    return highest_co2_day, highest_co2_mean


@app.cell(hide_code=True)
def _(highest_co2_day, highest_co2_mean):
    def test_task_1_3_1_4():
        assert highest_co2_day is not None, "Assign the date to `highest_co2_day`."
        assert highest_co2_mean is not None, (
            "Assign the mean CO2 for that day to `highest_co2_mean`."
        )
        assert str(highest_co2_day)[:10] == "2022-01-18", (
            f"Expected 2022-01-18, got {highest_co2_day}. Group by the date part "
            "of `Time`, rather than the full timestamp, or every group has just one row."
        )
        assert round(float(highest_co2_mean), 1) == 855.9, (
            f"Expected about 855.9 ppm, got {highest_co2_mean}."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 😎 Finished early?

        Have a go at answering one of the questions you wrote in Task 1.3.1.2, adding
        cells below as you need them. Anything here is a bonus rather than a
        requirement.

        One worth starting with: the answer to Task 1.3.1.4 turns out to be the
        *first* day in the file. Is that a real finding, or an artefact of how much of
        that day actually got recorded? `.value_counts()` on the date column should
        tell you.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        ## 🏁 END OF NOTEBOOK

        **Submit by the end of today's session.** Two files, both to Canvas:

        1. This notebook, renamed `SI618_01_<uniqname>.py`
        2. An HTML export of it:
           ```bash
           uvx marimo export html --sandbox SI618_01_<uniqname>.py -o SI618_01_<uniqname>.html
           ```

        Before submitting, check that every test above is passing. marimo runs them as
        you work, so there shouldn't be any surprises waiting.

        ❗️ Late in-class work is not accepted for credit.
        """
    )
    return


if __name__ == "__main__":
    app.run()
