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
    # SI 618 - 10: decision trees and random forests

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 21 (Mon Nov 16)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.11.14.1.CT

    ---

    ## Today you will be able to

    - Read the rules of a decision tree, and follow one case through them
    - Compute the Gini impurity of a group, and explain how a tree chooses a split
    - Explain why a deep tree fits its training set better than new cases
    - Explain how a random forest combines many trees, and compare it with a single
      tree and with logistic regression by cross-validation

    ## Reading

    Géron, on decision trees and on ensemble learning.

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Where we left off | 5 |
    | The passengers | 5 |
    | Logistic regression on the passengers | 5 |
    | Decision trees | 20 |
    | The depth of a tree | 8 |
    | Random forests | 15 |
    | Choosing a model and testing it once | 7 |
    """)
    return


@app.cell
def imports():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score, cross_validate, train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

    return (
        DecisionTreeClassifier,
        LogisticRegression,
        RandomForestClassifier,
        SimpleImputer,
        StandardScaler,
        cross_val_score,
        cross_validate,
        export_text,
        make_pipeline,
        mo,
        np,
        pd,
        plot_tree,
        plt,
        train_test_split,
    )


@app.cell(hide_code=True)
def recap(mo):
    mo.md(r"""
    ---
    ## Where we left off

    In session 19, notebook 09b fitted logistic regression to the tumours, and the
    paper sheet asked you to compute z and a probability for one tumour, and the true
    and false positive rates at a threshold. We will go over the two most common
    errors.

    ### The threshold applies to the probability

    The model predicts malignant when the probability p is at least 0.5, which
    happens when z is at least 0, because the logistic function gives 0.5 at z = 0.
    Ten sheets compared z with 0.5 instead. For the radius at which p is 0.5, the
    equation to solve is z = -19.37 + 1.165 x radius = 0, which gives a radius of
    19.37 / 1.165 = 16.63.

    ### Each rate has its own denominator

    The true positive rate divides by the malignant tumours, TP + FN, and the false
    positive rate divides by the benign ones, FP + TN. Several sheets divided both
    counts by the tumours above the threshold, which gives the precision rather than
    either rate. With TP = 2, FN = 1, FP = 2 and TN = 3, the rates are 2/3 and 2/5.

    ### Today

    Logistic regression and k-NN are the two classifiers we have used so far. Today
    we fit a third kind, the decision tree, and then a random forest, which combines
    hundreds of trees, and compare all three on new data.
    """)
    return


@app.cell(hide_code=True)
def data_intro(mo):
    mo.md(r"""
    ---
    ## The passengers

    The data describe 891 passengers on the Titanic, which sank on its first voyage
    in April 1912, and whether each of them survived. They come from the training set
    of a well-known Kaggle competition, in the copy that the seaborn library
    distributes. We use six features:

    | Column | Meaning |
    |---|---|
    | `pclass` | Ticket class: 1, 2 or 3 |
    | `female` | True for a woman or girl |
    | `age` | Age in years |
    | `sibsp` | Number of siblings and spouses on board |
    | `parch` | Number of parents and children on board |
    | `fare` | Fare paid, in pounds |

    We split the passengers as in topics 08 and 09, holding out a quarter of them as
    the test set, stratified by survival.
    """)
    return


@app.cell
def load_passengers(pd, train_test_split):
    TITANIC_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
    FEATURES = ["pclass", "female", "age", "sibsp", "parch", "fare"]

    passengers = pd.read_csv(TITANIC_URL)
    passengers["female"] = passengers["sex"] == "female"
    train_passengers, test_passengers = train_test_split(
        passengers, test_size=0.25, stratify=passengers["survived"], random_state=618)
    X_train = train_passengers[FEATURES]
    y_train = train_passengers["survived"]
    train_passengers[FEATURES + ["survived"]].head()
    return FEATURES, X_train, passengers, test_passengers, train_passengers, y_train


@app.cell(hide_code=True)
def data_reading(mo, passengers, train_passengers, y_train):
    _missing_age = passengers["age"].isna().sum()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The training set has {len(train_passengers)} passengers, of whom
    {y_train.mean():.1%} survived, so predicting that every passenger died would be
    right {1 - y_train.mean():.1%} of the time, and every model today is compared
    with this baseline.

    The age of {_missing_age} of the {len(passengers)} passengers was not recorded.
    scikit-learn's models do not accept missing values, so every model today starts
    with a `SimpleImputer`, which computes and stores the median age of the training
    passengers and puts it in place of each missing age. Because it is the first step
    of a pipeline, the median comes from the training set alone, as the scaler's means
    and standard deviations did in topic 08.
    """)
    return


