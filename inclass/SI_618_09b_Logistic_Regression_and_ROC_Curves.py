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
    # SI 618 - 09b: logistic regression and ROC curves

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 19 (Mon Nov 9)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.11.09.2.CT

    ---

    ## Today you will be able to

    - Explain how logistic regression turns a weighted sum of features into a
      probability, and read the sign of a coefficient
    - Compute a probability for one new case with `predict_proba`
    - Read a ROC curve and its AUC, and explain the AUC as the share of
      malignant-benign pairs that a classifier puts in the right order

    ## Reading

    Géron, on classification (the section on the ROC curve) and on training models
    (the section on logistic regression).

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Where we left off | 5 |
    | Logistic regression | 15 |
    | Your card | 3 |
    | The line | 17 |
    | ROC curves and AUC | 12 |
    """)
    return


@app.cell
def imports():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.datasets import load_breast_cancer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (RocCurveDisplay, precision_score, recall_score,
                                 roc_auc_score)
    from sklearn.model_selection import cross_val_predict, train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    return (
        LogisticRegression,
        RocCurveDisplay,
        StandardScaler,
        cross_val_predict,
        load_breast_cancer,
        make_pipeline,
        mo,
        np,
        pd,
        plt,
        precision_score,
        recall_score,
        roc_auc_score,
        train_test_split,
    )


@app.cell(hide_code=True)
def recap(mo):
    mo.md(r"""
    ---
    ## Where we left off

    On Wednesday, notebook 09a measured k-NN on the Wisconsin breast cancer data by
    precision and recall, and chose a threshold from cross-validation before testing
    once. Most of Wednesday's sheets did this well, so we will go over only two
    points.

    ### A threshold that meets a condition

    Question 5 asked for the threshold with the highest precision among those that
    find at least 95% of the cancers. The condition comes first: at least 1 of 5 and
    at least 2 of 5 have a cross-validated recall above 0.95, but at least 3 of 5,
    with 0.931, does not, so its higher precision does not make it eligible. Of the
    two that meet the condition, 2 of 5 has the higher precision, 0.922. The numbers
    to report are its test precision and recall, 0.944 and 0.962, because the
    cross-validated ones were used to make the choice.

    ### One scaler, fitted to the training set

    Question 4 asked about a second scaler fitted to the test tumours. A few sheets
    said that this is right, because a scaler fitted to both sets would leak. Any
    scaler fitted to the test tumours, alone or together with the training tumours,
    uses the test set before the model is tested. The scaler should be fitted to the
    training tumours only, and the test tumours standardised
    with the training set's means and standard deviations, which is what a pipeline
    does.

    ### Today

    Every model so far has been k-NN. Today we fit a second kind of classifier,
    logistic regression, to the same tumours with the same split, and then use the
    room to rank some of the test tumours by its probabilities.
    """)
    return


@app.cell
def load_tumours(load_breast_cancer, train_test_split):
    tumours = load_breast_cancer(as_frame=True).frame
    tumours["malignant"] = tumours["target"] == 0
    train_tumours, test_tumours = train_test_split(
        tumours, test_size=0.25, stratify=tumours["malignant"], random_state=618)
    len(train_tumours), len(test_tumours)
    return test_tumours, train_tumours


@app.cell(hide_code=True)
def logistic_intro(mo):
    mo.md(r"""
    ---
    ## Logistic regression

    In topic 05, linear regression predicted a number as a weighted sum of the
    features, an intercept plus a coefficient times each feature. *Logistic
    regression* computes the same kind of weighted sum, which we will call z, but
    turns it into a probability between 0 and 1 with the *logistic function*,

    `p = 1 / (1 + e**(-z))`

    When z is 0, p is 0.5. When z is large and positive, p is close to 1, and when
    it is large and negative, p is close to 0. Despite its name, logistic regression
    is a classifier: it predicts the positive class when p is at least 0.5, and
    `predict_proba` returns p, so the thresholds of 09a apply to it unchanged.

    We start with a single feature, `worst radius`, the mean radius of the three
    largest nuclei in the image, in micrometres.
    """)
    return


@app.cell
def fit_one_feature(LogisticRegression, train_tumours):
    one_feature_model = LogisticRegression()
    one_feature_model.fit(train_tumours[["worst radius"]], train_tumours["malignant"])
    one_feature_model.intercept_, one_feature_model.coef_
    return (one_feature_model,)


@app.cell(hide_code=True)
def one_feature_reading(mo, np, one_feature_model):
    _b0 = one_feature_model.intercept_[0]
    _b1 = one_feature_model.coef_[0][0]
    _cut = -_b0 / _b1

    def _p(radius: float) -> float:
        return 1 / (1 + np.exp(-(_b0 + _b1 * radius)))

    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The fitted model is z = {_b0:.2f} + {_b1:.3f} x worst radius. The coefficient
    is positive, so a larger radius raises z and the probability of malignant. z is
    0, and p is 0.5, at a worst radius of {_cut:.1f}, so the model predicts
    malignant for tumours larger than that.

    | Worst radius | z | p |
    |---:|---:|---:|
    | 13 | {_b0 + _b1 * 13:.2f} | {_p(13):.3f} |
    | {_cut:.1f} | 0.00 | 0.500 |
    | 20 | {_b0 + _b1 * 20:.2f} | {_p(20):.3f} |

    The figure shows the training tumours, malignant at the top and benign at the
    bottom, and the fitted probability as a curve.
    """)
    return


