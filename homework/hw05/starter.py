# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "matplotlib==3.11.1",
#     "scikit-learn==1.9.0",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 618 - Homework 5: Predicting red wine ratings

    **Name:**
    **Uniqname:**

    This homework is due **Monday, November 9, before class (3:30 PM)**. The full spec is in
    `README.md`, and the rubric is in `RUBRIC.md`. Please read both before you
    start.

    Rename this file `SI618_HW05_<uniqname>.py` before you submit, and upload
    its HTML export alongside it.

    ### Working in marimo

    - A variable can be defined in only one cell, so give each new result a
      new name, such as `cv_scores_k5`, or prefix a name with `_` to keep it
      inside its cell.
    - Add as many cells as you need, wherever you need them.
    - For written answers, edit the markdown cells marked *Your answer here*.
    - The tests at the end of each part check that your work has the right
      shape, not that it is right, so a green test does not mean that a part
      is complete.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    return mo, np, pd


@app.cell
def _():
    DATA_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "winequality-red.csv"
    )
    FEATURES = [
        "fixed acidity", "volatile acidity", "citric acid", "residual sugar",
        "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density",
        "pH", "sulphates", "alcohol",
    ]
    # These are the values of k to cross-validate in Parts 3 and 4.
    K_VALUES = [1, 3, 5, 9, 15, 25, 41, 61, 81]
    return FEATURES, K_VALUES


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Look at the data (15 points)

    ### 1.1 Load the wines (5)
    """)
    return


@app.cell
def _():
    # Load DATA_URL into `wines`, and add a column `good`: True for a rating of 6
    # or more. Then show how many wines have each rating, and how many are good.
    wines = None
    return (wines,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2 Baseline (4)
    """)
    return


@app.cell
def _():
    # Compute the accuracy of always predicting the more common class.
    baseline = None
    return (baseline,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: why every model has to be compared with the baseline.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3 Scales of the measurements (6)
    """)
    return


@app.cell
def _():
    # Show the mean, standard deviation, minimum and maximum of each of FEATURES.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: which measurements you expect to decide unscaled
    distances, and why.*
    """)
    return


@app.cell(hide_code=True)
def _(baseline, pd, wines):
    def test_part_1():
        assert isinstance(wines, pd.DataFrame), "`wines` should be a DataFrame."
        assert len(wines) == 1599, (
            "`wines` should have 1,599 rows, one per wine. Keep the duplicates for now."
        )
        assert "good" in wines.columns, "`wines` needs a `good` column."
        assert wines["good"].dtype == bool, "`good` should be True or False for every wine."
        assert isinstance(baseline, float), "`baseline` should be a single number."
        assert 0.5 <= baseline <= 1, (
            "The baseline predicts the more common class, so it is at least 0.5."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Scaling (20 points)

    ### 2.1 Split (4)
    """)
    return


@app.cell
def _():
    # Put a quarter of the wines in the test set, stratified by `good`, with
    # random_state=618.
    train_wines = None
    test_wines = None
    return test_wines, train_wines


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 Share of the distance by measurement (8)
    """)
    return


@app.cell
def _():
    # Compute each measurement's share of the summed variances of all eleven in
    # the training set, and sort the shares from largest to smallest.
    variance_share = None
    return (variance_share,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: whether `variance_share` confirms what you expected in 1.3.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 Unscaled against scaled (8)
    """)
    return


@app.cell
def _():
    # Fit k-NN with k = 5 to the training wines, once unscaled and once in a
    # pipeline that standardises first, and compute both accuracies on the test
    # wines.
    unscaled_accuracy = None
    scaled_accuracy = None
    return scaled_accuracy, unscaled_accuracy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: why the two accuracies differ, using 2.2.*
    """)
    return


@app.cell(hide_code=True)
def _(
    FEATURES,
    pd,
    scaled_accuracy,
    test_wines,
    train_wines,
    unscaled_accuracy,
    variance_share,
):
    def test_part_2():
        assert isinstance(train_wines, pd.DataFrame) and isinstance(test_wines, pd.DataFrame), (
            "`train_wines` and `test_wines` should be DataFrames."
        )
        assert len(test_wines) == 400, (
            "The test set should have 400 wines, a quarter of 1,599 rounded up. Check `test_size`."
        )
        assert isinstance(variance_share, pd.Series), "`variance_share` should be a Series."
        assert sorted(variance_share.index) == sorted(FEATURES), (
            "`variance_share` should have one value for each of the eleven measurements."
        )
        assert abs(variance_share.sum() - 1) < 1e-6, (
            "The shares should add up to 1. Divide each variance by the sum of all eleven."
        )
        assert variance_share.is_monotonic_decreasing, "Sort `variance_share` from largest to smallest."
        for _name, _value in [("unscaled_accuracy", unscaled_accuracy),
                              ("scaled_accuracy", scaled_accuracy)]:
            assert isinstance(_value, float) and 0 <= _value <= 1, (
                f"`{_name}` should be an accuracy between 0 and 1."
            )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Choosing k (20 points)

    ### 3.1 Cross-validate (10)
    """)
    return


@app.cell
def _():
    # Cross-validate the scaling pipeline with five folds on the training wines,
    # for every k in K_VALUES. Index `cv_table` by k, with a column `mean`.
    cv_table = None
    return (cv_table,)


@app.cell
def _():
    # Plot the mean accuracy against k.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2 Choose and test once (10)
    """)
    return