@app.cell(hide_code=True)
def logistic_intro(mo):
    mo.md(r"""
    ---
    ## Logistic regression on the passengers

    As a point of comparison, we cross-validate the classifier from 09b, logistic
    regression on the standardised features, on the training passengers.
    """)
    return


@app.cell
def logistic_cv(
    LogisticRegression,
    SimpleImputer,
    StandardScaler,
    X_train,
    cross_val_score,
    make_pipeline,
    y_train,
):
    logistic_model = make_pipeline(
        SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression())
    logistic_cv_accuracy = cross_val_score(logistic_model, X_train, y_train, cv=5).mean()
    logistic_cv_accuracy
    return (logistic_cv_accuracy,)


@app.cell(hide_code=True)
def logistic_reading(logistic_cv_accuracy, mo, y_train):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The cross-validated accuracy is {logistic_cv_accuracy:.3f}, against a baseline
    of {1 - y_train.mean():.3f}. We will come back to this number at the end, after
    fitting the trees.
    """)
    return


@app.cell(hide_code=True)
def tree_intro(mo):
    mo.md(r"""
    ---
    ## Decision trees

    A *decision tree* predicts by asking a series of yes-or-no questions, each about
    one feature, such as "is the passenger's age at most 9.5?". Fitting the tree
    finds the question that best separates the training passengers who survived from
    those who died, splits them into two groups by the answer, and then splits each
    group again, until the tree reaches its maximum depth. Each final group is called
    a *leaf*, and the tree predicts the more common class in it.

    Because each question is about one feature at a time, a tree does not need its
    features standardised, so the pipeline below has no scaler. We fit a tree with a
    maximum depth of 2, which asks at most two questions about each passenger.
    """)
    return


@app.cell
def fit_small_tree(
    DecisionTreeClassifier,
    FEATURES,
    SimpleImputer,
    X_train,
    export_text,
    make_pipeline,
    y_train,
):
    small_tree = make_pipeline(
        SimpleImputer(strategy="median"),
        DecisionTreeClassifier(max_depth=2, random_state=618))
    small_tree.fit(X_train, y_train)
    print(export_text(small_tree[-1], feature_names=FEATURES))
    return (small_tree,)


@app.cell(hide_code=True)
def small_tree_figure(FEATURES, plot_tree, plt, small_tree):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _fig, _ax = plt.subplots(figsize=(10, 4.5))
    plot_tree(small_tree[-1], feature_names=FEATURES, class_names=["died", "survived"],
              filled=True, impurity=False, proportion=True, rounded=True, ax=_ax)
    _fig
    return


@app.cell(hide_code=True)
def small_tree_reading(X_train, mo, pd, small_tree, y_train):
    # Each training passenger ends in one leaf. scikit-learn numbers the nodes from
    # the top, left branch first, so the leaves in order of number run left to right.
    _leaf = small_tree[-1].apply(small_tree[0].transform(X_train))
    _leaves = y_train.groupby(_leaf).agg(["size", "mean"])
    _leaves.index = ["Boys aged 9.5 or under", "Males over 9.5",
                     "Women and girls in first or second class",
                     "Women and girls in third class"]
    _rows = "\n".join(f"    | {_name} | {int(_n)} | {_rate:.1%} |"
                      for _name, (_n, _rate) in _leaves.iterrows())
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    `female` is True or False, which the tree treats as 1 or 0, so `female <= 0.50`
    asks whether the passenger is male. The tree's four leaves are these:

    | Leaf | Training passengers | Survived |
    |---|---:|---:|
{_rows}

    The tree predicts survival for boys and for women and girls in first or second
    class, and death for the other two groups. The second question differs between
    the branches: for males it is about age, and for females it is about ticket
    class. A tree can do this because each branch is split separately, whereas
    logistic regression gives each feature one coefficient for every passenger.
    """)
    return


