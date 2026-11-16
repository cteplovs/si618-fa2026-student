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
    # SI 618 - 11: PCA and k-means clustering

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 22 (Wed Nov 18)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.11.16.1.CT

    ---

    ## Today you will be able to

    - Explain what a principal component is, and read the share of the variance that
      each component accounts for
    - Plot data on its first two principal components, and read which measurements
      each component depends on
    - Explain the two steps of k-means, and choose a number of clusters from a plot of
      the inertia
    - Explain why measurements should be standardised before PCA and k-means

    ## Reading

    Géron, on dimensionality reduction and on unsupervised learning techniques.

    ## Timing

    | Part | Minutes |
    |---|---:|
    | Where we left off | 3 |
    | The wines | 5 |
    | Principal component analysis | 20 |
    | k-means clustering | 20 |
    | Clustering the unscaled measurements | 7 |
    | Exercise: cluster the wines with a number of clusters of your choice | 8 |
    """)
    return


@app.cell
def imports():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.datasets import load_wine
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    return KMeans, PCA, StandardScaler, load_wine, mo, np, pd, plt


@app.cell(hide_code=True)
def recap(mo):
    mo.md(r"""
    ---
    ## Where we left off

    Every model from topic 08 to Monday's trees and forests was fitted to examples whose
    answer was known: a species, a diagnosis, whether a passenger survived. That is
    *supervised* learning, and its results could be checked against the answers in a
    test set.

    Today's methods are *unsupervised*: they use the measurements alone, with no column
    of answers. Principal component analysis (PCA) finds a smaller number of new
    variables that keep as much of the variation in the data as possible, and k-means
    divides the rows into groups of similar rows. Neither predicts anything, so there is
    no training and test split today.
    """)
    return


@app.cell(hide_code=True)
def data_intro(mo):
    mo.md(r"""
    ---
    ## The wines

    The data describe 178 wines from one region of Italy, made from three cultivars
    (grape varieties), with thirteen chemical measurements each. They come from a
    study by Forina and colleagues and are included in scikit-learn. We keep the
    cultivar in a separate Series, `cultivar`, and do not give it to PCA or k-means; we
    use it only afterwards, to compare their results with the cultivars.
    """)
    return


@app.cell
def load_wines(load_wine):
    _wine = load_wine(as_frame=True)
    wines = _wine.data
    cultivar = _wine.target
    wines.describe().T[["mean", "std", "min", "max"]].round(2)
    return cultivar, wines


@app.cell(hide_code=True)
def scale_reading(cultivar, mo, wines):
    _counts = cultivar.value_counts().sort_index()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    There are {_counts[0]}, {_counts[1]} and {_counts[2]} wines of cultivars 0, 1 and 2.
    The measurements are on very different scales: `proline` has a standard
    deviation of {wines['proline'].std():.0f}, and `hue` one of
    {wines['hue'].std():.2f}. PCA and k-means both work with distances and variances,
    so, as with k-NN in topic 08 and Homework 5, we standardise every measurement
    first, so that each has a mean of 0 and a standard deviation of 1.
    """)
    return


@app.cell
def standardise(StandardScaler, pd, wines):
    wines_scaled = pd.DataFrame(StandardScaler().fit_transform(wines),
                                columns=wines.columns, index=wines.index)
    wines_scaled.std().round(2).head(3)
    return (wines_scaled,)


@app.cell(hide_code=True)
def pca_intro(mo):
    mo.md(r"""
    ---
    ## Principal component analysis

    The first *principal component* is the direction through the thirteen-dimensional
    cloud of wines along which they vary most. The second is the direction, at right
    angles to the first, along which they vary most of what is left, and so on, up to
    thirteen components. Each component is a weighted sum of the standardised
    measurements, and its weights are called *loadings*.

    Because the components are ordered by how much of the variance they account for, the
    first few can stand in for all thirteen measurements, for example to plot the wines
    in two dimensions. We fit PCA with all thirteen components and look at the share of
    the variance that each accounts for.
    """)
    return


@app.cell
def fit_pca(PCA, np, pd, wines_scaled):
    pca = PCA().fit(wines_scaled)
    variance_shares = pd.DataFrame({
        "share": pca.explained_variance_ratio_,
        "cumulative": np.cumsum(pca.explained_variance_ratio_),
    }, index=[f"PC{_i}" for _i in range(1, 14)])
    variance_shares.round(3)
    return pca, variance_shares


