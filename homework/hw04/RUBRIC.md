# Rubric: Homework 4 - Who wrote the last forty chapters?

**100 points.** This is the rubric we grade against, published before you start so
that you know where the points are.

## How to read it

Code that runs is necessary but not sufficient. Most of the points in every part go
to **decisions and explanations**: what you found, what you changed, and what your
own output shows. A correct table with no interpretation earns partial credit,
whereas a defensible choice that is clearly explained earns full credit, even if a
classmate made a different choice that is equally defensible.

"Specific" in this rubric means that a sentence refers to your data, whether by a
chapter number, a character, a count, a rate or another number from your output.
"Generic" means that it could have been written without running the code.

You are not expected to read Chinese. Interpretations are judged against the
meanings given in the spec's table of function characters.

## Points

| Part | Points |
|---|---|
| 1.1 Load and strip | 5 |
| 1.2 Split | 10 |
| 2.1 Show the problem | 4 |
| 2.2 Convert | 6 |
| 3.1 The table | 12 |
| 3.2 Look first | 8 |
| 4.1 Test | 14 |
| 4.2 Read the table | 8 |
| 4.3 Where does the change happen? | 8 |
| 5 Content against style | 10 |
| 6 For a reader who doesn't code | 15 |
| **Total** | **100** |

---

## Part 1: Get the chapters (15)

### 1.1 Load and strip (5)

| Points | What it looks like |
|---|---|
| 5 | The file is loaded, Project Gutenberg's text is removed from both ends, and the length and the first and last 200 characters of what remains are shown, so a reader can see that the novel begins and ends where it should. |
| 3 | Loaded and stripped, but only one end is shown or checked. |
| 1 | Loaded, with the licence text left in. |
| 0 | Not loaded. |

### 1.2 Split (10)

| Points | What it looks like |
|---|---|
| 9-10 | `chapters` has 120 rows numbered 1 to 120 with no gaps or repeats, and a check shows it. The matches that are not headings and the repeated chapter are each shown with the rows of `heading_matches` that revealed them, and the fix is explained. `n_chars` counts Chinese characters only, and the shortest and longest chapters are shown. |
| 6-8 | 120 correct chapters, but the problems are fixed without being shown, or `n_chars` counts punctuation and spaces. |
| 3-5 | A split that is close but wrong, for example 121 or 123 rows. |
| 0-2 | No usable split. |

---

## Part 2: Normalise (10)

### 2.1 Show the problem (4)

| Points | What it looks like |
|---|---|
| 4 | A table of simplified and traditional counts for the function characters that have two forms, with a sentence saying that counting the simplified list in the file as it stands would give zero for most of them, and a sentence on how unequal mixing between the halves would bias the comparison. |
| 2-3 | The counts are shown but one of the two sentences is missing or generic. |
| 0-1 | The problem is asserted without counts. |

### 2.2 Convert (6)

| Points | What it looks like |
|---|---|
| 6 | Every chapter is converted with `t2s`, every function character is checked, the one with no occurrences is found, the reason is given, and the fix is defended. |
| 3-5 | The conversion and the check are done, but the reason or the defence of the fix is missing or wrong. |
| 1-2 | Converted, with no check. |
| 0 | Not converted. |

---

## Part 3: Count (20)

### 3.1 The table (12)

| Points | What it looks like |
|---|---|
| 11-12 | `CountVectorizer` with `analyzer="char"` and the given vocabulary, run on the converted text. `rates` is indexed by chapter, has one column per character, and is divided by each chapter's count of Chinese characters and multiplied by 1,000. The sentence says that written Chinese has no spaces between words, so splitting on spaces gives whole sentences rather than words. |
| 7-10 | The table is right but divides by the wrong length, such as including punctuation, or the sentence on `analyzer="char"` is missing or generic. |
| 3-6 | Raw counts instead of rates, or counted on the unconverted text. |
| 0-2 | Missing or not built with `CountVectorizer`. |

### 3.2 Look first (8)

| Points | What it looks like |
|---|---|
| 7-8 | Both characters plotted across all 120 chapters with a line between 80 and 81. The description names specific stretches of chapters, and says that the first 80 are not uniform. |
| 4-6 | Plotted and described, but the description covers only the comparison at chapter 80. |
| 1-3 | Plotted with little or no description. |
| 0 | Missing. |

---

## Part 4: Compare the two parts (30)

### 4.1 Test (14)

| Points | What it looks like |
|---|---|
| 13-14 | One table with both means, the difference, Cohen's d and Welch's p-value for every character, sorted by p-value. The Bonferroni threshold is stated (0.05 divided by the number of characters tested), and the number of characters that pass it is given. |
| 9-12 | The tests are right but a column is missing, the t-test assumes equal variances, or the correction is applied wrongly. |
| 5-8 | Tests run for only some characters, or with no correction. |
| 0-4 | Missing or wrong in method. |

### 4.2 Read the table (8)

| Points | What it looks like |
|---|---|
| 7-8 | The characters that fell and those that rose are grouped by meaning, using the spec's table, and the paragraph says what kind of change that suggests in the writing, with specific characters and sizes. |
| 4-6 | The direction of each change is reported, but the grouping by meaning or the conclusion about the writing is generic. |
| 0-3 | A restatement of the table. |

### 4.3 Where does the change happen? (8)

| Points | What it looks like |
|---|---|
| 7-8 | A rolling mean or another justified method, applied to more than one character, with a conclusion about where the change happens and whether it is a single change, tied to the plot from 3.2. |
| 4-6 | A method applied and a conclusion reached, but for one character only, or without addressing whether the change is single. |
| 0-3 | An assertion with no method. |

---

## Part 5: Content against style (10)

| Points | What it looks like |
|---|---|
| 9-10 | Fifteen characters shown with the change in mean TF-IDF, those in `FUNCTION_CHARS` marked, the rest looked up and identified (names, titles, plot words). The explanation says that these characters follow what happens in the story, so they would change between parts of a book by one author, whereas function-character rates are not chosen consciously. |
| 5-8 | The list is shown and an explanation given, but the characters are not identified or the explanation is generic. |
| 0-4 | Missing, or TF-IDF not computed per chapter. |

---

## Part 6: For a reader who doesn't code (15)

| Points | What it looks like |
|---|---|
| 13-15 | All four elements present, with no code or jargon. The evidence bullets carry specific numbers, and the so-what names at least two explanations other than a different author and says plainly that the counts cannot by themselves prove who wrote the ending. |
| 9-12 | All four elements, but one alternative explanation, some jargon, or vague evidence. |
| 4-8 | Elements missing, or a conclusion that claims more than the evidence shows. |
| 0-3 | Missing. |

---

## Deductions

| Deduction | When |
|---|---|
| -5 | Files not named `SI618_HW04_<uniqname>.py` and `.html` |
| -5 | HTML export missing |

If the exported HTML shows cells that failed, we grade what the export shows.

