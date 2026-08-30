# data/

Nothing in this directory is committed, and `.gitignore` excludes everything here apart
from this file.

Course datasets are fetched when a notebook runs, rather than being stored in the repo,
which keeps the repository small enough to clone comfortably and means nobody is working
from a stale copy. Each notebook loads its own data by one of a few routes:

1. A remote URL, as in
   `pd.read_csv("https://raw.githubusercontent.com/umsi-data-science/data/main/...")`
2. Something built into a library, such as `sklearn.datasets.load_wine()` or
   `seaborn.load_dataset("penguins")`
3. Generated in the notebook itself, usually by a `make_*_data()` factory seeded so that
   everyone gets the same numbers

A few datasets are either too large or too licence-restricted for that, the Kaggle
downloads and the BoardGameGeek reviews file among them. Those are distributed through
Canvas and downloaded into this directory, and they shouldn't be added to git.
