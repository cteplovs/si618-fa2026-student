# SI 618 — Data Manipulation & Analysis

**Fall 2026: Mondays & Wednesdays, 3:30–4:50PM**
**Location: LCSIB 1290**

> **Note:** Some syllabus details may be subject to change.

Last update: Sunday, August 30, 2026 · Version 2026.08.30.4.CT

**Lead Instructor:** Dr. Chris Teplovs

**Email:** cteplovs@umich.edu (see [Communication](#communication) below)

**Office hours:** Tuesdays, 10:00-11:30AM, LCSIB 4566

**Graduate Student Instructors (GSIs):** Xin Ye

**GSI office hours:** Fridays, 4:00-5:00PM, LCSIB 4540

---

## Communication

The best way to reach any member of the teaching team about course content is to
come to class and to office hours. Alternatively, use Slack (link via Canvas).

We try to answer questions sent via Slack within about **48 hours**. Responses on
weekends and holidays may be slower. For that reason, we strongly urge you not to
use Slack for last-minute questions about assignments. Your GSIs should be your
first choice for technical questions; conceptual questions are best directed to
Dr. Teplovs.

Personal matters should be communicated via email to Dr. Teplovs. Please include
"[SI 618]" in your subject line to receive a timely response.

---

## Course Description

This course aims to help students get started with their own data harvesting,
processing, aggregation, and analysis. Data analysis is crucial to evaluating and
designing solutions and applications, as well as understanding users' information
needs and use. In many cases the data we need to access is distributed online
among many web pages, stored in a database, or available in a large text file.
Often these data (e.g. web server logs) are too large to obtain and/or process
manually. Instead, we need an automated way of gathering the data, parsing it, and
summarizing it, before we can do more advanced analysis.

Students will learn to use Python and its modules to accomplish these tasks in a
"quick and easy" yet useful and repeatable way. Next, students will learn
techniques of exploratory data analysis, using scripting, text parsing, structured
query language, regular expressions, graphing, and clustering methods to explore
data. Students will be able to make sense of and see patterns in otherwise
intractable quantities of data.

The skills students will learn include: big data processing; converting messy data
into a form that can be analyzed using pandas; computing and visualizing summary
statistics of datasets; specifying graphical displays using seaborn and matplotlib;
combining graphics with data manipulation to visualize relationships between
variables; using machine learning techniques including clustering and
classification; and using dimension reduction techniques.

---

## Learning Outcomes

At the end of the course, students should be able to:

- **C:** use Python (via marimo notebooks) for data analysis
- **C:** load and manipulate data in a variety of formats (CSV, JSON, Parquet,
  unstructured text, results of SQL queries)
- **C:** filter, sort, select columns, etc.
- **L:** create visualizations using matplotlib and seaborn
- **L:** extract data using SQL
- **L:** construct a machine learning pipeline using scikit-learn
- **L:** use a scikit-learn classifier
- **A:** explain when and why a dataset needs out-of-core or distributed
  processing, and recognize the shape of a Polars or Spark solution
- **AL:** describe common techniques used in natural language processing
- **AL:** describe how large language models can be used as tools within a data
  analysis workflow, and where they should not be trusted


---

## Textbooks

Nearly everything assigned in this course is available to you at no cost through
O'Reilly, which the
[U-M Library](https://www.lib.umich.edu/announcements/oreilly-safari-books-online)
provides institutional access to. Sign in there once, and you can then search
O'Reilly for any of the titles below and read them in full.

The books we draw on most are:

- Bruce, Bruce & Gedeck, *AI-Assisted Statistics for Data Scientists*, 3rd edition
- Chen, *Pandas for Everyone*
- McKinney, *Python for Data Analysis*
- Géron, *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow*
- Grus, *Data Science from Scratch*
- VanderPlas, *Python Data Science Handbook*

A few readings are free on the open web rather than on O'Reilly, and those are
linked directly where they're assigned.

Readings are given by chapter topic rather than by chapter number, since O'Reilly
serves whichever edition is current and the numbering shifts between editions.
Search the book's table of contents for the topic named and you'll find it.

---

## Schedule

The course combines short lectures with live hands-on coding. The general idea is
that you learn the concepts and techniques and then practice them by writing code
in class. In addition, there are regular programming and analysis assignments to be
done as homework. You will use Python for all in-class work and homework.

**This term the course meets twice a week for 80 minutes rather than once for
2 hours 50 minutes.** Most topics run across **two consecutive sessions from a
single notebook**: the Wednesday session opens the notebook, the following Monday
session finishes it, and you submit once at the end of Monday. Four late-term
topics run as single sessions.

---

## Course Outline

> **Note 1:** Some syllabus details and timing may be subject to change.
> **Note 2:** "NB" refers to the in-class notebook.
> **Note 3:** Readings are named by topic rather than chapter number. See
> [Textbooks](#textbooks) above for how to reach them through O'Reilly.

| # | Date | Topic | Pre-class preparation | Due by end of class |
|---|---|---|---|---|
| 1 | Mon Aug 31 | **01 Introduction** — marimo, Python review | — | — |
| 2 | Wed Sep 2 | 01 Introduction *(cont.)* | | **In-class 01** |
| — | *Mon Sep 7* | *Labor Day — no class* | | |
| 3 | Wed Sep 9 | **02 Data manipulation I:** pandas DataFrames | Chen, the chapters on DataFrame basics and pandas data structures | — |
| 4 | Mon Sep 14 | 02 Data manipulation I *(cont.)* | | **In-class 02** |
| 5 | Wed Sep 16 | **03 Data manipulation II:** pandas | Chen, on grouping and on tidy data; McKinney, on data cleaning, on joining and reshaping, and on aggregation and group operations | — |
| 6 | Mon Sep 21 | 03 Data manipulation II *(cont.)* | | **In-class 03** · **HW 1** |
| 7 | Wed Sep 23 | **04 Data analysis I:** univariate stats, visualization, seaborn, intro to correlation | McKinney, on plotting and visualization | — |
| 8 | Mon Sep 28 | 04 Data analysis I *(cont.)* | | **In-class 04** |
| 9 | Wed Sep 30 | **05 Data analysis II:** ANOVA, t-test, linear models | Bruce, Bruce & Gedeck, on statistical experiments and significance testing, and on regression and prediction | — |
| 10 | Mon Oct 5 | 05 Data analysis II *(cont.)* | | **In-class 05** · **HW 2** |
| 11 | Wed Oct 7 | **06 Data analysis III:** categorical data (contingency tables, chi-square, mosaic plots); text processing and regular expressions | Bruce, Bruce & Gedeck, the chi-square section of the significance testing chapter; and the [Python regex HOWTO](https://docs.python.org/3/howto/regex.html) | — |
| 12 | Mon Oct 12 | 06 Data analysis III *(cont.)* | | **In-class 06** · **HW 3** |
| 13 | Wed Oct 14 | **Project Studio** — work session, teaching team circulating | | **Project milestone 1** (data description + manipulation) |
| — | *Mon Oct 19* | *Fall Study Break — no class* | | |
| 14 | Wed Oct 21 | **07 Natural language processing** (nltk) | Jurafsky & Martin, [*Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/), chapter 1, which is free online; Grus, on natural language processing *(optional)* | — |
| 15 | Mon Oct 26 | 07 NLP *(cont.)* | | **In-class 07** · **HW 4** |
| 16 | Wed Oct 28 | **08 Machine learning:** introduction & Classification I | VanderPlas, on machine learning; Géron, on the machine learning landscape and the end-to-end project; Grus, on machine learning and on k-nearest neighbors | — |
| 17 | Mon Nov 2 | 08 Intro to ML *(cont.)* | | **In-class 08** |
| 18 | Wed Nov 4 | **09 Machine learning:** Classification II | Géron, on training models, decision trees, and ensemble learning; Grus, on decision trees and logistic regression | — |
| 19 | Mon Nov 9 | 09 Classification II *(cont.)* | | **In-class 09** · **HW 5** |
| 20 | Wed Nov 11 | **10 Unsupervised learning:** PCA & k-means clustering | Géron, on dimensionality reduction and on unsupervised learning techniques; Grus, on clustering | — |
| 21 | Mon Nov 16 | 10 Unsupervised learning *(cont.)* | | **In-class 10** · **Project milestone 2** (analysis) |
| 22 | Wed Nov 18 | **11 End-to-end ML pipeline** (Titanic, or another competitive framework) — *single session* | Géron, on the end-to-end machine learning project, which is worth a second read now that you have the pieces | **In-class 11** |
| 23 | Mon Nov 23 | **12 Scaling up I:** Polars — *single session* | The [Polars user guide](https://docs.pola.rs/), the getting-started and concepts sections | **In-class 12** · **HW 6** · **Peer review** |
| — | *Wed Nov 25* | *Thanksgiving — no class* | | |
| 24 | Mon Nov 30 | **13 Scaling up II:** PySpark — *single session* | Chambers & Zaharia, *Spark: The Definitive Guide*, the overview and structured API chapters | **In-class 13** |
| 25 | Wed Dec 2 | **14 Generative AI as a data tool** — *single session* | Posted on Canvas, since this material dates faster than a syllabus can | **In-class 14** · **Project milestone 3** (machine learning) |
| 26 | Mon Dec 7 | **Project presentations I** | | |
| 27 | Wed Dec 9 | **Project presentations II** | | **Project presentation** |
| — | Fri Dec 11 | *No class* | | **Project final report** |

---

## Software and Setup

**This course uses [marimo](https://marimo.io) rather than Jupyter.** A marimo
notebook is a plain Python file that re-runs the affected cells by itself whenever
you change something, and there are a couple of consequences you'll notice fairly
quickly.

The first is that there's no hidden state to trip over, so you can't produce a
result that depends on the order in which you happened to run the cells, which is
probably the most common reason notebook results turn out not to be reproducible.

The second is that a variable may only be defined in one cell. This is the rule that
catches most people out to begin with, and session 1 covers what to do about it.

There's a useful side effect too, which is that your notebook is real Python, so it
diffs cleanly in git and `pytest` will run it directly. That last part is how the
in-class exercises manage to check themselves while you type.

### Getting started

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), and you can
then open any course notebook with a single command:

```bash
uvx marimo edit --sandbox SI_618_01_Introduction.py
```

That downloads marimo, builds a throwaway environment containing the packages the
notebook says it needs, and opens it, so there shouldn't be a virtual environment
for you to create or to accidentally break.

If you can't install anything locally, every notebook is also published to
[molab](https://molab.marimo.io/), which runs marimo in a browser tab without
installing anything. Signing in is required before you can run a notebook, and a
Google account will do it. The links are posted on Canvas. It's worth reaching for if
your laptop is fighting you on day one, and sorting out the local setup afterwards.

There is a step-by-step version of all this, including a troubleshooting table, in the
setup document posted on Canvas. The same file lives in the course repository as
`docs/setup.md` if you'd rather read it there.

### Course materials

All in-class notebooks live in the public course repository:
<https://github.com/cteplovs/si618-fa2026-student>

Homework **specifications are markdown documents** in that repository rather than
notebooks, and you write your answers in a marimo notebook, starting from the
`starter.py` that comes with each assignment.

### Submission format

Every deliverable in this course is submitted as two files, the marimo notebook
named `SI618_<assignment>_<uniqname>.py`, and an HTML export of it named
`SI618_<assignment>_<uniqname>.html`, which you produce with:

```bash
uvx marimo export html --sandbox SI618_01_uniqname.py -o SI618_01_uniqname.html
```

Do keep `--sandbox` on that command, because without it the export will report
success while quietly producing an HTML file in which every cell has failed.

Both files go to Canvas, and we don't accept `.ipynb` files anywhere in this course.

---

## In-class Activities

Our synchronous meetings are centered on co-constructed marimo notebooks, although
we will use alternative materials (including paper!) for some classes. I create
these materials to support learning by providing hands-on exercises that let you
practice applying the techniques we are learning.

Most topics span two sessions and a single notebook. You open the notebook on
Wednesday, we stop partway through at a marked session boundary, and you finish it
the following Monday. Your deliverable is submitted at the end of the second session
for each topic, which after the first week always means Monday, so there's nothing
to hand in at the end of a first session. The four single-session topics late in the
term are submitted at the end of that one session instead.

These activities aren't meant to be homework assignments, which are covered in the
next section. You'll be working in groups during some of the hands-on segments, but
you are still asked to submit your own work for credit.

Each notebook contains self-checking exercises marked 🚀, which run as you type and
will generally tell you whether your answer is right before you submit it. They're
there to be used.

---

## Homework Assignments

There are six homework assignments this term, each worth 100 points.

Homework is typically released after class and due the following week before class,
and the [Late Policy](#late-policy) below covers what happens if you can't make the
deadline. As much as possible, the assignments are based on real-world datasets and
focused on realistic problems.

Each assignment is a folder in the course repository, containing a `README.md` with
the specification, laid out part by part with the points marked; a `RUBRIC.md`,
which is the rubric we grade against, published in advance so that you can see it
before you start; and a `starter.py`, which is a marimo notebook with the sections
stubbed out for you.

Please make sure you read the section below on Academic Integrity. If you copy
someone else's homework solution completely, or almost completely (and/or fail to
acknowledge your source), then this will be considered cheating, and I'll refer
your case to the academic advising office for disciplinary action. I have long
experience and a particular talent for catching people, so just don't do it.

Please contact the instructor if you have any uncertainty or questions about this
policy.

---

## Final Project

The goal of the final project is to further apply what you've learned in class to
real-world datasets. This is a group project, with each group consisting of either
2 or 3 members. Solo projects are not permitted. If you wish to have more than
three people on your team you will be required to split into multiple teams, each
with only 2 or 3 people in it.

The project is worth 800 points, distributed across five deliverables:

| Deliverable | Due | Points |
|---|---|---|
| Milestone 1: data description & manipulation | Wed Oct 14 | 200 |
| Milestone 2: analysis | Mon Nov 16 | 200 |
| Peer review of two other groups' analyses | Mon Nov 23 | 50 |
| Milestone 3: machine learning | Wed Dec 2 | 200 |
| Presentation | Dec 7 / Dec 9 | 150 |
| **Total** | | **800** |

A few things are new this term, and the smaller class is what makes them possible.

The **Project Studio** on Wednesday October 14 is a full session given over to
project work, with the teaching team circulating, and Milestone 1 is due at the end
of it. It sits immediately before Fall Study Break, which is deliberate.

There's also a round of **structured peer review**. After Milestone 2, each group
reviews two other groups' analyses against a rubric published in advance, with the
reviews submitted on Canvas and counting toward the project grade. You may well
learn as much from reading two other analyses as from writing your own.

Finally, there are **live presentations** on December 7 and 9, where every group
presents to the class for roughly seven minutes, spread across the two final
sessions.

The final report is due **Friday, December 11**. Details on the final project will
be available as we move through the course.

---

## Attendance

Attendance and participation during regularly scheduled classes is mandatory.
Repeatedly missing class or failing to participate will likely lead to a failing
grade.

Note that the course now meets twice a week. Missing one session means missing half
of a topic, and the notebook you are asked to submit on Monday begins on Wednesday.
If you have to miss a session, get the notebook from the repository and work
through the first half before the next meeting.

## Readings

There are readings assigned almost every week. These are intended to supplement the
face-to-face classes, and you will get much more out of class if you read them
before you attend. To encourage you to complete the readings before class, some
parts of the in-class notebooks are based on the readings.

---

## Grading

This course uses a points system to determine your final grade. Point distribution
for the different components is as follows:

| Assignment | Overall weight | Number | Points each | Total |
|---|---|---|---|---|
| In-class notebooks (two-session topics) | | 10 | 32 | 320 |
| In-class notebooks (single-session topics) | ~22% | 4 | 20 | 80 |
| Homework | ~33% | 6 | 100 | 600 |
| Project | ~44% | 5 deliverables | varies | 800 |
| — Milestone 1: data description & manipulation | ~11% | | | 200 |
| — Milestone 2: analysis | ~11% | | | 200 |
| — Peer review | ~3% | | | 50 |
| — Milestone 3: machine learning | ~11% | | | 200 |
| — Presentation | ~8% | | | 150 |
| **Total points available** | | | | **1800** |


Conversion from points to letter grades will use the following mapping:

| Grade | Points |
|---|---|
| A+ | 1780 |
| A | 1735 |
| A- | 1660 |
| B+ | 1610 |
| B | 1565 |
| B- | 1515 |
| C+ | 1470 |
| C | 1420 |
| C- | 1375 |
| D+ | 1325 |
| D | 1280 |
| D- | 1230 |

**DO NOT TRUST THE PERCENTAGE (%) SCORES IN CANVAS!** Always compare your earned
points to the table above to determine your grade (or your projected grade).

---

## Late Policy

I realize that the occasional crisis might mess up your schedule enough to require
a bit of extra time in completing a course assignment. Thus, I have instituted the
following late policy that gives you a limited number of flexible "late day"
credits.

You have **three (3)** free late days to use during SI 618. One late day equals
exactly one 24-hour period after the due date of the assignment (including
weekends). No fractional late days: they are all or nothing. Once you have used up
your late days, a **25% penalty** applies for each subsequent 24h period after the
deadline that an assignment is late. For example, if the due date is 1pm Thursday,
with no late days left, penalties would be:

- Before 1pm Friday: 25% deduction
- Before 1pm Saturday: 50% deduction
- Before 1pm Sunday: 75% deduction
- After 1pm Sunday: 100% deduction

You don't need to explain or get permission to use late days, and we will track
them for you. In cases where late days can be assigned in multiple ways (e.g. you
have only one late day left but hand in two late assignments) we will always
allocate late days in a way that maximizes your grade. Note that resubmissions
after the deadline will be counted as late submissions.

**Late days may not be applied to in-class deliverables, the project final report,
or the peer review.** In-class work is due at the end of the session; the peer
review is time-boxed because another group is waiting on it.

If you are submitting your work late and you believe you have a *valid* excuse not
to use your free late days, please complete the SI 618 FA 2026 Late Form, linked on
Canvas. Completion of the form does not guarantee that the late penalty will be
waived.


## Classroom Policy

Students are asked to attend class on time and remain through the entire class.
Please mute your IMs during class — it can be embarrassing if a member of the
teaching team is helping you and you get a very personal IM.

---

## Audio and Video Recording

### Class recordings

We will be doing audio and video recording of all sessions to enable those who
cannot attend class in person on a given day to access the content. These
recordings will not be made available publicly. Recordings of all sessions will be
available on Canvas only to students registered for this class.

As part of your participation in this course, you may be recorded. If you do not
wish to be recorded, please contact the professor during the first week of class to
discuss alternative arrangements. The camera only picks up the front of the room,
but this may require you to sit in a particular place in the room, outside the
cameras' view. As of the time of writing this syllabus, our classroom has a ceiling
mic that picks up student voices; only the instructor's microphone records audio in
the room. Further, students may not share these sessions with those not in the
class, or upload them to any other online environment (this is a violation of the
Federal Education Rights and Privacy Act (FERPA)).

### Personal recordings are prohibited except with permission

Students are prohibited from recording/distributing any class activity without
written permission from the instructor, except as necessary as part of approved
accommodations for students with disabilities. Any approved recordings may only be
used for the student's own private use.

---

## Generative AI

You may use generative AI in this course, including coding agents, and I would
rather you learned to use it well than pretended not to use it. Many of you already
use these tools professionally, and the ones who don't will be asked to within a
year of graduating. Session 25 is given over to exactly this question, where large
language models genuinely help with data work and where they confidently invent
things, so it seemed odd to spend a session on the topic while forbidding the tool.

Let me give the reasoning rather than just the rule, because the reasoning is what
tells you where the line sits when a specific situation isn't covered here.

**In-class notebooks.** Each notebook carries self-checking exercises marked 🚀,
which go green when your answer is right. An agent can turn them all green in about
forty seconds. It is worth being clear that those tests exist to give *you* feedback
while you work, not to satisfy a grader, and that turning them green without knowing
why is possible and entirely pointless. The in-class deliverable is graded on
completion rather than correctness, so there is nothing to gain by faking it and a
term's worth of fluency to lose.

**Homework.** Use AI, and say so. Each assignment's rubric is published with the
spec, and if you read one you'll notice that a substantial share of the points is
for explaining what you did and justifying why, rather than for code that runs. A
model can write the code. It cannot tell me why you chose that transformation over
the obvious alternative, because it wasn't there when you looked at the data and
decided.

**The project.** This is where the reasoning matters most, and it's also where the
course is hardest to fake, for three reasons that have nothing to do with detection.
You review two other groups' analyses, which is difficult to do convincingly without
understanding your own. You present to the room in December and take questions. And
your report has to be anchored in your own analysis, meaning specific numbers from
your own notebooks, which a model that did not run that analysis cannot supply.
Prose that floats free of your actual output reads very differently from prose that
doesn't, and by December I will have read a lot of both.

**What I ask of you.** Attribute substantial AI assistance the same way you would
attribute a colleague or a Stack Overflow answer, which means a sentence saying what
you used and what it did, not a full transcript. Don't submit code you can't explain,
since being asked to walk through your own submission is a normal thing that happens
in this course and in the jobs it leads to. And keep an eye on whether the tool is
building your skill or quietly replacing it, because that distinction is invisible
in September and extremely visible in a technical interview.

I'll say plainly that most of this is unenforceable, and it isn't meant to be
otherwise. You are graduate students, and you're paying for a skill rather than for
a credential. The reason to do your own thinking is not that I'll catch you. It's
that the market rate for someone who can prompt a model is converging on zero, while
the rate for someone who can tell when the model is wrong is not.

If you find that an agent can do an entire assignment end to end with no judgement
required from you, please tell me. That means I wrote a weak assignment, and I'd
genuinely like to know.

---

## Academic Integrity and Misconduct

### Collaboration

UMSI strongly encourages collaboration while working on some assignments, such as
homework problems and interpreting reading assignments as a general practice.
Active learning is effective. Collaboration with other students in the course will
be especially valuable in summarizing the reading materials and picking out the key
concepts. You must, however, write your homework submission on your own, in your
own words, before turning it in. If you worked with someone on the homework before
writing it, you must list any and all collaborators on your written submission.
Each course and each instructor may place restrictions on collaboration for any or
all assignments. Read the instructions carefully and request clarification about
collaboration when in doubt. Collaboration is almost always forbidden for take-home
and in-class exams.

### Plagiarism

All written submissions must be your own, original work. Original work for
narrative questions is not mere paraphrasing of someone else's completed answer:
you must not share written answers with each other at all. At most, you should be
working from notes you took while participating in a study session. Largely
duplicate copies of the same assignment will receive an equal division of the total
point score from the one piece of work.

You may incorporate selected excerpts, statements, phrases and code from other
authors, but they must be clearly marked as quotations and must be attributed. If
you build on the ideas of others, you must cite their work. You may obtain copy
editing assistance, and you may discuss your ideas with others, but all substantive
writing, code, and ideas must be your own, or be explicitly attributed to another.
See the program-specific student handbooks available on the UMSI Current Students
webpage for the definition of plagiarism, resources to help you avoid it, and the
consequences for intentional or unintentional plagiarism.

---

## Accommodations for Students with Disabilities

If you think you need an accommodation for a disability, please let me know at your
earliest convenience. Some aspects of this course, the assignments, the in-class
activities, and the way we teach may be modified to facilitate your participation
and progress. As soon as you make me aware of your needs, we can work with the
Office of Services for Students with Disabilities (SSD) to help us determine
appropriate accommodations. SSD (734-763-3000; [ssd.umich.edu](https://ssd.umich.edu))
recommends students request disability-related academic accommodations via the
Accommodate system, a core electronic case management system that will assist
students, faculty, instructors, and staff in requesting, approving, and
implementing disability-related accommodations. I will treat any information that
you provide in as confidential a manner as possible.

---

## Student Mental Health and Wellbeing

Students may experience stressors that can impact both their academic experience
and their personal well-being. These may include academic pressure and challenges
associated with relationships, mental health, alcohol or other substances,
identities, finances, food insecurity, or other external stressors.

If you are experiencing concerns, seeking help is a courageous thing to do for
yourself and those who care about you. If the source of your stressors is academic,
please contact UMSI's academic success team via
[umsi.academicsuccess@umich.edu](mailto:umsi.academicsuccess@umich.edu) or me so
that we can find solutions together. For personal concerns, U-M offers the
following resources:

- **[Counseling and Psychological Services (CAPS)](https://caps.umich.edu)** —
  confidential. For mental health support, call the central office at (734)
  764-8312 or email the School of Information Embedded CAPS Psychologist, Ashley
  Evearitt, Psy.D., at [evearitt@umich.edu](mailto:evearitt@umich.edu). If you are
  in crisis, please call CAPS at 734.764.8312, or the UM Psychiatric Emergency
  Services (PES) at 734.936.5900, or 911. Directions to PES:
  <http://www.psych.med.umich.edu/contact/er.asp>
- **[Dean of Students Office](https://deanofstudents.umich.edu)** — 734-764-7420;
  provides support services to students and manages critical incidents impacting
  students and the campus community
- **[Ginsberg Center for Community Service Learning](https://ginsberg.umich.edu)** —
  734-763-3548; opportunities to engage as learners and leaders to create a better
  community and world
- **[Maize and Blue Cupboard](https://mbc.studentlife.umich.edu)** — provides food,
  kitchen and cooking supplies, personal and household items, and support services
  for students experiencing food insecurity
- **[Multi-ethnic Student Affairs (MESA)](https://mesa.umich.edu)** — 734-763-9044;
  diversity and social justice through the lens of race and ethnicity
- **[Office of Student Conflict Resolution](https://oscr.umich.edu)** — 734-936-6308;
  offers multiple pathways for resolving conflict
- **[Office of the Ombuds](https://ombuds.umich.edu)** — 734-763-3545; students can
  raise questions and concerns about the functioning of the university
- **[Services for Students with Disabilities (SSD)](https://ssd.umich.edu)** —
  734-763-3000; accommodations and access to students with disabilities
- **[Sexual Assault Prevention and Awareness Center (SAPAC)](https://sapac.umich.edu)** —
  confidential; 734-764-7771 or 24-hour crisis line 734-936-3333; addresses sexual
  assault, intimate partner violence, sexual harassment, and stalking
- **[Spectrum Center](https://spectrumcenter.umich.edu)** — 734-763-4186; support
  services for LGBTQ+ students
- **[Trotter Multicultural Center](https://trotter.umich.edu)** — 734-763-3670;
  intercultural engagement and inclusive leadership education initiatives
- **[University Health Service (UHS)](https://uhs.umich.edu)** — 734-764-8320;
  clinical services include nurse advice by phone, day or night
- **[Well-being for U-M Students](https://wellbeing.studentlife.umich.edu)** —
  searchable list of many more campus resources
- **[Wolverine Wellness](https://uhs.umich.edu/wolverine-wellness)** — confidential;
  734-763-1320; provides Wellness Coaching and much more
