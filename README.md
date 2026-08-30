# SI 618: Data Manipulation & Analysis

**Fall 2026, University of Michigan School of Information**

Mondays & Wednesdays, 80 minutes, 27 sessions running from August 31 to December 9, 2026.

---

## This course uses marimo rather than Jupyter

All the notebooks here are [marimo](https://marimo.io) notebooks, which are plain Python
`.py` files that happen to run as reactive notebooks. We don't use `.ipynb` files, and we
don't accept them for submissions.

The reason is that marimo notebooks don't carry hidden state around. When you change a
cell, everything depending on it re-runs by itself, so "it was working until I restarted
the kernel" largely stops happening. They're also readable Python files, which means they
diff and review much like ordinary code does.

## Getting started

You'll need [`uv`](https://docs.astral.sh/uv/), which on macOS or Linux you can install
with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then open any notebook, and `uv` will read the dependency header inside the file and
build an isolated environment to match:

```bash
uvx marimo edit --sandbox inclass/SI_618_01_Introduction.py
```

That's more or less the whole install, with no `pip install` to run, no virtualenv to
activate, and no `requirements.txt` for you to edit.

There's a fuller walkthrough, including Windows and a troubleshooting table, in
[docs/setup.md](docs/setup.md).

### If you can't install anything locally

Every notebook also runs in the browser via molab, with nothing installed. You'll need
to sign in, which you can do with your Google or GitHub account, and the free tier is
all this course needs. Links are posted on Canvas alongside each session.

## Repository layout

```
docs/        the syllabus, and setup.md if your laptop isn't set up yet
inclass/     one marimo notebook per topic, usually taught across two sessions
homework/    hwNN/README.md (the spec), RUBRIC.md, and starter.py
project/     final project brief, milestones, and the peer-review rubric
data/        nothing committed here, see data/README.md for why
```

## Submitting work

Every deliverable goes to Canvas as two files, the marimo notebook named
`SI618_<assignment>_<uniqname>.py`, and an HTML export of it produced with:

```bash
uvx marimo export html --sandbox <notebook>.py -o <notebook>.html
```

Please keep `--sandbox` on all of these commands. Without it, marimo runs your notebook
in a bare environment with neither pandas nor pytest, and will then report the export as
successful even though the cells inside it failed and the exercise tests never ran. The
resulting HTML looks broken to whoever grades it, and nothing warns you at the time.

Before submitting, it's worth checking that your work runs cleanly from a cold start:

```bash
uvx marimo run --sandbox <notebook>.py
```

The exercise tests run live inside the notebook, so checking your answers mostly amounts
to confirming that every 🚀 exercise is showing green before you export.

## Contact

Lead instructor is Dr. Chris Teplovs, at cteplovs@umich.edu, and it helps to put
`[SI 618]` in the subject line. Course questions are usually best raised in class, at
office hours, or on Slack, as described in the syllabus.

---

© 2026 University of Michigan School of Information. Course materials are for enrolled
students, and shouldn't be redistributed.
