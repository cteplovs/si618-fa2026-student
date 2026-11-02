# Milestone 2: analysis

Milestone 2 is due **Monday, November 16, before class (3:30 PM)**, and is worth 200
points. Each group makes one submission.

In this milestone, your group will answer the three research questions it posed in
Milestone 1, using the merged dataset it built there. The methods are the ones from
topics 04 to 07: descriptive statistics and plots, correlation, t-tests, ANOVA,
linear regression, contingency tables and the chi-square test, and the text methods
from 07 if your data has text. Machine learning belongs to Milestone 3, so leave
classifiers and clustering until then.

We will grade how well you answer your questions, not how many techniques you use.
One well-chosen test whose result you explain earns more than five tests
reported without a reason for any of them. A clear "no" is a full answer, provided
the evidence for it is sound.

Two other groups will read your notebook for the peer review due on November 23,
so please write it for a reader who knows the course material but has not seen your
data.

## The notebook

Submit one marimo notebook with the sections below, in this order and under these
headings. It should load and merge your data itself, either by repeating the
Milestone 1 code or by loading a file that the Milestone 1 notebook saved, and in
the second case it should say how that file was made.

### Title and group

Give a working title, and the name and uniqname of each member.

### Response to feedback

Feedback on Milestone 1 will come in two forms: the comments on your Canvas
submission, and the meeting your group will have with the teaching team at the
Project Studio on Wednesday, November 11, which will last about ten minutes and
cover the decisions in your Milestone 1.

For each point raised in either, say in a sentence or two what you changed, or, if
you changed nothing, why not, as described on the [decision log](decision-log.md)
page. For the meeting, also record which of your decisions you were asked about,
how you explained each one, and whether the conversation changed your view of it.
Disagreeing with a point is fine, provided you give a reason.

### Research questions

Restate your three questions, each with the columns it depends on. If you have
revised a question since Milestone 1, give the original wording and say why you
changed it. Revising a question because the data could not answer it is a good
reason; revising it so that the answer becomes more interesting is not.

### Question 1, Question 2, Question 3

Write one section for each question, with the question as its heading. Each section
should have three parts, under these subheadings.

#### Approach

Say which method you used and why it suits this question and this data. Say what
the method assumes, check those assumptions in the notebook, and say what you did
about any that do not hold. Every test in topics 05 and 06 assumes that the rows
are independent of one another, which consecutive days or months, several rows for
the same person or place, and overlapping areas are not. If your data is like that,
say so, and either test on a version of the data in which the rows are independent,
such as one row per place or a sample of months spaced apart, or explain how the
dependence could affect your p-value.

#### Result

Show the output that answers the question: the test statistic, the p-value, an
effect size (such as a difference in means, a coefficient, Cohen's d or Cramer's
V), the number of observations used, and a plot where one helps. If you run several
tests for one question, say how you adjusted for that. With tens of thousands of
rows, almost any difference has a tiny p-value, so in a large dataset the answer
depends on the effect size, and on whether it is big enough to matter.

#### Answer

Give the answer to the question in plain language, in two or three sentences that
refer to your numbers. Then say what the result does not show, such as whether it
could be explained by something your data does not measure, or whether it would
hold outside the places, years or people your data covers.

### Summary of findings

Write a summary of about 200 words for a reader who does not code, with no code
and no jargon. For each question, give the answer in one sentence and the single number
that best supports it. End with the limitation that matters most for how far your
answers can be trusted.

### Decision log

Write three entries, as described on the [decision log](decision-log.md) page,
drawn from your analysis: which test you chose, which subset you compared, which
transformation you applied, or how you handled an assumption that did not hold.

## Grading

Title and group, and the restated research questions, are required but not graded.
We will grade the meeting on November 11 on how well your group explains its
Milestone 1 work, and the sections of the notebook as follows.

| Part | Points |
|---|---|
| The meeting | 20 |
| Response to feedback | 20 |
| Question 1 | 40 |
| Question 2 | 40 |
| Question 3 | 40 |
| Summary of findings | 20 |
| Decision log | 20 |
| **Total** | **200** |

Each part is marked at one of four levels, described below, worth all, 70%, 40%
or none of its points, so that a question worth 40 earns 40, 28, 16 or 0.

| Part | All | 70% | 40% | None |
|---|---|---|---|---|
| The meeting | Every member can explain, in their own words, the decisions they are asked about, the alternatives the group rejected, and any code or markdown in the Milestone 1 notebook they are asked to explain. | The group explains most of what it is asked about, but one decision or one piece of code cannot be explained, or one member answers for the others. | The group can explain little of what it is asked about beyond reading from the notebook. | The group does not attend. |
| Response to feedback | Answers every point raised in the Canvas comments and in the meeting, saying what changed or why nothing did, and records each decision discussed in the meeting and how the group explained it. | Answers most of the points, leaves out the meeting, or answers some points without saying what changed. | Mentions the feedback or the meeting without responding to it point by point. | Missing. |
| Each question | The method suits the question and its assumptions are checked in the notebook. The result is reported with its statistic, p-value, effect size and number of observations, and the answer is stated in plain language with what the result does not show. | The method and result are sound, but the assumptions are not checked, the effect size is missing, or the answer leaves out what the result does not show. | A method is applied, but it does not suit the question, or the result is reported without being interpreted as an answer. | The question is not answered. |
| Summary of findings | Answers all three questions in plain language, each with a number from the analysis, and names a real limitation. | Answers all three, but with some jargon, a missing number, or a generic limitation. | Answers fewer than three, or is written for a technical reader. | Missing. |
| Decision log | Graded at the five levels on the [decision log](decision-log.md) page. | | | |

## Submitting

One member should submit two files for the group, on Canvas under *Project
Milestone 2*:

1. The notebook, named `SI618_M2_<group name>.py`
2. Its HTML export:
   ```bash
   uvx marimo export html --sandbox SI618_M2_<group name>.py -o SI618_M2_<group name>.html
   ```

Please check the HTML before you upload it. If the notebook could not load its data,
the export still succeeds but every cell after the loading shows an error, and the
HTML is what the grader reads.