@app.cell
def _():
    # Fit the pipeline with `best_k` to all the training wines, and compute its
    # accuracy on the test wines.
    best_k = None
    final_accuracy = None
    return best_k, final_accuracy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: why you chose `best_k`, and how `final_accuracy` compares
    with the baseline and with the cross-validated estimate.*
    """)
    return


@app.cell(hide_code=True)
def _(K_VALUES, best_k, cv_table, final_accuracy, pd):
    def test_part_3():
        assert isinstance(cv_table, pd.DataFrame), "`cv_table` should be a DataFrame."
        assert list(cv_table.index) == K_VALUES, (
            "`cv_table` should have one row for each k in K_VALUES, indexed by k, in order."
        )
        assert "mean" in cv_table.columns, "`cv_table` needs a `mean` column."
        assert best_k in K_VALUES, "`best_k` should be one of the values in K_VALUES."
        assert isinstance(final_accuracy, float) and 0 <= final_accuracy <= 1, (
            "`final_accuracy` should be an accuracy between 0 and 1."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: Duplicates (25 points)

    ### 4.1 Find them (6)
    """)
    return


@app.cell
def _():
    # Count the rows that are identical, in every column, to an earlier row. Then
    # show two or three groups of identical rows.
    n_duplicates = None
    return (n_duplicates,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: what you think the duplicates are, and why.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 Effect on k = 1 (9)
    """)
    return


@app.cell
def _():
    # Count the test wines that have an identical wine in the training set.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: how the duplicates change the cross-validated accuracy for
    small values of k, and what they do to the test accuracy.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3 Without the duplicates (10)
    """)
    return


@app.cell
def _():
    # Drop the duplicates, keeping the first of each group. Then repeat 2.1, 3.1
    # and 3.2 on `wines_unique`, with the same split settings.
    wines_unique = None
    cv_table_unique = None
    best_k_unique = None
    final_accuracy_unique = None
    return best_k_unique, cv_table_unique, final_accuracy_unique, wines_unique


@app.cell
def _():
    # Show both cross-validation curves on one plot, and the two baselines, the
    # two choices of k and the two test accuracies in one table.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: which test accuracy you would report for this model, and
    why.*
    """)
    return


@app.cell(hide_code=True)
def _(
    K_VALUES,
    best_k_unique,
    cv_table_unique,
    final_accuracy_unique,
    n_duplicates,
    np,
    pd,
    wines,
    wines_unique,
):
    def test_part_4():
        assert isinstance(n_duplicates, (int, np.integer)), (
            "`n_duplicates` should be a single whole number."
        )
        assert isinstance(wines_unique, pd.DataFrame), "`wines_unique` should be a DataFrame."
        assert not wines_unique.duplicated().any(), "`wines_unique` still contains duplicate rows."
        assert len(wines_unique) == len(wines) - n_duplicates, (
            "`wines_unique` should have one row fewer than `wines` for each duplicate."
        )
        assert isinstance(cv_table_unique, pd.DataFrame), "`cv_table_unique` should be a DataFrame."
        assert list(cv_table_unique.index) == K_VALUES, (
            "`cv_table_unique` should have one row for each k in K_VALUES, indexed by k, in order."
        )
        assert best_k_unique in K_VALUES, "`best_k_unique` should be one of the values in K_VALUES."
        assert isinstance(final_accuracy_unique, float) and 0 <= final_accuracy_unique <= 1, (
            "`final_accuracy_unique` should be an accuracy between 0 and 1."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Summary for a winemaker (20 points)

    - Question:
    - Finding:
    - Evidence:
        -
        -
    - Limits:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## AI attribution

    *If you used generative AI in a substantial way, say what you used and what
    it did. Otherwise, write "None".*

    ---
    ## Before you submit

    1. Make sure that every cell has run successfully.
    2. Rename this file `SI618_HW05_<uniqname>.py`.
    3. Export it:
       ```bash
       uvx marimo export html --sandbox SI618_HW05_<uniqname>.py -o SI618_HW05_<uniqname>.html
       ```
    4. Upload both files to Canvas.
    """)
    return


if __name__ == "__main__":
    app.run()
