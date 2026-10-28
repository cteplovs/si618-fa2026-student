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
    # SI 618 - 08a: introduction to machine learning

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 16 (Wed Oct 28)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.10.28.1.CT

    ---

    ## Today you will be able to

    - Explain what supervised learning is, and how classification differs from
      regression
    - Name the parts of a classification problem: features, labels, a training set
      and a test set
    - Explain how k-nearest neighbours classifies a new case, and what the choice of
      k changes
    - Fit a classifier with scikit-learn and measure its accuracy on a test set,
      against a baseline
    - Read a confusion matrix

    ## Reading

    VanderPlas, on machine learning; Géron, on the machine learning landscape and
    the end-to-end project; Grus, on machine learning and on k-nearest neighbours
    (optional).

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Machine learning | 10 |
    | The penguins | 5 |
    | k-nearest neighbours | 10 |
    | scikit-learn: fit and predict | 10 |
    | Test sets, accuracy and the confusion matrix | 10 |
    | Choosing k | 10 |
    """)
    return


@app.cell
def imports():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier

    return (
        KNeighborsClassifier,
        accuracy_score,
        mo,
        np,
        pd,
        plt,
        train_test_split,
    )


@app.cell(hide_code=True)
def ml_intro(mo):
    mo.md(r"""
    ---
    ## Machine learning

    The regression in topic 05 and in Homework 3 was a model: a formula with
    adjustable numbers, which were estimated from data and then used to make
    predictions. Machine learning applies the same idea more widely. A model is
    fitted to data, and the fitted model is then used to make predictions for cases
    it was not fitted to.

    VanderPlas and Géron both divide machine learning into two kinds. In
    *supervised* learning, the data include the answer for every case, called its
    *label*, and the model is fitted to predict the label. In *unsupervised*
    learning there are no labels, and the model looks for structure in the data
    alone.

    | Task | Kind | What is predicted | Example | In this course |
    |---|---|---|---|---|
    | Classification | Supervised | A category | The species of a penguin | Topics 08 and 09 |
    | Regression | Supervised | A number | Median income, from the share of managers (Homework 3) | Topic 05 |
    | Clustering | Unsupervised | Nothing; it finds groups | Groups of similar news stories | Topic 10 |
    | Dimensionality reduction | Unsupervised | Nothing; it summarises many columns in a few | The map of news stories in 07b | Topic 10 |

    The rest of the course uses the following terms for supervised learning.

    | Term | Meaning | Today |
    |---|---|---|
    | Feature | A column used to make the prediction | Bill length and bill depth |
    | Label | The column to be predicted | Species |
    | Training set | The cases the model is fitted to | 75% of the penguins |
    | Test set | Cases set aside to measure how well the model predicts | The other 25% |
    | Fit | Compute and store what the model needs from the training set | |
    | Predict | Give a label for each case | |

    scikit-learn's documentation, and most code you will read, call the table of
    features `X` and the labels `y`, and this notebook does the same. The diagram
    below shows how the parts fit together.
    """)
    return


@app.cell(hide_code=True)
def workflow_diagram(mo):
    # mo.mermaid is a marimo function that draws a diagram from Mermaid's text format.
    mo.mermaid("""
    flowchart LR
        data["penguins<br/>features X and labels y"] --> split["train_test_split"]
        split --> train["training set<br/>X_train, y_train"]
        split --> test["test set<br/>X_test, y_test"]
        train --> fit["model.fit(X_train, y_train)"]
        fit --> fitted["fitted model"]
        fitted --> predict["model.predict(X_test)"]
        test --> predict
        predict --> score["compare the predictions with y_test<br/>accuracy"]
    """)
    return


@app.cell(hide_code=True)
def penguins_intro(mo):
    mo.md(r"""
    ---
    ## The penguins

    The data are measurements of 344 penguins of three species, recorded by Kristen
    Gorman at Palmer Station, Antarctica, from 2007 to 2009, and published by Allison
    Horst, Alison Hill and Kristen Gorman as the *palmerpenguins* dataset. Each row
    is one penguin.

    | Column | Description |
    |---|---|
    | `species` | Adelie, Chinstrap or Gentoo: the label |
    | `island` | Biscoe, Dream or Torgersen |
    | `bill_length_mm`, `bill_depth_mm` | Length and depth of the bill, in millimetres |
    | `flipper_length_mm` | Length of the flipper, in millimetres |
    | `body_mass_g` | Body mass, in grams |
    | `sex` | Male or female |

    The two penguins with no measurements are dropped immediately after we read the
    file:
    """)
    return


@app.cell
def load_penguins(pd):
    PENGUINS_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
    MEASUREMENTS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    SPECIES = ["Adelie", "Chinstrap", "Gentoo"]
    # One colour per species, used in every plot in this notebook.
    SPECIES_COLOURS = {"Adelie": "#1b9e77", "Chinstrap": "#d95f02", "Gentoo": "#7570b3"}

    penguins = (pd.read_csv(PENGUINS_URL)
                .dropna(subset=MEASUREMENTS)
                .reset_index(drop=True))
    penguins.head()
    return MEASUREMENTS, SPECIES, SPECIES_COLOURS, penguins


@app.cell
def species_counts(penguins):
    penguins["species"].value_counts()
    return


@app.cell(hide_code=True)
def bill_plot_intro(mo):
    mo.md(r"""
    Consider two of the measurements first. Each point below is a penguin.
    """)
    return


@app.cell
def bill_plot(SPECIES, SPECIES_COLOURS, penguins, plt):
    _fig, _ax = plt.subplots(figsize=(7, 4.5))
    for _species in SPECIES:
        _rows = penguins[penguins["species"] == _species]
        _ax.scatter(_rows["bill_length_mm"], _rows["bill_depth_mm"], s=14, alpha=0.7,
                    color=SPECIES_COLOURS[_species], label=_species)
    _ax.set_xlabel("Bill length (mm)")
    _ax.set_ylabel("Bill depth (mm)")
    _ax.set_title("Bill length and bill depth of 342 penguins")
    _ax.legend()
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def bill_plot_reading(mo):
    mo.md(r"""
    Adelie penguins have short, deep bills, Gentoo penguins long, shallow ones, and
    Chinstrap penguins long, deep ones, so each species has a region of its own,
    although the regions overlap at their edges. Classifying a penguin from these
    two measurements means deciding which region a new point belongs to.
    """)
    return


@app.cell(hide_code=True)
def knn_intro(mo):
    mo.md(r"""
    ---
    ## k-nearest neighbours

    *k-nearest neighbours* (k-NN) classifies a new case by finding the k cases in
    the training set that are closest to it, and predicting the label that is most
    common among them. Evelyn Fix and Joseph Hodges described the method in a 1951
    report for the US Air Force School of Aviation Medicine, and in 1967 Thomas
    Cover and Peter Hart showed that, given enough data, the one-nearest-neighbour
    rule makes at most twice as many errors as the best possible classifier.

    *Closest* here means the straight-line distance on the plot. For two penguins,
    the distance is

    `sqrt((length_1 - length_2)**2 + (depth_1 - depth_2)**2)`

    which is Pythagoras' theorem applied to the differences in the two
    measurements.

    Please use the sliders below to place a new penguin, shown as a black star, and
    to choose k. The figure draws a line to each of its k nearest neighbours among
    all 342 penguins, and the table under it lists them, computed with the formula
    above.
    """)
    return


@app.cell
def demo_sliders(mo):
    # mo.ui.slider is a marimo function that makes a slider; its .value is the chosen setting.
    new_length = mo.ui.slider(32, 60, step=0.5, value=45, label="Bill length (mm)",
                              show_value=True)
    new_depth = mo.ui.slider(13, 22, step=0.1, value=17, label="Bill depth (mm)",
                             show_value=True)
    demo_k = mo.ui.slider(1, 15, step=1, value=5, label="k", show_value=True)
    # The sliders are displayed with the figure below, so that both are on screen together.
    return demo_k, new_depth, new_length


@app.cell(hide_code=True)
def demo_plot(
    SPECIES,
    SPECIES_COLOURS,
    demo_k,
    demo_nearest,
    mo,
    new_depth,
    new_length,
    penguins,
    plt,
):
    _fig, _ax = plt.subplots(figsize=(6.5, 4))
    for _species in SPECIES:
        _rows = penguins[penguins["species"] == _species]
        _ax.scatter(_rows["bill_length_mm"], _rows["bill_depth_mm"], s=14, alpha=0.4,
                    color=SPECIES_COLOURS[_species], label=_species)
    for _, _row in demo_nearest.iterrows():
        _ax.plot([new_length.value, _row["bill_length_mm"]],
                 [new_depth.value, _row["bill_depth_mm"]], color="black", linewidth=0.8)
    _ax.scatter([new_length.value], [new_depth.value], marker="*", s=250, color="black",
                label="New penguin")
    _ax.set_xlabel("Bill length (mm)")
    _ax.set_ylabel("Bill depth (mm)")
    _ax.legend()
    _fig.tight_layout()
    _votes = demo_nearest["species"].value_counts()
    # mo.vstack is a marimo function that stacks outputs one above the other.
    # mo.md is a marimo function that displays Markdown text.
    mo.vstack([
        # mo.hstack is a marimo function that puts outputs side by side.
        mo.hstack([new_length, new_depth, demo_k], justify="start", gap=2),
        _fig,
        mo.md(f"The votes are "
              + ", ".join(f"{_name} {_count}" for _name, _count in _votes.items())
              + f", so k-NN predicts **{_votes.index[0]}**."),
    ])
    return


@app.cell
def demo_neighbours(demo_k, new_depth, new_length, np, penguins):
    # The distance from the new penguin to every penguin, by the formula above.
    demo_distance = np.sqrt((penguins["bill_length_mm"] - new_length.value) ** 2
                            + (penguins["bill_depth_mm"] - new_depth.value) ** 2)
    demo_nearest = (penguins.assign(distance=demo_distance.round(2))
                    .nsmallest(demo_k.value, "distance")
                    [["species", "bill_length_mm", "bill_depth_mm", "distance"]])
    demo_nearest
    return (demo_nearest,)


@app.cell(hide_code=True)
def practice_knn_intro(mo):
    mo.md(r"""
    ### Practice: write k-NN yourself

    Please complete the function in the cell below so that it returns the species
    k-NN predicts for a penguin with the given bill length and depth, following its
    three comments. The code that builds the table of nearest neighbours shows how
    to compute the distances and keep the nearest penguins, and `.value_counts().index[0]` gives the most
    common value in a column.

    Then check your function against the figure: with the sliders at 45 mm, 17 mm
    and k = 5, it should return Chinstrap. Try a penguin with a bill 50 mm long and
    15 mm deep, and then find a position where k = 1 and k = 9 give different
    answers.
    """)
    return


@app.cell
def practice_knn():
    def my_knn_predict(length, depth, k):
        """The species k-NN predicts from bill length and depth, using all the penguins."""
        # 1. Compute the distance from (length, depth) to every penguin.
        # 2. Keep the k penguins with the smallest distances.
        # 3. Return the most common species among them.
        return None

    my_knn_predict(45, 17, 5)
    return


@app.cell(hide_code=True)
def sklearn_intro(mo):
    mo.md(r"""
    ---
    ## scikit-learn: fit and predict

    scikit-learn, which you used in 07a and 07b for TF-IDF and `train_test_split`,
    provides k-NN as `KNeighborsClassifier`. Every scikit-learn model is used in the
    same three steps.

    | Step | Code | Effect |
    |---|---|---|
    | Create | `KNeighborsClassifier(n_neighbors=5)` | Records the setting k = 5; nothing is computed |
    | Fit | `.fit(X_train, y_train)` | Stores the training cases and their labels |
    | Predict | `.predict(X_test)` | For each row of `X_test`, finds its 5 nearest training cases and returns their most common label |

    A setting chosen before fitting, such as k, is called a *hyperparameter*. For
    k-NN, fitting does little more than store the training set, and the distances
    are computed when it predicts; most other models do their work when they are
    fitted.

    ---
    ## Training and test sets

    A model always does better on the cases it was fitted to than on new ones. A
    one-nearest-neighbour model is right about almost every training case, because
    the nearest neighbour of each training case is itself. To measure how well a
    model predicts, some of the cases are set aside before fitting, as a *test set*.

    In the cell below, `train_test_split` sets aside 25% of the penguins at random.
    `stratify` keeps the share of each species the same in both sets, and
    `random_state` fixes the random choice so that the split is the same every time
    the cell runs.
    """)
    return


@app.cell
def make_split(penguins, train_test_split):
    train_penguins, test_penguins = train_test_split(
        penguins, test_size=0.25, stratify=penguins["species"], random_state=618)
    len(train_penguins), len(test_penguins)
    return test_penguins, train_penguins


@app.cell
def fit_and_predict(KNeighborsClassifier, pd, test_penguins, train_penguins):
    FEATURES = ["bill_length_mm", "bill_depth_mm"]
    X_train, y_train = train_penguins[FEATURES], train_penguins["species"]
    X_test, y_test = test_penguins[FEATURES], test_penguins["species"]

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)                 # fit: training set only
    test_predictions = knn.predict(X_test)    # predict: test set
    pd.DataFrame({"true species": y_test, "predicted": test_predictions}).head(8)
    return test_predictions, y_test, y_train


@app.cell(hide_code=True)
def accuracy_intro(mo):
    mo.md(r"""
    ---
    ## Accuracy

    *Accuracy* is the share of the test cases whose prediction matches the true
    label.
    """)
    return


@app.cell
def knn_accuracy_cell(accuracy_score, test_predictions, y_test):
    knn_accuracy = accuracy_score(y_test, test_predictions)
    knn_accuracy
    return (knn_accuracy,)


@app.cell(hide_code=True)
def practice_accuracy_intro(mo):
    mo.md(r"""
    ### Practice: accuracy by hand

    Please type this one yourself. Replace `None` below with the accuracy computed
    with pandas: compare `test_predictions` with `y_test` using `==`, and take the
    `.mean()` of the result, which counts each `True` as 1 and each `False` as 0.
    Check that it matches the value above.
    """)
    return


@app.cell
def practice_accuracy():
    my_accuracy = None
    my_accuracy
    return


@app.cell(hide_code=True)
def baseline_reading(knn_accuracy, mo, y_test, y_train):
    _most_common = y_train.mode()[0]
    _baseline = (y_test == _most_common).mean()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    An accuracy means little on its own, so it is compared with a *baseline*. The
    simplest baseline predicts the most common species in the training set,
    {_most_common}, for every penguin, and it would be right about
    **{_baseline:.0%}** of the test set. k-NN on the two bill measurements is right
    about **{knn_accuracy:.0%}**.
    """)
    return


