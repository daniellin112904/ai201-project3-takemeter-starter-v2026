"""Label the 30 staff posts under the STAFF taxonomy. Writes my_staff_labels.csv."""
import csv
import os

KEYS = {"a": "analysis", "h": "hot_take", "r": "reaction"}
OUT = "my_staff_labels.csv"

RULES = """
STAFF RULES (not yours):
  analysis  argument backed by a checkable fact that does WORK in the argument
  hot_take  confident claim, no support. A stat used as decoration = still hot_take
  reaction  immediate response, feeling not argument, about the WRITER'S experience
  1. analysis vs hot_take: is the fact load-bearing, or a flourish?
  2. reaction vs hot_take: about the writer (reaction) or a general claim (hot_take)?
  3. reaction vs analysis: recency doesn't outrank a load-bearing fact
  4. still tied: pick what the post spends most of its words on
"""

with open("data/staff_posts.csv", encoding="utf-8") as f:
    posts = list(csv.DictReader(f))

done = set()
if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        done = {r["text"] for r in csv.DictReader(f)}

new_file = not os.path.exists(OUT)
out = open(OUT, "a", newline="", encoding="utf-8")
writer = csv.DictWriter(out, fieldnames=["id", "text", "label"])
if new_file:
    writer.writeheader()

print(RULES)
for i, p in enumerate(posts, 1):
    if p["text"] in done:
        continue
    print("-" * 70 + f"\n[{i}/30]  {p['text']}\n")
    key = ""
    while key not in KEYS and key != "q":
        key = input("a=analysis  h=hot_take  r=reaction  q=quit > ").strip().lower()
    if key == "q":
        break
    writer.writerow({"id": p["id"], "text": p["text"], "label": KEYS[key]})
    out.flush()

out.close()
with open(OUT, encoding="utf-8") as f:
    print(f"\n{sum(1 for _ in csv.DictReader(f))} of 30 labeled. Run again to resume.")