@app.cell(hide_code=True)
def one_feature_figure(np, one_feature_model, pd, plt, train_tumours):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _rng = np.random.default_rng(618)
    _radius = train_tumours["worst radius"]
    _y = train_tumours["malignant"].astype(int) + _rng.uniform(-0.04, 0.04, len(_radius))
    _grid = pd.DataFrame({"worst radius": np.linspace(_radius.min(), _radius.max(), 300)})
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    _ax.scatter(_radius, _y, s=10, alpha=0.4, color="grey")
    _ax.plot(_grid["worst radius"], one_feature_model.predict_proba(_grid)[:, 1],
             color="black", label="fitted probability of malignant")
    _ax.axhline(0.5, linestyle="--", color="grey", linewidth=1)
    _ax.set_xlabel("Worst radius")
    _ax.set_ylabel("Malignant (1) or benign (0)")
    _ax.legend(loc="center right")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def line_model_intro(mo):
    mo.md(r"""
    ### Two features

    Worst radius separates the tumours so well that a line of tumours ranked by it
    would have almost every benign tumour at one end and every malignant one at the
    other. For today's line we use two features that separate them less well, so
    that the middle of the line is mixed:

    - `mean texture` is the standard deviation of the grey values in the image,
      which is higher when the nuclei look more uneven.
    - `mean smoothness` is the local variation in the length of the radius, which is
      higher when the outline of a nucleus is more irregular.

    With two features, z has an intercept and two coefficients. We standardise the
    features first, in a pipeline, so that each coefficient is the change in z for
    one standard deviation of its feature and the two can be compared. A pipeline's
    steps are numbered from 0, so `line_model[-1]` is its last step, the fitted
    logistic regression.
    """)
    return


@app.cell
def fit_line_model(
    LogisticRegression,
    StandardScaler,
    make_pipeline,
    train_tumours,
):
    LINE_FEATURES = ["mean texture", "mean smoothness"]
    line_model = make_pipeline(StandardScaler(), LogisticRegression())
    line_model.fit(train_tumours[LINE_FEATURES], train_tumours["malignant"])
    line_model[-1].intercept_, line_model[-1].coef_
    return LINE_FEATURES, line_model