@app.cell(hide_code=True)
def scree_figure(plt, variance_shares):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    _ax.bar(range(1, 14), variance_shares["share"], color="grey", label="share")
    _ax.plot(range(1, 14), variance_shares["cumulative"], "ko-", label="cumulative")
    _ax.set_xticks(range(1, 14))
    _ax.set_xlabel("Principal component")
    _ax.set_ylabel("Share of the variance")
    _ax.legend(loc="center right")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def variance_reading(mo, variance_shares):
    _first_two = variance_shares.loc["PC2", "cumulative"]
    _n_80 = int((variance_shares["cumulative"] < 0.8).sum()) + 1
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The first component accounts for {variance_shares.loc['PC1', 'share']:.1%} of the
    variance and the second for {variance_shares.loc['PC2', 'share']:.1%}, so a plot of
    the first two shows {_first_two:.1%} of the variation in the thirteen measurements.
    It takes {_n_80} components to reach 80%. A plot like the one above is called a
    *scree plot*, and the point where its bars level off is one guide to how many
    components are worth keeping.
    """)
    return


@app.cell(hide_code=True)
def projection_intro(mo):
    mo.md(r"""
    ### The wines on the first two components

    `transform` computes each wine's value on each component. The figure below plots
    every wine on the first two, coloured by its cultivar, which PCA was not given.
    """)
    return


@app.cell
def project(cultivar, pca, pd, wines_scaled):
    wine_components = pd.DataFrame(pca.transform(wines_scaled)[:, :2],
                                   columns=["PC1", "PC2"], index=wines_scaled.index)
    wine_components["cultivar"] = cultivar
    wine_components.head()
    return (wine_components,)


@app.cell(hide_code=True)
def projection_figure(plt, variance_shares, wine_components):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _fig, _ax = plt.subplots(figsize=(6, 5))
    for _c, _marker in zip([0, 1, 2], ["o", "s", "^"]):
        _rows = wine_components[wine_components["cultivar"] == _c]
        _ax.scatter(_rows["PC1"], _rows["PC2"], marker=_marker, alpha=0.7,
                    label=f"cultivar {_c}")
    _ax.set_xlabel(f"PC1 ({variance_shares.loc['PC1', 'share']:.0%} of the variance)")
    _ax.set_ylabel(f"PC2 ({variance_shares.loc['PC2', 'share']:.0%} of the variance)")
    _ax.legend()
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def loadings_intro(mo):
    mo.md(r"""
    The three cultivars fall in three regions of the plot, with some overlap, although
    PCA used only the measurements. To read what each component measures, we look at
    its loadings: a measurement with a large positive loading raises a wine's value on
    the component, and one with a large negative loading lowers it.
    """)
    return


@app.cell
def loadings(pca, pd, wines):
    component_loadings = pd.DataFrame(pca.components_[:2].T, index=wines.columns,
                                      columns=["PC1", "PC2"])
    component_loadings.sort_values("PC1").round(2)
    return (component_loadings,)


@app.cell(hide_code=True)
def loadings_reading(component_loadings, mo):
    _pc1 = component_loadings["PC1"].sort_values()
    _pc2 = component_loadings["PC2"].sort_values()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    PC1 is highest for wines with more `{_pc1.index[-1]}` and `{_pc1.index[-2]}`, and
    lowest for wines with more `{_pc1.index[0]}` and `{_pc1.index[1]}`. PC2 is highest for wines with more
    `{_pc2.index[-1]}` and `{_pc2.index[-2]}`. In the plot, cultivar 0 is high on both
    components, cultivar 2 is low on PC1 and high on PC2, and cultivar 1 is low on PC2.
    """)
    return


@app.cell(hide_code=True)
def kmeans_intro(mo):
    mo.md(r"""
    ---
    ## k-means clustering

    k-means divides the rows into k groups, called *clusters*. It starts with k points,
    called *centroids*, and then repeats two steps until the clusters stop changing:

    1. Each wine is assigned to the cluster of its nearest centroid.
    2. Each centroid is moved to the mean of the wines assigned to it.

    The result depends on where the centroids start, so scikit-learn runs the whole
    process `n_init` times from different starting points and keeps the run with the
    lowest *inertia*, the sum of the squared distances from each wine to its centroid.

    k-means needs k before it starts. One guide is to compute the inertia for several
    values of k and look for the value after which adding a cluster lowers it only a
    little, which is called the *elbow*. We do that for k from 1 to 8 on the thirteen
    standardised measurements.
    """)
    return


@app.cell
def inertia_table(KMeans, pd, wines_scaled):
    inertias = pd.Series({
        _k: KMeans(n_clusters=_k, n_init=10, random_state=618).fit(wines_scaled).inertia_
        for _k in range(1, 9)
    }, name="inertia")
    inertias.round(0)
    return (inertias,)


@app.cell(hide_code=True)
def elbow_figure(inertias, plt):
    # This cell only draws the figure for teaching; you would not write it in your own
    # analysis.
    _fig, _ax = plt.subplots(figsize=(6, 3.5))
    _ax.plot(inertias.index, inertias.values, "ko-")
    _ax.set_xlabel("Number of clusters, k")
    _ax.set_ylabel("Inertia")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def elbow_reading(inertias, mo):
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The inertia falls by {inertias[1] - inertias[2]:.0f} from one cluster to two, by
    {inertias[2] - inertias[3]:.0f} from two to three, and by only
    {inertias[3] - inertias[4]:.0f} from three to four, so the elbow is at k = 3. Real
    data rarely give an elbow this clear, and k is often chosen partly by what the
    clusters are for. We fit k-means with k = 3 and compare its clusters with the
    cultivars.
    """)
    return


@app.cell
def fit_kmeans(KMeans, cultivar, pd, wines_scaled):
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=618).fit(wines_scaled)
    pd.crosstab(kmeans.labels_, cultivar, rownames=["cluster"], colnames=["cultivar"])
    return (kmeans,)


@app.cell(hide_code=True)
def kmeans_reading(cultivar, kmeans, mo, pd):
    _table = pd.crosstab(kmeans.labels_, cultivar)
    _matched = int(_table.max(axis=1).sum())
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    The cluster numbers are arbitrary, so what matters is whether each cluster contains
    mainly one cultivar. Each does: if each cluster is labelled with its most common
    cultivar, {_matched} of the {len(cultivar)} wines are in the cluster of their own
    cultivar. k-means was not given the cultivars, so this shows that the three
    cultivars differ in their chemistry consistently enough for the clusters to
    recover them.

    With data that have no known groups, there is nothing to compare the clusters
    with, and the clusters are described instead by their centroids: the mean of each
    measurement in each cluster.
    """)
    return