@app.cell(hide_code=True)
def follow_intro(mo):
    mo.md(r"""
    ### Following one passenger

    The first passenger in the test set is shown below with the tree's prediction.
    """)
    return


@app.cell
def follow_passenger(FEATURES, small_tree, test_passengers):
    first_passenger = test_passengers[FEATURES].iloc[[0]]
    first_passenger.assign(predicted=small_tree.predict(first_passenger))
    return (first_passenger,)


@app.cell(hide_code=True)
def follow_reading(first_passenger, mo):
    _p = first_passenger.iloc[0]
    _sex = "female" if _p["female"] else "male"
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The passenger is {_sex}, aged {_p['age']:.0f}, in class {_p['pclass']}. The
    first question, "is `female` at most 0.5?", is answered yes, so the passenger
    goes left, and the second, "is `age` at most 9.5?", is answered no, so the
    passenger ends in the leaf of males over 9.5, and the tree predicts that they
    died. The fare and the numbers of relatives are not used, because neither
    question is about them.
    """)
    return


@app.cell(hide_code=True)
def gini_intro(mo):
    mo.md(r"""
    ### How a split is chosen

    A tree measures how mixed a group is by its *Gini impurity*. If a share p of
    the group survived,

    `Gini = 1 - p**2 - (1 - p)**2`

    which is 0 for a group in which everyone survived or everyone died, and 0.5, its
    largest value, for a group split evenly. The impurity of a split is the average
    of its two groups' impurities, weighted by their sizes. To choose a split,
    scikit-learn computes this for every feature and every cut point between two of
    its values, and uses the split with the lowest weighted impurity.

    The cell below does the calculation for the first split, by sex.
    """)
    return


@app.cell
def gini_by_hand(train_passengers, y_train):
    def gini(survived) -> float:
        """Gini impurity of a group, from a Series of 0s and 1s."""
        p = survived.mean()
        return 1 - p**2 - (1 - p)**2

    _is_female = train_passengers["female"]
    gini_all = gini(y_train)
    gini_male = gini(y_train[~_is_female])
    gini_female = gini(y_train[_is_female])
    gini_split = (gini_male * (~_is_female).sum() + gini_female * _is_female.sum()) / len(y_train)
    round(gini_all, 3), round(gini_male, 3), round(gini_female, 3), round(gini_split, 3)
    return gini_all, gini_female, gini_male, gini_split


@app.cell(hide_code=True)
def gini_reading(gini_all, gini_female, gini_male, gini_split, mo, train_passengers):
    _n_female = int(train_passengers["female"].sum())
    _n_male = len(train_passengers) - _n_female
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    | Group | Passengers | Gini impurity |
    |---|---:|---:|
    | All training passengers | {len(train_passengers)} | {gini_all:.3f} |
    | Males | {_n_male} | {gini_male:.3f} |
    | Females | {_n_female} | {gini_female:.3f} |
    | Split by sex, weighted | {len(train_passengers)} | {gini_split:.3f} |

    Splitting by sex lowers the impurity from {gini_all:.3f} to {gini_split:.3f}. No
    cut on any other feature lowers it as far, which is why sex is the first
    question. The same calculation, repeated within each of the two groups, gives the
    second questions.
    """)
    return


@app.cell(hide_code=True)
def depth_intro(mo):
    mo.md(r"""
    ---
    ## The depth of a tree

    A deeper tree asks more questions and can separate the training passengers more
    finely. The table below gives, for trees of several depths, the mean accuracy on
    the folds each tree was fitted to and on the folds it was tested on, in
    five-fold cross-validation. `None` sets no maximum, so that the tree keeps
    splitting until every leaf is pure or cannot be split further.
    """)
    return


