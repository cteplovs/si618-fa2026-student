# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "marimo==0.24.0",
#     "pandas==3.0.5",
#     "numpy==2.5.2",
#     "pyarrow==25.0.1",
#     "scikit-learn==1.9.0",
#     "spacy==3.8.16",
#     "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
#     "pytest==9.1.1",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SI 618 - 07a: text as data

    Dr. Chris Teplovs, University of Michigan School of Information

    **Fall 2026** - Session 14 (Wed Oct 21)

    Copyright (c) 2026. This notebook may not be shared outside of the course
    without permission. Notebook version 2026.10.20.1.CT

    ---

    ## Learning objectives

    By the end of today you will be able to:

    - Split text into tokens with spaCy, and say what it does that splitting on
      spaces does not
    - Use lemmas and stop words to count the words that say what a text is about
    - Turn a collection of documents into a document-term matrix, and weight it
      with TF-IDF so that common words stop dominating

    ## How this notebook works

    **This file is today's session, start to finish**, and it is the first half
    of In-class 07. Each exercise gives each of you one of four versions of the
    same question, and once you have answered yours, a **Reveal the room**
    button shows all four side by side.

    **Today begins on paper.** Please complete the sheet handed out at the
    start of class, which shows your own work from Homework 3, before you
    open this notebook. Answer it without a laptop or phone, and hand it in
    when you have finished; it is worth 4 of In-class 07's 32 points.

    ✅ **Then type your uniqname below**, because it chooses your news
    category for both exercises.
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
    import numpy as np
    import pandas as pd
    import spacy
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

    pd.set_option("display.max_colwidth", 120)
    pd.set_option("display.max_rows", 30)
    return CountVectorizer, TfidfVectorizer, mo, np, pd, re, spacy, zlib


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The data

    AG News is a collection of news items gathered from more than 2,000 news
    sources in 2004 and widely used for teaching and research in text
    classification. Each item is a headline followed by the first sentence or
    two of the story, and each has one of four categories: World, Sports,
    Business, and Sci/Tech. We use its test set of 7,600 items, 1,900 in each
    category, which is published as a single file.
    """)
    return


@app.cell
def _(pd):
    NEWS_URL = (
        "https://huggingface.co/datasets/fancyzhx/ag_news/resolve/main/"
        "data/test-00000-of-00001.parquet"
    )
    CATEGORIES = ["World", "Sports", "Business", "Sci/Tech"]
    news = pd.read_parquet(NEWS_URL)
    news["category"] = news["label"].map(dict(enumerate(CATEGORIES)))
    news[["category", "text"]].sample(5, random_state=1)
    return CATEGORIES, news


@app.cell(hide_code=True)
def _(mo):
    predict_length = mo.ui.radio(
        options=["World", "Sports", "Business", "Sci/Tech", "They are about the same"],
        label="**Predict first.** Which category's items are longest, on average, in words?",
    )
    predict_length
    return (predict_length,)


@app.cell(hide_code=True)
def _(mo, predict_length):
    reveal_length = mo.ui.run_button(label="Reveal", disabled=predict_length.value is None)
    reveal_length
    return (reveal_length,)


@app.cell(hide_code=True)
def _(mo, news, reveal_length):
    mo.stop(not reveal_length.value)
    _lengths = news.groupby("category")["text"].apply(lambda _s: _s.str.split().str.len().mean()).round(1)
    mo.vstack([
        _lengths.to_frame("mean words per item"),
        mo.md(
            "They are about the same, between 37 and 39 words. Every item is a headline "
            "and an opening sentence, and the people who built the dataset kept that "
            "shape for every category, so length tells the categories apart no better "
            "than chance. Whatever separates them has to be in the words themselves."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Tokens, lemmas and stop words

    Splitting a text into units that can be counted is called **tokenising**,
    and each unit is a **token**. The cell below tokenises one sentence by
    splitting on spaces, which is what you did with restaurant names in 06b.
    """)
    return


