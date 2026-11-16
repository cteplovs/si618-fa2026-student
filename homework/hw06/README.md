# Homework 6: Predicting credit card default

Homework 6 is worth 100 points. It will be released on Monday, November 16, after
class, and is due **Monday, November 23, before class (3:30 PM)**.

Submit two files to Canvas: your notebook, renamed `SI618_HW06_<uniqname>.py`, and
its HTML export, `SI618_HW06_<uniqname>.html`. The rubric we grade against is in
[RUBRIC.md](RUBRIC.md), and the notebook to start from is
[starter.py](starter.py).

---

## Background

A bank would like to know, a month ahead, which of its credit card holders are likely
to miss a payment, so that it can call them and offer a payment plan before they
default. In this homework you will compare logistic regression, a decision tree and a
random forest for that prediction, choose a model and a threshold, and decide how far
the result can be trusted.

Everything you need is in notebooks 08 to 10: the training and test split, pipelines,
cross-validation, precision and recall, thresholds, ROC curves and AUC, logistic
regression, decision trees and random forests.

Most of the points are for decisions and explanations rather than for code. Where
the spec asks you to explain or decide, please write full sentences in a markdown
cell, and refer to specific numbers from your own output.

## AI assistants

An AI assistant could complete this homework, explanations included, and nothing in
the homework or its rubric is designed to prevent that. The syllabus asks you to use
AI and to say so, and that applies here as it has all term. The decisions this
homework asks for are like the ones your group will make for Milestone 3 and explain
in the presentation.

---

## Data

The data describe 30,000 credit card holders at a bank in Taiwan in 2005, collected
by Yeh and Lien (2009) and published in the UCI Machine Learning Repository as
"Default of credit card clients". A copy is kept in the course data repository so
that everyone works from the same file:

```
https://raw.githubusercontent.com/umsi-data-science/data/main/credit_default.csv
```

Each row is one card holder. The starter renames two columns, `PAY_0` to `PAY_1` so
that the six repayment columns are numbered like the others, and `default payment
next month` to `default`. The documentation gives the columns as follows.

| Column | Meaning |
|---|---|
| `LIMIT_BAL` | Credit limit, in New Taiwan dollars |
| `SEX` | 1 = male, 2 = female |
| `EDUCATION` | 1 = graduate school, 2 = university, 3 = high school, 4 = others |
| `MARRIAGE` | 1 = married, 2 = single, 3 = others |
| `AGE` | Age in years |
| `PAY_1` to `PAY_6` | Repayment status in September (`PAY_1`) back to April 2005 (`PAY_6`): -1 = paid on time, 1 = payment one month late, 2 = two months late, and so on up to 9 = nine months or more |
| `BILL_AMT1` to `BILL_AMT6` | Amount of the bill statement, September back to April, in New Taiwan dollars |
| `PAY_AMT1` to `PAY_AMT6` | Amount paid, September back to April, in New Taiwan dollars |
| `default` | 1 if the card holder defaulted in October 2005, 0 otherwise |

---

## Part 1: Look at the data (15 points)

### 1.1 Load the card holders (5)

Load the file into a DataFrame called `credit`, using the starter's renaming. Show
how many card holders defaulted, and compute `baseline`, the accuracy of a classifier
that predicts no default for every card holder.

### 1.2 Codes the documentation does not list (10)

Show how many card holders have each value of `EDUCATION`, `MARRIAGE` and `PAY_1`,
and compare the values with the documentation above. For each column, say which
values are not documented and how many card holders have them, and decide what you
will do about them: keep them as they are, combine them with a documented value, or
drop the rows. Give a reason for each decision, and apply your decisions to a copy of
`credit` called `credit_clean`, which you will use from here on.

---

## Part 2: Logistic regression (20 points)

### 2.1 Split (3)

Split `credit_clean` into `train_credit` and `test_credit`, with a quarter of the card
holders in the test set, stratified by `default`, and with `random_state=618`, so that
your numbers match your classmates'.

