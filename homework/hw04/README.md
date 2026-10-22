# Homework 4: Who wrote the last forty chapters?

**100 points.** The homework is released on Wednesday, October 21, after class,
and is due **Wednesday, October 28, before class (3:30 PM)**.

Submit two files to Canvas: your notebook, renamed `SI618_HW04_<uniqname>.py`, and
its HTML export, `SI618_HW04_<uniqname>.html`. The rubric we grade against is in
[RUBRIC.md](RUBRIC.md), and the notebook to start from is
[starter.py](starter.py).

---

## What this assignment is about

*Dream of the Red Chamber* (红楼梦), written in the middle of the eighteenth
century, is the most celebrated novel in Chinese literature. Its author, Cao
Xueqin, died before it was finished, and the manuscripts that circulated after his
death stop at chapter 80. The novel first appeared in print in 1791, edited by Gao
E and Cheng Weiyuan, with 120 chapters, and scholars have argued ever since about
who wrote the last forty: Cao from surviving drafts, Gao E, someone else, or some
mixture of them.

You do not need to read Chinese to do this homework. Writers use small function
words, such as "of", "also" and "then", at rates they do not choose consciously,
and those rates can differ between writers even when the story stays the same. In
notebook 07a you turn text into a table of counts; here you will count a set of
function characters in every chapter, and ask whether chapters 81 to 120 use them
at different rates from chapters 1 to 80. The table of characters below gives the
meaning of each one, which is all you need to interpret the results.

**Everything you need is in notebooks 02 to 07 and the starter**: filtering rows
from 02 and 03, the t-test and Cohen's d from 05a, the Bonferroni correction from
06b, and `CountVectorizer` and TF-IDF from 07a.

**Most of the points are for decisions and explanations rather than for code.**
Where the spec asks you to explain or decide, write full sentences in a markdown
cell, and refer to specific numbers from your own output.

---

## The data

The text is the Project Gutenberg edition of the novel (eBook 24264), in the
120-chapter form first printed in 1791. A copy is kept in the course data
repository so that everyone works from the same file:

```
https://raw.githubusercontent.com/umsi-data-science/data/main/hongloumeng_pg24264.txt
```

It is a single plain-text file of about 2.6 MB, encoded as UTF-8, with Project
Gutenberg's licence text at the beginning and end. Each chapter begins with a
heading line of the form 第N回 ("chapter N"), followed by the chapter's title, a
pair of matched phrases. The file was typed by volunteers, and it is not as tidy
as that description suggests, so please check what you get at every step.

**The function characters.** The starter defines this list as `FUNCTION_CHARS`.
The first seven belong to classical, literary Chinese, and the rest to the
everyday spoken language of the novel's dialogue and narration.

| Character | Pinyin | Meaning |
|---|---|---|
| 之 | zhi | literary "of"; also "it, him" |
| 其 | qi | literary "his, its, their" |
| 亦 | yi | literary "also" |
| 乃 | nai | literary "then; is" |
| 而 | er | literary "and, but" |
| 矣 | yi | literary particle marking a completed state |
| 焉 | yan | literary particle, "there; how" |
| 了 | le | marks a completed action |
| 的 | de | everyday "of", possessive |
| 着 | zhe | marks an action in progress |
| 呢 | ne | particle for questions and emphasis |
| 吗 | ma | particle that makes a yes-or-no question |
| 么 | me | as in 什么 "what" and 怎么 "how" |
| 罢 | ba | "let it be; that will do" |
| 便 | bian | "then, thereupon" |
| 就 | jiu | "then, just" |
| 也 | ye | "also" |
| 又 | you | "again" |
| 都 | dou | "all" |
| 还 | hai | "still" |
| 只 | zhi | "only" |
| 这 | zhe | "this" |
| 那 | na | "that" |

---

## Part 1: Get the chapters (15 points)

**1.1 Load and strip (5).** Load the file, remove Project Gutenberg's text at the
beginning and end, and store what remains in a string called `novel`. Show how
many characters the novel has, and the first and last 200 characters of what you
kept.

**1.2 Split (10).** The starter finds every line of `novel` that begins with a
chapter heading and lists the matches in a DataFrame, `heading_matches`, with
each match's position in `novel`, its chapter number as an integer, and the whole
line, and it finds more than 120. Using pandas, work out which matches are not real
chapter headings and which chapters are counted more than once, and show the rows
that told you. Then build a DataFrame `chapters` with one row per chapter, a
column `chapter` holding the chapter number from 1 to 120, and a column `text`
holding that chapter's text, which runs from its heading to the next one. Finish
with a check that `chapter` runs from 1 to 120 with no gaps or repeats. Then add a
column `n_chars` counting the Chinese characters in each chapter (not punctuation
or spaces), which you can do with the starter's `CHINESE_CHAR` and pandas'
`.str.count()`, and show the shortest and longest chapters.