@app.cell(hide_code=True)
def confusion_intro(mo):
    mo.md(r"""
    ---
    ## The confusion matrix

    Accuracy counts the mistakes but does not say which they are. A *confusion
    matrix* counts the test cases by their true label (the rows) and their
    predicted label (the columns). The correct predictions are on the diagonal, and
    each count off the diagonal is one kind of mistake. `pd.crosstab`, which you
    used in topic 06, builds it.
    """)
    return


@app.cell
def confusion_matrix(pd, test_predictions, y_test):
    pd.crosstab(y_test, test_predictions, rownames=["true"], colnames=["predicted"])
    return


@app.cell(hide_code=True)
def confusion_reading(mo, pd, test_predictions, y_test):
    _table = pd.crosstab(y_test, test_predictions)
    _mistakes = [(_table.loc[_true, _pred], _true, _pred)
                 for _true in _table.index for _pred in _table.columns
                 if _true != _pred and _table.loc[_true, _pred] > 0]
    if _mistakes:
        _count = max(_n for _n, _, _ in _mistakes)
        _times = "once" if _count == 1 else f"{_count} times"
        _top = [f"a {_true} penguin predicted to be {_pred}"
                for _n, _true, _pred in _mistakes if _n == _count]
        if len(_top) == 1:
            _text = (f"The most common mistake is {_top[0]}, which happens {_times}. "
                     f"Compare that with where the two species overlap in the plot of "
                     f"bill length and bill depth.")
        else:
            _text = (f"The most common mistakes, each of which happens {_times}, are "
                     f"{', '.join(_top[:-1])} and {_top[-1]}. Compare those with where the "
                     f"species overlap in the plot of bill length and bill depth.")
    else:
        _text = "There are no mistakes on this test set."
    # mo.md is a marimo function that displays Markdown text.
    mo.md(_text)
    return


