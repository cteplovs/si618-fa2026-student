# Milestone 1: data description and manipulation

**Due Wednesday, October 14, at the end of the Project Studio session.** 200 points,
one submission per group.

In this milestone your group chooses its datasets, poses the questions the rest of
the project will answer, and builds the single merged dataset that Milestones 2 and
3 will use. It stops short of statistical testing, which is Milestone 2's job, so
use only the techniques from the course's first four topics: loading, cleaning,
merging, reshaping, grouping, summarising and plotting.

The Project Studio on October 14 is a full class session for project work, with the
teaching team circulating. Please arrive with your data loaded and merged, so
that the session can be spent on the parts of the work that benefit from having
the teaching team in the room.

## The notebook

Submit one marimo notebook with the sections below, in this order and under these
headings.

### Title and group

Give a working title, and the name and uniqname of each member.

### Overview

Write a paragraph saying what the project is about and what the merged data will let you
do that neither dataset could do alone.

### Research questions

Pose **three questions** for the rest of the project to answer. Each question
needs three things, because Milestones 2 and 3 will be graded on how well you answer
these questions rather than on how many techniques you use:

1. **The question itself.** It should be broad enough that it cannot be answered
   by looking up a single number. "How many bikes were hired in New York in 2024?" is a lookup,
   whereas "Does rain reduce bike hire more on weekdays than at weekends?" is a
   question.
2. **The columns it depends on.** Name them as they appear in your merged data,
   and make sure that at least one question draws on columns from more than one
   of your datasets.
3. **What an answer would look like.** Describe the comparison, relationship or
   pattern that would answer it, and what you would expect to find if the answer
   turned out to be no.

### Data sources

For each dataset, give its name, who publishes it, its URL, the date you
downloaded it, and its licence or terms of use if it has them. Then explain how
the datasets complement each other, and which columns you will match them on.

### Data description

For each dataset before merging, and for the merged dataset after, give the
number of rows and columns, what one row represents, the variables your research
questions depend on with their types and units, and how much of each is missing.
A table is fine, and computing it in the notebook is better than typing it.

### Data manipulation

This section is mostly code, with markdown explaining each step. It covers loading
each dataset, cleaning it, merging the datasets, and creating any new columns your
questions need. Report how many rows survive each step, and in particular how many
rows the merge matched and how many it did not.

### Data visualisation

Include **three or more plots** that describe the merged data, each chosen to show
something relevant to one of your research questions, with a title, labelled axes
and a sentence or two saying what it shows.

### Decision log

Write three entries, as described on the [decision log](decision-log.md) page,
drawn from your cleaning and merging.

## Grading

Title and group are required but not graded. The other sections are graded as
follows.

| Section | Points |
|---|---|
| Overview | 10 |
| Research questions | 10 |
| Data sources | 20 |
| Data description | 40 |
| Data manipulation | 50 |
| Data visualisation | 50 |
| Decision log | 20 |
| **Total** | **200** |

Each section is marked at one of four levels, described below, worth all, 70%,
40% or none of the section's points, so that a section worth 40 earns 40, 28, 16 or
0.

| Section | All | 70% | 40% | None |
|---|---|---|---|---|
| Overview | Says what the project is about and what the merged data makes possible. | Says what the project is about but not what the merge adds. | Is vague about both. | Missing. |
| Research questions | Three questions, each with its columns and what an answer would look like, at least one drawing on more than one dataset. | Three questions, but one lacks its columns or its description of an answer. | Fewer than three questions, or questions that are lookups. | Missing. |
| Data sources | Every dataset is fully cited and the matching columns are named and justified. | Every dataset is cited, but the matching columns are not explained. | A dataset is missing its URL or its publisher. | Missing. |
| Data description | Before and after the merge, gives rows, columns, the unit of a row, types, units and missingness for every variable the questions use, computed in the notebook. | Covers all of that, but some of it is typed rather than computed, or one variable is missed. | Covers only the merged data, or leaves out missingness. | Missing. |
| Data manipulation | Loads, cleans and merges the data in code that runs, reports the rows surviving each step including the merge's matched and unmatched rows, and explains each step. | Does all of that, but does not report the rows lost at one or more steps. | Merges the data, but the cleaning is unexplained or the result is not a single tidy table. | The data is not merged. |
| Data visualisation | Three or more labelled plots, each tied to a research question and interpreted. | Three plots, but one is unlabelled, uninterpreted or unrelated to the questions. | Fewer than three plots, or plots without interpretation. | Missing. |
| Decision log | Graded at the five levels on the [decision log](decision-log.md) page. | | | |

## Submitting

One member submits for the group, on Canvas under *Project Milestone 1*, two files:

1. The notebook, named `SI618_M1_<group name>.py`
2. Its HTML export:
   ```bash
   uvx marimo export html --sandbox SI618_M1_<group name>.py -o SI618_M1_<group name>.html
   ```

Please check the HTML before you upload it. If the notebook could not load its data, the
export still succeeds but every cell after the loading shows an error, and the
HTML is what the grader reads.