@app.cell(hide_code=True)
def line_model_reading(line_model, mo, np):
    _b0 = line_model[-1].intercept_[0]
    _b_texture, _b_smoothness = line_model[-1].coef_[0]
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The fitted model is z = {_b0:.2f} + {_b_texture:.2f} x texture +
    {_b_smoothness:.2f} x smoothness, with both features measured in standard
    deviations from the training mean. Both coefficients are positive, so more uneven
    and more irregular nuclei make malignant more likely, and texture has the larger
    coefficient of the two. A tumour that is average on both features has z =
    {_b0:.2f} and a probability of malignant of {1 / (1 + np.exp(-_b0)):.2f},
    which is below 0.5 because benign tumours outnumber malignant ones in the
    training set.
    """)
    return


@app.cell(hide_code=True)
def threshold_intro(mo):
    mo.md(r"""
    ### Choosing the threshold before the line

    The line will be made of test tumours, so we choose the threshold now, from
    cross-validation on the training set, as in 09a. Suppose we want the classifier
    to find at least 85% of the cancers, and among the thresholds that do, the one
    with the highest precision. The table below gives the cross-validated precision and recall at
    each threshold.
    """)
    return


@app.cell
def threshold_table(
    LINE_FEATURES,
    cross_val_predict,
    line_model,
    pd,
    precision_score,
    recall_score,
    train_tumours,
):
    _malignant = train_tumours["malignant"]
    cv_line_probabilities = cross_val_predict(
        line_model, train_tumours[LINE_FEATURES], _malignant,
        cv=5, method="predict_proba")[:, 1]

    line_thresholds = pd.DataFrame(index=[0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6])
    for _threshold in line_thresholds.index:
        _predicted = cv_line_probabilities >= _threshold
        line_thresholds.loc[_threshold, "precision"] = precision_score(_malignant, _predicted)
        line_thresholds.loc[_threshold, "recall"] = recall_score(_malignant, _predicted)
    line_thresholds.round(3)
    return cv_line_probabilities, line_thresholds


@app.cell(hide_code=True)
def threshold_reading(line_thresholds, mo):
    _eligible = line_thresholds[line_thresholds["recall"] >= 0.85]
    _chosen = _eligible["precision"].idxmax()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The thresholds up to {_eligible.index.max()} have a recall of at least 0.85, and
    of those, {_chosen} has the highest precision,
    {line_thresholds.loc[_chosen, 'precision']:.3f}. Fewer than two in three of the
    tumours it calls malignant are malignant, because two weak features separate
    the tumours poorly.
    The threshold of {_chosen} will be marked on the wall.
    """)
    return


@app.cell(hide_code=True)
def card_intro(mo):
    mo.md(r"""
    ---
    ## Your card

    Each card describes one tumour from the test set, with its mean texture and mean
    smoothness on the front. Its diagnosis is printed on the back, so the card should
    stay face up until everyone is in the line.

    ### Practice: the card's probability

    Please type the two numbers from the front of your card into the boxes below, and
    write the probability that appears on your card and on your sheet.

    `line_model.predict_proba` computes that probability in three steps, which we
    write out separately below:

    1. The pipeline's `StandardScaler` standardises each measurement with the
       training set's mean and standard deviation, so that it is expressed in
       standard deviations from the training mean.
    2. The `LogisticRegression` computes z, the intercept plus each coefficient
       times its standardised measurement.
    3. The logistic function turns z into a probability between 0 and 1.

    After the three steps, we call `predict_proba` on the card to check that it
    gives the same number.
    """)
    return


@app.cell
def card_inputs(mo):
    card_texture = mo.ui.number(label="Mean texture")
    card_smoothness = mo.ui.number(label="Mean smoothness")
    mo.hstack([card_texture, card_smoothness], justify="start")
    return card_smoothness, card_texture


