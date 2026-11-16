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
    # SI 618 - Homework 6: Predicting credit card default

    **Name:**
    **Uniqname:**

    This homework is due **Monday, November 23, before class (3:30 PM)**. The full spec is
    in `README.md`, and the rubric is in `RUBRIC.md`. Please read both before you
    start.

    Rename this file `SI618_HW06_<uniqname>.py` before you submit, and upload
    its HTML export alongside it.

    ### Working in marimo

    - A variable can be defined in only one cell, so give each new result a
      new name, such as `auc_depth_6`, or prefix a name with `_` to keep it
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
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (RocCurveDisplay, precision_score, recall_score,
                                 roc_auc_score)
    from sklearn.model_selection import (cross_val_predict, cross_val_score,
                                         cross_validate, train_test_split)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    return mo, np, pd


@app.cell
def _():
    DATA_URL = (
        "https://raw.githubusercontent.com/umsi-data-science/data/main/"
        "credit_default.csv"
    )
    # Pass this to .rename(columns=...) when you load the file.
    RENAME = {"PAY_0": "PAY_1", "default payment next month": "default"}
    # The maximum depths to cross-validate in 3.1. None sets no maximum.
    DEPTHS = [2, 3, 4, 5, 6, 8, 10, None]
    # The values of min_samples_leaf to cross-validate in 3.2.
    LEAF_SIZES = [1, 5, 10, 20, 50, 100]
    # The thresholds to compare in 4.1.
    THRESHOLDS = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    return DEPTHS, LEAF_SIZES, THRESHOLDS


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Look at the data (15 points)

    ### 1.1 Load the card holders (5)
    """)
    return


@app.cell
def _():
    # Load DATA_URL into `credit`, renaming the columns with RENAME. Show how many
    # card holders defaulted, and compute the accuracy of predicting no default
    # for every card holder.
    credit = None
    baseline = None
    return baseline, credit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2 Codes the documentation does not list (10)
    """)
    return


@app.cell
def _():
    # Show how many card holders have each value of EDUCATION, MARRIAGE and PAY_1.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: the undocumented values in each column, how many card
    holders have them, and what you will do about them, with a reason.*
    """)
    return


@app.cell
def _():
    # Apply your decisions to a copy of `credit`, and use `credit_clean` from here
    # on. A variable can be defined in only one cell, so `credit` itself stays as
    # loaded.
    credit_clean = None
    return (credit_clean,)


@app.cell(hide_code=True)
def _(baseline, credit, credit_clean, pd):
    def test_part_1():
        assert isinstance(credit_clean, pd.DataFrame), (
            "`credit_clean` should be a DataFrame: `credit` with your decisions from 1.2 applied."
        )
        assert isinstance(credit, pd.DataFrame), "`credit` should be a DataFrame."
        assert len(credit) == 30000, (
            "`credit` should have 30,000 rows, one per card holder, as loaded."
        )
        assert "default" in credit.columns and "PAY_1" in credit.columns, (
            "Rename the columns with RENAME when you load the file."
        )
        assert isinstance(baseline, float), "`baseline` should be a single number."
        assert 0.5 <= baseline <= 1, (
            "The baseline predicts no default for everyone, the more common class, "
            "so it is at least 0.5."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Logistic regression (20 points)

    ### 2.1 Split (3)
    """)
    return


@app.cell
def _():
    # Split `credit_clean`, putting a quarter of the card holders in the test set,
    # stratified by `default`, with random_state=618.
    train_credit = None
    test_credit = None
    return test_credit, train_credit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 Accuracy and AUC (7)
    """)
    return


@app.cell
def _():
    # Cross-validate a pipeline of StandardScaler and LogisticRegression with five
    # folds on the training set, scoring by accuracy and by AUC ("roc_auc"). Use
    # every column except ID and default as a feature.
    logistic_accuracy = None
    logistic_auc = None
    return logistic_accuracy, logistic_auc


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: how the accuracy compares with the baseline, and why AUC
    is the better measure for comparing models on these data.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 Sex, marital status and age (10)
    """)
    return


@app.cell
def _():
    # Cross-validate the same pipeline without SEX, MARRIAGE and AGE, scoring by
    # AUC. Then set FEATURES_USED to the list of features you will use from here on.
    logistic_auc_without = None
    FEATURES_USED = None
    return FEATURES_USED, logistic_auc_without


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: whether your models will use these three columns, and why.*
    """)
    return


@app.cell(hide_code=True)
def _(
    FEATURES_USED,
    logistic_accuracy,
    logistic_auc,
    logistic_auc_without,
    pd,
    test_credit,
    train_credit,
):
    def test_part_2():
        assert isinstance(train_credit, pd.DataFrame) and isinstance(test_credit, pd.DataFrame), (
            "`train_credit` and `test_credit` should be DataFrames."
        )
        _share = len(test_credit) / (len(train_credit) + len(test_credit))
        assert abs(_share - 0.25) < 0.001, (
            "A quarter of the card holders should be in the test set. Check `test_size`."
        )
        for _name, _value in [("logistic_accuracy", logistic_accuracy),
                              ("logistic_auc", logistic_auc),
                              ("logistic_auc_without", logistic_auc_without)]:
            assert isinstance(_value, float) and 0 <= _value <= 1, (
                f"`{_name}` should be a single number between 0 and 1, the mean over the folds."
            )
        assert isinstance(FEATURES_USED, list) and FEATURES_USED, (
            "`FEATURES_USED` should be a list of column names."
        )
        assert set(FEATURES_USED) <= set(train_credit.columns), (
            "Every name in `FEATURES_USED` should be a column of `train_credit`."
        )
        assert "default" not in FEATURES_USED and "ID" not in FEATURES_USED, (
            "`FEATURES_USED` should not include `default`, which is the target, or `ID`."
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Trees and forests (25 points)

    ### 3.1 The depth of a tree (7)
    """)
    return


