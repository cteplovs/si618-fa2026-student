# Rubric: Homework 1 — Joining the world's data

**100 points.** This is the rubric we grade against, published before you start so
that you know where the points are.

## How to read it

Code that runs is necessary but not enough. Most of the points in every part go to
**decisions and explanations**: what you chose, what you considered instead, and
what your own output shows. A correct merge with no explanation of why it's correct
earns partial credit. A defensible merge that's clearly explained earns full credit,
even if a classmate made a different, equally defensible choice.

"Specific" in this rubric means it refers to your data: a column name, a row count,
a country, a number from your output. "Generic" means it could have been written
without running the code.

## Points

| Part | Points |
|---|---|
| 1.1 A loading function | 5 |
| 1.2 Why this indicator | 3 |
| 1.3 Inspect | 7 |
| 2.1 Find the problems | 10 |
| 2.2 Decide, then merge | 15 |
| 2.3 Check the merge | 5 |
| 3.1 Stack | 8 |
| 3.2 Reshape | 10 |
| 3.3 Rank | 7 |
| 4.1 Ask | 4 |
| 4.2 Answer | 10 |
| 4.3 Interpret | 6 |
| 5 For a reader who doesn't code | 10 |
| **Total** | **100** |

---

## Part 1: Load and inspect (15)

### 1.1 A loading function (5)

| Points | What it looks like |
|---|---|
| 5 | `fetch_indicator` takes a code, returns a flat DataFrame with one row per country per year, has a docstring and type hints, and is used for both indicators. The country list is loaded and flattened too. |
| 3 | The data is loaded and flat, but the function is missing, isn't reused, or has no docstring. |
| 1 | Data is loaded but still nested, such as a column of dictionaries. |
| 0 | Not loaded. |

### 1.2 Why this indicator (3)

| Points | What it looks like |
|---|---|
| 3 | A specific reason for the choice and a concrete expectation that the rest of the work can confirm or contradict. |
| 2 | A reason and an expectation, but a generic one, such as "it seemed interesting". |
| 0–1 | Missing, or a single phrase. |

### 1.3 Inspect (7)

| Points | What it looks like |
|---|---|
| 7 | Shape, types and missing counts for all three tables. The markdown names the columns you'll use and points out at least one type problem, with the column named. |
| 5 | All three tables inspected, but the explanation is generic or doesn't name a type problem. |
| 3 | Some tables or some checks missing. |
| 0–1 | Little or no inspection. |

---

## Part 2: Clean and join (30)

### 2.1 Find the problems (10)

About 2.5 points per problem, up to four.

| Per problem | What it looks like |
|---|---|
| 2.5 | A real problem, demonstrated with code, with a count of the rows or values affected, and a sentence on why it would break or mislead a merge. |
| 1.5 | A real problem, but asserted rather than demonstrated, or with no count. |
| 0.5 | Vague ("there are missing values") or not actually a problem. |

### 2.2 Decide, then merge (15)

| Points | What it looks like |
|---|---|
| 13–15 | Every question in the spec answered **before** the merge. Each decision names an alternative and a reason specific to this data for rejecting it. The merge carries out exactly what was decided. |
| 9–12 | All decisions recorded and the merge matches them, but at least one reason is generic, or alternatives are missing for some decisions. |
| 5–8 | Some decisions recorded, or the merge doesn't match what was written. |
| 1–4 | A merge with little or no reasoning. |
| 0 | No merge. |

Different choices can earn full marks. What's graded is whether the choice is
defensible and whether the reasoning is yours.

### 2.3 Check the merge (5)

| Points | What it looks like |
|---|---|
| 5 | Row counts before and after, an explicit check for unmatched rows, and a sentence that interprets the numbers. |
| 3 | Counts shown but not interpreted, or no check for unmatched rows. |
| 0–1 | Missing, or "it worked". |

---

## Part 3: Combine and reshape (25)

### 3.1 Stack (8)

| Points | What it looks like |
|---|---|
| 8 | Population cleaned and merged consistently with 2.2, stacked with `pd.concat()`, and the row count justified with arithmetic, not just displayed. |
| 5 | Stacked correctly, but the count isn't justified, or population was handled inconsistently with 2.2. |
| 2 | Attempted, with the wrong columns or a mismatched stack. |
| 0 | Missing. |

### 3.2 Reshape (10)

| Points | What it looks like |
|---|---|
| 10 | `by_year` has one row per country and one column per year. The change column is correct. The decision about missing years is stated, with a reason, and with how many countries it affects. |
| 7 | Correct reshape and change column, but the missing-data decision is unstated or has no reason. |
| 4 | Reshaped, but the change is wrong, such as the wrong years or a sign error. |
| 0–2 | Not reshaped. |

### 3.3 Rank (7)

| Points | What it looks like |
|---|---|
| 7 | Top and bottom ten shown, with region and income level brought in by a merge. Two or three sentences that say something specific about who is at each end. |
| 5 | Both lists shown and described, but generically, or without region and income. |
| 2–3 | Only one list, or no description. |
| 0 | Missing. |

---

## Part 4: Find something interesting (20)

### 4.1 Ask (4)

| Points | What it looks like |
|---|---|
| 4 | Specific, answerable from this data, involves population, region or income, and isn't obvious in advance. |
| 2–3 | Answerable but broad, or answerable but obvious. |
| 0–1 | Generic ("what patterns exist?") or not about the world. |

### 4.2 Answer (10)

| Points | What it looks like |
|---|---|
| 9–10 | The analysis actually answers the question asked, uses techniques from notebooks 02 and 03 appropriately, and the results are displayed so a reader can see the answer. |
| 6–8 | Answers the question, but the output is hard to read or a step is unexplained. |
| 3–5 | Answers a different or easier question than the one asked. |
| 0–2 | Little or no analysis. |

### 4.3 Interpret (6)

| Points | What it looks like |
|---|---|
| 6 | Says what was found, with numbers; whether it's surprising; a plausible explanation; and what you'd need to check before believing it. |
| 4 | Three of those four. |
| 2 | A restatement of the output. |
| 0 | Missing. |

---

## Part 5: For a reader who doesn't code (10)

| Points | What it looks like |
|---|---|
| 9–10 | All four elements present. No code or jargon. Evidence bullets carry specific numbers from your analysis, and the limitation is real and specific. |
| 6–8 | All four elements, but with some jargon, vague evidence, or a generic limitation. |
| 3–5 | Elements missing, or written for a technical reader. |
| 0–2 | Missing. |

---

## Deductions

| Deduction | When |
|---|---|
| −5 | Files not named `SI618_HW01_<uniqname>.py` and `.html` |
| −5 | HTML export missing |

If the exported HTML shows cells that failed, we grade what the export shows.