@app.cell(hide_code=True)
def choosing_k_intro(mo):
    mo.md(r"""
    ---
    ## Choosing k

    k is chosen before fitting. A small k follows individual training cases closely,
    including unusual ones, so the regions it draws are ragged. A large k takes a
    vote over many neighbours, so its regions are smoother, but it can miss a small
    group of cases. The figure below colours every point of the plot by the species
    k-NN would predict there, with the training penguins as dots and the test
    penguins as crosses.

    In k-NN, k is the number of neighbours that vote, not the number of groups. With
    k = 1, each new penguin takes the species of the single training penguin nearest
    to it, so all three species are still predicted, each in its own region. At the
    other extreme, with k equal to the size of the training set, 256, every training
    penguin votes on every new one, so k-NN predicts the most common species, Adelie,
    everywhere, which is the baseline. The k in k-means clustering, which you will
    see in topic 10, is a different quantity: the number of clusters.

    Please move the slider and watch how the regions and the two accuracies change.
    """)
    return


@app.cell(hide_code=True)
def regions_helper(
    KNeighborsClassifier,
    SPECIES,
    SPECIES_COLOURS,
    accuracy_score,
    np,
    pd,
    plt,
    test_penguins,
    train_penguins,
):
    # This function only draws the figure for teaching; you would not write it in your own
    # analysis.
    def regions_plot(features, k):
        """Colour the plane by k-NN's prediction for two features, with the penguins on top."""
        model = KNeighborsClassifier(n_neighbors=k).fit(train_penguins[features],
                                                        train_penguins["species"])
        _x, _y = features
        _xs = np.linspace(train_penguins[_x].min() * 0.95, train_penguins[_x].max() * 1.05, 250)
        _ys = np.linspace(train_penguins[_y].min() * 0.95, train_penguins[_y].max() * 1.05, 250)
        _grid_x, _grid_y = np.meshgrid(_xs, _ys)
        _grid = pd.DataFrame({_x: _grid_x.ravel(), _y: _grid_y.ravel()})
        _codes = pd.Categorical(model.predict(_grid), categories=SPECIES).codes
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.contourf(_grid_x, _grid_y, _codes.reshape(_grid_x.shape), levels=[-0.5, 0.5, 1.5, 2.5],
                    colors=[SPECIES_COLOURS[s] for s in SPECIES], alpha=0.2)
        for _species in SPECIES:
            _train = train_penguins[train_penguins["species"] == _species]
            _test = test_penguins[test_penguins["species"] == _species]
            ax.scatter(_train[_x], _train[_y], s=12, color=SPECIES_COLOURS[_species],
                       label=_species)
            ax.scatter(_test[_x], _test[_y], s=40, marker="x", color=SPECIES_COLOURS[_species])
        train_accuracy = accuracy_score(train_penguins["species"],
                                        model.predict(train_penguins[features]))
        test_accuracy = accuracy_score(test_penguins["species"],
                                       model.predict(test_penguins[features]))
        ax.set_xlabel(_x)
        ax.set_ylabel(_y)
        ax.set_title(f"k = {k}: training accuracy {train_accuracy:.0%}, "
                     f"test accuracy {test_accuracy:.0%}")
        ax.legend()
        fig.tight_layout()
        return fig

    return (regions_plot,)


