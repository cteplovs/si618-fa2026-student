# Milestone 3: machine learning

**Due Wednesday, December 2, before class (3:30 PM).** 200 points, one submission
per group.

In this milestone your group will use machine learning to take its research
questions further. In Milestone 2 you asked whether a relationship exists in your
data; in this milestone you will ask how well that relationship lets you predict an
outcome for cases the model has not seen, and what you can learn from the model's
mistakes. The methods are the ones
from topics 08 to 11: classification, the evaluation of a classifier on held-out
data, decision trees and random forests, and PCA and k-means clustering. Polars,
PySpark and generative AI are not required.

You will be graded on how well the modelling answers your questions, not on how
many models you fit. You will earn more for two models compared fairly against a
baseline, with a result you explain, than for six models whose scores are listed
without a reason for any of them. A model that does no better than the baseline is a full answer, provided the
comparison is sound and you say what it means for your question.

Your presentation on December 7 or 9 will draw on this milestone, so please write
the summary at the end with that audience in mind.

## The notebook

Submit one marimo notebook with the sections below, in this order and under these
headings. As in Milestone 2, it should load and prepare your data itself, or load a
file that an earlier notebook saved and say how that file was made.

### Title and group

Give a working title, and the name and uniqname of each member.

### Response to feedback

For each point the teaching team raised on your Milestone 2, say in a sentence or
two what you changed, or, if you changed nothing, why not, as described on the
[decision log](decision-log.md) page.

### The prediction task

State which of your research questions the modelling addresses, and turn at least
one of them into a prediction task:

1. Say what the model will predict (the target), and for what unit (a tract, a day,
   a listing). A classification target suits most questions; if your question is about
   a number, a regression target is fine, and so is a category you derive from that
   number, provided you say how you chose the cut-off.
2. Say which columns the model will use (the features), and why. Check each one for
   **leakage**: a feature that would not be known at the time of prediction, or that
   is computed from the target, makes a model look better than it is.
3. Say how you will divide the data into training and test sets (the split), and why
   that division suits your data. Data with a time order usually needs a split by time
   rather than a random one, and grouped data, such as several rows per person or
   place, needs the groups kept together.
4. Give the score of the simplest rule (the baseline), such as always predicting the
   most common class or the training mean, so that you can compare every model with
   it.

### Models

Fit at least two kinds of model, such as logistic regression and a decision tree or
random forest. Choose any settings (hyperparameters) by cross-validation on the
training set only, and report the settings you chose and how much they mattered.
Leave the test set untouched until the next section.

### Evaluation

Score every model and the baseline on the test set. Choose a metric that suits your
question and say why: accuracy can mislead when one class is rare, and precision,
recall, F1 or ROC AUC may be more informative. For the model you prefer, show a confusion
matrix, or for a regression target a plot of predicted against actual values, and
look at the cases it gets wrong. Say what those cases have in common.

### Answer

Say what the modelling shows about your research questions, in plain language and
with your numbers. Use the model's coefficients or feature importances to say which
features matter, and compare that with what you found in Milestone 2. A fitted random
forest's `feature_importances_` gives each feature's average share, across the
forest's trees, of the decrease in Gini impurity from their splits, and its values
tend to be larger for features with many distinct values, such as a measurement, than
for yes-or-no features. Then say what
the model does not show, such as whether a feature that predicts well is a cause,
or whether the model would work on data from another place or year.

PCA or k-means may help here, for example to show whether your cases fall into
groups that the target does not capture, but neither is required unless one of
your research questions asks whether your cases fall into groups, as a question
about profiles or types does. In that case, answer it here with k-means: say how
you chose the number of clusters, describe what distinguishes each cluster, use
PCA to show the clusters if that helps, and compare the clusters with the
variables the question names. The prediction task above is still required, built
from another of your questions.

### Summary of findings

Write a summary of about 200 words for a reader who does not code, with no code and
no jargon. Say what you tried to predict, how well it worked compared with the simple
rule, what drove the predictions, and the limitation that matters most. We will share
your summary with the class as part of a package that describes the schedule and
content of the presentation sessions.

### Decision log

Write three entries, as described on the [decision log](decision-log.md) page,
drawn from your modelling: which features you used, how you split the data, how you
tuned a setting, or which metric you used to judge a model.

## Grading

Title and group are required but not graded. The other sections are graded as
follows.

| Section | Points |
|---|---|
| Response to feedback | 10 |
| The prediction task | 40 |
| Models | 40 |
| Evaluation | 40 |
| Answer | 40 |
| Summary of findings | 10 |
| Decision log | 20 |
| **Total** | **200** |

We will mark each section at one of four levels, described below, worth all, 70%,
40% or none of the section's points, so that a section worth 40 earns 40, 28, 16 or
0.

| Section | All | 70% | 40% | None |
|---|---|---|---|---|
| Response to feedback | Answers every point raised on Milestone 2, saying what changed or why nothing did. | Answers most of the points, or answers some without saying what changed. | Mentions the feedback without responding to it point by point. | Missing. |
| The prediction task | The target, features, split and baseline are all stated and justified, and the features are checked for leakage in the notebook. | All four are stated, but one is not justified, or leakage is not checked. | The target and features are stated, but the split or the baseline is missing. | Missing. |
| Models | At least two kinds of model, with settings chosen by cross-validation on the training set and the chosen settings reported. | Two kinds of model, but the settings are not tuned, or are tuned using the test set. | One model only. | No model is fitted. |
| Evaluation | Every model and the baseline are scored on the test set with a metric chosen for the question, and the preferred model's errors are examined. | Scored against the baseline, but the metric is not justified or the errors are not examined. | Scored without a baseline, or only on the training data. | Missing. |
| Answer | Says what the modelling shows about the questions with numbers, uses the features to explain it, compares it with Milestone 2, and says what the model does not show. | Answers the questions, but without the comparison with Milestone 2 or without saying what the model does not show. | Reports the scores without saying what they mean for the questions. | Missing. |
| Summary of findings | Covers the target, the comparison with the baseline, what drove the predictions and a real limitation, in plain language. | Covers all four, but with some jargon or a generic limitation. | Leaves out the baseline or the limitation, or is written for a technical reader. | Missing. |
| Decision log | Graded at the five levels on the [decision log](decision-log.md) page. | | | |

## Submitting

One member should submit two files for the group, on Canvas under *Project
Milestone 3*:

1. The notebook, named `SI618_M3_<group name>.py`
2. Its HTML export:
   ```bash
   uvx marimo export html --sandbox SI618_M3_<group name>.py -o SI618_M3_<group name>.html
   ```

Please check the HTML before you upload it. If the notebook could not load its data,
the export still succeeds but every cell after the loading shows an error, and the
HTML is what the grader reads.