### 2.2 Accuracy and AUC (7)

Cross-validate a pipeline that standardises the features and fits logistic
regression, with five folds on the training set, and store its mean accuracy and
mean AUC in `logistic_accuracy` and `logistic_auc`. Compare the accuracy with
`baseline`, and explain why AUC is the better measure for comparing models on these
data.

### 2.3 Sex, marital status and age (10)

Cross-validate the same pipeline again without `SEX`, `MARRIAGE` and `AGE`, and store
its mean AUC in `logistic_auc_without`. Then decide whether your models should use
these three columns, and store the list of features you will use from here on in
`FEATURES_USED`. Your reason should go beyond the change in AUC: in the United States,
for example, the Equal Credit Opportunity Act prohibits lenders from discriminating
on the basis of sex or marital status, among other characteristics.

---

## Part 3: Trees and forests (25 points)

### 3.1 The depth of a tree (7)

Cross-validate a `DecisionTreeClassifier` with `random_state=618` on `FEATURES_USED`
for every maximum depth in the starter's `DEPTHS`, scoring by AUC. Store the mean AUC
for each depth in `depth_table`, plot it against the depth, and choose `best_depth`,
with a reason.

### 3.2 The size of a forest's leaves (9)

A forest's trees have no maximum depth, but `min_samples_leaf` sets the smallest
number of training card holders that a leaf may contain. Cross-validate a
`RandomForestClassifier` with 300 trees, `random_state=618` and `n_jobs=-1`, scoring
by AUC, for every value in the starter's `LEAF_SIZES`. Store the mean AUC for each
value in `leaf_table`, and choose `best_leaf`. Explain why the forest's AUC changes
with the size of its leaves, using what 3.1 shows about deep trees.

### 3.3 Compare and choose (9)

Using `cross_val_predict` with five folds on the training set, compute the
cross-validated probabilities of default for logistic regression, the tree with
`best_depth` and the forest with `best_leaf`. Plot the three ROC curves on one figure,
and show the three AUCs in one table. Choose the model you will use from here on,
with a reason, and store its probabilities in `chosen_probabilities`.

---

## Part 4: A threshold, and one test (20 points)

### 4.1 Choose a threshold (10)

The bank has enough staff to call at most 20% of its card holders each month. For
every threshold in the starter's `THRESHOLDS`, compute from `chosen_probabilities` the
share of training card holders who would be called, and the precision and recall of
calling them. Store these in `threshold_table`. Choose `chosen_threshold`, the
threshold that finds the most defaulters while calling at most 20% of card holders,
and say in a sentence what its precision and recall would mean for the bank's callers.

### 4.2 Test once (10)

Fit your chosen model to all the training card holders, and compute on the test card
holders its AUC, and the share called, the precision and the recall at
`chosen_threshold`. Store them in `test_results`. Compare each with its
cross-validated estimate, and say which numbers you would report.

---

## Part 5: Summary for a credit manager (20 points)

Write a summary in a markdown cell, with no code and no jargon, for the bank's credit
manager, who will decide whether to start the calls:

- Question: state what you set out to learn, in one sentence.
- Finding: state the most important result, in one sentence.
- Evidence: give two or three bullet points, each with a specific number.
- Limits: say what the model can and cannot tell the manager, including how many of
  the people called would not have defaulted, how many defaulters would not be
  called, and what your decision in 2.3 means for the bank.

---

## Before you submit

- Make sure that every cell has run successfully before you submit your work.
- If you used generative AI in a substantial way, add a sentence at the end saying
  what you used and what it did, as the syllabus asks; it does not affect your
  grade.
- Name both files correctly and upload both.

The starter's tests check that your work has the right shape: that `credit` has a
`default` column, that `depth_table` has one row for each depth in `DEPTHS`, and so
on. They do not check your answers, and a green test does not mean a section is
complete.