@app.cell
def card_probability(card_smoothness, card_texture, line_model, mo, np, pd):
    mo.stop(card_texture.value is None or card_smoothness.value is None,
            mo.md("Type both numbers from your card into the boxes above."))
    scaler = line_model[0]     # the first step of the pipeline, the StandardScaler
    logistic = line_model[-1]  # the last step, the LogisticRegression

    # Step 1: standardise each measurement with the training mean and standard deviation.
    texture_sds = (card_texture.value - scaler.mean_[0]) / scaler.scale_[0]
    smoothness_sds = (card_smoothness.value - scaler.mean_[1]) / scaler.scale_[1]

    # Step 2: the weighted sum z.
    b0 = logistic.intercept_[0]
    b_texture, b_smoothness = logistic.coef_[0]
    z = b0 + b_texture * texture_sds + b_smoothness * smoothness_sds

    # Step 3: the logistic function turns z into a probability.
    probability = 1 / (1 + np.exp(-z))

    # The check: predict_proba does all three steps. Its result has a row for each
    # tumour and a column for each class, and column 1 is malignant.
    card = pd.DataFrame({"mean texture": [card_texture.value],
                         "mean smoothness": [card_smoothness.value]})
    check = line_model.predict_proba(card)[0, 1]

    mo.md(f"""
    | Step | Calculation | Result |
    |---|---|---:|
    | 1. Standardise texture | ({card_texture.value} - {scaler.mean_[0]:.2f}) / {scaler.scale_[0]:.2f} | {texture_sds:.2f} |
    | 1. Standardise smoothness | ({card_smoothness.value} - {scaler.mean_[1]:.5f}) / {scaler.scale_[1]:.5f} | {smoothness_sds:.2f} |
    | 2. Weighted sum | {b0:.2f} + {b_texture:.2f} x ({texture_sds:.2f}) + {b_smoothness:.2f} x ({smoothness_sds:.2f}) | z = {z:.2f} |
    | 3. Logistic function | `1 / (1 + e**(-z))` with z = {z:.2f} | {probability:.3f} |
    | Check | `line_model.predict_proba(card)[0, 1]` | {check:.3f} |

    ## Probability of malignant: {probability:.3f}
    """)
    return probability, z


@app.cell(hide_code=True)
def card_figure(np, plt, probability, z):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _zs = np.linspace(min(-5, z - 1), max(5, z + 1), 300)
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    _ax.plot(_zs, 1 / (1 + np.exp(-_zs)), color="black", label="logistic function")
    _ax.axhline(0.3, linestyle="--", color="grey", linewidth=1, label="threshold 0.3")
    _ax.plot([z, z, _zs[0]], [0, probability, probability], linestyle=":", color="tab:red")
    _ax.scatter([z], [probability], color="tab:red", zorder=3, label="your card")
    _ax.set_xlabel("z, the weighted sum")
    _ax.set_ylabel("Probability of malignant")
    _ax.set_ylim(0, 1)
    _ax.legend(loc="upper left")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def line_instructions(mo):
    mo.md(r"""
    ---
    ## The line

    Please stand along the walls in order of your probability, lowest at the marker
    for 0.1 and highest at the marker for 0.9. Go to roughly the right place first,
    and then compare your number with your neighbours' and change places until
    everyone to your left has a lower probability than you and everyone to your right
    a higher one. When the line is in order, everyone will turn their card over.

    The threshold of 0.3 was chosen before anyone joined the line, so where it
    falls gives the test result: everyone on the high side of it is predicted
    malignant. We will then move the cut along the line, which will show what every
    other threshold would have given, but the choice will stay at 0.3, because it
    was made from cross-validation.
    """)
    return


@app.cell(hide_code=True)
def roc_intro(mo):
    mo.md(r"""
    ---
    ## ROC curves and AUC

    Moving the cut along the line changes two shares at once:

    | Share | Formula | Meaning |
    |---|---|---|
    | True positive rate | TP / (TP + FN) | The share of malignant tumours called malignant, which is the recall |
    | False positive rate | FP / (FP + TN) | The share of benign tumours called malignant |

    A *ROC curve* (for receiver operating characteristic, a name that comes from
    radar engineering) plots the true positive rate against the false positive rate
    for every position of the cut. With the cut past the highest probability, no
    tumour is called malignant, and the curve starts at (0, 0); with the cut before
    the lowest, every tumour is, and it ends at (1, 1). A classifier that put every
    malignant tumour above every benign one would pass through the top-left corner,
    (0, 1), where it finds every cancer with no false alarms, and one that guessed at
    random would follow the diagonal.

    The *area under the curve*, or *AUC*, is 1 for a curve through the top-left
    corner and 0.5 for the diagonal. It is also the share of malignant-benign pairs
    in which the malignant tumour has the higher probability. On the 44 cards, 0.914
    of the 17 x 27 = 459 pairs are in the right order.
    """)
    return


@app.cell(hide_code=True)
def test_roc_intro(mo):
    mo.md(r"""
    The cards are 44 of the 143 test tumours. The figure below is the ROC curve of
    `line_model` on all 143, with the threshold of 0.3 marked.
    """)
    return


