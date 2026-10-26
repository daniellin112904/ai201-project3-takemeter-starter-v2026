# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts comments from r/nba, the main NBA subreddit, into three kinds of basketball discussion: `analysis`, which backs a position with a specific, checkable fact; `hot_take`, which takes a confident position with no fact behind it; and `reaction`, which expresses a feeling about something that just happened. It is a DistilBERT model fine-tuned on 240 comments I collected and labeled from four r/nba threads. Comments that aren't about basketball are outside its scope.

### What I noticed reading r/nba (Milestone 1)

I read comments from three threads before designing anything: a drama thread about Jaylen Brown and Jayson Tatum, a Sixers vs. Knicks post-game thread, and a thread reacting to an Onion headline about Ben Simmons. Four distinctions showed up in the text:

1. **Some comments cite a specific, checkable fact.** "And shot 27.5% from 3 because it took them 3 quarters to start hitting some 3s." "That stat at the end of they had 28 assists to their 35 made field goals." Most comments don't.
2. **Some make a confident claim with nothing behind it.** "This guy is insufferable truly." "anyone who thinks philly isn't a top 5 team in the league is delusional."
3. **Some are an immediate emotional reaction** to something that just happened, with no claim at all. "I'm crying lmao he used the Embiid troll response." "Maxey is fucking insane."
4. **A large share aren't about basketball.** A long thread on what lamb costs at restaurants, a list of favorite Onion headlines, the Sixers song typed out one word per comment.

---

## Label Taxonomy

My dataset is **comments about basketball**. Comments that aren't about basketball at all (a tangent about what lamb costs at restaurants, favorite Onion headlines, song lyrics typed one word per comment) are out of scope and were left out rather than forced into a label.

### `analysis`

**Definition:** Backs up a position with a specific, checkable fact: a stat, a ranking, a date, a contract figure, or a quote.

**Example 1:** "And shot 27.5% from 3 because it took them 3 quarters to start hitting some 3s. Thats definitely going to go up and this team will look unstoppable when it does. Embiid takes a couple weeks to get into form too."

**Example 2:** "James and Embiid played 34 and 33 minutes respectively. That's absolutely fine considering we were missing two players who definitely get minutes."

### `hot_take`

**Definition:** Takes a confident position someone could argue against, such as a ranking, a prediction, or a judgment of a player or team, with no specific fact offered as support.

**Example 1:** "anyone who thinks philly isn't a top 5 team in the league is delusional"

**Example 2:** "Jaylen is a child compared to Tatum lol Boston kept the right one…"

### `reaction`

**Definition:** Expresses an immediate feeling about something that just happened, without defending a position, even if it mentions a stat in passing.

**Example 1:** "Maxey is fucking insane"

