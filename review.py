"""Review AI pre-labels one at a time. Enter accepts; a/h/r/s overrides."""
import csv
import os

KEYS = {"a": "analysis", "h": "hot_take", "r": "reaction", "s": "skip"}

done = set()
if os.path.exists("labels.csv"):
    with open("labels.csv", encoding="utf-8") as f:
        done |= {r["text"] for r in csv.DictReader(f)}
if os.path.exists("skipped.txt"):
    with open("skipped.txt", encoding="utf-8") as f:
        done |= set(f.read().splitlines())

with open("to_prelabel.csv", encoding="utf-8") as f:
    batch = [r for r in csv.DictReader(f) if r["text"] not in done]

out = open("labels.csv", "a", newline="", encoding="utf-8")
writer = csv.DictWriter(out, fieldnames=["text", "label", "note"])
changed = 0

for i, row in enumerate(batch, 1):
    ai = row["suggested"]
    print("\n" + "-" * 70)
    print(f"[{i}/{len(batch)}]  {row['text']}\n")
    print(f"  AI says: {ai}   ({row['reason']})")
    choice = None
    while choice is None:
        key = input("  Enter=accept  a/h/r/s=change  q=quit > ").strip().lower()
        if key == "":
            choice = ai
        elif key in KEYS:
            choice = KEYS[key]
        elif key == "q":
            out.close()
            print(f"\nStopped. Changed {changed} so far. Run again to resume.")
            raise SystemExit
    if choice != ai:
        changed += 1
    if choice == "skip":
        with open("skipped.txt", "a", encoding="utf-8") as f:
            f.write(row["text"] + "\n")
        continue
    note = "AI pre-labeled, reviewed" if choice == ai else f"AI pre-labeled as {ai}, changed"
    writer.writerow({"text": row["text"], "label": choice, "note": note})
    out.flush()

out.close()
print(f"\nDone. You changed {changed} of the AI's labels.")