# Homework 2: What a restaurant grade hides

**100 points.** Released Monday, September 28, after class. Due **Monday,
October 5, before class (3:30 PM)**.

Submit two files to Canvas: your notebook, renamed `SI618_HW02_<uniqname>.py`, and
its HTML export, `SI618_HW02_<uniqname>.html`. The rubric we grade against is in
[RUBRIC.md](RUBRIC.md), and the notebook to start from is
[starter.py](starter.py).

---

## What this assignment is about

Every restaurant in New York City is inspected by the Department of Health and
Mental Hygiene, which adds points for each violation it finds, so that a lower
score is better. The score then decides the letter grade that the restaurant has to
post in its window: 0 to 13 points earns an A, 14 to 27 a B, and 28 or more a C.
Diners see only the letter, but the city publishes the scores behind it.

In notebook 04 you described distributions, gave their shapes names, and learned
to plot before you summarise. This homework asks you to do the same with a real
distribution, one produced by a process with rules and consequences attached, and
then to compare groups of restaurants with the tests from Wednesday's session of
notebook 05.

**Everything you need is in notebooks 02 to 04 and the first session of notebook
05**, which covers the t-test and one-way ANOVA.

**Most of the points are for decisions and explanations rather than for code.**
Where the spec asks you to explain or decide, write full sentences in a markdown
cell, and refer to specific numbers from your own output.

---

## The data

The data is a snapshot of the city's restaurant inspection results, taken on
September 28, 2026, and kept in the course data repository so that everyone works
from the same numbers:

```
https://raw.githubusercontent.com/umsi-data-science/data/main/nyc_restaurant_inspections_2026-09-28.csv.gz
```

pandas reads the compressed file directly, so there is no need to download or
unzip it. It has eleven columns:

| Column | What it holds |
|---|---|
| `camis` | The restaurant's permanent ID |
| `dba` | The restaurant's name ("doing business as") |
| `boro` | The borough |
| `cuisine_description` | The cuisine, as the restaurant describes it |
| `inspection_date` | The date of the inspection |
| `inspection_type` | The kind of inspection, such as an initial cycle inspection or a re-inspection |
| `action` | What the inspector did as a result |
| `score` | The inspection's score, where lower is better |
| `grade` | The letter grade, where one was given |
| `violation_code` | The code of one violation cited at the inspection |
| `critical_flag` | Whether that violation is critical |

Besides A, B and C, the `grade` column uses N for "not yet graded", Z for "grade
pending", and P for "grade pending, issued on reopening after a closure". The full
dataset, and the city's own documentation of it, are on
[NYC Open Data](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j).

Read the columns carefully before you compute anything, because a row in this file
is not what it first appears to be.

---

## Part 1: From violations to inspections (20 points)

**1.1 Load and inspect (5).** Load the data and show its shape, its column
types, and how many values are missing in each column. Then, in a markdown cell,
say what a single row represents, and show the code that convinced you.

**1.2 Collapse (7).** Build `inspections`, a DataFrame with one row per
inspection. Before you do, check that anything you intend to keep from the
row-level data, such as the score, really is the same on every row of a given
inspection, and show that check. Say how many rows you started with, how many
inspections you ended with, and how you know the second number is right.

**1.3 Decide what to keep (8).** Not every inspection belongs in an analysis of
scores. Look at the inspection dates, the inspection types, the boroughs and the
missing scores, and decide which inspections your analysis will use. Record your
decisions in a markdown cell, giving for each one an alternative you considered and
a reason, specific to this data, for rejecting it, and say how many inspections
each decision removes. Assign the result to `scored`.

---

## Part 2: Describe the scores (25 points)

**2.1 Summarise (7).** For the scores in `scored`, report the mean, the median and
the skewness, and say what the three numbers together tell you about the shape of
the distribution before you have plotted it.

**2.2 Plot (8).** Show the distribution of scores with a histogram and a box plot,
and compare it with a normal distribution using a Q-Q plot. For the histogram,
choose a bin width and say why you chose it, and say what each of the three plots
shows that the other two do not.

**2.3 Look closely (10).** Plot the histogram again, this time with one bar for
every possible score from 0 to 50. Compare it with what a smooth right-skewed
distribution would look like, and describe any places where the two differ,
giving counts for the scores involved. If you find that they do not differ in any
way that matters, say so and show why.

---

## Part 3: Explain what you found (15 points)

The grade cutoffs are fixed at 13 and 27 points, and a restaurant's first
inspection in a cycle and its re-inspection do not carry the same consequences.
Compare the distribution of scores at those two kinds of inspection, around both
cutoffs, and use the comparison to judge whether the grading rules help explain
what you described in 2.3, or whether something else does.

In a paragraph, say what you conclude and why, offer at least two explanations that
could produce the pattern you see, and say what further data would let someone
tell those explanations apart.

---

## Part 4: Compare groups (30 points)

For both comparisons, use the scores in `scored`, state your hypotheses before you
run the test, and report the difference between the groups in inspection points as
well as the test's result. Then say whether the test's assumptions are reasonable
for these data, bearing in mind what you learned about their shape in Part 2 and
the fact that most restaurants appear more than once.

**4.1 Two cuisines (15).** Choose two cuisines that you expect to differ, and say
why you expect it. Compare their scores with a t-test, and in a paragraph interpret
the result, including whether the difference is large enough to matter to a diner.

**4.2 Five boroughs (15).** Compare the scores across the five boroughs with a
one-way ANOVA. Show the mean, the median and the number of inspections in each
borough alongside the test's result. With groups this large, a very small
difference can produce a very small p-value, so in a paragraph say what the test
tells you, what it does not, and how large the differences between boroughs
actually are.

---

## Part 5: For a reader who doesn't code (10 points)

Write a summary in a markdown cell, with no code and no jargon, for a New Yorker
deciding how much to trust the letter in a restaurant's window:

- **Question:** what you set out to learn, in one sentence
- **Finding:** the most important result, in one sentence
- **Evidence:** two or three bullet points, each with a specific number
- **So what:** what this means for the reader, and one limitation of the data
  behind it

---

## Before you submit

- **Run it top to bottom.** Restart the notebook and run every cell. If the HTML
  export shows errors, we grade what the export shows.
- **Attribute AI use.** If you used generative AI in a substantial way, add a
  sentence at the end saying what you used and what it did, as the syllabus asks.
  It doesn't affect your grade.
- **Name both files correctly** and upload both.

The starter's tests check that your work has the right shape: that `inspections`
exists, that it's a DataFrame, and so on. They don't check your answers, and a
green test doesn't mean a section is complete.

Late work follows the late-day policy in the syllabus: three free late days for the
term, then 25% per day.
