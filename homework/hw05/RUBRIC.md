# Rubric: Homework 5 - Predicting red wine ratings

Homework 5 is worth 100 points. This is the rubric we grade against, published
before you start so that you know where the points are.

## Grading approach

Code that runs is necessary but not sufficient. Most of the points in every part go
to decisions and explanations: what you found, what you chose, and what your own
output shows. A correct table with no interpretation earns partial credit, whereas
a defensible choice that is clearly explained earns full credit, even if a
classmate made a different choice that is equally defensible.

"Specific" in this rubric means that a sentence refers to your data, whether by a
measurement, a count, an accuracy, a value of k or another number from your output.
"Generic" means that it could have been written without running the code.

## Points

| Part | Points |
|---|---|
| 1.1 Load the wines | 5 |
| 1.2 Baseline | 4 |
| 1.3 Scales of the measurements | 6 |
| 2.1 Split | 4 |
| 2.2 Share of the distance by measurement | 8 |
| 2.3 Unscaled against scaled | 8 |
| 3.1 Cross-validate | 10 |
| 3.2 Choose and test once | 10 |
| 4.1 Find them | 6 |
| 4.2 Effect on k = 1 | 9 |
| 4.3 Without the duplicates | 10 |
| 5 Summary for a winemaker | 20 |
| **Total** | **100** |

---

## Part 1: Look at the data (15)

### 1.1 Load the wines (5)

| Points | Description |
|---|---|
| 5 | `wines` is loaded, `good` is True for a rating of 6 or more, and the counts of each rating and of good wines are shown. |
| 3 | Loaded, but `good` uses the wrong cut-off, or the counts are missing. |
| 1 | Loaded, with no `good` column. |
| 0 | Not loaded. |

### 1.2 Baseline (4)

| Points | Description |
|---|---|
| 4 | `baseline` is the share of the more common class, and the sentence says that a model is only useful to the extent that it beats what predicting that class for every wine would achieve. |
| 2-3 | The baseline is right, but the sentence is missing or generic. |
| 0-1 | Missing, or computed as something other than the share of the more common class. |

### 1.3 Scales of the measurements (6)

| Points | Description |
|---|---|
| 5-6 | The table shows the mean, standard deviation, minimum and maximum of all eleven measurements, and the prediction names the measurements with the largest spread (the two sulfur dioxide columns), with a reason based on the size of their differences in the distance formula. |
| 3-4 | The table is shown, but the prediction is vague, or rests on the means rather than the spread. |
| 0-2 | The table is missing, or no prediction is made. |

---

## Part 2: Scaling (20)

### 2.1 Split (4)

| Points | Description |
|---|---|
| 4 | `train_test_split` with `test_size=0.25`, stratified by `good`, and `random_state=618`. |
| 2 | Split, but without stratifying or with another seed. |
| 0 | Not split, or the test wines are used for fitting. |

### 2.2 Share of the distance by measurement (8)

| Points | Description |
|---|---|
| 7-8 | `variance_share` is computed from the training wines, sums to 1 and is sorted, and the answer says with specific shares whether it confirms the prediction in 1.3. |
| 4-6 | Computed correctly, but the comparison with 1.3 is missing or generic, or the shares come from all the wines rather than the training set. |
| 1-3 | Standard deviations or ranges instead of variances, with no shares. |
| 0 | Missing. |

### 2.3 Unscaled against scaled (8)

| Points | Description |
|---|---|
| 7-8 | Both models use k = 5, the scaled one is a pipeline fitted to the training wines, both are scored on the test wines, and the explanation uses 2.2 to say that the unscaled distance is decided almost entirely by sulfur dioxide, so the other measurements count for almost nothing until they are standardised. |
| 4-6 | Both accuracies are right, but the explanation does not use 2.2, or the scaler is fitted outside a pipeline. |
| 1-3 | The scaler is fitted to all the wines, or the models are scored on the training set. |
| 0 | Missing. |

---

## Part 3: Choosing k (20)

### 3.1 Cross-validate (10)

| Points | Description |
|---|---|
| 9-10 | Five-fold cross-validation of the scaling pipeline on the training wines only, for every k in `K_VALUES`, in `cv_table` with a `mean` column, and a plot of mean accuracy against k. |
| 5-8 | The table is right, but the plot is missing, or the model is not a pipeline. |
| 1-4 | Cross-validated on all the wines, or on the test wines. |
| 0 | Missing. |

### 3.2 Choose and test once (10)

| Points | Description |
|---|---|
| 9-10 | `best_k` is chosen from `cv_table` with a reason, the pipeline is fitted to all the training wines and tested once, and `final_accuracy` is compared, with numbers, with both the baseline and the cross-validated estimate for the same k. |
| 5-8 | The choice and the test are right, but one of the two comparisons is missing or generic. |
| 1-4 | k is chosen from test accuracies, or several values of k are tested. |
| 0 | Missing. |

---

## Part 4: Duplicates (25)

### 4.1 Find them (6)

| Points | Description |
|---|---|
| 6 | `n_duplicates` counts rows identical to an earlier row, two or three groups are shown, and the answer says what the duplicates are likely to be, with a reason drawn from the rows themselves. |
| 3-5 | The count and the groups are right, but the answer about what they are is missing or generic. |
| 1-2 | A count with no groups shown, or a count that includes the first row of each group. |
| 0 | Missing. |

### 4.2 Effect on k = 1 (9)

| Points | Description |
|---|---|
| 8-9 | The count of test wines with an identical wine in the training set is shown, and the explanation says that with duplicates in different folds, or in both the training and test sets, a wine's nearest neighbour at k = 1 is often its own copy, with the same rating, so small values of k look better than they are, in cross-validation and on the test set alike. |
| 5-7 | The mechanism is explained, but only for cross-validation or only for the test set, or without the count. |
| 1-4 | The answer notes that k = 1 scores well without explaining why. |
| 0 | Missing. |

### 4.3 Without the duplicates (10)

| Points | Description |
|---|---|
| 9-10 | Duplicates are dropped before splitting, the split, cross-validation and final test are repeated with the same settings, both curves are on one plot, the table compares the baselines, the choices of k and the test accuracies, and the answer chooses which accuracy to report, with a reason. |
| 5-8 | The repeat is done, but the plot or the table is missing, or the choice of accuracy is not argued. |
| 1-4 | Duplicates are dropped after splitting, or only from the training set. |
| 0 | Missing. |

---

## Part 5: Summary for a winemaker (20)

| Points | Description |
|---|---|
| 17-20 | All four elements are present, with no code or jargon. The evidence bullets give specific numbers, and the limits say how far the accuracy is above the baseline, that the model predicts the tasters' ratings rather than the taste itself, and why the duplicates changed the estimate. |
| 12-16 | All four elements, but one of the limits is missing, there is some jargon, or the evidence is vague. |
| 6-11 | Elements missing, or a conclusion that claims more than the evidence shows. |
| 0-5 | Missing. |

---

## Deductions

| Deduction | When |
|---|---|
| -5 | Files not named `SI618_HW05_<uniqname>.py` and `.html` |
| -5 | HTML export missing |