**Example 2:** "I'm crying lmao he used the “Embiid troll” response"

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`.

The comment that showed me the boundary: "White was literally the least efficient non rookie in the league last year, that report was so disresepctful." It cites a checkable claim, but the tone is heated and the main point is that a report was disrespectful.

**The decision rule I used every time:** If a comment supports its point with a specific, checkable fact, it's `analysis`, even if the tone is heated or dismissive. Whether the fact is actually correct doesn't matter: I label what the comment offers as support, not whether it's true. A reply in that same thread said "You're making this up," and the White comment is still `analysis`, because the model can only see what a comment claims, not whether it checks out, and verifying every stat would make labeling slow and inconsistent.

**A second rule, for `hot_take` vs. `reaction`:** If a comment stakes out a position someone could argue against, it's a `hot_take`. If it expresses a feeling about something that just happened without defending a position, it's a `reaction`. "Maxey is fucking insane" is a `reaction`; "anyone who thinks philly isn't a top 5 team in the league is delusional" is a `hot_take`.

**A third rule, added after stress-testing:** A number only makes a comment `analysis` if it is backing up a position. A stat mentioned while celebrating, with no argument attached, is a `reaction`. "BRO DID YOU SEE THAT BLOCK. 7 blocks tonight, I'm losing my mind" is a `reaction`; "He's shooting 38% from the field this month, that's just not good enough for a max player" is `analysis`.

---

## The Dataset

**Where the posts came from:** Four public r/nba threads: a drama thread about Jaylen Brown and Jayson Tatum, a Sixers vs. Knicks post-game thread, a thread reacting to an Onion headline about Ben Simmons, and a Sixers vs. Cavaliers post-game thread. Reddit blocks unauthenticated scripts (both reddit.com and old.reddit.com returned 403), so I opened each thread in my browser and copied its comments with one line in the developer console. `build_csv.py` then joined multi-line comments, dropped deleted comments, bare links, anything under 20 or over 700 characters, and duplicates. That left 722 candidate comments.

**How I labelled them:** I labeled 20 comments cold, with no AI help, using `label.py`. They are marked `cold` in the note column. Every other row was labeled by Claude Code applying my three definitions and decision rules. Comments not about basketball, including comments about the subreddit or its users rather than the game, were left out instead of forced into a label. After the first pass, `analysis` was only 13.7% of the data, so I ran a second, targeted pass over the remaining unlabeled comments that kept only `analysis` rows, adding 28. I also removed 9 rows that had been labeled twice.

**Counts per label:**

| Label      | Count   | Share |
| ---------- | ------- | ----- |
| `hot_take` | 107     | 44.6% |
| `reaction` | 76      | 31.7% |
| `analysis` | 57      | 23.8% |
| **Total**  | **240** | 100%  |

**Three hard cases**

**1.**

> _The post:_ "White was literally the least efficient non rookie in the league last year, that report was so disresepctful."
>
> _Could have been:_ `analysis` or `hot_take`
>
> _I chose, because:_ `analysis`. It cites a checkable ranking, even though the tone is heated and the main point is that a report was disrespectful. A reply in the same thread said "You're making this up," but my rule labels what a comment offers as support, not whether it's true. This is the comment my hardest-boundary rule was built on.

**2.**

> _The post:_ "LeBron is 100% the reason they didnt get blown out by 20. Huge 3rd from him and he kept their heads in it."
>
> _Could have been:_ `analysis` or `hot_take`
>
> _I chose, because:_ I labeled it `analysis` in my cold pass, but under my own written rule it's a `hot_take`: "huge 3rd" isn't a specific stat, and "100% the reason" is a judgment. Reading my cold labels back, six of my seven `analysis` labels had reasoning but no checkable fact. I had been labeling "argued vs. unargued" instead of "fact vs. no fact." I kept all 20 cold labels unchanged as an honest record and held the written rule for everything after.

**3.**

> _The post:_ "49-19 against the Knicks. 29-11 at MSG. 20 plus years of belt"
>
> _Could have been:_ `analysis` or `reaction`
>
> _I chose, because:_ `reaction`. It's full of checkable records, but none of them backs up a position: it's a fan celebrating a rivalry win. Under my third rule, a stat only makes a comment `analysis` if it supports an argument. It was first labeled `analysis` and changed to `reaction` on a second pass for exactly that reason.

---

## The Training Run

**Base model:** `distilbert-base-uncased`, trained on CPU (`torch 2.14.1+cpu`).

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42.

**Anything I changed from the defaults, and why:** Nothing. I kept every default.

**Split sizes:**

|            | train   | val    | test   |
| ---------- | ------- | ------ | ------ |
| `analysis` | 40      | 8      | 9      |
| `hot_take` | 75      | 16     | 16     |
| `reaction` | 53      | 12     | 11     |
| **Total**  | **168** | **36** | **36** |

`analysis` has 9 examples in the test split, so a single wrong answer moves its F1 by roughly 11 points.

One thing I noticed while it trained: validation accuracy stayed at 0.472 and macro F1 at 0.260 across all three epochs, even as training loss fell from 1.07 to 0.94. With 168 training comments at batch size 16, the run is only 33 steps in total. I've left the settings as they are for this unit and will look at this properly next unit.

---

## How I Used AI

**Moment 1**

- _What I asked for:_ After writing my three definitions, I asked Claude to write eight r/nba-style posts that sit right on the boundaries between my labels, then labeled them myself.
- _What came back:_ Seven I could place cleanly. One, "BRO DID YOU SEE THAT BLOCK. 7 blocks tonight, I'm losing my mind", I hesitated on between `analysis` and `reaction`, because my rule at the time said any checkable fact made a comment `analysis`.
- _What I changed:_ I added a third rule: a stat only makes a comment `analysis` if it backs up a position. A number mentioned while celebrating is a `reaction`. I updated the `analysis` and `reaction` definitions in the README and in `label_definitions.txt` to match, before labeling anything.

**Moment 2**

- _What I asked for:_ A script to collect r/nba comments automatically.
- _What came back:_ A script using Reddit's JSON endpoints. Both reddit.com and old.reddit.com returned 403, because Reddit blocks scripts that aren't logged in.
- _What I changed:_ I switched to copying comments from my own browser with one console command, then had Claude write `build_csv.py` to clean and deduplicate them. Its first version dropped anything under 60 characters. When I worked out that "Maxey is fucking insane" was a `reaction` and only 22 characters long, I realized that cutoff was quietly removing most reactions, so I lowered it to 20. The pool went from 334 comments to 537.

**Pre-labelling disclosure:** The 20 rows marked `cold` in `labels.csv` I labeled myself with no AI help. Every other row was labeled by Claude Code applying my definitions and decision rules, including the 28 rows from the targeted `analysis` pass.

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure          | Baseline | Trained | Difference |
| ---------------- | -------- | ------- | ---------- |
| Overall accuracy |          |         |            |
| Macro F1         |          |         |            |
| F1 — `label_one` |          |         |            |
| F1 — `label_two` |          |         |            |

**What I predicted before I looked:**

<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**

<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |     |     |     |
| ---------------- | --- | --- | --- |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |

**My biggest off-diagonal number, and what it means:**

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1   |           |        |         |               |
| 2   |           |        |         |               |
| 3   |           |        |         |               |
| 4   |           |        |         |               |
| 5   |           |        |         |               |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **_ / 30 = _**%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**2.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**What the pattern in my disagreements tells me:**

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**The gap between what I meant my labels to capture and what the model
learned:**

<!-- Two sentences. Your confusion matrix is the evidence. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
