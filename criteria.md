# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. _"The model is accurate"_ is an
opinion. _"Every label has an F1 of at least 0.60 on the held-out set"_ is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — _"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"_. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area                  | A question it could answer                                            |
| --------------------- | --------------------------------------------------------------------- |
| Overall accuracy      | How often does it need to be right to be worth using?                 |
| Per-label performance | Is one label allowed to be much worse than the others?                |
| Balance               | How lopsided can your label counts get before it's a problem?         |
| Consistency           | If someone else labelled the same posts, how often should you agree?  |
| Confidence            | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Accuracy on the held-out test set is at least 0.65 on every one of the three seeds.

**Why this target:**
With about 200 comments, the test split is roughly 30, so 0.65 means classifying
about 20 of 30 correctly. That is well above the 33% a random guesser gets across
three labels, and above the roughly 45% a model would get by always guessing my
most common label. I didn't go higher because one comment moves accuracy by about
3 points on a test set this small, and the target has to hold on all three seeds,
not just on average.

---

## 2. Per-label F1

On every one of the three seeds, `hot_take` and `reaction` each have an F1 of at
least 0.60, and `analysis` has an F1 of at least 0.50.

**Why this target:**
From reading r/nba, `analysis` comments mostly appeared in game threads and were
rare in drama and meme threads, so I expect it to be my smallest label. That means
fewer examples to learn from and only a handful in the test split, where one wrong
answer swings its F1 more than for the larger labels. I set its floor 0.10 lower
for that reason. I didn't go below 0.50, because under that the model would be
missing as many real `analysis` comments as it catches, which means it hasn't
learned the label. The other two get 0.60 because they should be easier to learn
and will have more test examples.

---

## 3. Label balance

In labels.csv, no label is more than 50% of the rows, and no label is less than
20% of the rows.

**Why this target:**
The assignment caps any label at 70%, but at 70% a model that always guesses that
label would beat my 65% accuracy target without learning anything. At 50%, always
guessing the biggest label still falls 15 points short of 0.65, so passing
criterion 1 means something. The 20% floor gives my smallest label about 40 of 200
comments, or roughly 6 in a 30-comment test split. That is still small, but below
it the label's F1 in criterion 2 would rest on 4 or 5 comments and swing too much
between seeds to tell me anything.

---

## 4. Agreement with staff labels

When I label the 30 staff posts using the staff taxonomy, I match the staff label
on at least 24 of 30 (80%).

**Why this target:**
This is the only check on my labeling that doesn't involve the model. I'll be
applying definitions someone else wrote, which is harder than applying my own, so
perfect agreement isn't realistic. 80% sits inside the 70 to 85% range that human
labelers commonly reach on judgment tasks like this, so it asks me to apply their
rules carefully without assuming I'll read their minds. Each disagreement costs
about 3.3 points out of 30, so 24 leaves room for six honest judgment calls but
not for careless labeling.

---

## 5. Beat the zero-shot baseline

On every one of the three seeds, the trained model's accuracy on the held-out
test posts is at least 10 percentage points higher than `baseline.py`'s accuracy
on the same posts.

**Why this target:**
The baseline is a general model that only gets my label definitions, with no
training. If my fine-tuned model can't clearly beat it, training on 200 labeled
comments added nothing over describing the labels. I picked 10 points rather than
5 because on a 30-comment test set each comment is worth about 3.3 points, so 5
would be under two comments, which is close to normal seed-to-seed noise. 10
points means about three more comments right, which is still small but harder to
reach by luck. Both models are scored on the same held-out posts so the
comparison is fair.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