@app.cell
def _():
    example = "Wal-Mart's U.S. sales rose 2.5% to $4.3bn, but it isn't enough, analysts said."
    example.split()
    return (example,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Punctuation stays attached to words (`'$4.3bn,'`, `'said.'`), so `said.`
    and `said` would be counted as different words, and `isn't` stays as one
    piece although it is two words. **spaCy** is a library that tokenises with
    rules written for each language and labels every token, and loading its
    small English model, in the next cell, takes a few seconds.
    """)
    return


@app.cell
def _(spacy):
    nlp = spacy.load("en_core_web_sm")
    return (nlp,)


@app.cell
def _(example, nlp, pd):
    example_doc = nlp(example)
    pd.DataFrame(
        [(_t.text, _t.lemma_, _t.pos_, _t.is_stop, _t.is_alpha) for _t in example_doc],
        columns=["token", "lemma", "part of speech", "stop word", "letters only"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each row is one token, and each column is something spaCy worked out about
    it:

    - **token** shows that `isn't` is now `is` and `n't`, and that punctuation
      has tokens of its own, while `U.S.` stays whole because spaCy knows the
      abbreviation.
    - **lemma** is the dictionary form, so `rose` becomes `rise`, `said` becomes
      `say`, and `sales` becomes `sale`, which lets different forms of a word be
      counted together.
    - **part of speech** labels each token as a noun, a verb, a proper noun and
      so on.
    - **stop word** marks words such as `to`, `but` and `it`, which are so
      common in every text that counting them says little about any one text.
    - **letters only** is `False` for punctuation, numbers and symbols.

    The next cell runs spaCy on all 7,600 items and keeps, for each item, the
    lemmas of the tokens that are letters only and not stop words, in a new
    DataFrame, `news_tok`, with a `lemmas` column. It turns off the parts of
    spaCy we do not need yet, and it still takes about 20 seconds.
    """)
    return


@app.cell
def _(news, nlp):
    news_tok = news.assign(lemmas=[
        [_t.lemma_.lower() for _t in _doc if _t.is_alpha and not _t.is_stop]
        for _doc in nlp.pipe(news["text"], batch_size=256, disable=["parser", "ner"])
    ])
    news_tok[["category", "lemmas"]].head(3)
    return (news_tok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🚀 Exercise 1: the words of your category

    Your uniqname has assigned you one of the four categories, shown below as
    `my_category`.

    ✅ Step 1: Build `my_items`, the rows of `news_tok` whose category is
    `my_category`.

    ✅ Step 2: Build `my_lemmas`, a Series with one row per lemma across all of
    `my_items`. The `.explode()` method from 06b turns a column of lists into
    one row per item of each list.

    ✅ Step 3: Assign to `my_top_lemmas` the ten most common lemmas in
    `my_lemmas`, with their counts, as a Series.

    ✅ Step 4: Once the test below passes, press **Reveal the room** to see the
    ten most common lemmas of all four categories.
    """)
    return


@app.cell
def _(CATEGORIES, UNIQNAME, mo, zlib):
    mo.stop(
        not UNIQNAME.strip(),
        mo.md("⚠️ Type your uniqname into `UNIQNAME` at the top of the notebook."),
    )
    my_category = CATEGORIES[zlib.crc32(UNIQNAME.strip().lower().encode()) % len(CATEGORIES)]
    my_category
    return (my_category,)


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_items = None
    my_lemmas = None
    my_top_lemmas = None
    return my_items, my_lemmas, my_top_lemmas


@app.cell(hide_code=True)
def _(my_category, my_items, my_lemmas, my_top_lemmas, news_tok, pd):
    def check_exercise_1():
        _all = news_tok.loc[news_tok["category"] == my_category, "lemmas"].explode()
        _expected = _all.value_counts().head(10)
        assert isinstance(my_items, pd.DataFrame), "Build `my_items` by filtering `news_tok` on `category`."
        assert len(my_items) == 1900 and set(my_items["category"]) == {my_category}, (
            f"`my_items` has {len(my_items)} rows; each category has 1,900. Keep only the "
            f"rows where `category` is {my_category!r}."
        )
        assert isinstance(my_lemmas, pd.Series), "Build `my_lemmas` as a Series, with `.explode()`."
        assert len(my_lemmas) == len(_all), (
            f"`my_lemmas` has {len(my_lemmas)} rows. It should have one row per lemma, "
            "across every item; explode the `lemmas` column of `my_items`."
        )
        assert isinstance(my_top_lemmas, pd.Series), "Assign a Series to `my_top_lemmas`."
        assert list(my_top_lemmas.index) == list(_expected.index), (
            "`my_top_lemmas` should be the ten most common lemmas, most common first. "
            "`.value_counts()` sorts them for you, and `.head(10)` keeps ten."
        )

    return (check_exercise_1,)


@app.cell(hide_code=True)
def _(check_exercise_1):
    def test_exercise_1():
        check_exercise_1()

    return


@app.cell(hide_code=True)
def _(check_exercise_1, mo):
    try:
        check_exercise_1()
        _ready_1 = True
    except AssertionError:
        _ready_1 = False
    reveal_lemmas = mo.ui.run_button(label="Reveal the room", disabled=not _ready_1)
    mo.vstack([
        reveal_lemmas,
        mo.md("" if _ready_1 else "*The button unlocks once Steps 1 to 3 pass their test.*"),
    ])
    return (reveal_lemmas,)


@app.cell
def _(CATEGORIES, mo, my_category, news_tok, pd, reveal_lemmas):
    mo.stop(not reveal_lemmas.value)
    pd.DataFrame({
        (_c + "  <- yours" if _c == my_category else _c): (
            news_tok.loc[news_tok["category"] == _c, "lemmas"].explode().value_counts().head(10).index
        )
        for _c in CATEGORIES
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some lemmas belong to one category (`iraq`, `game`, `oil`, `software`),
    while others appear in several. `say` and `new` are in most news stories,
    and `ap`, `reuters` and `afp` are news agencies, which name their source
    whatever the story is about. Removing stop words did not remove these,
    because they are common in news rather than in English, and Part 2 handles
    them differently.

    ---
    ## Part 2: The document-term matrix

    To compare documents, or to use them in a model later in the term, each
    document has to become a row of numbers. A **document-term matrix** has
    one row per document and one column per word in the whole collection, and
    each cell counts how many times that word appears in that document.

    Before building one, the text needs cleaning. AG News was scraped from web
    pages, and some HTML survived:
    """)
    return


