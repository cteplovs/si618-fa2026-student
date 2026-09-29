# The decision log

Every project milestone ends with a decision log, worth **20 of the milestone's 200
points**. It records the choices your group made that shaped your results, what you
chose instead of the obvious alternative, and the output in your own notebook that
settled each choice.

The log exists because the reasoning behind an analysis is the part of it that
cannot be delegated. Code that runs is now easy to produce, whereas an account of
why you dropped those rows rather than imputing them depends on having looked at
your data and decided, and that is what this section of the project assesses.

## What goes in it

End each milestone notebook with a section headed `## Decision log`, containing
**three entries**. Each entry has four parts:

| Part | What it records |
|---|---|
| **Decision** | What your group did. |
| **Alternative** | The option you considered and did not take. |
| **Evidence** | The output in this notebook that settled it: a number, a table or a plot. |
| **Consequence** | What would have changed in your results if you had taken the alternative. |

The decisions should come from the milestone at hand:

- **Milestone 1:** cleaning and merging, such as how you matched records across
  your datasets, what you did with rows that did not match, and how you handled
  missing values.
- **Milestone 2:** analysis, such as which test you chose, which subset of the data
  you compared, or which transformation you applied before a test.
- **Milestone 3:** modelling, such as which features you used, how you tuned a
  parameter, or which metric you used to judge a model.

Choose decisions that made a difference. Renaming a column is not one, whereas
choosing an inner join that lost a quarter of your rows is.

## Responding to feedback

Milestones 2 and 3 also **open** with a short section headed `## Response to
feedback`. For each point the teaching team raised on your previous milestone, say
in a sentence or two what you changed, or, if you changed nothing, why not.
Disagreeing with a comment is fine, provided you give a reason.

## Keep the evidence live

Wherever you can, compute the numbers in your log rather than typing them. In a
marimo notebook, an f-string in a markdown cell does this:

```python
mo.md(f"""
**Evidence.** The inner join kept {n_matched:,} of {n_total:,} rows
({n_matched / n_total:.0%}), and the rows it dropped were mostly from
{top_dropped_state}.
""")
```

If you later change the cleaning upstream, the log changes with it, and the numbers
you report are always the ones your notebook produced.

## An example entry

> **Decision.** We matched each hour of bike-share trips to the weather recorded at
> the Central Park station, rather than to the average of the city's three
> stations.
>
> **Alternative.** Averaging the three stations, which smooths out any one
> station's gaps.
>
> **Evidence.** In the 1,406 hours with rain at any station, the three disagree on
> whether it rained at all in 38% of them, and Central Park has no missing hours
> in our date range.
>
> **Consequence.** Averaging would have turned short, heavy showers into longer
> spells of light rain, which weakens the drop in ridership during rain that our
> first research question is about.

The numbers in this example are illustrative, and yours will come from your own
notebook.

## How it is graded

The log is graded as a whole, at one of five levels.

| Points | The log... |
|---|---|
| 20 | has three entries, each with all four parts. Every alternative is one a reasonable analyst might have taken, every piece of evidence is output from this notebook, and at least one consequence is shown by running the alternative rather than described. |
| 15 | has three complete entries with genuine alternatives and evidence from this notebook, but every consequence is described rather than shown. |
| 10 | has three entries, but one or more has a token alternative ("we could have done nothing") or evidence that is asserted rather than shown in the notebook. |
| 5 | has fewer than three entries, or entries that describe what was done without an alternative or evidence. |
| 0 | is missing. |

In Milestones 2 and 3, a missing response to feedback lowers the log by one level.

## Where else it is used

- **Peer review.** When you review another group's Milestone 2, one part of the
  review asks you to assess one entry from their decision log.
- **Presentation.** Your presentation includes one decision from any of your three
  logs, and the questions afterwards may start there.
