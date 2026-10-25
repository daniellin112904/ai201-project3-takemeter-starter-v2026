"""Turn raw_comments.txt into raw_posts.csv, ready for labeling."""
import csv
import re

with open("raw_comments.txt", encoding="utf-8") as f:
    chunks = f.read().split("=====")

seen, rows = set(), []
for chunk in chunks:
    text = " ".join(chunk.split())          # collapse newlines and extra spaces
    if text in ("[deleted]", "[removed]") or text in seen:
        continue
    if re.fullmatch(r"https?://\S+", text):  # bare links
        continue
    if not (20 <= len(text) <= 700):         # too short to label, or too long
        continue
    seen.add(text)
    rows.append({"text": text, "label": "", "note": ""})

with open("raw_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
    writer.writeheader()
    writer.writerows(rows)

print(f"{len(chunks)} raw chunks -> {len(rows)} usable comments in raw_posts.csv")