@app.cell
def test_roc(
    LINE_FEATURES,
    RocCurveDisplay,
    line_model,
    plt,
    precision_score,
    recall_score,
    roc_auc_score,
    test_tumours,
):
    _probabilities = line_model.predict_proba(test_tumours[LINE_FEATURES])[:, 1]
    _malignant = test_tumours["malignant"]
    _predicted = _probabilities >= 0.3
    line_auc = roc_auc_score(_malignant, _probabilities)
    line_precision = precision_score(_malignant, _predicted)
    line_recall = recall_score(_malignant, _predicted)
    # The false positive rate is the share of benign tumours predicted malignant.
    _false_positive_rate = _predicted[~_malignant].mean()

    RocCurveDisplay.from_predictions(_malignant, _probabilities, pos_label=True,
                                     name="line_model, test set", plot_chance_level=True)
    plt.plot(_false_positive_rate, line_recall, "ko", label="threshold 0.3")
    plt.legend()
    plt.gca()
    return line_auc, line_precision, line_recall


@app.cell(hide_code=True)
def test_roc_reading(line_auc, line_precision, line_recall, mo):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    On the whole test set, `line_model` has an AUC of {line_auc:.3f}, and at the
    threshold of 0.3, a precision of {line_precision:.3f} and a recall of
    {line_recall:.3f}. These are the numbers to report. The room's line used only 44
    of the test tumours, so its AUC and its counts at 0.3 can differ from these.
    """)
    return


@app.cell(hide_code=True)
def better_features_intro(mo):
    mo.md(r"""
    ### Better features

    The line was mixed in the middle because of the two features we chose. The
    figure below compares the cross-validated ROC curves, on the training set, of
    `line_model` and of the same pipeline with three other features: worst radius,
    worst concave points and worst texture.
    """)
    return


@app.cell
def compare_features(
    LogisticRegression,
    RocCurveDisplay,
    StandardScaler,
    cross_val_predict,
    cv_line_probabilities,
    make_pipeline,
    plt,
    roc_auc_score,
    train_tumours,
):
    _malignant = train_tumours["malignant"]
    _three = ["worst radius", "worst concave points", "worst texture"]
    _cv_three = cross_val_predict(
        make_pipeline(StandardScaler(), LogisticRegression()),
        train_tumours[_three], _malignant, cv=5, method="predict_proba")[:, 1]
    three_feature_auc = roc_auc_score(_malignant, _cv_three)

    _fig, _ax = plt.subplots()
    RocCurveDisplay.from_predictions(_malignant, cv_line_probabilities, pos_label=True,
                                     name="mean texture and smoothness", ax=_ax)
    RocCurveDisplay.from_predictions(_malignant, _cv_three, pos_label=True,
                                     name="worst radius, concave points and texture",
                                     ax=_ax, plot_chance_level=True)
    _fig
    return (three_feature_auc,)


@app.cell(hide_code=True)
def better_features_reading(
    cv_line_probabilities,
    mo,
    roc_auc_score,
    three_feature_auc,
    train_tumours,
):
    _line_auc = roc_auc_score(train_tumours["malignant"], cv_line_probabilities)
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The cross-validated AUC is {_line_auc:.3f} with mean texture and smoothness, and
    {three_feature_auc:.3f} with the three worst-value features. A line of tumours
    ranked by the second model would have almost every benign tumour at one end and
    every malignant one at the other. The comparison uses cross-validation on the
    training set, because choosing between the two models is one more choice, and
    the test set is kept for the model that is chosen.
    """)
    return


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - Logistic regression computes a weighted sum of the features and turns it into
      a probability with the logistic function; a positive coefficient makes the
      positive class more likely.
    - `predict_proba` gives the probability for a new case, and a threshold turns it
      into a prediction. The threshold is chosen from cross-validation before the
      test set is used.
    - A ROC curve plots the true positive rate against the false positive rate for
      every threshold. Its AUC is the share of positive-negative pairs that the
      classifier puts in the right order.
    - Better features give a higher AUC, and the choice between models is made by
      cross-validation on the training set.

    ## Next class

    Wednesday is Project Studio II, with a meeting for each group. On Monday,
    November 16, notebook 10 will cover unsupervised learning.
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