@app.cell
def _(news):
    print("Items containing '#39;':", int(news["text"].str.contains("#39;", regex=False).sum()))
    print("Items containing 'quot;':", int(news["text"].str.contains("quot;", regex=False).sum()))
    print("Items containing '&lt;':", int(news["text"].str.contains("&lt;", regex=False).sum()))
    print()
    print(news.loc[news["text"].str.contains("FullQuote", regex=False), "text"].iloc[0][:260])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The code `#39;` is what remains of `&#39;`, the HTML code for an
    apostrophe, so `isn #39;t` was `isn't`, and each `&lt;A HREF=...&gt;` is a
    whole link to a stock quote. The function below replaces the codes with
    the characters they stand for and removes the links.

    Two of its lines use **regular expressions** (`re.sub`), patterns that
    describe text rather than spell it out. You will not need to write one in
    this course.
    """)
    return


@app.cell
def _(news, re):
    def clean_text(text: str) -> str:
        """Undo the HTML codes left in AG News and drop embedded links."""
        text = re.sub(r"&lt;.*?&gt;", " ", text)
        text = text.replace("#39;", "'").replace("&quot;", '"').replace("quot;", '"')
        text = text.replace("&amp;", "&")
        return re.sub(r"\s+", " ", text).strip()

    clean_texts = news["text"].map(clean_text)
    clean_texts[news["text"].str.contains("FullQuote", regex=False)].iloc[0][:200]
    return (clean_texts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    scikit-learn's `CountVectorizer` builds the matrix. Its `fit_transform`
    learns the vocabulary from the documents and counts every word in every
    document in one step, lowercasing as it goes.
    """)
    return


@app.cell
def _(CountVectorizer, clean_texts):
    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(clean_texts)
    count_vocab = count_vectorizer.get_feature_names_out()
    print("Shape:", counts.shape)
    print("Share of cells that are not zero:", round(counts.nnz / (counts.shape[0] * counts.shape[1]), 5))
    return count_vocab, counts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That is 7,600 rows and more than 21,000 columns, and only about one cell in
    700 is not zero, because a news item uses about 30 different words.
    scikit-learn stores the matrix in a **sparse** form that records only the
    cells that are not zero; storing all 160 million cells would waste memory
    on zeros.

    **TF-IDF** reweights the counts by multiplying two numbers: the **term
    frequency** (TF), which is the count in the document as before, and the
    **inverse document frequency** (IDF), which is large for words that appear
    in few documents and small for words that appear in nearly all of them.
    The product is high for a word that is frequent in this document and rare
    in the rest, which is what makes a word tell you what a document is about.
    `TfidfVectorizer` builds this matrix in the same way as `CountVectorizer`.
    """)
    return


@app.cell
def _(TfidfVectorizer, clean_texts):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(clean_texts)
    tfidf_vocab = tfidf_vectorizer.get_feature_names_out()
    return tfidf, tfidf_vocab


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The helper below takes rows of either matrix and returns, for each row, the
    word with the highest score. Applied to the first three items, it shows
    which word each matrix ranks highest for each item.
    """)
    return


