"""Label comments one at a time. Usage: python label.py 20 cold"""
import csv
import os
import random
import sys

KEYS = {"a": "analysis", "h": "hot_take", "r": "reaction"}
target = int(sys.argv[1]) if len(sys.argv) > 1 else 20
note = sys.argv[2] if len(sys.argv) > 2 else ""

with open("raw_posts.csv", encoding="utf-8") as f:
    pool = list(csv.DictReader(f))
random.Random(42).shuffle(pool)  # fixed order, mixes the threads together

done = set()
if os.path.exists("labels.csv"):
    with open("labels.csv", encoding="utf-8") as f:
        done |= {r["text"] for r in csv.DictReader(f)}
if os.path.exists("skipped.txt"):
    with open("skipped.txt", encoding="utf-8") as f:
        done |= set(f.read().splitlines())

new_file = not os.path.exists("labels.csv")
out = open("labels.csv", "a", newline="", encoding="utf-8")
writer = csv.DictWriter(out, fieldnames=["text", "label", "note"])
if new_file:
    writer.writeheader()

labeled = 0
for row in pool:
    if row["text"] in done:
        continue
    print("\n" + "-" * 70 + f"\n[{labeled}/{target}]  {row['text']}\n")
    choice = ""
    while choice not in ("a", "h", "r", "s", "q"):
        choice = input("a=analysis  h=hot_take  r=reaction  s=skip (off-topic)  q=quit > ").strip().lower()
    if choice == "q":
        break
    if choice == "s":
        with open("skipped.txt", "a", encoding="utf-8") as f:
            f.write(row["text"] + "\n")
        continue
    writer.writerow({"text": row["text"], "label": KEYS[choice], "note": note})
    out.flush()
    labeled += 1
    if labeled >= target:
        break

out.close()
print(f"\nLabeled {labeled} this session.")