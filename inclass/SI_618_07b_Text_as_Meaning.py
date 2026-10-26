# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "pyarrow==25.0.1",
#     "matplotlib==3.11.1",
#     "scikit-learn==1.9.0",
#     "model2vec==0.10.0",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 618 - 07b: text as meaning

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 15 (Mon Oct 26)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.10.19.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Explain why two texts can mean the same thing while sharing almost no
      words, and what that does to word counts
    - Turn texts into embeddings and compare them with cosine similarity
    - Search a collection by meaning, and judge when that does better than
      TF-IDF and when it does not
    - Build a first classifier, which assigns each text to the category whose
      average embedding it is closest to, and measure how often it is right
    - Name two things embeddings of this kind cannot see

    ## How this notebook works

    This file is today's session, start to finish, and it is the second half
    of In-class 07. At the end of today you upload four files: Wednesday's
    two and today's two. As on Wednesday, each exercise gives each of you one
    version of the question, and a **Reveal the room** button shows them all.

    ✅ **Before anything else, please type your uniqname below**, because it
    chooses your search query in Exercise 1 and your split of the data in
    Exercise 2.
    """)
    return


@app.cell
def _():
    UNIQNAME = ""
    return (UNIQNAME,)


@app.cell
def _():
    import re
    import zlib

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from model2vec import StaticModel
    from sklearn.decomposition import PCA
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.model_selection import train_test_split

    pd.set_option("display.max_colwidth", 110)
    return (
        PCA,
        StaticModel,
        TfidfVectorizer,
        cosine_similarity,
        mo,
        np,
        pd,
        plt,
        re,
        train_test_split,
        zlib,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data and the TF-IDF matrix are Wednesday's: 7,600 AG News items from
    2004 in four categories, cleaned of HTML in the same way.
    """)
    return


@app.cell
def _(TfidfVectorizer, pd, re):
    NEWS_URL = (
        "https://huggingface.co/datasets/fancyzhx/ag_news/resolve/main/"
        "data/test-00000-of-00001.parquet"
    )
    CATEGORIES = ["World", "Sports", "Business", "Sci/Tech"]

    def clean_text(text: str) -> str:
        """Undo the HTML codes left in AG News and drop embedded links."""
        text = re.sub(r"&lt;.*?&gt;", " ", text)
        text = text.replace("#39;", "'").replace("&quot;", '"').replace("quot;", '"')
        text = text.replace("&amp;", "&")
        return re.sub(r"\s+", " ", text).strip()

    news = pd.read_parquet(NEWS_URL)
    news["category"] = news["label"].map(dict(enumerate(CATEGORIES)))
    news["clean"] = news["text"].map(clean_text)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(news["clean"])
    return CATEGORIES, news, tfidf, tfidf_vectorizer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Where counting words fails

    Here are two items from the collection. Please read them before running the
    next cell, and decide whether they are about the same thing.
    """)
    return


@app.cell
def _(news):
    PAIR = [
        news.index[news["clean"].str.startswith("Two Car Bombs Kill 10 Iraqis")][0],
        news.index[news["clean"].str.startswith("Iraq: 26 killed on horrific day")][0],
    ]
    for _i in PAIR:
        print(news.loc[_i, "clean"][:300], "\n")
    return (PAIR,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both report deadly bombings in Iraq. **Cosine similarity** measures how
    alike two rows of a matrix are: it is 1 when the rows point in exactly the
    same direction, and 0 when they have nothing in common. For TF-IDF rows,
    "nothing in common" means no shared words.
    """)
    return