@app.cell
def _(clean_texts, count_vocab, counts, np, pd, tfidf, tfidf_vocab):
    def top_word(matrix, vocab) -> pd.Series:
        """For each row of a document-term matrix, the column with the highest score."""
        return pd.Series(vocab[np.asarray(matrix.argmax(axis=1)).ravel()])

    pd.DataFrame({
        "item": clean_texts.str[:70].head(3),
        "highest count": top_word(counts[:3], count_vocab),
        "highest TF-IDF": top_word(tfidf[:3], tfidf_vocab),
    })
    return (top_word,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🚀 Exercise 2: what TF-IDF finds in your category

    You have the same category as in Exercise 1.

    ✅ Step 1: Build `my_mask`, a boolean array or Series that is `True` for the
    rows of `news` in `my_category`. A matrix can be filtered with it, as in
    `counts[my_mask]`.

    ✅ Step 2: Assign to `my_count_top` the eight words that are most often the
    highest-count word of an item in your category, with how many items each
    one tops, as a Series. Use `top_word` on `counts` and `count_vocab`, and then
    `.value_counts()`.

    ✅ Step 3: Assign to `my_tfidf_top` the same for `tfidf` and `tfidf_vocab`.

    ✅ Step 4: Once the test below passes, press **Reveal the room**, then
    assign to `tfidf_sentence` two or three sentences saying why the two lists
    differ, and naming one word on any category's TF-IDF list that you did not
    expect, with a guess at why it is there.
    """)
    return


@app.cell
def _():
    # Your code here. Extra cells are fine, as long as the names are new.
    my_mask = None
    my_count_top = None
    my_tfidf_top = None
    tfidf_sentence = ""
    return my_count_top, my_mask, my_tfidf_top, tfidf_sentence


@app.cell(hide_code=True)
def _(
    count_vocab,
    counts,
    my_category,
    my_count_top,
    my_mask,
    my_tfidf_top,
    news,
    np,
    pd,
    tfidf,
    tfidf_vocab,
    top_word,
):
    def check_exercise_2():
        _m = (news["category"] == my_category).to_numpy()
        assert my_mask is not None, "Build `my_mask` from the `category` column."
        assert np.array_equal(np.asarray(my_mask, dtype=bool), _m), (
            f"`my_mask` should be True exactly for the 1,900 rows in {my_category!r}."
        )
        for _name, _got, _matrix, _vocab in [
            ("my_count_top", my_count_top, counts, count_vocab),
            ("my_tfidf_top", my_tfidf_top, tfidf, tfidf_vocab),
        ]:
            _expected = top_word(_matrix[_m], _vocab).value_counts().head(8)
            assert isinstance(_got, pd.Series), f"Assign a Series to `{_name}`."
            assert len(_got) == 8, f"`{_name}` has {len(_got)} rows; keep eight with `.head(8)`."
            assert set(_got.index) == set(_expected.index), (
                f"`{_name}` does not match. Use `top_word` on the rows selected by "
                "`my_mask`, then `.value_counts().head(8)`."
            )

    return (check_exercise_2,)


@app.cell(hide_code=True)
def _(check_exercise_2, tfidf_sentence):
    def test_exercise_2():
        check_exercise_2()

    def test_tfidf_sentence():
        assert len(tfidf_sentence.strip()) >= 100, (
            f"`tfidf_sentence` is {len(tfidf_sentence.strip())} characters, where a reason "
            "and an unexpected word are expected."
        )

    return


@app.cell(hide_code=True)
def _(check_exercise_2, mo):
    try:
        check_exercise_2()
        _ready_2 = True
    except AssertionError:
        _ready_2 = False
    reveal_tfidf = mo.ui.run_button(label="Reveal the room", disabled=not _ready_2)
    mo.vstack([
        reveal_tfidf,
        mo.md("" if _ready_2 else "*The button unlocks once Steps 1 to 3 pass their test.*"),
    ])
    return (reveal_tfidf,)


@app.cell
def _(
    CATEGORIES,
    mo,
    my_category,
    news,
    pd,
    reveal_tfidf,
    tfidf,
    tfidf_vocab,
    top_word,
):
    mo.stop(not reveal_tfidf.value)
    pd.DataFrame({
        (_c + "  <- yours" if _c == my_category else _c): (
            top_word(tfidf[(news["category"] == _c).to_numpy()], tfidf_vocab).value_counts().head(8).index
        )
        for _c in CATEGORIES
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    By raw count, the top word of nearly every item is `the`, `to` or `of`, so
    the count lists are almost identical across categories. TF-IDF discounts
    words that appear everywhere, and the words that remain name the subject of
    each story, such as a person, a team or a company. A word such as `you` on
    a TF-IDF list usually comes from the few items written as advice or
    reviews, where it is both frequent and unusual.

    ---
    ## Part 3: Languages without spaces

    Splitting on spaces assumes that a space marks the end of a word, which
    holds for English but not for many of the world's languages. Chinese,
    Japanese, Thai, Lao, Khmer and Burmese are written with no spaces between
    words. Vietnamese puts a space between syllables, so many of its words are
    split in two, and Korean puts one after a word together with the particles
    attached to it, so the same word turns up in several forms. The Chinese
    sentence below means "Tomorrow we are going to the library to read".
    """)
    return