@app.cell
def regions_slider(mo):
    # mo.ui.slider is a marimo function that makes a slider; its .value is the chosen setting.
    regions_k = mo.ui.slider(1, 50, step=1, value=1, label="k", show_value=True)
    # The slider is displayed with the figure below, so that both are on screen together.
    return (regions_k,)


@app.cell
def regions_figure(mo, regions_k, regions_plot):
    # mo.vstack is a marimo function that stacks outputs one above the other.
    mo.vstack([regions_k, regions_plot(["bill_length_mm", "bill_depth_mm"], regions_k.value)])
    return


@app.cell(hide_code=True)
def choosing_k_reading(mo):
    mo.md(r"""
    At k = 1 the training accuracy is close to 100%, because each training penguin
    is its own nearest neighbour, and the test accuracy is the honest measure. It
    is tempting to pick the k with the highest test accuracy, but then the test set
    has been used to make a choice, and it no longer measures how the model will do
    on new penguins. On Monday, notebook 08b will show how cross-validation chooses
    k from the training set alone.

    The choice of measurements matters as much as the choice of k. `body_mass_g` is
    measured in grams, so two penguins usually differ by hundreds in body mass but by
    only a few millimetres in bill length, and the differences in body mass mostly
    decide which penguins are nearest. Body mass separates the Gentoo penguins from
    the other two species, but Adelie and Chinstrap penguins weigh about the same,
    and bill length is the measurement that tells them apart. With k = 5, k-NN has
    the following test accuracies:

    | Measurements | Test accuracy |
    |---|---:|
    | Body mass only | 71% |
    | Bill length only | 73% |
    | Bill length and body mass, in their own units | 81% |
    | Bill length and body mass, on the same scale | 91% |

    In their own units, bill length still adds something, because it decides between
    penguins of similar mass. Notebook 08b will show how to put the measurements on
    the same scale, as in the last row.
    """)
    return


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - Supervised learning fits a model to cases whose labels are known, so that it
      can predict the labels of new cases; classification predicts a category, and
      regression a number.
    - k-nearest neighbours predicts the most common label among the k training cases
      closest to the new case.
    - Every scikit-learn model is created with its settings, fitted with `fit`, and
      used with `predict`.
    - A model's accuracy is measured on a test set that was set aside before
      fitting, and compared with a baseline.
    - A confusion matrix shows which labels are mistaken for which.

    ## Next class

    On Monday, notebook 08b will cover why k-NN needs its features on the same
    scale, how a pipeline keeps the steps of a model together, and how
    cross-validation chooses k without using the test set.
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
