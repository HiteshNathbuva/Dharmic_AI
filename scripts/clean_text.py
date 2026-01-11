import os
import json
import re

BASE_DIR = "data"
OUTPUT_FILE = "data/clean_corpus.json"

records = []

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            book_name = os.path.basename(root)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            blocks = content.split("\n\n")
            for block in blocks:
                block = clean_text(block)
                if len(block) < 30:
                    continue

                record = {
                    "book": book_name,
                    "source_file": file,
                    "text": block
                }
                records.append(record)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"✅ Clean corpus created with {len(records)} records")
print(f"📁 Saved at: {OUTPUT_FILE}")