@app.cell
def _(CountVectorizer):
    chinese_example = "我们明天去图书馆看书。"
    print(chinese_example.split())
    _char_vectorizer = CountVectorizer(analyzer="char")
    _char_vectorizer.fit([chinese_example])
    print(list(_char_vectorizer.get_feature_names_out()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `.split()` returns the whole sentence as one piece. `analyzer="char"` tells
    `CountVectorizer` to count characters instead of words, which needs no
    word boundaries at all and suits Chinese in particular, where most
    characters have a meaning of their own. It is what Homework 4 asks you to
    do with a novel of 120 chapters. spaCy also has Chinese models that learn
    where words begin and end, but counting characters does not need them.

    ---
    ## Summary

    - **Tokenising** splits text into countable units, and spaCy's rules handle
      punctuation, contractions and abbreviations that `.split()` does not
    - **Lemmas** count different forms of a word together, and **stop words**
      are removed because they are common everywhere
    - A **document-term matrix** has a row per document and a column per word,
      and is stored sparsely because almost every cell is zero
    - **TF-IDF** weights a word up when it is frequent in a document and rare in
      the collection, which surfaces what each document is about

    ## Next class

    **Notebook 07b** compares documents by meaning rather than by shared words,
    with embeddings, and builds a first classifier from them.

    ## Additional resources

    - [spaCy 101](https://spacy.io/usage/spacy-101)
    - [scikit-learn: text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
    - Jurafsky & Martin, [*Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/), the chapter on words and tokens
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🧭 Optional: going further

    Nothing here is graded; it is for anyone who finishes early or wants more
    afterwards.

    **Named entities.** spaCy can also mark spans of text that name something,
    such as a person, a place or an organisation, which are called **named
    entities**. In the example sentence from Part 1, it found these:
    """)
    return


@app.cell
def _(example, nlp):
    [(_e.text, _e.label_) for _e in nlp(example).ents]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `GPE` stands for a geopolitical entity, meaning a country, city or state.
    The cell below runs the full model on the World items, which takes about
    ten seconds, and counts the places and people they mention most.
    """)
    return


@app.cell
def _(news, nlp, pd):
    _world = news.loc[news["category"] == "World", "text"]
    world_entities = pd.DataFrame(
        [(_e.text, _e.label_) for _doc in nlp.pipe(_world, batch_size=128) for _e in _doc.ents],
        columns=["entity", "label"],
    )
    pd.concat(
        {
            "places": world_entities.query("label == 'GPE'")["entity"].value_counts().head(8).reset_index(),
            "people": world_entities.query("label == 'PERSON'")["entity"].value_counts().head(8).reset_index(),
        },
        axis=1,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The list is a record of 2004: the war in Iraq, the crisis in Darfur, the
    US presidential election between George W. Bush and John Kerry, and Yasser
    Arafat, who died that November. Notice also that `US` and `U.S.` are
    counted separately, as are `Arafat` and `Yasser Arafat`, so counting
    entities well means deciding which spellings refer to the same thing.

    **Merge the spellings.** Map `U.S.` to `US` and `Arafat` to `Yasser Arafat`
    in `world_entities`, recount, and see how the order changes.

    **Remove the agencies.** Pass `stop_words=["ap", "reuters", "afp"]` plus
    spaCy's own list to `CountVectorizer`, and compare the raw-count lists
    with Exercise 2.

    **Try bigrams.** `TfidfVectorizer(ngram_range=(1, 2))` counts pairs of
    words as well as single words. Find out which pairs top the Sports items.
    """)
    return


@app.cell(hide_code=True)
def _(UNIQNAME, mo):
    _name = UNIQNAME.strip().lower() or "<uniqname>"
    mo.md(rf"""
    ---
    ## 🏁 END OF NOTEBOOK

    **Before you leave today.** Please save two files:

    1. This notebook, renamed `SI618_07a_{_name}.py`
    2. An HTML export of it:
       ```bash
       uvx marimo export html --sandbox SI618_07a_{_name}.py -o SI618_07a_{_name}.html
       ```

    ❗️ **Keep both files.** In-class 07 is one deliverable covering today and
    Monday, and at the end of Monday's session you will upload all four files,
    today's two and Monday's two, in a single submission.
    """)
    return


if __name__ == "__main__":
    app.run()