@app.cell
def _(PAIR, cosine_similarity, tfidf):
    print("TF-IDF cosine similarity:", round(float(cosine_similarity(tfidf[PAIR[0]], tfidf[PAIR[1]])[0, 0]), 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The similarity is 0.06, which is close to none. Apart from `Iraq` and `at least`, the
    two reports use different words for the same events (`bombs` and
    `bombers`, `kill`, `killing` and `killed`), and TF-IDF treats every
    different word as unrelated, even when the words mean nearly the same
    thing.

    ---
    ## Part 2: Embeddings

    An **embedding** represents a text as a list of numbers, a vector, chosen
    so that texts with similar meanings get similar vectors. The numbers come
    from a model trained on a very large amount of text, which learned that
    words used in similar contexts, such as `bombs` and `bombers`, should sit
    close together.

    We use **model2vec**, a library of small embedding models that run quickly
    on a laptop without a graphics card. The cell below downloads the model
    the first time it runs, which is about 30 MB, and then encodes all 7,600
    items, which takes a few seconds.
    """)
    return


@app.cell
def _(StaticModel, news):
    model = StaticModel.from_pretrained("minishlab/potion-base-8M")
    embeddings = model.encode(news["clean"].tolist())
    print("Shape:", embeddings.shape)
    embeddings[:2, :6].round(3)
    return embeddings, model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each item is now a row of 256 numbers. Unlike the numbers in a TF-IDF row,
    no single number means anything you can name; only the pattern across all
    256 matters, and only in comparison with other rows. The next cell
    compares the same pair of items this way.
    """)
    return


@app.cell
def _(PAIR, cosine_similarity, embeddings):
    print("Embedding cosine similarity:", round(float(cosine_similarity(embeddings[[PAIR[0]]], embeddings[[PAIR[1]]])[0, 0]), 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The similarity is 0.73, where TF-IDF gave 0.06.

    ### 🚀 Exercise 1: search by meaning

    Searching a collection means turning the query into the same kind of
    vector as the documents, and ranking the documents by cosine similarity to
    it. Your uniqname has assigned you one of four queries, shown below as
    `my_query`.

    ✅ Step 1: Encode `my_query` with `model.encode`, passing it inside a list
    as the cell above does, and assign the result to `my_query_vec`.

    ✅ Step 2: Assign to `my_embed_scores` the cosine similarity between
    `my_query_vec` and every row of `embeddings`, as a one-dimensional array of
    7,600 numbers. `cosine_similarity` returns a table with one row per query,
    so take its first row with `[0]`.

    ✅ Step 3: Do the same with TF-IDF and assign the result to
    `my_tfidf_scores`. Turn the query into a TF-IDF row with
    `tfidf_vectorizer.transform([my_query])`, and compare it with `tfidf`.

    ✅ Step 4: Run the cell after yours, which shows the top five items by each
    score. Once the test passes, press **Reveal the room**, then assign to
    `search_sentence` two or three sentences on which method found better
    items for your query and why, and whether that was true of every query in
    the room's table.
    """)
    return


@app.cell
def _(UNIQNAME, mo, zlib):
    mo.stop(
        not UNIQNAME.strip(),
        mo.md("⚠️ Type your uniqname into `UNIQNAME` at the top of the notebook."),
    )
    QUERIES = [
        "mobile phone maker reports lower earnings",
        "athlete banned after failing drug test",
        "rebels attack government troops",
        "astronauts return safely to Earth",
    ]
    my_seed = zlib.crc32((UNIQNAME.strip().lower() + "07b").encode())
    my_query = QUERIES[my_seed % len(QUERIES)]
    my_query
    return QUERIES, my_query, my_seed


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_query_vec = None
    my_embed_scores = None
    my_tfidf_scores = None
    search_sentence = ""
    return my_embed_scores, my_query_vec, my_tfidf_scores, search_sentence


@app.cell
def _(mo, my_embed_scores, my_tfidf_scores, news, np, pd):
    mo.stop(my_embed_scores is None or my_tfidf_scores is None)

    def top_items(scores, n: int = 5) -> pd.DataFrame:
        """The n items with the highest scores, with their category and score."""
        _best = np.argsort(np.asarray(scores))[::-1][:n]
        return news.loc[_best, ["category", "clean"]].assign(score=np.asarray(scores)[_best].round(3))

    mo.vstack([
        mo.md("**By embedding**"), top_items(my_embed_scores),
        mo.md("**By TF-IDF**"), top_items(my_tfidf_scores),
    ])
    return


@app.cell(hide_code=True)
def _(
    cosine_similarity,
    embeddings,
    model,
    my_embed_scores,
    my_query,
    my_query_vec,
    my_tfidf_scores,
    np,
    tfidf,
    tfidf_vectorizer,
):
    def check_exercise_1():
        assert my_query_vec is not None, "Encode `my_query` with `model.encode([my_query])`."
        assert np.asarray(my_query_vec).shape == (1, embeddings.shape[1]), (
            f"`my_query_vec` has shape {np.asarray(my_query_vec).shape}, where (1, 256) is "
            "expected. Pass the query inside a list: `model.encode([my_query])`."
        )
        _expected_e = cosine_similarity(model.encode([my_query]), embeddings)[0]
        _expected_t = cosine_similarity(tfidf_vectorizer.transform([my_query]), tfidf)[0]
        for _name, _got, _expected in [
            ("my_embed_scores", my_embed_scores, _expected_e),
            ("my_tfidf_scores", my_tfidf_scores, _expected_t),
        ]:
            assert _got is not None, f"Assign the cosine similarities to `{_name}`."
            _got = np.asarray(_got)
            assert _got.shape == (len(_expected),), (
                f"`{_name}` has shape {_got.shape}, where ({len(_expected)},) is expected. "
                "`cosine_similarity` returns one row per query; take `[0]`."
            )
            assert np.allclose(_got, _expected, atol=1e-5), (
                f"`{_name}` does not match. Compare the query's vector with every row of "
                "the matching matrix."
            )

    return (check_exercise_1,)


@app.cell(hide_code=True)
def _(check_exercise_1, search_sentence):
    def test_exercise_1():
        check_exercise_1()

    def test_search_sentence():
        assert len(search_sentence.strip()) >= 100, (
            f"`search_sentence` is {len(search_sentence.strip())} characters, where a "
            "judgement on your query and on the room's table is expected."
        )

    return


@app.cell(hide_code=True)
def _(check_exercise_1, mo):
    try:
        check_exercise_1()
        _ready_1 = True
    except AssertionError:
        _ready_1 = False
    reveal_search = mo.ui.run_button(label="Reveal the room", disabled=not _ready_1)
    mo.vstack([
        reveal_search,
        mo.md("" if _ready_1 else "*The button unlocks once Steps 1 to 3 pass their test.*"),
    ])
    return (reveal_search,)


@app.cell
def _(
    QUERIES,
    cosine_similarity,
    embeddings,
    mo,
    model,
    my_query,
    news,
    np,
    pd,
    reveal_search,
    tfidf,
    tfidf_vectorizer,
):
    mo.stop(not reveal_search.value)
    _rows = []
    for _q in QUERIES:
        _e = cosine_similarity(model.encode([_q]), embeddings)[0]
        _t = cosine_similarity(tfidf_vectorizer.transform([_q]), tfidf)[0]
        for _rank in range(3):
            _rows.append({
                "query": (_q + "  <- yours" if _q == my_query else _q) if _rank == 0 else "",
                "by embedding": news.loc[np.argsort(_e)[::-1][_rank], "clean"][:70],
                "by TF-IDF": news.loc[np.argsort(_t)[::-1][_rank], "clean"][:70],
            })
    pd.DataFrame(_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Embeddings do much better when the query and the stories use different words
    for the same thing: no story says "mobile phone maker", but Motorola and
    Siemens are both found. When the query's own words appear in the right
    stories, as `astronauts` and `Earth` do, TF-IDF does about as well, and it
    is cheaper and easier to explain.

    ---
    ## Part 3: A map of the collection

    Each item is a point in 256 dimensions, which nobody can draw. The map
    below reduces those 256 numbers to two, keeping as much of the spread
    between items as two numbers can hold, and colours each point by its
    category. How the two numbers are chosen is the subject of session 20;
    for now, look at which categories overlap.
    """)
    return


@app.cell
def _(CATEGORIES, PCA, embeddings, mo, news, plt):
    map_xy = PCA(n_components=2, random_state=0).fit_transform(embeddings)
    _fig, _ax = plt.subplots(figsize=(7, 6))
    for _c in CATEGORIES:
        _m = (news["category"] == _c).to_numpy()
        _ax.scatter(map_xy[_m, 0], map_xy[_m, 1], s=4, alpha=0.4, label=_c)
    _ax.legend(markerscale=4)
    _ax.set_xticks([])
    _ax.set_yticks([])
    news_map = mo.ui.matplotlib(_ax, debounce=True)
    mo.vstack([
        mo.md("Drag a box over part of the map, or hold Shift and draw a "
              "lasso, to list the stories inside it."),
        news_map,
    ])
    return map_xy, news_map


@app.cell
def _(map_xy, mo, news, news_map):
    mo.stop(not news_map.value, mo.md("*Nothing selected yet.*"))
    _picked = news.loc[news_map.value.get_mask(map_xy[:, 0], map_xy[:, 1]),
                       ["category", "clean"]]
    mo.vstack([
        mo.md(f"**{len(_picked)} stories selected**"),
        mo.ui.table(_picked, page_size=10, selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sports and World each form a cloud of their own, while Business and
    Sci/Tech overlap heavily, which makes sense for 2004, when much technology
    news was company news. Points that are close on this map are not always close in
    256 dimensions, but the overlap is worth keeping in mind during the next
    exercise.

    ---
    ### 🚀 Exercise 2: a first classifier

    If items in the same category have similar embeddings, a new item can be
    classified by asking which category's average embedding it is closest
    to. This is called a **nearest-centroid** classifier, the **centroid**
    being the average point of a group.

    To find out how often a classifier is right, it has to be tested on items
    it did not learn from. Your uniqname has split the data into a training
    set, `my_train`, of 5,700 items, and a test set, `my_test`, of 1,900 items,
    each an array of row positions. Everyone in the room has a different
    split.

    ✅ Step 1: Build `my_centroids`, a 4 by 256 array whose rows are the mean
    embedding of the training items in each category, in the order of
    `CATEGORIES`. `embeddings[rows].mean(axis=0)` averages a set of rows.

    ✅ Step 2: Assign to `my_predictions` an array with one category name per
    test item: the category whose centroid has the highest cosine similarity
    to the item. `cosine_similarity(embeddings[my_test], my_centroids)` gives
    one row per item and one column per category, and `.argmax(axis=1)` gives
    the position of the highest value in each row.

    ✅ Step 3: Assign to `my_accuracy` the share of test items whose
    prediction matches their category, as a float.

    ✅ Step 4: Once the test passes, look at the table of mistakes that
    appears, press **Reveal the room**, and assign to `centroid_sentence` two
    or three sentences: which categories your classifier confuses most and
    why, and what the spread of accuracies across the room says about a
    single test score.
    """)
    return


@app.cell
def _(mo, my_seed, news, np, train_test_split):
    my_train, my_test = train_test_split(
        np.arange(len(news)), test_size=0.25, random_state=my_seed % 10_000,
        stratify=news["category"],
    )
    mo.md(f"Your training set has {len(my_train):,} items and your test set {len(my_test):,}.")
    return my_test, my_train


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_centroids = None
    my_predictions = None
    my_accuracy = None
    centroid_sentence = ""
    return centroid_sentence, my_accuracy, my_centroids, my_predictions


@app.cell(hide_code=True)
def _(
    CATEGORIES,
    cosine_similarity,
    embeddings,
    my_accuracy,
    my_centroids,
    my_predictions,
    my_test,
    my_train,
    news,
    np,
):
    def check_exercise_2():
        _labels = news["category"].to_numpy()
        _centroids = np.vstack([embeddings[my_train[_labels[my_train] == _c]].mean(axis=0) for _c in CATEGORIES])
        _predictions = np.array(CATEGORIES)[cosine_similarity(embeddings[my_test], _centroids).argmax(axis=1)]
        assert my_centroids is not None, "Build `my_centroids` from the training rows only."
        assert np.asarray(my_centroids).shape == (4, embeddings.shape[1]), (
            f"`my_centroids` has shape {np.asarray(my_centroids).shape}, where (4, 256) is "
            "expected: one row per category."
        )
        assert np.allclose(my_centroids, _centroids, atol=1e-5), (
            "`my_centroids` does not match. Average only the rows in `my_train` for each "
            "category, in the order of `CATEGORIES`; averaging test rows lets the "
            "classifier see the answers."
        )
        assert my_predictions is not None and len(my_predictions) == len(my_test), (
            "`my_predictions` should have one category name per item in `my_test`."
        )
        assert (np.asarray(my_predictions) == _predictions).mean() > 0.999, (
            "`my_predictions` does not match. Turn each `.argmax` position into a name "
            "with `np.array(CATEGORIES)[positions]`."
        )
        assert my_accuracy is not None and abs(float(my_accuracy) - (_predictions == _labels[my_test]).mean()) < 1e-6, (
            f"`my_accuracy` is {my_accuracy}. Compare `my_predictions` with the categories "
            "of the test items, and take the mean of the matches."
        )

    return (check_exercise_2,)


@app.cell(hide_code=True)
def _(centroid_sentence, check_exercise_2):
    def test_exercise_2():
        check_exercise_2()

    def test_centroid_sentence():
        assert len(centroid_sentence.strip()) >= 100, (
            f"`centroid_sentence` is {len(centroid_sentence.strip())} characters, where the "
            "categories confused and a comment on the room's spread are expected."
        )

    return


@app.cell(hide_code=True)
def _(check_exercise_2, mo, my_predictions, my_test, news, pd):
    try:
        check_exercise_2()
        _ready_2 = True
    except AssertionError:
        _ready_2 = False
    mo.stop(not _ready_2, mo.md("*The table of mistakes and the button appear once Steps 1 to 3 pass their test.*"))
    reveal_accuracy = mo.ui.run_button(label="Reveal the room")
    mo.vstack([
        mo.md("Rows are the true category and columns the prediction."),
        pd.crosstab(news["category"].to_numpy()[my_test], my_predictions,
                    rownames=["true"], colnames=["predicted"]),
        reveal_accuracy,
    ])
    return (reveal_accuracy,)


@app.cell
def _(
    CATEGORIES,
    cosine_similarity,
    embeddings,
    mo,
    my_accuracy,
    news,
    np,
    plt,
    reveal_accuracy,
    tfidf,
    train_test_split,
):
    mo.stop(not reveal_accuracy.value)

    def _accuracy(matrix, seed: int) -> float:
        _tr, _te = train_test_split(np.arange(len(news)), test_size=0.25, random_state=seed,
                                    stratify=news["category"])
        _labels = news["category"].to_numpy()
        _cent = np.vstack([np.asarray(matrix[_tr[_labels[_tr] == _c]].mean(axis=0)).ravel() for _c in CATEGORIES])
        return float((np.array(CATEGORIES)[cosine_similarity(matrix[_te], _cent).argmax(axis=1)] == _labels[_te]).mean())

    _room = [_accuracy(embeddings, _s) for _s in range(40)]
    _tfidf_room = [_accuracy(tfidf, _s) for _s in range(10)]
    _fig, _ax = plt.subplots(figsize=(7, 3))
    _ax.hist(_room, bins=12, color="#4c72b0")
    _ax.axvline(float(my_accuracy), color="black", linestyle="--", label="yours")
    _ax.axvline(np.mean(_tfidf_room), color="#c44e52", label="TF-IDF centroids, average")
    _ax.set_xlabel("accuracy on the test set")
    _ax.set_ylabel("splits")
    _ax.legend()
    _ax
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The histogram shows 40 different splits of the same data, with the same
    classifier. Their accuracies run from about 84% to 87%, so a single test
    score is one draw from a range, and a difference of one point between two
    classifiers may say nothing. The red line is the same classifier built on
    TF-IDF rows, which does almost as well: for sorting news into four broad
    sections, which words a story uses already says most of what an embedding
    adds.

    ---
    ## Part 4: What these embeddings cannot see

    The model behind these embeddings gives each word a vector and averages
    them over the text. That makes it fast, and it has consequences you can
    test.
    """)
    return


@app.cell
def _(cosine_similarity, model, pd):
    _pairs = [
        ("dog bites man", "man bites dog"),
        ("the service was good", "the service was not good"),
        ("profits rose sharply", "profits fell sharply"),
    ]
    pd.DataFrame(
        [(_a, _b, round(float(cosine_similarity(model.encode([_a]), model.encode([_b]))[0, 0]), 3)) for _a, _b in _pairs],
        columns=["text", "other text", "cosine similarity"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `dog bites man` and `man bites dog` score exactly 1, because an average of
    the same three word vectors is the same whatever their order. Adding `not`
    changes the meaning entirely but moves the vector very little, since `not`
    is one word in five, and `rose` and `fell` are close because they appear in
    the same kinds of sentence. Larger models that read the whole sentence,
    such as the ones behind ChatGPT and Claude, handle order and negation much
    better, at a far greater cost in computing; session 25 returns to them.

    ---
    ## Summary

    - Word counts treat different words as unrelated, so two texts about the
      same thing can score close to zero
    - An **embedding** is a vector chosen so that texts with similar meanings
      are close, and **cosine similarity** measures how close
    - Searching by embedding finds texts that use other words for the same
      thing, while TF-IDF does as well when the query's words appear in the
      right texts
    - A **nearest-centroid** classifier assigns a text to the category whose
      average it is closest to, and its accuracy has to be measured on items it
      did not learn from, where it varies from split to split
    - Averaged word vectors ignore word order and barely notice negation

    ## Next class

    **Notebook 08a** begins machine learning: features, labels, training and
    test sets, and k-nearest neighbours, which classifies by the closest
    individual items rather than by the closest average.

    ## Additional resources

    - [model2vec](https://github.com/MinishLab/model2vec)
    - Jurafsky & Martin, [*Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/), the chapter on embeddings
    - [scikit-learn: cosine similarity](https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded; it is for anyone who finishes early or wants more
    afterwards.

    ### Write your own query

    Try a query of your own in both searches, and find one where TF-IDF does
    better than embeddings.

    ### Find the closest pair

    Use `cosine_similarity(embeddings)` to find the
    two different items with the highest similarity, and read them.

    ### Classify by TF-IDF

    Repeat Exercise 2 with `tfidf` in place of
    `embeddings`, and compare the table of mistakes.
    """)
    return


@app.cell(hide_code=True)
def _(UNIQNAME, mo):
    _name = UNIQNAME.strip().lower() or "<uniqname>"
    mo.md(rf"""
    ---
    ## 🏁 END OF NOTEBOOK

    In-class 07 is one deliverable covering both sessions, so before you leave
    today, please upload **four files** in a single submission:

    1. `SI618_07a_{_name}.py` and `SI618_07a_{_name}.html` from Wednesday
    2. This notebook, renamed `SI618_07b_{_name}.py`, and its export:
       ```bash
       uvx marimo export html --sandbox SI618_07b_{_name}.py -o SI618_07b_{_name}.html
       ```

    ❗️ Late in-class work is not accepted for credit.
    """)
    return


if __name__ == "__main__":
    app.run()
