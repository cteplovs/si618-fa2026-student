# Setting up your laptop

This takes about ten minutes, most of which is waiting for things to download. We will
do it together in our first session, so there is no need to have it working beforehand,
though you are welcome to try if you would rather arrive with it sorted.

If it goes sideways, please don't spend your evening fighting it. Read the last two
sections, and bring the error message to class.

## You probably don't need to install Python

This is the part that trips people up, so it's worth saying plainly: there is no need to
go to python.org. You are installing one thing, called `uv`, and `uv` will fetch a
suitable version of Python for you, tucked away somewhere that shouldn't disturb anything
else on your machine.

If you already have Python from a previous course, or Anaconda, or Homebrew's Python,
that's fine, and you can leave it alone. It won't be used here, and it shouldn't conflict.

You also won't need Jupyter, JupyterLab, or the VS Code Jupyter extension. This course
uses [marimo](https://marimo.io), and we don't use or accept `.ipynb` files anywhere in
it.

---

## Step 1: install uv

Open a terminal. On macOS that's Terminal, which you can find with ⌘-space and typing
"terminal"; on Windows it's PowerShell, from the Start menu, rather than Command Prompt.

If you have written Python before but never used a terminal directly, don't let it put
you off. A terminal is just a window where you type a command and press Enter, and this
course needs about four of them in total, all of which are written out for you here.

Paste in the line for your machine, and press Enter.

**macOS / Linux**

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Now close that terminal window and open a fresh one, because the installer adds `uv` to
your PATH and a terminal that was already open hasn't heard the news. Skipping this is
far and away the most common reason step 2 appears to fail.

## Step 2: check that it worked

```
uv --version
```

You should get back a version number, something along the lines of `uv 0.9.x`, and any
version number at all is good enough for our purposes.

If you get `command not found` or `not recognized` instead, have a look at the
troubleshooting section below.

## Step 3: get the course files

The course repository is public, and lives at:

<https://github.com/cteplovs/si618-fa2026-student>

Click the green **Code** button, choose **Download ZIP**, and unzip it somewhere you'll
be able to find again. Your Desktop is a perfectly good answer, though you may want to
avoid anything inside a synced folder that likes to tidy up after you.

Then move your terminal into that folder:

```
cd Desktop/si618-fa2026-student-main
```

The same line works in PowerShell on Windows. If you unzipped somewhere other than the
Desktop, a reliable trick is to type `cd ` (with the space) and then drag the folder from
Finder or File Explorer onto the terminal window, which fills in the path for you.

If you're comfortable with git, you're welcome to clone the same URL instead, and you'll
then be able to pick up updates with `git pull` rather than downloading again. If that
sentence meant nothing to you, the ZIP is not a lesser option, it's the same files.

Everything in this course happens in marimo, which opens in your browser, so once you're
in the folder there's nothing else to set up and no editor to configure.

## Step 4: open the first notebook

```
uvx marimo edit --sandbox inclass/SI_618_01_Introduction.py
```

The first time you run this it will likely take a minute or two, because it's downloading
Python along with marimo and the packages this particular notebook needs. It isn't stuck,
and every run after this one should be quick.

A browser tab will open with the notebook in it, and that tab is where you work. There's
nothing else to install, and no extension to add to anything.

To stop it, go back to the terminal and press `Ctrl-C`.

### What that command is actually doing

This is worth thirty seconds, because it explains most of how the course works.

`uvx` runs a tool without installing it permanently, and `--sandbox` tells marimo to read
the list of dependencies written at the top of the notebook file itself, then build a
private environment matching it.

So each notebook carries its own requirements around with it. There's no shared
environment to corrupt, no `pip install` to run, and no `requirements.txt` for you to
edit. When you open a notebook in week 9 that happens to need scikit-learn, it should
simply work, without you having installed anything first.

It also means you can run any single `.py` file on its own, including your own submitted
work, months from now.

---

## Step 5: notice that the exercises check themselves

Scroll down in the notebook you just opened. The exercises are marked 🚀, and underneath
each one there's a test that runs by itself as you type. At the moment they're all
failing, with messages along the lines of *"Assign your result to `answer_1`."*

That's exactly right, and they're supposed to fail until you've done the work. As you
fill in an answer the matching test turns green straight away, which is your feedback
loop for the rest of the term. You'll generally know whether an exercise is right before
you submit it, rather than a week later.

If you can't see any test results at all, do tell us, because something is misconfigured
and that's our problem rather than yours.

---

## If your laptop is fighting you

Nobody is going to be locked out of class because of a laptop. There's
**[molab](https://molab.marimo.io)**, marimo's free cloud sandbox, which runs the same
notebooks in a browser tab with nothing installed at all. You will need to sign in
before you can run anything, and signing in with your Google account is the quickest
route. It's a perfectly legitimate way to take this course, and links are posted on
Canvas.

One thing to know if you work this way: molab runs the notebook on a temporary server
and does not save your work automatically. Download your `.py` file before you close
the tab, or fork the notebook into your own molab workspace, which does save.

Do bring the failure along to class anyway. We can usually either fix it or decide it
isn't worth fixing, in about ten minutes, which beats you banging your head against the
machine for an hour.

## Troubleshooting

| What you see | What to do |
|---|---|
| `uv: command not found` / `'uv' is not recognized` | Close the terminal completely, and open a new one. If that doesn't do it, restarting the laptop genuinely does help here. |
| Windows: `running scripts is disabled on this system` | The install command was probably modified somewhere along the way. Try the `-ExecutionPolicy ByPass` version exactly as written above. |
| `No such file or directory: inclass/SI_618_01_Introduction.py` | Your terminal probably isn't in the course folder. Run `ls` on macOS, or `dir` on Windows, and you should see `inclass`, `homework`, and `docs` listed. If you don't, `cd` into the unzipped folder, remembering that it's usually called `si618-fa2026-student-main`, with the `-main` on the end. |
| The install command hangs, or times out | Often a VPN or a restricted network. Worth trying again on an ordinary connection. |
| Your laptop is managed by an employer and blocks installs | Probably not worth fighting, so use molab. |
| `uvx` fails with a long red wall of text | Copy the **last five lines** and bring them to class, or post them on Canvas. The first forty lines are almost never the useful part. |
| The browser tab never opens | Look in the terminal for a `http://localhost:...` address, and paste that into a browser yourself. |
| The notebook opens, but the exercise tests never appear | Post on Canvas with your operating system and the output of `uv --version`. This one is on us. |
| Something else entirely | Post it on Canvas with the exact error text and your operating system, since it's a fair bet somebody else has it too. |

## What "done" looks like

You ran `uvx marimo edit --sandbox inclass/SI_618_01_Introduction.py`, a browser tab
opened, and you can see the notebook with its exercise tests showing red. That's the
whole bar, and there's nothing to submit.

---

## Later on: submitting work

You don't need this yet, and it's here mostly so you know where to find it.

Every deliverable is submitted to Canvas as two files, the notebook itself and an HTML
export of it.

```
uvx marimo export html --sandbox SI618_01_uniqname.py -o SI618_01_uniqname.html
```

Rename your copy of the notebook to `SI618_<assignment>_<uniqname>.py` before you export
it, so that both files carry your uniqname.

Do keep `--sandbox` on that command. Without it, marimo runs your notebook in an empty
environment with no pandas, and then cheerfully announces "Export was successful" while
handing you an HTML file in which every cell has failed. There's no warning, and the
first person to notice tends to be whoever grades it.