@app.cell
def _():
    # Cross-validate a DecisionTreeClassifier with random_state=618 on
    # FEATURES_USED, with five folds and scoring by AUC, for every depth in DEPTHS.
    # Store the mean AUC for each depth in `depth_table`, in the order of DEPTHS.
    depth_table = None
    best_depth = None
    return best_depth, depth_table


@app.cell
def _():
    # Plot the mean AUC against the depth.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: why you chose `best_depth`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2 The size of a forest's leaves (9)
    """)
    return


@app.cell
def _():
    # Cross-validate a RandomForestClassifier with n_estimators=300,
    # random_state=618 and n_jobs=-1, with five folds and scoring by AUC, for every
    # value of min_samples_leaf in LEAF_SIZES. Each value takes a few seconds.
    leaf_table = None
    best_leaf = None
    return best_leaf, leaf_table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: why you chose `best_leaf`, and why the forest's AUC changes
    with the size of its leaves, using 3.1.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3 Compare and choose (9)
    """)
    return


@app.cell
def _():
    # Use cross_val_predict with five folds and method="predict_proba" to get the
    # cross-validated probability of default from each of the three models. Plot
    # the three ROC curves on one figure, and show the three AUCs in one table.
    # Store the probabilities from the model you choose in `chosen_probabilities`.
    chosen_probabilities = None
    return (chosen_probabilities,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: which model you chose, and why.*
    """)
    return


@app.cell(hide_code=True)
def _(
    DEPTHS,
    LEAF_SIZES,
    best_depth,
    best_leaf,
    chosen_probabilities,
    depth_table,
    leaf_table,
    np,
    train_credit,
):
    def test_part_3():
        assert depth_table is not None and len(depth_table) == len(DEPTHS), (
            "`depth_table` should have one value for each depth in DEPTHS."
        )
        assert best_depth in DEPTHS, "`best_depth` should be one of the values in DEPTHS."
        assert leaf_table is not None and len(leaf_table) == len(LEAF_SIZES), (
            "`leaf_table` should have one value for each size in LEAF_SIZES."
        )
        assert best_leaf in LEAF_SIZES, "`best_leaf` should be one of the values in LEAF_SIZES."
        _p = np.asarray(chosen_probabilities)
        assert _p.ndim == 1 and len(_p) == len(train_credit), (
            "`chosen_probabilities` should have one probability per training card holder. "
            "Keep only the column for default, `[:, 1]`."
        )
        assert ((_p >= 0) & (_p <= 1)).all(), "Probabilities should lie between 0 and 1."

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 4: A threshold, and one test (20 points)

    ### 4.1 Choose a threshold (10)
    """)
    return


@app.cell
def _():
    # For every threshold in THRESHOLDS, compute from `chosen_probabilities` the
    # share of training card holders called, and the precision and recall of
    # calling them. Make `threshold_table` a DataFrame indexed by threshold, with
    # the columns "called", "precision" and "recall".
    threshold_table = None
    chosen_threshold = None
    return chosen_threshold, threshold_table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: what the precision and recall at `chosen_threshold` would
    mean for the bank's callers.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 Test once (10)
    """)
    return


@app.cell
def _():
    # Fit your chosen model to all the training card holders, and compute on the
    # test card holders its AUC, and the share called, the precision and the
    # recall at `chosen_threshold`. Make `test_results` a dict with the keys
    # "auc", "called", "precision" and "recall".
    test_results = None
    return (test_results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answer here: how each test number compares with its cross-validated
    estimate, and which numbers you would report.*
    """)
    return


@app.cell(hide_code=True)
def _(THRESHOLDS, chosen_threshold, pd, test_results, threshold_table):
    def test_part_4():
        assert isinstance(threshold_table, pd.DataFrame), "`threshold_table` should be a DataFrame."
        assert len(threshold_table) == len(THRESHOLDS), (
            "`threshold_table` should have one row for each threshold in THRESHOLDS."
        )
        assert {"called", "precision", "recall"} <= set(threshold_table.columns), (
            '`threshold_table` needs the columns "called", "precision" and "recall".'
        )
        assert chosen_threshold in THRESHOLDS, (
            "`chosen_threshold` should be one of the values in THRESHOLDS."
        )
        assert isinstance(test_results, dict), "`test_results` should be a dict."
        assert set(test_results) == {"auc", "called", "precision", "recall"}, (
            '`test_results` should have exactly the keys "auc", "called", "precision" and "recall".'
        )
        for _key, _value in test_results.items():
            assert 0 <= _value <= 1, f'`test_results["{_key}"]` should be between 0 and 1.'

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 5: Summary for a credit manager (20 points)

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
    2. Rename this file `SI618_HW06_<uniqname>.py`.
    3. Export it:
       ```bash
       uvx marimo export html --sandbox SI618_HW06_<uniqname>.py -o SI618_HW06_<uniqname>.html
       ```
    4. Upload both files to Canvas.
    """)
    return


if __name__ == "__main__":
    app.run()