@app.cell(hide_code=True)
def unscaled_intro(mo):
    mo.md(r"""
    ---
    ## Clustering the unscaled measurements

    We now fit the same k-means to the measurements as they were recorded, without
    standardising them.
    """)
    return


@app.cell
def unscaled_kmeans(KMeans, cultivar, pd, wines):
    kmeans_unscaled = KMeans(n_clusters=3, n_init=10, random_state=618).fit(wines)
    pd.crosstab(kmeans_unscaled.labels_, cultivar, rownames=["cluster"],
                colnames=["cultivar"])
    return (kmeans_unscaled,)


@app.cell(hide_code=True)
def unscaled_reading(cultivar, kmeans_unscaled, mo, pd, wines):
    _table = pd.crosstab(kmeans_unscaled.labels_, cultivar)
    _matched = int(_table.max(axis=1).sum())
    _share = wines.var()["proline"] / wines.var().sum()
    # mo.md is a marimo function that displays Markdown text.
    mo.md(f"""
    Without standardising, only {_matched} of the {len(cultivar)} wines are in the
    cluster of their own cultivar. `proline` accounts for {_share:.1%} of the summed
    variance of the thirteen unscaled measurements, so the distances between wines,
    and with them the clusters, depend almost entirely on proline. This is the same
    effect that sulfur dioxide had on k-NN in Homework 5.
    """)
    return


@app.cell(hide_code=True)
def cluster_exercise_intro(mo):
    mo.md(r"""
    ### 🚀 Exercise: cluster the wines with a number of clusters of your choice

    ✅ Step 1: In the cell below, set `my_k` to a whole number from 2 to 8 other than
    3. Then fit `KMeans` with `n_clusters=my_k`, `n_init=10` and `random_state=618` to
    `wines_scaled`, store it in `my_kmeans`, and show a crosstab of its clusters
    against `cultivar`.

    ✅ Step 2: In the markdown cell after it, say in a sentence or two how your clusters
    relate to the three cultivars: which cultivars are combined, or which are split.
    """)
    return


@app.cell
def my_clusters():
    # Choose k, fit k-means with it, and show the crosstab.
    my_k = None
    my_kmeans = None
    return my_k, my_kmeans


@app.cell(hide_code=True)
def cluster_answer(mo):
    mo.md(r"""
    *Your answer here: which cultivars your clusters combine or split.*
    """)
    return


@app.cell(hide_code=True)
def check_cluster_exercise(my_k, my_kmeans, wines_scaled):
    def test_my_clusters():
        assert isinstance(my_k, int) and 2 <= my_k <= 8 and my_k != 3, (
            "Set `my_k` to a whole number from 2 to 8 other than 3."
        )
        assert hasattr(my_kmeans, "labels_"), (
            "Store the fitted KMeans in `my_kmeans`, after calling `.fit(wines_scaled)`."
        )
        assert len(my_kmeans.labels_) == len(wines_scaled), (
            "Fit `my_kmeans` to `wines_scaled`, which has one row per wine."
        )
        assert len(set(my_kmeans.labels_)) == my_k, (
            "`my_kmeans` should have `my_k` clusters. Check `n_clusters`."
        )
    return


@app.cell(hide_code=True)
def summary(mo):
    mo.md(r"""
    ---
    ## Summary

    - Unsupervised methods use the measurements alone, with no column of answers, so
      there is no test set to check them against.
    - PCA finds new variables, the principal components, ordered by the share of the
      variance they account for. The loadings show which measurements each component
      depends on, and the first two components give a plot of all the measurements.
    - k-means assigns each row to the nearest of k centroids and moves each centroid to
      the mean of its rows, repeating until the clusters stop changing. A plot of the
      inertia against k is one guide to choosing k.
    - Both methods depend on distances and variances, so the measurements should be
      standardised first.

    ## Next class

    On Monday, November 23, notebook 12 will introduce Polars. Homework 6 is due at
    3:30 that day.
    """)
    return


@app.cell(hide_code=True)
def end_of_notebook(mo):
    mo.md(r"""
    ---
    ## 🏁 END OF NOTEBOOK

    In-class 11 is a one-line answer to the question on Canvas under *In-class 11*,
    which you should submit before the end of the session. There is nothing to upload
    from this notebook.
    """)
    return


if __name__ == "__main__":
    app.run()