@app.cell
def depth_table(
    DecisionTreeClassifier,
    SimpleImputer,
    X_train,
    cross_validate,
    make_pipeline,
    pd,
    y_train,
):
    tree_depths = pd.DataFrame(columns=["fitted folds", "held-out fold"])
    for _depth in [1, 2, 3, 4, 5, 6, 8, 10, None]:
        _tree = make_pipeline(SimpleImputer(strategy="median"),
                              DecisionTreeClassifier(max_depth=_depth, random_state=618))
        _scores = cross_validate(_tree, X_train, y_train, cv=5, return_train_score=True)
        tree_depths.loc[str(_depth)] = [_scores["train_score"].mean(),
                                       _scores["test_score"].mean()]
    tree_depths.round(3)
    return (tree_depths,)


@app.cell(hide_code=True)
def depth_reading(mo, tree_depths):
    _best = tree_depths["held-out fold"].idxmax()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The accuracy on the fitted folds rises with every extra level, to
    {tree_depths.loc['None', 'fitted folds']:.3f} with no maximum, because a deep tree
    can give small groups of passengers, and eventually single passengers, a leaf of
    their own. The accuracy on the held-out folds rises at first, is highest at a
    depth of {_best}, with {tree_depths.loc[_best, 'held-out fold']:.3f}, and then
    falls, to {tree_depths.loc['None', 'held-out fold']:.3f} with no maximum. The
    deepest trees fit details of the training passengers that do not hold for other
    passengers, which is called *overfitting*. The maximum depth is a choice, like k in
    k-NN, and is made by cross-validation.
    """)
    return


@app.cell(hide_code=True)
def forest_intro(mo):
    mo.md(r"""
    ---
    ## Random forests

    A small change to the training set can change a tree's first question, and with
    it every question below. A *random forest* fits many trees, each to a different
    random version of the training set, and combines their predictions. Two things
    differ from tree to tree:

    1. Each tree is fitted to a *bootstrap sample*: as many passengers as the
       training set has, drawn from it at random with replacement, so that some
       passengers appear more than once and others not at all.
    2. At each split, only a random subset of the features is considered. For a
       classifier, scikit-learn uses the square root of the number of features,
       which for our six is two.

    The trees have no maximum depth, so each of them overfits its own sample, but
    in different ways, and averaging them cancels much of the error. For a new
    passenger, `predict_proba` averages the trees' probabilities of survival, and the
    forest predicts survival when that average is at least 0.5. With fully grown
    trees, each tree's probability is almost always 0 or 1, so the average is the
    share of trees that vote for survival.

    We fit a forest of 300 trees and look at the first test passenger again.
    """)
    return


@app.cell
def fit_forest(
    RandomForestClassifier,
    SimpleImputer,
    X_train,
    first_passenger,
    make_pipeline,
    np,
    y_train,
):
    forest = make_pipeline(
        SimpleImputer(strategy="median"),
        RandomForestClassifier(n_estimators=300, random_state=618))
    forest.fit(X_train, y_train)

    # Each tree's vote for the first test passenger: 1 for survived, 0 for died.
    _imputed = forest[0].transform(first_passenger)
    votes = np.array([_tree.predict(_imputed)[0] for _tree in forest[-1].estimators_])
    votes.mean(), forest.predict_proba(first_passenger)[0, 1]
    return forest, votes


@app.cell(hide_code=True)
def forest_reading(forest, mo, votes):
    _n_trees = len(forest[-1].estimators_)
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    {int(votes.sum())} of the {_n_trees} trees vote that the first test passenger
    survived, a share of {votes.mean():.3f}, and `predict_proba` gives the same
    number. It is below 0.5, so the forest predicts that the passenger died, as the
    small tree did.
    """)
    return


@app.cell(hide_code=True)
def n_trees_intro(mo):
    mo.md(r"""
    ### The number of trees

    The table below gives the cross-validated accuracy of forests of different sizes.
    """)
    return


