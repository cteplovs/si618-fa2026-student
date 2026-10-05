# Rubric: Homework 3 - What a neighbourhood's jobs say about its income

**100 points.** This is the rubric we grade against, published before you start so
that you know where the points are.

## How to read it

Code that runs is necessary but not sufficient. Most of the points in every part go
to **decisions and explanations**: what you chose, what you considered instead, and
what your own output shows. A correct regression with no interpretation earns
partial credit, whereas a defensible choice that is clearly explained earns full
credit, even if a classmate made a different choice that is equally defensible.

"Specific" in this rubric means that a sentence refers to your data, whether by a
column name, a tract count, a county, a coefficient or another number from your
output. "Generic" means that it could have been written without running the code.

## Points

| Part | Points |
|---|---|
| 1.1 Load and inspect | 5 |
| 1.2 Find the problems | 7 |
| 1.3 Decide and clean | 8 |
| 2.1 The scatterplot | 8 |
| 2.2 Five correlations | 12 |
| 3.1 Fit | 10 |
| 3.2 The tracts the line fits worst | 15 |
| 4.1 Choose | 5 |
| 4.2 Fit and interpret | 12 |
| 4.3 Judge | 8 |
| 5 For a reader who doesn't code | 10 |
| **Total** | **100** |

---

## Part 1: Load and clean (20)

### 1.1 Load and inspect (5)

| Points | What it looks like |
|---|---|
| 5 | Shape, types and missing counts shown, with the mean, median, minimum and maximum of `median_income`. The markdown says what those numbers reveal, in particular that the mean and the minimum are impossible for an income and that something in the column is not a real value. |
| 3 | All of it shown, but the markdown does not notice that the numbers are impossible, or notices without saying what it implies. |
| 1 | Data loaded, with some of the checks missing. |
| 0 | Not loaded. |

### 1.2 Find the problems (7)

| Points | What it looks like |
|---|---|
| 7 | At least three real problems, each demonstrated with code, given a tract count, and followed by a sentence on what it would do to a correlation or a fitted line. |
| 5 | Three real problems, but at least one is asserted rather than demonstrated, has no count, or has no sentence on its effect. |
| 3 | One or two real problems, or three of which one is not actually a problem. |
| 0-1 | Vague ("there are outliers") or missing. |

### 1.3 Decide and clean (8)

| Points | What it looks like |
|---|---|
| 7-8 | A decision on each problem from 1.2, with an alternative considered and a reason specific to this data for rejecting it. `tracts` carries out what was written, with a `county` column and five shares between 0 and 1, and the markdown says how many tracts remain and how many each decision removed. |
| 5-6 | Decisions recorded and carried out, but at least one reason is generic, alternatives are missing for some, or the counts are missing. |
| 3-4 | Some decisions recorded, or `tracts` does not match what was written, or the shares are percentages or counts rather than proportions. |
| 0-2 | Little or no cleaning, or cleaning with no reasoning. |

Different choices can earn full marks. What we grade is whether a choice is
defensible and whether the reasoning is the student's own.

---

## Part 2: Plot before you fit (20)

### 2.1 The scatterplot (8)

| Points | What it looks like |
|---|---|
| 8 | A labelled scatterplot of income against the management share. The markdown describes the shape of the relationship, how the spread changes along it, and at least one point that stands apart, naming the tract or its county. |
| 5-6 | The plot is right, but the description is generic or misses the change in spread or the points that stand apart. |
| 2-4 | Plotted with little description, or plotted before cleaning so that the placeholder values dominate it, without comment. |
| 0 | Missing. |

### 2.2 Five correlations (12)

| Points | What it looks like |
|---|---|
| 11-12 | Pearson's and Spearman's coefficients for all five shares in one table. The markdown names the share that goes most strongly with income and its direction, and plots the share with the largest gap between the two coefficients, using the plot to say whether the gap matters. |
| 8-10 | The table and the strongest share are right, but the plot is missing or the explanation of the gap is generic. |
| 4-7 | Only one kind of correlation, or only some of the shares, or the strongest relationship is misread, for example by ignoring the sign. |
| 0-3 | Little or no correlation analysis. |

---

## Part 3: Fit a line (25)

### 3.1 Fit (10)

| Points | What it looks like |
|---|---|
| 9-10 | Slope, intercept and R-squared reported. The markdown converts the slope into dollars per 10 percentage points correctly, says whether the intercept describes a real tract (a share of zero), and says what R-squared leaves unexplained. |
| 6-8 | The model and numbers are right, but one of the three interpretations is missing, generic, or wrong, most often the conversion of the slope. |
| 3-5 | Fitted, with the numbers but little interpretation. |
| 0-2 | Not fitted, or fitted to uncleaned data without comment. |

### 3.2 The tracts the line fits worst (15)

| Points | What it looks like |
|---|---|
| 13-15 | Both lists of ten shown, with county, share, income and margin of error. The paragraph says what each end has in common, offers an explanation for why the line misses them, names further data that would check it, and uses the margins of error to say whether any of them could be noise. |
| 9-12 | Both lists and a pattern described, but the explanation is thin, the further data is vague, or the margins of error are not used. |
| 5-8 | Both lists, described generically ("these tracts are unusual"), or one list with a real description. |
| 1-4 | The residuals are computed but not examined. |
| 0 | Missing. |

---

## Part 4: Add a predictor (25)

### 4.1 Choose (5)

| Points | What it looks like |
|---|---|
| 5 | A predictor chosen, with a reason that refers to something found earlier in the homework, and a concrete expectation for the management share's coefficient. If the predictor is another share, the student shows that they have thought about the five shares adding up to 1. |
| 3 | A predictor and a reason, but the reason is generic or the expectation is missing. |
| 0-1 | Missing, or a predictor with no reason. |

### 4.2 Fit and interpret (12)

| Points | What it looks like |
|---|---|
| 11-12 | Both coefficients and R-squared reported. The new coefficient is read correctly with the management share held constant, and the management share's coefficient and R-squared are compared with 3.1, with numbers. |
| 7-10 | The model is right and compared with 3.1, but the "held constant" reading is missing or loose, or a categorical predictor's reference category is not stated. |
| 3-6 | Fitted, but the interpretation is wrong, for example reading the coefficient as the predictor's effect on its own. |
| 0-2 | Not fitted. |

### 4.3 Judge (8)

| Points | What it looks like |
|---|---|
| 7-8 | Says whether and how the second predictor changed what Part 3 appeared to show, with numbers. Names what would have to be assumed before reading either model causally, and explains why a relationship between tracts need not hold for the people in them. |
| 4-6 | Two of those three, or all three generically. |
| 1-3 | A restatement of 4.2's numbers. |
| 0 | Missing. |

---

## Part 5: For a reader who doesn't code (10)

| Points | What it looks like |
|---|---|
| 9-10 | All four elements present, with no code or jargon. The evidence bullets carry specific numbers from the analysis, and the limitation is real and specific. |
| 6-8 | All four elements, but with some jargon, vague evidence, or a generic limitation. |
| 3-5 | Elements missing, or written for a technical reader. |
| 0-2 | Missing. |

---

## Deductions

| Deduction | When |
|---|---|
| -5 | Files not named `SI618_HW03_<uniqname>.py` and `.html` |
| -5 | HTML export missing |

If the exported HTML shows cells that failed, we grade what the export shows.

