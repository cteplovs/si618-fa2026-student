# Rubric: Homework 6 - Predicting credit card default

Homework 6 is worth 100 points. This is the rubric we grade against, published
before you start so that you know where the points are.

## Grading approach

Code that runs is necessary but not sufficient. Most of the points in every part go
to decisions and explanations: what you found, what you chose, and what your own
output shows. A correct table with no interpretation earns partial credit, whereas
a defensible choice that is clearly explained earns full credit, even if a
classmate made a different choice that is equally defensible.

"Specific" in this rubric means that a sentence refers to your data, whether by a
count, an AUC, a precision, a recall, a threshold or another number from your output.
"Generic" means that it could have been written without running the code.

## Points

| Part | Points |
|---|---|
| 1.1 Load the card holders | 5 |
| 1.2 Codes the documentation does not list | 10 |
| 2.1 Split | 3 |
| 2.2 Accuracy and AUC | 7 |
| 2.3 Sex, marital status and age | 10 |
| 3.1 The depth of a tree | 7 |
| 3.2 The size of a forest's leaves | 9 |
| 3.3 Compare and choose | 9 |
| 4.1 Choose a threshold | 10 |
| 4.2 Test once | 10 |
| 5 Summary for a credit manager | 20 |
| **Total** | **100** |

---

## Part 1: Look at the data (15)

### 1.1 Load the card holders (5)

| Points | Description |
|---|---|
| 5 | `credit` is loaded with the starter's renaming, the number of defaulters is shown, and `baseline` is the share of card holders who did not default. |
| 3 | Loaded, but the count of defaulters or the baseline is missing. |
| 1 | Loaded, with the baseline computed as something other than the share who did not default. |
| 0 | Not loaded. |

### 1.2 Codes the documentation does not list (10)

| Points | Description |
|---|---|
| 9-10 | The counts of each value are shown for all three columns, the undocumented values in each are named with their counts, and each column has a decision with a reason drawn from the counts or the documentation, applied in `credit_clean`. |
| 6-8 | The undocumented values are found, but one decision has no reason, or a decision is stated but not applied. |
| 3-5 | Only one or two of the three columns are examined, or the undocumented values in `PAY_1` are missed. |
| 0-2 | The counts are shown with no comparison with the documentation. |

---

## Part 2: Logistic regression (20)

### 2.1 Split (3)

| Points | Description |
|---|---|
| 3 | `train_test_split` with `test_size=0.25`, stratified by `default`, and `random_state=618`. |
| 1-2 | Split, but without stratifying or with another seed. |
| 0 | Not split, or the test card holders are used for fitting. |

### 2.2 Accuracy and AUC (7)

| Points | Description |
|---|---|
| 6-7 | Both measures come from five-fold cross-validation of a scaling pipeline on the training set, the accuracy is compared with `baseline` with numbers, and the explanation says that with 22% defaulters accuracy is dominated by the non-defaulters, whereas AUC measures how well the model ranks defaulters above non-defaulters at every threshold. |
| 4-5 | Both measures are right, but the comparison with the baseline or the explanation is generic. |
| 1-3 | Computed on the test set, or without a pipeline. |
| 0 | Missing. |

### 2.3 Sex, marital status and age (10)

| Points | Description |
|---|---|
| 9-10 | `logistic_auc_without` is computed the same way, the change in AUC is stated with numbers, and the decision gives a reason beyond the AUC, such as the law, fairness to the card holders, or how the bank would explain a call, and `FEATURES_USED` matches it. |
| 6-8 | The decision is made and applied, but the reason is only the change in AUC, or is generic. |
| 3-5 | The AUC is computed, but no decision is made, or `FEATURES_USED` does not match it. |
| 0-2 | Missing. |

---

## Part 3: Trees and forests (25)

### 3.1 The depth of a tree (7)

| Points | Description |
|---|---|
| 6-7 | Cross-validated by AUC on the training set for every depth in `DEPTHS`, in `depth_table`, with a plot, and `best_depth` is chosen from the table with a reason. |
| 4-5 | The table is right, but the plot or the reason is missing. |
| 1-3 | Scored by accuracy, or on the test set. |
| 0 | Missing. |

### 3.2 The size of a forest's leaves (9)

| Points | Description |
|---|---|
| 8-9 | Cross-validated by AUC for every value in `LEAF_SIZES`, in `leaf_table`, `best_leaf` is chosen with a reason, and the explanation says that with leaves of one card holder each tree overfits, as the unlimited tree in 3.1 does, and that larger leaves make each tree's probabilities less extreme and less dependent on single card holders. |
| 5-7 | The table and the choice are right, but the explanation does not use 3.1, or is generic. |
| 1-4 | Run for only some leaf sizes, or with another number of trees. |
| 0 | Missing. |

### 3.3 Compare and choose (9)

| Points | Description |
|---|---|
| 8-9 | Cross-validated probabilities for all three models, their ROC curves on one figure, their AUCs in one table, and a choice with a reason that uses the AUCs, with `chosen_probabilities` from the chosen model. |
| 5-7 | The comparison is right, but the figure or the table is missing, or the reason is generic. |
| 1-4 | The models are compared on the test set, or with probabilities from models fitted to the whole training set. |
| 0 | Missing. |

---

## Part 4: A threshold, and one test (20)

### 4.1 Choose a threshold (10)

| Points | Description |
|---|---|
| 9-10 | `threshold_table` gives the share called, the precision and the recall for every threshold in `THRESHOLDS`, computed from `chosen_probabilities`; `chosen_threshold` is the lowest threshold that calls at most 20%; and the sentence says what the precision and recall mean in calls and defaulters. |
| 6-8 | The table and the choice are right, but the sentence is generic, or restates the definitions of precision and recall. |
| 3-5 | The threshold is chosen without the 20% condition, or the table is computed on the test set. |
| 0-2 | Missing. |

### 4.2 Test once (10)

| Points | Description |
|---|---|
| 9-10 | The chosen model is fitted to all the training card holders and tested once, `test_results` has all four numbers, each is compared with its cross-validated estimate, and the answer says that the test numbers are the ones to report. |
| 5-8 | Tested once, but a number is missing, or the comparison is generic. |
| 1-4 | Several models or thresholds are tested, or the threshold is changed after the test. |
| 0 | Missing. |

---

## Part 5: Summary for a credit manager (20)

| Points | Description |
|---|---|
| 17-20 | All four elements are present, with no code or jargon. The evidence bullets give specific numbers, and the limits say how many of the people called would not have defaulted, how many defaulters would not be called, and what the decision in 2.3 means for the bank. |
| 12-16 | All four elements, but one of the limits is missing, there is some jargon, or the evidence is vague. |
| 6-11 | Elements missing, or a conclusion that claims more than the evidence shows. |
| 0-5 | Missing. |

---

## Deductions

| Deduction | When |
|---|---|
| -5 | Files not named `SI618_HW06_<uniqname>.py` and `.html` |
| -5 | HTML export missing |

