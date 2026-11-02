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

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def title(mo):
    mo.md(r"""
    # SI 618 - 08b: scaling, pipelines and cross-validation

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 17 (Mon Nov 2)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.11.02.1.CT

    ---

    ## Today you will be able to

    - Explain why k-NN needs its features on the same scale, and what happens to its
      predictions when they are not
    - Standardise a feature by hand and with `StandardScaler`
    - Combine scaling and a model in a pipeline, and explain why the scaler is fitted
      to the training set only
    - Estimate a model's accuracy by cross-validation, and use it to choose k without
      using the test set

    ## Reading

    VanderPlas, on hyperparameters and model validation; Géron, on the end-to-end
    project, in particular feature scaling, transformation pipelines and
    cross-validation.

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Where we left off | 5 |
    | Features on different scales | 15 |
    | Standardising | 10 |
    | Pipelines | 15 |
    | Cross-validation | 20 |
    """)
    return


@app.cell
def imports():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    return (
        KNeighborsClassifier,
        StandardScaler,
        cross_val_score,
        make_pipeline,
        mo,
        np,
        pd,
        plt,
        train_test_split,
    )


@app.cell(hide_code=True)
def recap(mo):
    mo.md(r"""
    ---
    ## Where we left off

    On Wednesday, notebook 08a fitted k-nearest neighbours to the penguins, using
    the same training and test sets as today. At the end, it compared four choices
    of measurements, with k = 5:

    | Measurements | Test accuracy |
    |---|---:|
    | Body mass only | 71% |
    | Bill length only | 73% |
    | Bill length and body mass, unscaled | 81% |
    | Bill length and body mass, on the same scale | 91% |

    Today we will see why the last two rows differ, how to put measurements on the
    same scale, and how to choose k without using the test set. We read the data and
    split it exactly as in 08a.
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
def make_split(penguins, train_test_split):
    train_penguins, test_penguins = train_test_split(
        penguins, test_size=0.25, stratify=penguins["species"], random_state=618)

    FEATURES = ["bill_length_mm", "body_mass_g"]
    X_train, y_train = train_penguins[FEATURES], train_penguins["species"]
    X_test, y_test = test_penguins[FEATURES], test_penguins["species"]
    len(train_penguins), len(test_penguins)
    return (
        FEATURES,
        X_test,
        X_train,
        test_penguins,
        train_penguins,
        y_test,
        y_train,
    )


@app.cell(hide_code=True)
def scales_intro(mo):
    mo.md(r"""
    ---
    ## Features on different scales

    Today's two features are bill length, in millimetres, and body mass, in grams.
    The table below describes them in the training set.
    """)
    return


@app.cell
def describe_features(X_train):
    X_train.describe().round(1)
    return


@app.cell(hide_code=True)
def scales_reading(mo):
    mo.md(r"""
    Bill lengths range over about 25 mm, and body masses over about 3,600 g. k-NN
    measures distance with the same formula as on Wednesday,

    `sqrt((length_1 - length_2)**2 + (mass_1 - mass_2)**2)`

    and the formula treats a difference of 1 g in body mass exactly like a
    difference of 1 mm in bill length. Two penguins whose masses differ by 100 g
    are therefore 100 units apart, however similar their bills, while no two
    penguins are more than 25 units apart in bill length alone.

    Consider one penguin from the test set, penguin 178, a Chinstrap whose bill is
    49.5 mm long and who weighs 3,800 g. The table below lists its five nearest
    neighbours in the training set, using the unscaled measurements, with the two squared
    differences that go into each distance.
    """)
    return


@app.cell
def example_penguin_cell(FEATURES, penguins):
    example_penguin = penguins.loc[178, FEATURES].astype(float)
    penguins.loc[[178], ["species"] + FEATURES]
    return (example_penguin,)


@app.cell
def unscaled_neighbours(FEATURES, example_penguin, np, train_penguins):
    _diff = train_penguins[FEATURES] - example_penguin
    unscaled_nearest = (train_penguins[["species"] + FEATURES]
                        .assign(length_diff_squared=(_diff["bill_length_mm"] ** 2).round(2),
                                mass_diff_squared=(_diff["body_mass_g"] ** 2).round(2),
                                distance=np.sqrt((_diff ** 2).sum(axis=1)).round(2))
                        .nsmallest(5, "distance"))
    unscaled_nearest
    return


@app.cell(hide_code=True)
def unscaled_reading(mo):
    mo.md(r"""
    All five neighbours weigh exactly 3,800 g, so their squared differences in mass
    are zero, and the distance is decided by bill length alone among penguins of
    that one mass. Three of the five are Adelie penguins whose bills are 9 to 11 mm
    shorter, so k-NN predicts Adelie, which is wrong. A Chinstrap penguin with a
    bill 49.6 mm long, almost the same as penguin 178's, is not among the five,
    because it weighs 3,775 g, and a difference of 25 g counts for more than a
    difference of 10 mm.
    """)
    return


@app.cell(hide_code=True)
def standardise_intro(mo):
    mo.md(r"""
    ---
    ## Standardising

    To put the features on the same scale, each is *standardised*: its mean is
    subtracted, and the result is divided by its standard deviation,

    `z = (x - mean) / standard deviation`

    A standardised value, sometimes called a *z-score*, counts standard deviations
    above or below the mean, so a penguin whose bill is one standard deviation
    longer than average has a standardised bill length of 1, whatever the unit. After
    standardising, a difference of 1 means the same thing for both features.

    scikit-learn's `StandardScaler` does this, in the same steps as a model.

    | Step | Code | Effect |
    |---|---|---|
    | Create | `StandardScaler()` | Nothing is computed |
    | Fit | `.fit(X_train)` | Computes and stores the mean and standard deviation of each column of the training set |
    | Transform | `.transform(X)` | Standardises the rows of `X` with the stored means and standard deviations |

    The scaler is fitted to the training set only. The test penguins are then
    standardised with the training set's means and standard deviations, so that
    nothing about the test set is used before the model is tested.
    """)
    return


@app.cell
def fit_scaler(FEATURES, StandardScaler, X_train, pd):
    scaler = StandardScaler().fit(X_train)
    pd.DataFrame({"mean": scaler.mean_, "standard deviation": scaler.scale_},
                 index=FEATURES).round(1)
    return (scaler,)


@app.cell(hide_code=True)
def scaler_note(mo):
    mo.md(r"""
    `StandardScaler` divides by the number of penguins, n, when it computes the
    standard deviation, where pandas' `.std()`, in the table above, divides by
    n - 1, so the two differ slightly.
    """)
    return


@app.cell(hide_code=True)
def worked_example(example_penguin, mo, scaler):
    _mean_length, _mean_mass = scaler.mean_.round(1)
    _sd_length, _sd_mass = scaler.scale_.round(1)
    _z_length = (example_penguin["bill_length_mm"] - _mean_length) / _sd_length
    _z_mass = (example_penguin["body_mass_g"] - _mean_mass) / _sd_mass
    # mo.md is a marimo function that displays Markdown text.
    mo.md(rf"""
    We standardise penguin 178's measurements with the rounded means and standard
    deviations above:

    | Feature | Value | Standardised |
    |---|---:|---:|
    | Bill length | {example_penguin["bill_length_mm"]:.1f} mm | ({example_penguin["bill_length_mm"]:.1f} - {_mean_length}) / {_sd_length} = {_z_length:.2f} |
    | Body mass | {example_penguin["body_mass_g"]:,.0f} g | ({example_penguin["body_mass_g"]:,.0f} - {_mean_mass:,}) / {_sd_mass} = {_z_mass:.2f} |

    Its bill is about one standard deviation longer than average, and it weighs about
    half a standard deviation less than average.
    """)
    return


@app.cell
def scaled_neighbours(
    FEATURES,
    X_train,
    example_penguin,
    np,
    pd,
    scaler,
    train_penguins,
):
    _train_z = pd.DataFrame(scaler.transform(X_train), columns=FEATURES, index=X_train.index)
    _example_z = scaler.transform(example_penguin.to_frame().T)[0]
    _diff = _train_z - _example_z
    scaled_nearest = (train_penguins[["species"] + FEATURES]
                      .assign(distance=np.sqrt((_diff ** 2).sum(axis=1)).round(2))
                      .nsmallest(5, "distance"))
    scaled_nearest
    return


@app.cell(hide_code=True)
def scaled_reading(mo):
    mo.md(r"""
    On the same scale, penguin 178's five nearest neighbours are all Chinstrap
    penguins, with bills between 49.0 and 50.6 mm long and masses between 3,675 and
    3,950 g, and k-NN predicts Chinstrap.

    The figure below, in which penguin 178 is the black star, shows the same change
    for every point of the plot. The two kinds of colour in it mean different things:

    - The pale shading is a prediction: each point of the background is coloured by
      the species k-NN would predict for a new penguin with that bill length and
      body mass, so the shading divides the plot into three regions, one for each
      species. The edges between the regions are called *decision boundaries*.
    - The dots are data: each is a training penguin, coloured by its true species.

    Where a dot's colour matches the shading around it, k-NN agrees with that
    penguin's species, and where it does not, k-NN gets that penguin wrong.

    On the left, unscaled, the regions are horizontal bands, because body
    mass decides almost every distance, so the prediction changes as you move up or
    down but hardly at all as you move left or right. Most of the orange Chinstrap
    dots lie in green Adelie shading, so k-NN would call most Chinstrap penguins
    Adelie, as it did penguin 178. On the right, on the same scale, both features
    shape the regions, the Chinstrap penguins have an orange region of their own,
    and the star sits in it.
    """)
    return


@app.cell(hide_code=True)
def regions_figure(
    FEATURES,
    KNeighborsClassifier,
    SPECIES,
    SPECIES_COLOURS,
    StandardScaler,
    example_penguin,
    make_pipeline,
    np,
    pd,
    plt,
    train_penguins,
):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _x, _y = FEATURES
    _xs = np.linspace(train_penguins[_x].min() * 0.95, train_penguins[_x].max() * 1.05, 250)
    _ys = np.linspace(train_penguins[_y].min() * 0.95, train_penguins[_y].max() * 1.05, 250)
    _grid_x, _grid_y = np.meshgrid(_xs, _ys)
    _grid = pd.DataFrame({_x: _grid_x.ravel(), _y: _grid_y.ravel()})
    _models = {
        "Unscaled": KNeighborsClassifier(n_neighbors=5),
        "On the same scale": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    }
    _fig, _axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for _ax, (_name, _model) in zip(_axes, _models.items()):
        _model.fit(train_penguins[FEATURES], train_penguins["species"])
        _codes = pd.Categorical(_model.predict(_grid), categories=SPECIES).codes
        _ax.contourf(_grid_x, _grid_y, _codes.reshape(_grid_x.shape),
                     levels=[-0.5, 0.5, 1.5, 2.5],
                     colors=[SPECIES_COLOURS[s] for s in SPECIES], alpha=0.2)
        for _species in SPECIES:
            _rows = train_penguins[train_penguins["species"] == _species]
            _ax.scatter(_rows[_x], _rows[_y], s=12, color=SPECIES_COLOURS[_species],
                        label=_species)
        _ax.scatter([example_penguin[_x]], [example_penguin[_y]], marker="*", s=250,
                    color="black", label="Penguin 178")
        _ax.set_title(f"{_name}, k = 5")
        _ax.set_xlabel("Bill length (mm)")
    _axes[0].set_ylabel("Body mass (g)")
    _axes[1].legend()
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def pipeline_intro(mo):
    mo.md(r"""
    ---
    ## Pipelines

    A scaled model is now two steps, a scaler and a model, and each must be fitted
    to the training set only and then applied, in order, to any new penguin. A
    *pipeline* keeps the steps together, so that the pair can be used as a single
    model. `make_pipeline` builds one from the steps, in order.

    | Pipeline method | Effect on the scaler | Effect on k-NN |
    |---|---|---|
    | `.fit(X_train, y_train)` | Fits it to `X_train` and standardises `X_train` | Fits it to the standardised `X_train` |
    | `.predict(X_test)` | Standardises `X_test` with the training means and standard deviations | Predicts from the standardised `X_test` |
    | `.score(X_test, y_test)` | As for `.predict` | Returns the accuracy of the predictions |

    `.score` is a shorter way of writing `accuracy_score(y_test, model.predict(X_test))`,
    which you used on Wednesday, and every scikit-learn classifier has it.
    """)
    return


@app.cell
def build_pipeline(
    KNeighborsClassifier,
    StandardScaler,
    X_train,
    make_pipeline,
    y_train,
):
    knn_pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    knn_pipeline.fit(X_train, y_train)
    return (knn_pipeline,)


@app.cell
def compare_scaling(KNeighborsClassifier, X_test, X_train, knn_pipeline, pd, y_test, y_train):
    _unscaled = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
    pd.DataFrame({"test accuracy": [_unscaled.score(X_test, y_test),
                                    knn_pipeline.score(X_test, y_test)]},
                 index=["unscaled", "on the same scale"]).round(3)
    return


@app.cell(hide_code=True)
def pipeline_reading(mo):
    mo.md(r"""
    These are the last two rows of Wednesday's table. Fitting the scaler to all 342
    penguins, before the split, would have let the test penguins' measurements
    change the means and standard deviations used for the training set. The effect
    on the penguins would be small, but the test set would no longer be wholly unseen
    by the model, and its accuracy would no longer be a fair estimate for new
    penguins. With a pipeline fitted to the training set alone, that mistake cannot
    happen.
    """)
    return


@app.cell(hide_code=True)
def practice_pipeline_intro(mo):
    mo.md(r"""
    ### Practice: a pipeline with four measurements

    Without scaling, k-NN with k = 5 on all four measurements (bill length, bill
    depth, flipper length and body mass) is right about 79% of the test set, which
    is worse than with two. Please complete the cell below: build a pipeline that
    standardises the four measurements and then applies k-NN with k = 5, fit it to
    the training penguins, and compute its accuracy on the test penguins. The four
    column names are in `MEASUREMENTS`, so `train_penguins[MEASUREMENTS]` is the
    training set's features, and the cell that builds `knn_pipeline` above shows the
    steps.
    """)
    return


@app.cell
def practice_pipeline(MEASUREMENTS, test_penguins, train_penguins):
    my_pipeline = None
    my_pipeline_accuracy = None
    my_pipeline_accuracy
    return


@app.cell(hide_code=True)
def cv_intro(mo):
    mo.md(r"""
    ---
    ## Cross-validation

    On Wednesday, the figure for choosing k showed the test accuracy for every k,
    and it was tempting to pick the k with the highest. That uses the test set to
    make a choice, after which it no longer measures how the model will do on new
    penguins, so the choice has to be made from the training set alone.

    *Cross-validation* does this by splitting the training set into parts, called
    *folds*, usually five. The model is fitted five times, each time to four folds,
    and its accuracy is measured on the fifth, which it was not fitted to. Each fold
    is the validation fold once:

    | Round | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 |
    |---|---|---|---|---|---|
    | 1 | validation | fit | fit | fit | fit |
    | 2 | fit | validation | fit | fit | fit |
    | 3 | fit | fit | validation | fit | fit |
    | 4 | fit | fit | fit | validation | fit |
    | 5 | fit | fit | fit | fit | validation |

    The average of the five accuracies estimates how well the model will do on new
    penguins, and every training penguin is used for validation exactly once. Our
    256 training penguins make five folds of 51 or 52, and for a classifier
    scikit-learn keeps the share of each species about the same in every fold.

    `cross_val_score` runs the five rounds and returns the five accuracies. Given a
    pipeline, it fits the scaler again in every round, to the four folds the model
    is fitted to, so the validation fold is never used for scaling either.
    """)
    return


@app.cell
def cv_once(X_train, cross_val_score, knn_pipeline, y_train):
    cv_scores = cross_val_score(knn_pipeline, X_train, y_train, cv=5)
    cv_scores.round(3), cv_scores.mean().round(3)
    return


@app.cell(hide_code=True)
def choose_k_intro(mo):
    mo.md(r"""
    To choose k, we cross-validate a pipeline for each of several values of k and
    keep the k whose mean accuracy is highest, without using the test set.
    """)
    return


@app.cell
def cv_by_k(
    KNeighborsClassifier,
    StandardScaler,
    X_train,
    cross_val_score,
    make_pipeline,
    pd,
    y_train,
):
    K_VALUES = [1, 3, 5, 7, 9, 11, 15, 21, 25, 31, 41, 51]
    _rows = []
    for _k in K_VALUES:
        _pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=_k))
        _scores = cross_val_score(_pipeline, X_train, y_train, cv=5)
        _rows.append({"k": _k, **{f"fold {_i}": _s for _i, _s in enumerate(_scores, start=1)},
                      "mean": _scores.mean()})
    cv_table = pd.DataFrame(_rows).set_index("k").round(3)
    cv_table
    return (cv_table,)


@app.cell
def cv_plot(cv_table, plt):
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    _ax.plot(cv_table.index, cv_table["mean"], marker="o", color="black")
    _ax.set_xlabel("k")
    _ax.set_ylabel("Mean cross-validation accuracy")
    _fig.tight_layout()
    _fig
    return


@app.cell
def best_k_cell(cv_table):
    best_k = int(cv_table["mean"].idxmax())
    best_k
    return (best_k,)


@app.cell(hide_code=True)
def cv_reading(best_k, cv_table, mo):
    _low, _high = cv_table["mean"].min(), cv_table["mean"].max()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The highest mean accuracy is {_high:.1%}, at k = {best_k}. Every k in the table
    is within a few points of it, from {_low:.1%} to {_high:.1%}, and one penguin in
    a fold of 51 is about 2 points, so the choice among the middle values of k
    matters less than the scaling did. With k chosen, we fit the pipeline to the
    whole training set and test it once.
    """)
    return


