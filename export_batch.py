"""Write the next unlabeled comments, in label.py's order, to to_prelabel.csv."""
import csv
import os
import random
import sys

count = int(sys.argv[1]) if len(sys.argv) > 1 else 280

with open("raw_posts.csv", encoding="utf-8") as f:
    pool = list(csv.DictReader(f))
random.Random(42).shuffle(pool)  # same order as label.py

done = set()
if os.path.exists("labels.csv"):
    with open("labels.csv", encoding="utf-8") as f:
        done |= {r["text"] for r in csv.DictReader(f)}
if os.path.exists("skipped.txt"):
    with open("skipped.txt", encoding="utf-8") as f:
        done |= set(f.read().splitlines())

batch = [r for r in pool if r["text"] not in done][:count]
with open("to_prelabel.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["text", "suggested", "reason"])
    w.writeheader()
    for r in batch:
        w.writerow({"text": r["text"], "suggested": "", "reason": ""})
print(f"wrote {len(batch)} comments to to_prelabel.csv")