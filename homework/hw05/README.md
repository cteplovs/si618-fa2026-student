# Homework 5: Predicting red wine ratings

**100 points.** The homework will be released on Monday, November 2, after class, and is
due **Monday, November 9, before class (3:30 PM)**.

Submit two files to Canvas: your notebook, renamed `SI618_HW05_<uniqname>.py`, and
its HTML export, `SI618_HW05_<uniqname>.html`. The rubric we grade against is in
[RUBRIC.md](RUBRIC.md), and the notebook to start from is
[starter.py](starter.py).

---

## Background

A winery would like to know, before a wine goes to the tasters, whether they are
likely to rate it well. In this homework you will build a k-nearest neighbours
classifier that predicts a wine's rating from eleven chemical measurements, and
you will decide how far its accuracy can be trusted.

Everything you need is in notebooks 08a and 08b: the training and test split,
k-NN and its accuracy, the baseline, `StandardScaler`, pipelines, and
cross-validation.

Most of the points are for decisions and explanations rather than for code. Where
the spec asks you to explain or decide, please write full sentences in a markdown
cell, and refer to specific numbers from your own output.

---

## Data

The data describe 1,599 red wines of the Portuguese *vinho verde* style, collected
by Cortez and colleagues (2009) and published in the UCI Machine Learning
Repository. A copy is kept in the course data repository so that everyone works
from the same file:

```
https://raw.githubusercontent.com/umsi-data-science/data/main/winequality-red.csv
```

Each row is one wine. Eleven columns are laboratory measurements, which the starter
lists as `FEATURES`:

| Column | Unit |
|---|---|
| fixed acidity | g of tartaric acid per litre |
| volatile acidity | g of acetic acid per litre |
| citric acid | g per litre |
| residual sugar | g per litre |
| chlorides | g of sodium chloride per litre |
| free sulfur dioxide | mg per litre |
| total sulfur dioxide | mg per litre |
| density | g per cubic centimetre |
| pH | none |
| sulphates | g of potassium sulphate per litre |
| alcohol | % by volume |

The twelfth column, `quality`, is the median of at least three tasters' ratings on a
scale from 0 to 10.

---

## Part 1: Look at the data (15 points)

### 1.1 Load the wines (5)

Load the file into a DataFrame called `wines`, and add a column `good` that is
`True` for a wine rated 6 or more and `False` otherwise. Show how many wines have
each rating, and how many are good.

### 1.2 Baseline (4)

Compute `baseline`, the accuracy of a classifier that predicts the more common
class for every wine. Say in a sentence why any model you build has to be compared
with this number.

### 1.3 Scales of the measurements (6)

Show the mean, standard deviation, minimum and maximum of each measurement. Then,
before you fit anything, say which measurements you expect to decide the distances
between wines if k-NN uses them unscaled, and why.

---

## Part 2: Scaling (20 points)

### 2.1 Split (4)

Split `wines` into `train_wines` and `test_wines`, with a quarter of the wines in
the test set, stratified by `good`, and with `random_state=618`, so that your
numbers match your classmates'.

### 2.2 Share of the distance by measurement (8)

The average squared difference between two wines in a measurement is twice that
measurement's variance, so each measurement's share of the total variance is its
share of the average unscaled squared distance. Compute `variance_share`, a Series with one
value per measurement, giving its share of the summed variances of all eleven in
the training set, sorted from largest to smallest. Say whether it confirms what you
expected in 1.3.

### 2.3 Unscaled against scaled (8)

Fit k-NN with k = 5 to the training wines twice: once on the unscaled measurements,
and once in a pipeline that standardises them first. Store the two test accuracies
in `unscaled_accuracy` and `scaled_accuracy`. Explain the difference between them,
using your answer to 2.2.

---

## Part 3: Choosing k (20 points)

### 3.1 Cross-validate (10)

Using the training wines only, cross-validate the scaling pipeline with five folds
for every k in the starter's `K_VALUES`. Store the results in `cv_table`, a
DataFrame indexed by k with a column `mean` holding the mean accuracy, and plot the
mean accuracy against k.

### 3.2 Choose and test once (10)

Choose `best_k` from `cv_table`, and say why you chose it. Then fit the pipeline
with `best_k` to all the training wines, compute its accuracy on the test wines,
and store it in `final_accuracy`. Compare it with the baseline and with the
cross-validated estimate for the same k.

---

## Part 4: Duplicates (25 points)

### 4.1 Find them (6)

Count the rows of `wines` that are identical, in every column, to an earlier row,
and store the count in `n_duplicates`. Show two or three groups of identical rows.
Say what you think the duplicates are, and why.

### 4.2 Effect on k = 1 (9)

Look at your `cv_table` again, and in particular at k = 1. Count how many of the
test wines have an identical wine in the training set. Explain how the duplicates
change the cross-validated accuracy for small values of k, and what they do to
the test accuracy.

### 4.3 Without the duplicates (10)

Drop the duplicates from `wines`, keeping the first of each group, and store the
result in `wines_unique`. Then repeat 2.1, 3.1 and 3.2 on it, with the same split
settings, storing the results in `cv_table_unique`, `best_k_unique` and
`final_accuracy_unique`. Show both cross-validation curves on one plot, and the two
baselines, the two choices of k and the two test accuracies in one table. Say
which test accuracy you would report for this model, and why.

---

## Part 5: Summary for a winemaker (20 points)

Write a summary in a markdown cell, with no code and no jargon, for a winemaker who
has been told that "a computer can taste wine from its chemistry":

- Question: state what you set out to learn, in one sentence.
- Finding: state the most important result, in one sentence.
- Evidence: give two or three bullet points, each with a specific number.
- Limits: say what the model can and cannot tell the winemaker, including how far its
  accuracy is above the baseline, and why the duplicates mattered to your
  estimate of it.

---

## Before you submit

- Make sure that every cell has run successfully before you submit your work.
- If you used generative AI in a substantial way, add a sentence at the end saying
  what you used and what it did, as the syllabus asks; it does not affect your
  grade.
- Name both files correctly and upload both.

The starter's tests check that your work has the right shape: that `wines` has a
`good` column, that `cv_table` has one row for each k in `K_VALUES`, and so on.
They do not check your answers, and a green test does not mean a section is
complete.