@app.cell
def final_test(
    KNeighborsClassifier,
    StandardScaler,
    X_test,
    X_train,
    best_k,
    make_pipeline,
    y_test,
    y_train,
):
    final_pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k))
    final_pipeline.fit(X_train, y_train)
    final_accuracy = final_pipeline.score(X_test, y_test)
    final_accuracy
    return (final_accuracy,)


@app.cell(hide_code=True)
def final_reading(best_k, cv_table, final_accuracy, mo):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    With k = {best_k}, the pipeline is right about {final_accuracy:.0%} of the test
    set, against {cv_table.loc[best_k, "mean"]:.0%} estimated by cross-validation.
    The two estimates differ because each comes from a different, small set of
    penguins: one test penguin is more than a point of accuracy. If we now went back
    and tried other values of k on the test set, we would be choosing k by the test
    set again, so this number is the one we report.
    """)
    return


@app.cell(hide_code=True)
def practice_cv_intro(mo):
    mo.md(r"""
    ### Practice: choose k by cross-validation

    Please cross-validate a pipeline that standardises all four measurements and
    applies k-NN, for k = 1, 5, 9, 15 and 25, using the training penguins only.
    Store the mean accuracy for each k in `my_cv_accuracies`, a dictionary from k to
    its mean accuracy, and the k you would choose in `my_best_k`. The cell that
    builds `cv_table` above shows the loop.
    """)
    return


@app.cell
def practice_cv(MEASUREMENTS, train_penguins):
    my_cv_accuracies = None
    my_best_k = None
    my_cv_accuracies, my_best_k
    return


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - k-NN measures distance in the units of the features, so a feature measured in
      large numbers, such as body mass in grams, decides which cases are nearest
      unless the features are put on the same scale.
    - Standardising subtracts each feature's mean and divides by its standard
      deviation; `StandardScaler` computes both from the training set.
    - A pipeline keeps the scaler and the model together, so that both are fitted to
      the training set only and applied in order to new cases.
    - Cross-validation fits a model to four folds of the training set and measures
      it on the fifth, five times, and is used to choose settings such as k without
      using the test set, which is used once, at the end.

    ## Next class

    On Wednesday, notebook 09a will cover ways of measuring a classifier other than
    accuracy.
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
