# Homework 3: What a neighbourhood's jobs say about its income

**100 points.** Released Monday, October 5, after class. Due **Monday, October 12,
before class (3:30 PM)**.

Submit two files to Canvas: your notebook, renamed `SI618_HW03_<uniqname>.py`, and
its HTML export, `SI618_HW03_<uniqname>.html`. The rubric we grade against is in
[RUBRIC.md](RUBRIC.md), and the notebook to start from is
[starter.py](starter.py).

---

## What this assignment is about

The Census Bureau's American Community Survey asks a sample of households every
year what work the people in them do and how much they earn, and publishes the
results for small areas called census tracts, each of which holds about 4,000
people. Michigan has a little over 3,000 of them.

In notebook 05 you measured how closely two columns move together, fitted a line
through a scatterplot, and saw how adding a second predictor can change what the
first one appears to say. This homework asks you to do the same with real survey
data: to find out how strongly the kind of work done in a tract goes with its
income, to look at the tracts the line fits worst, and to decide what a second
predictor adds.

**Everything you need is in notebooks 02 to 05**, including the second session of
notebook 05, which covers correlation and linear regression.

**Most of the points are for decisions and explanations rather than for code.**
Where the spec asks you to explain or decide, write full sentences in a markdown
cell, and refer to specific numbers from your own output.

---

## The data

The data comes from the ACS 5-year estimates for 2020 to 2024, which pool five
years of responses so that estimates for areas as small as a tract are reliable
enough to publish. It is kept in the course data repository so that everyone works
from the same numbers:

```
https://raw.githubusercontent.com/umsi-data-science/data/main/mi_tracts_acs2024.csv
```

It has one row per census tract in Michigan, and ten columns:

| Column | What it holds |
|---|---|
| `geo_id` | The tract's Census identifier |
| `name` | The tract's name, including its county |
| `employed` | Civilians aged 16 and over living in the tract who have a job |
| `management` | How many of them work in management, business, science and arts occupations |
| `service` | How many work in service occupations |
| `sales_office` | How many work in sales and office occupations |
| `construction` | How many work in natural resources, construction and maintenance occupations |
| `production` | How many work in production, transportation and material moving occupations |
| `median_income` | The tract's median household income, in 2024 dollars |
| `median_income_moe` | The margin of error of that median, at 90% confidence |

The five occupation columns are counts of people, and every employed person is in
exactly one of them. Each is a group of many occupations: "management, business,
science and arts", for example, includes teachers, nurses, engineers and lawyers as
well as managers. The Census Bureau's
[ACS documentation](https://www.census.gov/programs-surveys/acs/technical-documentation.html)
describes how the survey is conducted and how its estimates are coded.

Every number in this file is an estimate from a sample, and some of the values in
it are not estimates at all, so look at the columns before you compute anything.

---

## Part 1: Load and clean (20 points)

**1.1 Load and inspect (5).** Load the data and show its shape, its column types,
and how many values are missing in each column. Then show the mean, the median,
the minimum and the maximum of `median_income`, and say in a markdown cell what
those four numbers tell you before you have looked any further.

**1.2 Find the problems (7).** Find at least three things in this file that would
distort an analysis of income against occupation if you ignored them. For each one,
show the code that demonstrates it, give the number of tracts affected, and say in
a sentence what it would do to a correlation or a fitted line.

**1.3 Decide and clean (8).** Record your decisions about each problem in a
markdown cell, giving for each one an alternative you considered and a reason,
specific to this data, for rejecting it. Then build `tracts`, a DataFrame that
applies those decisions and adds a `county` column and five share columns, each
giving one occupation group's share of the tract's employed residents as a
proportion between 0 and 1. Say how many tracts remain, and how many each decision
removed.

---

## Part 2: Plot before you fit (20 points)

**2.1 The scatterplot (8).** Plot `median_income` against the management share.
Describe what you see, including the shape of the relationship, how the spread
changes along it, and any points that stand apart from the rest, naming at least
one of them.

**2.2 Five correlations (12).** Compute Pearson's and Spearman's correlation
between `median_income` and each of the five shares, and show them in one table.
Say which share goes most strongly with income and in which direction. Then take
the share for which the two coefficients differ most, plot it against income, and
use the plot to say whether the difference matters.

---

## Part 3: Fit a line (25 points)

**3.1 Fit (10).** Fit `median_income ~ management_share` (using whatever you named
the share column) to `tracts`, and report the slope, the intercept and R-squared.
Then, in a markdown cell, say what the slope means in dollars for a difference of
10 percentage points in the management share, whether the intercept describes any
real tract, and what R-squared says about how much of the variation in income the
line leaves unexplained.

**3.2 The tracts the line fits worst (15).** Find the ten tracts furthest below the
line and the ten furthest above it, using the model's residuals, and show them with
their county, their management share, their median income and its margin of error.
In a paragraph, say what the tracts at each end have in common, offer an
explanation for why the line misses them, and say what further data would let you
check that explanation. Say also whether the margin of error could account for any
of them.

---

## Part 4: Add a predictor (25 points)

**4.1 Choose (5).** Choose one predictor to add to the management share. It can be
another of the five shares, a county, or a column you build from the data, such as
whether a tract is in a county that contains a large university. Say why you chose
it and what you expect it to do to the management share's coefficient. The five
shares add up to 1 in every tract, so think about what that means before you
choose one of them.

**4.2 Fit and interpret (12).** Fit the model with both predictors, and report
both coefficients and R-squared. Say what your predictor's coefficient means with
the management share held constant, and compare the management share's coefficient
and R-squared with what you found in 3.1.

**4.3 Judge (8).** In a paragraph, say whether adding your predictor changed what
Part 3 appeared to show, and how. Then say what someone would have to assume before
reading either model as saying that changing the kind of work done in a tract would
change its income, and why a relationship between tracts may not hold for the
people living in them.

---

## Part 5: For a reader who doesn't code (10 points)

Write a summary in a markdown cell, with no code and no jargon, for someone in
local government deciding whether the mix of jobs in a neighbourhood is a useful
guide to its income:

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

The starter's tests check that your work has the right shape: that `tracts`
exists, that it's a DataFrame, and so on. They don't check your answers, and a
green test doesn't mean a section is complete.

Late work follows the late-day policy in the syllabus: three free late days for the
term, then 25% per day.