You do not need to write a regular expression, and if you ask an AI assistant
for help with any of this, please say so in your attribution. Either way, we
grade the evidence that your 120 chapters are right.

---

## Part 2: Normalise (10 points)

The volunteers who typed this edition did not all use the same script. Most of
the file is in traditional characters (這, 還), but some characters are typed in the
simplified forms used in mainland China today (么), and `FUNCTION_CHARS` is written
entirely in simplified forms.

**2.1 Show the problem (4).** For each character in `FUNCTION_CHARS`, count how
often it appears in the file in its simplified form and in its traditional form,
and show the counts in one table. Say what the table means for any count made from
the file as it stands, and what would happen to a comparison between the two halves
of the book if they had been typed in different proportions of each script.

**2.2 Convert (6).** Convert every chapter to simplified characters with OpenCC's
`t2s` converter, which the starter imports, and store the result in a new column
of `chapters` called `simplified`. Then check whether every character in
`FUNCTION_CHARS` occurs in the converted text. One of them does not, so find out
why, fix it in a way you can defend, and say what you did.

---

## Part 3: Count (20 points)

**3.1 The table (12).** Use scikit-learn's `CountVectorizer` with
`analyzer="char"` and `vocabulary=FUNCTION_CHARS` to count the function characters
in every chapter. Build a DataFrame `rates` with one row per chapter, indexed by
chapter number, and one column per character, giving its rate per 1,000 Chinese
characters. Explain in a sentence why `analyzer="char"` is the right choice for
Chinese, where splitting on spaces is not.

**3.2 Look first (8).** Before testing anything, plot the rate of 之 and of 么
across all 120 chapters, with a vertical line between chapters 80 and 81. Describe
what you see, including whether the first 80 chapters are themselves uniform.

---

## Part 4: Compare the two parts (30 points)

**4.1 Test (14).** For every character in `FUNCTION_CHARS`, compare its rate in
chapters 1 to 80 with its rate in chapters 81 to 120. Use Welch's t-test, and
report the two means, the difference, Cohen's d and the p-value in one table, a
DataFrame called `comparison` with one row per character, sorted by p-value. Then
apply a Bonferroni correction for the number of tests and say how many characters
still differ.

**4.2 Read the table (8).** Using the meanings in the table of function
characters, describe which characters went up and which went down, and say what
kind of change in the writing that pattern suggests.

**4.3 Where does the change happen? (8).** If the last forty chapters were written
by someone else, the rates would be expected to change at chapter 81. Use a rolling mean over
chapters, or another method you can justify, to judge whether the change happens
at chapter 81 or somewhere else, and whether it is a single change. Say what you
conclude, and refer to your plot from 3.2.

---

## Part 5: Content against style (10 points)

Use `TfidfVectorizer` with `analyzer="char"`, treating each of the 120 converted
chapters as a document. For every character, take its mean TF-IDF score in
chapters 81 to 120 minus its mean in chapters 1 to 80, and show the fifteen
characters with the largest increase. Mark which of them are in `FUNCTION_CHARS`,
and look up the rest in an online dictionary such as [MDBG](https://www.mdbg.net/)
to say what they are. Then explain why a study of authorship counts function
characters rather than the characters TF-IDF finds most distinctive.

---

## Part 6: For a reader who doesn't code (15 points)

Write a summary in a markdown cell, with no code and no jargon, for a reader who
knows the novel and has heard that "computers have proved" who wrote the ending:

- **Question:** what you set out to learn, in one sentence
- **Finding:** the most important result, in one sentence
- **Evidence:** two or three bullet points, each with a specific number
- **So what:** what this does and does not show about who wrote the last forty
  chapters, naming at least two explanations other than a different author that
  could produce the same pattern

---

## Before you submit

- **Run it top to bottom.** Restart the notebook and run every cell. If the HTML
  export shows errors, we grade what the export shows.
- **Attribute AI use.** If you used generative AI in a substantial way, add a
  sentence at the end saying what you used and what it did, as the syllabus asks;
  it doesn't affect your grade.
- **Name both files correctly** and upload both.

The starter's tests check that your work has the right shape: that `chapters` has
120 rows, that `rates` has one column per function character, and so on. They
don't check your answers, and a green test doesn't mean a section is complete.

Late work follows the late-day policy in the syllabus: three free late days for the
term, then 25% per day.
