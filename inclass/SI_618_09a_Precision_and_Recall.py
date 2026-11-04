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
def title(mo):
    mo.md(r"""
    # SI 618 - 09a: precision, recall and thresholds

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 18 (Wed Nov 4)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.11.04.1.CT

    ---

    ## Today you will be able to

    - Name the two kinds of mistake a classifier can make, and read them from a
      confusion matrix
    - Compute precision and recall by hand and with scikit-learn, and explain why
      accuracy alone can hide the mistake that matters most
    - Explain what k-NN's `predict_proba` returns, and how moving the threshold
      trades precision against recall
    - Choose a threshold from cross-validation on the training set, and test it once

    ## Reading

    Géron, on classification, in particular the confusion matrix, precision and
    recall, and the precision/recall trade-off.

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Where we left off | 10 |
    | The tumours | 7 |
    | Two kinds of mistake | 10 |
    | Precision and recall | 15 |
    | Thresholds | 15 |
    | Choosing a threshold | 8 |
    """)
    return


@app.cell
def imports():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.datasets import load_breast_cancer
    from sklearn.metrics import (ConfusionMatrixDisplay, PrecisionRecallDisplay,
                                 classification_report, precision_score, recall_score)
    from sklearn.model_selection import cross_val_predict, train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    return (
        ConfusionMatrixDisplay,
        KNeighborsClassifier,
        PrecisionRecallDisplay,
        StandardScaler,
        classification_report,
        cross_val_predict,
        load_breast_cancer,
        make_pipeline,
        mo,
        np,
        pd,
        plt,
        precision_score,
        recall_score,
        train_test_split,
    )


@app.cell(hide_code=True)
def recap(mo):
    mo.md(r"""
    ---
    ## Where we left off

    On Monday, notebook 08b standardised the penguins' measurements in a pipeline,
    and chose k by cross-validation on the training set before testing once. Many
    answers to the last two questions on Monday's sheet were incomplete, so we start
    by going over them again.

    ### Standardising before the split

    Question 4 described a classmate who standardises all 342 penguins and then
    splits them into a training set and a test set. The means and standard
    deviations then include the test penguins, so information from the test set
    reaches the model before it is tested, which is called *data leakage*. The test
    set is no longer unseen, and its accuracy is no longer a fair estimate for new
    penguins. A pipeline avoids this because its `.fit` fits the scaler to the
    training set only, and its `.predict` standardises the test penguins with the
    training set's means and standard deviations.

    Two other answers appeared on several sheets, and both are mistaken:

    - Some answers said that the test set should be standardised with its own mean
      and standard deviation. It should be standardised with the training set's,
      because otherwise the same bill length would become a different number in the
      two sets, and because a single new penguin has no mean of its own.
    - Some answers described a pipeline as cross-validation. A pipeline keeps the
      scaler and the model together, so that they are fitted and applied as one
      model. Cross-validation estimates a model's accuracy by fitting it to several
      groups of folds, and the model it fits may or may not be a pipeline.

    ### Choosing k and reporting accuracy

    Question 5 gave the following results.

    | k | Mean cross-validation accuracy | Test accuracy |
    |---:|---:|---:|
    | 7 | 93.4% | 94.2% |
    | 15 | 94.5% | 90.7% |
    | 41 | 93.0% | 94.2% |

    The two columns have different jobs:

    | Step | Data used | Result |
    |---|---|---|
    | Choose k | Cross-validation on the training set | k = 15, with 94.5% |
    | Report the accuracy | The test set, used once | 90.7% |

    Choosing k = 7 or 41 because they score 94.2% on the test set would use the test
    set to make a choice, and 94.2% would then overstate how well the model will do
    on new penguins, because k was picked to suit those particular test penguins.
    The 94.5% is not reported either, because it was used to choose k, and the
    highest of several estimates tends to be too high. The 90.7% is the lowest of
    the three, and it is the only one that comes from penguins that played no part
    in any choice.

    ### Today

    Every model so far has been measured by its accuracy, the share of the test
    cases it gets right. Accuracy counts every mistake the same. Calling a Chinstrap penguin an Adelie is
    no worse than the reverse, but in many uses of a classifier one kind of mistake
    costs far more than the other. Today's data come from a medical test, where
    that is the case.
    """)
    return


