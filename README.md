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

Both models scored on the same 36 held-out comments from `test_split.csv` (seed 42). The baseline is `facebook/bart-large-mnli` run zero-shot with my definitions from `label_definitions.txt`.

| Measure          | Baseline | Trained | Difference |
| ---------------- | -------- | ------- | ---------- |
| Overall accuracy | 0.278    | 0.472   | +0.194     |
| Macro F1         | 0.224    | 0.265   | +0.040     |
| F1 — `analysis`  | 0.400    | 0.000   | -0.400     |
| F1 — `hot_take`  | 0.273    | 0.627   | +0.355     |
| F1 — `reaction`  | 0.000    | 0.167   | +0.167     |

**What I predicted before I looked:** I expected the trained model to beat the baseline on `hot_take` and `reaction`, because it learned from labeled examples and the baseline got no `reaction` right at all, and to lose on `analysis`, because the baseline's best label was `analysis`, where my definition names concrete things like stats and rankings that a general model can spot from wording alone. This isn't a blind prediction: I had already seen my trained model's test numbers when the notebook printed them at the end of unit 5. The prediction held on all three labels.

**What the gap actually means:** The trained model's accuracy is 19.4 points higher, but its macro F1 is only 0.04 higher, and that difference is the story. Accuracy rewards the biggest label, and `hot_take` is 16 of the 36 test comments. The trained model gains nearly all of its edge by predicting `hot_take` far more often, which matches what I saw during training, when validation accuracy stayed at 0.472 for all three epochs. It learned nothing about `analysis`, the one label the untrained model could already partly recognize from wording alone. It beats the baseline on paper mostly by leaning on the common label, not by learning my distinctions. The baseline is also slow: a few seconds per comment, against a fraction of a second for the fine-tuned model.

---

## Run Log — Before

Trained on CPU (`torch 2.14.1+cpu`), default settings, seeds 42, 7 and 2024. From `results_three_seeds_before.json`.

| Criterion                 | Target                                                          | Seed 42                  | Seed 7                   | Seed 2024                | Verdict |
| ------------------------- | --------------------------------------------------------------- | ------------------------ | ------------------------ | ------------------------ | ------- |
| 1. Overall accuracy       | ≥ 0.65 every seed                                               | 0.472                    | 0.444                    | 0.500                    | MISSED  |
| 2. Per-label F1           | `hot_take` and `reaction` ≥ 0.60, `analysis` ≥ 0.50, every seed | a 0.00 · h 0.63 · r 0.17 | a 0.00 · h 0.62 · r 0.00 | a 0.00 · h 0.64 · r 0.31 | MISSED  |
| 3. Label balance          | max ≤ 50%, min ≥ 20%                                            | max 44.6%, min 23.8%     | same                     | same                     | MET     |
| 4. Agreement with staff   | ≥ 24 of 30                                                      | 30 of 30                 | same                     | same                     | MET     |
| 5. Beat baseline accuracy | ≥ +10 points every seed                                         | +19.4                    | +16.7                    | +8.3                     | MISSED  |

Criterion 3 is a property of `labels.csv`, measured before training, so it is the same on every seed. Criterion 4 is measured once, against the staff set.

**The spread across seeds:**

| Measure          | Seed 42 | Seed 7 | Seed 2024 | Spread |
| ---------------- | ------- | ------ | --------- | ------ |
| Overall accuracy | 0.472   | 0.444  | 0.500     | 0.056  |
| Macro F1         | 0.265   | 0.205  | 0.316     | 0.111  |
| F1 — `analysis`  | 0.000   | 0.000  | 0.000     | 0.000  |
| F1 — `hot_take`  | 0.627   | 0.615  | 0.640     | 0.025  |
| F1 — `reaction`  | 0.167   | 0.000  | 0.308     | 0.308  |

**The baseline on each seed's test split.** Criterion 5 is judged per seed, so I ran `baseline.py` on each seed's own 36 held-out comments, using the same stratified split the notebook uses:

| Seed | Baseline accuracy | Trained accuracy | Gap    |
| ---- | ----------------- | ---------------- | ------ |
| 42   | 0.278             | 0.472            | +0.194 |
| 7    | 0.278             | 0.444            | +0.167 |
| 2024 | 0.417             | 0.500            | +0.083 |

On seed 2024 the baseline's macro F1 (0.399) was higher than the trained model's (0.316).

### Confusion matrix

Seed 42, from section 7.

| true \ predicted | analysis | hot_take | reaction |
| ---------------- | -------- | -------- | -------- |
| **analysis**     | 0        | 9        | 0        |
| **hot_take**     | 0        | 16       | 0        |
| **reaction**     | 0        | 10       | 1        |

**My biggest off-diagonal number, and what it means:** 10 real `reaction` comments were called `hot_take`, and none went the other way. But that pair isn't the real story: the model called 35 of 36 comments `hot_take`, including all 9 `analysis` comments. It didn't learn a confused boundary between two labels; it never learned to separate any of them and fell back on the most common label.

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

**Agreement rate:** 30 / 30 = 100%

I labeled all 30 posts in `data/staff_posts.csv` under the staff taxonomy in `data/staff_taxonomy.md` using `staff_label.py`, committed `my_staff_labels.csv`, and only then got `staff_labels.csv`. `agreement.py` found no disagreements.

**Disagreements**

None. Since there is nothing to adjudicate, here is the evidence on whether the set was easy or the rule was applied tightly. Staff marked 7 of the 30 posts as borderline, each with a note beginning "HARD", and I matched staff on all 7. Three of them sit exactly on boundaries where my own unit 5 taxonomy would have pulled me the other way:

**1.**

> _The post:_ "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> _Staff said / I said:_ `hot_take` / `hot_take`
>
> _My call, and why:_ Staff rule 1 asks whether the fact is load-bearing. Here "so obviously" does the work and the 3% is decoration on a conclusion already reached. Under my own unit 5 rule, any checkable fact backing a position is `analysis`, so this post is where the two taxonomies disagree most, and I applied theirs.
>
> _Which pile:_ none, agreed.

**2.**

> _The post:_ "Third DNF this year. I don't really want to talk about it, just wanted to put it somewhere."
>
> _Staff said / I said:_ `reaction` / `reaction`
>
> _My call, and why:_ "Third this year" is countable, but nothing is argued from it; the writer is reporting their own state. This is the same idea as my own third rule, that a number only makes a post `analysis` if it backs a position.
>
> _Which pile:_ none, agreed.

**3.**

> _The post:_ "Nobody actually enjoys the long run. They enjoy having done it, which is a completely different thing, and the sport would be more honest if it said so."
>
> _Staff said / I said:_ `hot_take` / `hot_take`
>
> _My call, and why:_ It reads reflective, almost like a `reaction`, but staff rule 2 asks whether it reports the writer's experience or makes a general claim. It claims something about everyone, so it's a `hot_take`.
>
> _Which pile:_ none, agreed.

**What the pattern in my disagreements tells me:** With no disagreements, the useful finding is about consistency. Matching staff on all 7 of their hard cases is evidence that I can apply a written boundary rule the way its authors intended, including on the post built to separate "a fact that carries the argument" from "a fact used as decoration." Two caveats. First, the staff file was ordered in blocks of ten per label, which may have made the set easier than a shuffled one. Second, this measures my own labeling, which covers the 20 cold rows in `labels.csv`; the other 220 were labeled by Claude Code under my rules, so this result doesn't vouch for those directly.

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