@app.cell
def n_trees_table(
    RandomForestClassifier,
    SimpleImputer,
    X_train,
    cross_val_score,
    make_pipeline,
    pd,
    y_train,
):
    forest_sizes = pd.Series(dtype=float, name="cross-validated accuracy")
    for _n in [1, 10, 50, 100, 300]:
        _forest = make_pipeline(SimpleImputer(strategy="median"),
                                RandomForestClassifier(n_estimators=_n, random_state=618))
        forest_sizes.loc[_n] = cross_val_score(_forest, X_train, y_train, cv=5).mean()
    forest_sizes.round(3)
    return (forest_sizes,)


@app.cell(hide_code=True)
def n_trees_reading(forest_sizes, mo, tree_depths):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    A forest of one tree is a single unlimited tree fitted to a bootstrap sample,
    and its accuracy, {forest_sizes.loc[1]:.3f}, is below that of the unlimited tree in
    the depth table, {tree_depths.loc['None', 'held-out fold']:.3f}. The accuracy
    rises quickly with the number of trees and changes little after about 100, at
    {forest_sizes.loc[100]:.3f} with 100 and {forest_sizes.loc[300]:.3f} with 300.
    Adding trees does not make a forest overfit, as adding depth does to a tree; it
    makes the average more stable, at the cost of time.
    """)
    return


@app.cell(hide_code=True)
def compare_intro(mo):
    mo.md(r"""
    ---
    ## Choosing a model and testing it once

    The table below collects the cross-validated accuracy of each kind of model on
    the training passengers, with the tree at its best depth from the depth table.
    """)
    return


@app.cell
def compare_models(forest_sizes, logistic_cv_accuracy, pd, tree_depths, y_train):
    _best_depth = tree_depths["held-out fold"].idxmax()
    model_comparison = pd.Series({
        "baseline: everyone died": 1 - y_train.mean(),
        "logistic regression": logistic_cv_accuracy,
        f"decision tree, depth {_best_depth}": tree_depths.loc[_best_depth, "held-out fold"],
        "random forest, 300 trees": forest_sizes.loc[300],
    }, name="cross-validated accuracy")
    model_comparison.round(3)
    return (model_comparison,)


@app.cell
def test_forest(forest, mo, np, test_passengers, FEATURES):
    forest_test_accuracy = (forest.predict(test_passengers[FEATURES])
                            == test_passengers["survived"]).mean()
    _n = len(test_passengers)
    _se = np.sqrt(forest_test_accuracy * (1 - forest_test_accuracy) / _n)
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The forest has the highest cross-validated accuracy, so it is the model we test.
    On the {_n} test passengers, its accuracy is {forest_test_accuracy:.3f}. This is
    the number to report. It is higher than the cross-validated estimate, but an
    accuracy measured on {_n} passengers has a standard error of about {_se:.3f}, so
    the two are not far apart.

    The trees do better than logistic regression on these passengers because the
    effect of one feature depends on another: age matters a great deal for boys and
    little for adults, and ticket class matters most for women. A tree represents
    this with separate branches, whereas logistic regression would need extra
    features, such as the product of age and sex, to represent it.
    """)
    return (forest_test_accuracy,)


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - A decision tree predicts by a series of yes-or-no questions about one feature
      at a time, and each leaf predicts its more common class. It needs no scaling.
    - Each split is the one that most lowers the Gini impurity, weighted by group
      size, over every feature and every cut point.
    - A deeper tree fits its training set more closely, and past some depth it does
      worse on held-out data. The maximum depth is chosen by cross-validation.
    - A random forest averages many unlimited trees, each fitted to a bootstrap
      sample with a random subset of features at each split. Its accuracy levels off
      as trees are added.
    - The choice among logistic regression, a tree and a forest is made by
      cross-validation on the training set, and only the chosen model is tested.

    ## Next class

    On Wednesday, November 18, notebook 11 will cover unsupervised learning: PCA
    and k-means clustering.
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
