# Rubric: Homework 2 — What a restaurant grade hides

**100 points.** This is the rubric we grade against, published before you start so
that you know where the points are.

## How to read it

Code that runs is necessary but not sufficient. Most of the points in every part go
to **decisions and explanations**: what you chose, what you considered instead, and
what your own output shows. A correct test with no interpretation earns partial
credit, whereas a defensible choice that is clearly explained earns full credit,
even if a classmate made a different choice that is equally defensible.

"Specific" in this rubric means that a sentence refers to your data, whether by a
column name, a row count, a score, a borough or a number from your output.
"Generic" means that it could have been written without running the code.

## Points

| Part | Points |
|---|---|
| 1.1 Load and inspect | 5 |
| 1.2 Collapse | 7 |
| 1.3 Decide what to keep | 8 |
| 2.1 Summarise | 7 |
| 2.2 Plot | 8 |
| 2.3 Look closely | 10 |
| 3 Explain what you found | 15 |
| 4.1 Two cuisines | 15 |
| 4.2 Five boroughs | 15 |
| 5 For a reader who doesn't code | 10 |
| **Total** | **100** |

---

## Part 1: From violations to inspections (20)

### 1.1 Load and inspect (5)

| Points | What it looks like |
|---|---|
| 5 | Shape, types and missing counts shown. The markdown says that a row is one violation cited at one inspection, and the code demonstrates it, for example by showing that one restaurant on one date has several rows with the same score. |
| 3 | Data loaded and inspected, and what a row represents is stated correctly but not demonstrated. |
| 1 | Data loaded, but what a row represents is misidentified or not addressed. |
| 0 | Not loaded. |

### 1.2 Collapse (7)

| Points | What it looks like |
|---|---|
| 7 | `inspections` has one row per inspection. The code checks that the score, and anything else kept, does not vary within an inspection. Row counts before and after are given, and the markdown explains how the student knows the second is right. |
| 5 | Collapsed correctly, with counts, but the consistency check or the explanation of the count is missing. |
| 3 | Collapsed, but on a key that merges distinct inspections or splits one inspection into several, and the student does not notice. |
| 0–1 | Not collapsed, so that later parts analyse violations rather than inspections. |

### 1.3 Decide what to keep (8)

| Points | What it looks like |
|---|---|
| 7–8 | Decisions recorded on the placeholder dates, the inspection types, the unknown borough and the missing scores. Each names an alternative and a reason specific to this data, and says how many inspections it removes. `scored` matches what was written. |
| 5–6 | All the decisions are recorded and carried out, but at least one reason is generic, or the counts are missing for some. |
| 3–4 | Some decisions recorded, or `scored` does not match what was written. |
| 0–2 | Little or no filtering, or filtering with no reasoning. |

Different choices can earn full marks. What we grade is whether a choice is
defensible and whether the reasoning is the student's own.

---

## Part 2: Describe the scores (25)

### 2.1 Summarise (7)

| Points | What it looks like |
|---|---|
| 7 | Mean, median and skewness reported, and the markdown connects them, saying that a mean above the median and a positive skew both indicate a long right tail. |
| 5 | The three numbers are reported and the shape is named, but the connection between them is not explained. |
| 2–3 | Some of the numbers, or all three with no interpretation. |
| 0 | Missing. |

### 2.2 Plot (8)

| Points | What it looks like |
|---|---|
| 8 | Histogram, box plot and Q-Q plot, all labelled. A reason is given for the bin width, and the markdown says what each plot shows that the other two do not. |
| 5–6 | All three plots, but the bin width is not justified, or the comparison between the plots is generic. |
| 2–4 | One or two of the plots, or three with no explanation. |
| 0 | Missing. |

### 2.3 Look closely (10)

| Points | What it looks like |
|---|---|
| 9–10 | A histogram with one bar per score. The markdown identifies where it departs from a smooth right-skewed distribution and gives counts for the scores involved, at 13 and 14 at least. |
| 6–8 | The departure at 13 is identified, but without counts, or described vaguely. |
| 3–5 | The histogram is plotted at the right resolution, but the description does not identify where it departs from a smooth shape. |
| 0–2 | Missing, or plotted at a resolution that hides the pattern. |

A student who concludes that there is no departure worth describing can earn marks
here only if the conclusion is argued from their own counts.

---

## Part 3: Explain what you found (15)

| Points | What it looks like |
|---|---|
| 13–15 | Initial inspections and re-inspections compared around both cutoffs, with counts. The paragraph reaches a conclusion from that comparison, offers at least two explanations that could produce the pattern, and names further data that would tell them apart. |
| 9–12 | The comparison is made and a conclusion reached, but only one explanation is offered, or the data that would separate the explanations is vague. |
| 5–8 | Explanations are offered without the comparison between inspection types, or the comparison is made at only one cutoff. |
| 1–4 | A single explanation, asserted rather than argued from the data. |
| 0 | Missing. |

---

## Part 4: Compare groups (30)

### 4.1 Two cuisines (15)

| Points | What it looks like |
|---|---|
| 13–15 | A reason given for expecting the two cuisines to differ, and hypotheses stated before the test. The t-test is run correctly, and the difference is reported in inspection points as well as by its p-value. The assumptions are discussed in terms of this data, meaning the skew and the restaurants that appear more than once, and the paragraph says whether the difference would matter to a diner. |
| 9–12 | The test is correct and interpreted, but the assumptions are discussed generically or not at all, or the difference is reported only as a p-value. |
| 5–8 | The test is run, but the interpretation is thin or partly wrong, for example reading a small p-value as a large difference. |
| 1–4 | The test is run with little or no interpretation. |
| 0 | Missing. |

### 4.2 Five boroughs (15)

| Points | What it looks like |
|---|---|
| 13–15 | Hypotheses stated, and the ANOVA run correctly on the five boroughs. The mean, median and count are shown for each borough. The paragraph separates statistical significance from the size of the differences, using the borough means, and discusses the assumptions in terms of this data. |
| 9–12 | The test and table are correct and interpreted, but the paragraph does not separate significance from size, or the assumptions are discussed generically. |
| 5–8 | The test is run, but the table is missing or the interpretation is partly wrong. |
| 1–4 | The test is run with little or no interpretation. |
| 0 | Missing. |

---

## Part 5: For a reader who doesn't code (10)

| Points | What it looks like |
|---|---|
| 9–10 | All four elements present, with no code or jargon. The evidence bullets carry specific numbers from the analysis, and the limitation is real and specific. |
| 6–8 | All four elements, but with some jargon, vague evidence, or a generic limitation. |
| 3–5 | Elements missing, or written for a technical reader. |
| 0–2 | Missing. |

---

## Deductions

| Deduction | When |
|---|---|
| −5 | Files not named `SI618_HW02_<uniqname>.py` and `.html` |
| −5 | HTML export missing |

If the exported HTML shows cells that failed, we grade what the export shows.

