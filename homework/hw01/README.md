# Homework 1: Joining the world's data

**100 points.** Released Wednesday, September 16, after class. Due **Monday,
September 21, before class (3:30 PM)**.

Submit two files to Canvas: your notebook, renamed `SI618_HW01_<uniqname>.py`, and
its HTML export, `SI618_HW01_<uniqname>.html`. The rubric we grade against is in
[RUBRIC.md](RUBRIC.md), and the notebook to start from is
[starter.py](starter.py).

---

## What this assignment is about

In class you loaded, cleaned, joined and reshaped small tables that were built to
behave. This homework does the same thing with real data that doesn't.

The World Bank publishes hundreds of development indicators, such as life
expectancy, GDP per capita and internet access, for every country, every year,
through a free web API. The API returns nested JSON. The country list and the
indicator data don't name their keys the same way. And a large share of what the
API calls a "country" isn't a country at all.

You'll pick one indicator, get it into a shape you can analyze, and find something
worth saying about it.

**Everything you need is in notebook 02 and the first half of notebook 03**, up to
the "Homework 1 stops here" line. You won't need `groupby` or `pivot_table`.

**Most of the points are for decisions and explanations, not for code.** Where the
spec asks you to explain or decide, write full sentences in a markdown cell, and
refer to specific numbers from your own output.

---

## The data

Two API endpoints, both free and requiring no key:

| What | URL |
|---|---|
| Every country, with its region and income level | `https://api.worldbank.org/v2/country?format=json&per_page=400` |
| One indicator for every country, 2000–2024 | `https://api.worldbank.org/v2/country/all/indicator/<CODE>?format=json&per_page=20000&date=2000:2024` |

Replace `<CODE>` with an indicator code. Everyone uses **population**
(`SP.POP.TOTL`), plus **one** of these, your choice:

| Code | Indicator |
|---|---|
| `SP.DYN.LE00.IN` | Life expectancy at birth, years |
| `NY.GDP.PCAP.CD` | GDP per capita, current US$ |
| `IT.NET.USER.ZS` | Individuals using the internet, % of population |
| `SP.DYN.TFRT.IN` | Fertility rate, births per woman |
| `SP.URB.TOTL.IN.ZS` | Urban population, % of total |
| `EG.ELC.ACCS.ZS` | Access to electricity, % of population |
| `SL.TLF.CACT.FE.ZS` | Female labor force participation, % of women 15+ |
| `EN.GHG.CO2.PC.CE.AR5` | CO₂ emissions per capita, tonnes |
| `SH.DYN.MORT` | Under-5 mortality, per 1,000 live births |

Look at how each response is structured before you try to flatten it. Both come
back as a list of two items, and only one of the two is the data.

The World Bank revises its figures, so your numbers may differ slightly from a
classmate's who ran the same code on a different day. That's expected, and it
doesn't affect your grade.

---

## Part 1: Load and inspect (15 points)

**1.1 A loading function (5).** Write a function, `fetch_indicator(code: str)`,
that takes an indicator code and returns that indicator as a flat DataFrame, with
one row per country per year. Give it a docstring. Use it to load population and
your chosen indicator. Load the country list too.

**1.2 Why this indicator (3).** In a markdown cell, say which indicator you chose
and why, and what you expect to find before you look.

**1.3 Inspect (7).** For each of the three tables, show its shape, its column
types, and how many values are missing. Then, in a markdown cell, say which columns
you'll need, and point out anything about the types that you'd have to fix before
using them.

---

## Part 2: Clean and join (30 points)

**2.1 Find the problems (10).** Before you merge anything, investigate the two
tables you're about to join: your indicator and the country list. There are at
least four problems that will cause a naive merge to go wrong, or to go "right"
while quietly producing nonsense. For each problem you find, show the code that
demonstrates it, and give a number: how many rows or values are affected.

**2.2 Decide, then merge (15).** Merge your indicator with the country list. Before
you write the merge, record your decisions in a markdown cell. At minimum, answer
these questions:

- Which column in each table do you join on, and why that one rather than the
  alternative?
- Which join type (`how=`), and what does that choice keep or lose?
- What do you do about the rows that aren't countries?
- What, if anything, do you clean first?

For each decision, name at least one alternative you considered and say why you
didn't choose it. Then carry out the merge, and assign the result to `merged`.

**2.3 Check the merge (5).** Show that the merge did what you intended. Compare row
counts before and after, and look for rows that failed to match. In a sentence or
two, say what you checked and what you found.

---

## Part 3: Combine and reshape (25 points)

**3.1 Stack (8).** Clean and merge population the same way, then use `pd.concat()`
to stack the two indicators into one long table with the same columns. Show that
the result has the number of rows it should, and explain how you know.

**3.2 Reshape (10).** Build `by_year`, a wide table of your chosen indicator with
one row per country and one column per year. Then use it to compute each country's
change between 2000 and the most recent year, as a new column. Where a country
lacks data for one of those years, decide what to do, and say what you decided in
a sentence.

**3.3 Rank (7).** Show the ten countries with the largest change and the ten with
the smallest. Use the country list's region and income level to describe who is at
each end. You'll need a merge, not a `groupby`. Write two or three sentences on what
stands out.

---

## Part 4: Find something interesting (20 points)

**4.1 Ask (4).** Write one specific question about your indicator that the data can
answer and that you don't already know the answer to. It should involve population,
region or income level. "What patterns exist?" isn't specific enough, and "How many
rows are there?" isn't a question about the world.

**4.2 Answer (10).** Answer it with the techniques from notebooks 02 and 03:
filtering, sorting, `value_counts`, merging and reshaping. Show your work, and
display the results clearly.

**4.3 Interpret (6).** In a paragraph, say what you found, whether it surprised
you, what might explain it, and what you'd need to check before you believed it.
Use specific numbers from your output.

---

## Part 5: For a reader who doesn't code (10 points)

Write a summary in a markdown cell, with no code and no jargon, for someone deciding
whether your finding matters:

- **Question:** what you set out to learn, in one sentence
- **Finding:** the most important result, in one sentence
- **Evidence:** two or three bullet points, each with a specific number
- **So what:** what this means, and one limitation of the data behind it

---

## Before you submit

- **Run it top to bottom.** Restart the notebook and run every cell. If the HTML
  export shows errors, we grade what the export shows.
- **Attribute AI use.** If you used generative AI in a substantial way, add a
  sentence at the end saying what you used and what it did, as the syllabus asks.
  It doesn't affect your grade.
- **Name both files correctly** and upload both.

The starter's tests check that your work has the right shape: that `merged` exists,
that it's a DataFrame, and so on. They don't check your answers, and a green test
doesn't mean a section is complete.

Late work follows the late-day policy in the syllabus: three free late days for the
term, then 25% per day.