@app.cell(hide_code=True)
def tumours_intro(mo):
    mo.md(r"""
    ---
    ## The tumours

    The Wisconsin breast cancer data describe 569 breast tumours, each sampled with a
    fine needle and photographed under a microscope. For each image, ten
    measurements were taken of the cell nuclei, such as their radius, area and
    smoothness, and each is recorded three times: as the mean over the nuclei in the
    image, as its standard error, and as the mean of the three largest values,
    labelled "worst", which makes 30 features. Each tumour was later diagnosed as
    malignant (cancer) or benign (not cancer).

    The data come with scikit-learn. Its label is 0 for malignant and 1 for benign,
    so we replace it with a column `malignant` that is `True` for a malignant
    tumour.
    """)
    return


@app.cell
def load_tumours(load_breast_cancer):
    _data = load_breast_cancer(as_frame=True)
    FEATURES = list(_data.feature_names)
    tumours = (_data.frame
               .assign(malignant=_data.frame["target"] == 0)
               .drop(columns="target"))
    tumours.head()
    return FEATURES, tumours


@app.cell
def _(tumours):
    tumours[["mean radius", "mean area", "mean smoothness", "mean concave points"]].describe().round(3)
    return


@app.cell(hide_code=True)
def tumours_reading(mo):
    mo.md(r"""
    The four columns above, out of 30, are on very different scales: mean area is
    in the hundreds, and mean smoothness is about 0.1. As with the penguins, k-NN
    needs the features standardised, so every model today is a pipeline.

    The share of tumours that are malignant is shown below.
    """)
    return


@app.cell
def _(tumours):
    tumours["malignant"].value_counts(normalize=True).round(3)
    return


@app.cell
def make_split(FEATURES, train_test_split, tumours):
    train_tumours, test_tumours = train_test_split(
        tumours, test_size=0.25, stratify=tumours["malignant"], random_state=618)

    X_train, y_train = train_tumours[FEATURES], train_tumours["malignant"]
    X_test, y_test = test_tumours[FEATURES], test_tumours["malignant"]
    len(train_tumours), len(test_tumours), y_test.sum()
    return X_test, X_train, y_test, y_train


@app.cell(hide_code=True)
def accuracy_intro(mo):
    mo.md(r"""
    The split gives 426 training tumours and 143 test tumours, 53 of which are
    malignant. We fit the same pipeline as on Monday, with k = 5, to all 30
    features.
    """)
    return


@app.cell
def fit_pipeline(
    KNeighborsClassifier,
    StandardScaler,
    X_test,
    X_train,
    make_pipeline,
    y_test,
    y_train,
):
    knn_pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    knn_pipeline.fit(X_train, y_train)
    test_predictions = knn_pipeline.predict(X_test)
    knn_pipeline.score(X_test, y_test)
    return knn_pipeline, test_predictions


@app.cell(hide_code=True)
def accuracy_reading(mo, y_test):
    _baseline = 1 - y_test.mean()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The pipeline is right about 94% of the test tumours. The baseline, which
    predicts the more common class, benign, for every tumour, would be right about
    {_baseline:.0%} of them, so k-NN is well above it.
    """)
    return


@app.cell(hide_code=True)
def mistakes_intro(mo):
    mo.md(r"""
    ---
    ## Two kinds of mistake

    The confusion matrix below counts the test tumours by their true diagnosis (the
    rows) and the pipeline's prediction (the columns). In 08a we built it with
    `pd.crosstab`; `ConfusionMatrixDisplay` draws the same table as a grid shaded by
    the counts, and its `labels` argument puts malignant first in both.
    """)
    return


@app.cell
def confusion_default(ConfusionMatrixDisplay, plt, test_predictions, y_test):
    _fig, _ax = plt.subplots(figsize=(4, 3.5))
    ConfusionMatrixDisplay.from_predictions(
        y_test, test_predictions, labels=[True, False],
        display_labels=["malignant", "benign"], colorbar=False, cmap="Blues", ax=_ax)
    _ax.set(xlabel="Predicted", ylabel="True")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def mistakes_reading(mo):
    mo.md(r"""
    In a medical test, the condition being tested for is called *positive*,
    whether or not it is good news, so here a malignant tumour is a positive case.
    The four cells of the matrix have the following names.

    | | Predicted malignant | Predicted benign |
    |---|---|---|
    | Malignant | True positive (TP): 47 | False negative (FN): 6 |
    | Benign | False positive (FP): 3 | True negative (TN): 87 |

    The pipeline makes nine mistakes, which is why its accuracy is 134 out of 143,
    but they are not alike. A false positive is a benign tumour called malignant,
    and the patient will have further tests that come back clear. A false negative
    is a malignant tumour called benign, and a cancer goes untreated. Six of the 53
    cancers in the test set are missed, and the accuracy of 94% does not show that.
    """)
    return


@app.cell(hide_code=True)
def precision_recall_intro(mo):
    mo.md(r"""
    ---
    ## Precision and recall

    Two measures separate the kinds of mistake. Each is a share, between 0 and 1.

    | Measure | Formula | Question it answers | Here |
    |---|---|---|---|
    | Precision | TP / (TP + FP) | Of the tumours predicted malignant, what share are malignant? | 47 / 50 = 0.940 |
    | Recall | TP / (TP + FN) | Of the malignant tumours, what share are predicted malignant? | 47 / 53 = 0.887 |

    Precision is reduced by false positives, and recall by false negatives. Recall is
    also called *sensitivity*, the name more often used in medicine. scikit-learn
    computes both from the true labels and the predictions, in that order, and
    treats `True` as the positive class.
    """)
    return


@app.cell
def sklearn_scores(precision_score, recall_score, test_predictions, y_test):
    precision_score(y_test, test_predictions), recall_score(y_test, test_predictions)
    return


@app.cell(hide_code=True)
def report_intro(mo):
    mo.md(r"""
    `classification_report` prints both measures for each class at once.
    """)
    return


@app.cell
def report(classification_report, test_predictions, y_test):
    print(classification_report(y_test, test_predictions, labels=[True, False],
                                target_names=["malignant", "benign"], digits=3))
    return


@app.cell(hide_code=True)
def report_reading(mo):
    mo.md(r"""
    The malignant row repeats the precision and recall above. The benign row treats
    benign as the positive class: of the 93 tumours predicted benign, 87 are benign,
    a precision of 0.935, and of the 90 benign tumours, 87 are predicted benign, a
    recall of 0.967. `support` is the number of test tumours in each class, and the
    `f1-score` combines a row's precision and recall into one number, which we will
    not use in this course. The last three rows average over the two classes.
    """)
    return


@app.cell(hide_code=True)
def practice_precision_intro(mo):
    mo.md(r"""
    ### Practice: precision and recall by hand

    Please compute both with pandas in the cell below, and check them against the
    values above. `test_predictions & y_test` is `True` for a true positive, and
    `.sum()` counts the `True` values, so `(test_predictions & y_test).sum()` is the
    number of true positives. Divide it by the number of tumours predicted
    malignant for `my_precision`, and by the number that are malignant for
    `my_recall`.
    """)
    return


@app.cell
def practice_precision(test_predictions, y_test):
    my_precision = None
    my_recall = None
    my_precision, my_recall
    return


@app.cell(hide_code=True)
def baseline_recall(mo):
    mo.md(r"""
    The baseline shows why accuracy alone can mislead. Predicting benign for every
    tumour is right about 63% of the time, but its recall is 0, because it finds
    none of the cancers. Its precision cannot be computed, because it never predicts
    malignant, and scikit-learn reports it as 0 with a warning.
    """)
    return


@app.cell(hide_code=True)
def thresholds_intro(mo):
    mo.md(r"""
    ---
    ## Thresholds

    k-NN predicts malignant when most of the five neighbours are malignant, which
    means at least 3 of 5. That rule is a choice, and it can be changed. A pipeline's
    `predict_proba` returns, for each tumour, the share of its five neighbours in each
    class, in the order of `knn_pipeline.classes_`, which is `[False, True]`, so the
    second column, `[:, 1]`, is the share that are malignant. `predict` is the same
    as asking whether that share is at least 0.5.

    | Malignant neighbours | 0 of 5 | 1 of 5 | 2 of 5 | 3 of 5 | 4 of 5 | 5 of 5 |
    |---|---:|---:|---:|---:|---:|---:|
    | Share | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |

    The share at which a tumour is called malignant is the *threshold*. A lower
    threshold calls more tumours malignant, which finds more cancers and raises
    recall, but also calls more benign tumours malignant, which lowers precision. A
    higher threshold does the reverse.

    Choosing the threshold by looking at the test set would use the test set to make
    a choice, as choosing k did on Monday. Instead, `cross_val_predict` runs the
    same five rounds as `cross_val_score`, but returns, for every training tumour,
    the share computed by the round in which that tumour was in the validation
    fold. Each share therefore comes from a model that was not fitted to that tumour.
    """)
    return


@app.cell
def cv_shares(X_train, cross_val_predict, knn_pipeline, y_train):
    cv_malignant_share = cross_val_predict(
        knn_pipeline, X_train, y_train, cv=5, method="predict_proba")[:, 1]
    cv_malignant_share[:10]
    return (cv_malignant_share,)


@app.cell(hide_code=True)
def shares_table_intro(mo):
    mo.md(r"""
    The table below counts the training tumours by their share of malignant
    neighbours and their true diagnosis.
    """)
    return


@app.cell
def shares_table(cv_malignant_share, np, pd, y_train):
    pd.crosstab(cv_malignant_share.round(1), np.where(y_train, "malignant", "benign"),
                rownames=["share of malignant neighbours"], colnames=["true"])
    return


@app.cell(hide_code=True)
def shares_reading(mo):
    mo.md(r"""
    Most tumours are clear cases: 233 benign tumours have no malignant neighbours,
    and 124 malignant tumours have five. The mistakes come from the rows in between.

    Any threshold can be read from the table. At the default, 0.6 (3 of 5), the
    tumours in the bottom three rows are predicted malignant. They include 9 + 15 +
    124 = 148 of the 159 malignant tumours, so recall is 148 / 159 = 0.931, and 5 + 1 +
    0 = 6 benign ones, so precision is 148 / 154 = 0.961.
    """)
    return


@app.cell(hide_code=True)
def practice_threshold_intro(mo):
    mo.md(r"""
    ### Practice: a lower threshold

    Please predict malignant for every training tumour with at least 2 of 5
    malignant neighbours, that is, with `cv_malignant_share >= 0.4`, and compute the
    precision and recall of those predictions against `y_train` with
    `precision_score` and `recall_score`. Before you run it, use the table to say
    which of the two will go up and which will go down.
    """)
    return


@app.cell
def practice_threshold(cv_malignant_share, precision_score, recall_score, y_train):
    my_cv_precision = None
    my_cv_recall = None
    my_cv_precision, my_cv_recall
    return


@app.cell(hide_code=True)
def threshold_table_intro(mo):
    mo.md(r"""
    The table below repeats the calculation for every threshold, and the first
    figure after it plots precision and recall against the threshold. The second
    figure draws the same trade-off with `PrecisionRecallDisplay`, which plots
    precision against recall for every threshold, and we label each point with its
    threshold.
    """)
    return


@app.cell
def threshold_table(cv_malignant_share, pd, precision_score, recall_score, y_train):
    _rows = []
    for _votes in [1, 2, 3, 4, 5]:
        _predicted = cv_malignant_share >= _votes / 5
        _rows.append({"malignant neighbours": f"at least {_votes} of 5",
                      "threshold": _votes / 5,
                      "precision": precision_score(y_train, _predicted),
                      "recall": recall_score(y_train, _predicted),
                      "false positives": int((_predicted & ~y_train).sum()),
                      "false negatives": int((~_predicted & y_train).sum())})
    threshold_table = pd.DataFrame(_rows).set_index("malignant neighbours").round(3)
    threshold_table
    return (threshold_table,)


@app.cell
def threshold_lines(plt, threshold_table):
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    _ax.plot(threshold_table["threshold"], threshold_table["precision"], marker="o",
             label="precision")
    _ax.plot(threshold_table["threshold"], threshold_table["recall"], marker="s",
             label="recall")
    _ax.set_xlabel("Threshold (share of malignant neighbours)")
    _ax.set_ylabel("Cross-validated value")
    _ax.legend()
    _fig.tight_layout()
    _fig
    return


@app.cell
def threshold_plot(
    PrecisionRecallDisplay,
    cv_malignant_share,
    plt,
    threshold_table,
    y_train,
):
    _fig, _ax = plt.subplots(figsize=(6, 4.5))
    PrecisionRecallDisplay.from_predictions(y_train, cv_malignant_share, pos_label=True,
                                            ax=_ax)
    _ax.get_legend().remove()
    _ax.scatter(threshold_table["recall"], threshold_table["precision"], color="black")
    for _label, _row in threshold_table.iterrows():
        _ax.annotate(_label, (_row["recall"], _row["precision"]),
                     textcoords="offset points", xytext=(-8, -14), ha="right")
    _ax.set(xlabel="Recall (cross-validated)", ylabel="Precision (cross-validated)",
            xlim=(0.7, 1.0), ylim=(0.8, 1.01))
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def choose_threshold(mo):
    mo.md(r"""
    ---
    ## Choosing a threshold

    No threshold has the highest precision and the highest recall at once, so the
    choice depends on what each kind of mistake costs. At 1 of 5, the pipeline
    misses 3 of the 159 cancers in the training set, but calls 34 benign tumours
    malignant. At 3 of 5, the default, it misses 11 and calls 6 malignant. A
    screening test, which is followed by further tests, is usually set to miss as
    few cancers as possible, while a test that leads directly to surgery might be set
    the other way. The decision belongs to the people who bear the costs, the
    patients and their doctors, rather than to the classifier.

    For the rest of the notebook we use a threshold of 0.4 (2 of 5), which misses 6
    cancers and makes 13 false alarms in cross-validation. The threshold is chosen
    in the same way as k was on Monday:

    | Choice | Chosen with | Reported from |
    |---|---|---|
    | k (08b) | Mean cross-validation accuracy on the training set | Test accuracy, measured once |
    | Threshold (today) | Cross-validated precision and recall on the training set | Test precision and recall, measured once |

    With the threshold chosen, we apply it to the test set once.
    """)
    return


@app.cell
def final_test(
    ConfusionMatrixDisplay,
    X_test,
    knn_pipeline,
    plt,
    precision_score,
    recall_score,
    y_test,
):
    THRESHOLD = 0.4
    final_predictions = knn_pipeline.predict_proba(X_test)[:, 1] >= THRESHOLD
    final_precision = precision_score(y_test, final_predictions)
    final_recall = recall_score(y_test, final_predictions)
    _fig, _ax = plt.subplots(figsize=(4, 3.5))
    ConfusionMatrixDisplay.from_predictions(
        y_test, final_predictions, labels=[True, False],
        display_labels=["malignant", "benign"], colorbar=False, cmap="Blues", ax=_ax)
    _ax.set(xlabel="Predicted", ylabel="True")
    _fig.tight_layout()
    _fig
    return final_precision, final_recall


@app.cell(hide_code=True)
def final_reading(final_precision, final_recall, mo):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    At a threshold of 0.4, the pipeline finds 51 of the 53 cancers in the test set,
    a recall of {final_recall:.3f}, against 47 at the default, and its precision is
    {final_precision:.3f}, because 3 of the 54 tumours it calls malignant are
    benign. These are the numbers we report. As with k on Monday, trying other
    thresholds on the test set now would be choosing by the test set.
    """)
    return


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - A classifier makes two kinds of mistake, false positives and false negatives,
      and accuracy counts them the same even when one costs far more.
    - Precision, TP / (TP + FP), is the share of positive predictions that are
      right; recall, TP / (TP + FN), is the share of positive cases that are found.
    - k-NN's `predict_proba` returns the share of the k neighbours in each class, and
      `predict` calls a case positive when that share is at least 0.5.
    - Lowering the threshold raises recall and lowers precision. The threshold is
      chosen from cross-validation on the training set, according to the costs of
      the two mistakes, and the test set is used once, at the end.

    ## Next class

    On Monday, notebook 09b will cover two other classifiers, logistic regression
    and decision trees.
    """)
    return


@app.cell(hide_code=True)
def end_of_notebook(mo):
    mo.md(r"""
    ---
    ## 🏁 END OF NOTEBOOK
    """)
    return


if __name__ == "__main__":
    app.run()
