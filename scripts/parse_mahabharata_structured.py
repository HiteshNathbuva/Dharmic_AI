import json

INPUT_FILE = "data/mahabharata/mahabharata_structured.txt"
OUTPUT_FILE = "data/metadata_mahabharata_structured.json"

def parse_mahabharata():
    records = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    raw_entries = content.split("\n---\n")

    for entry in raw_entries:
        lines = entry.strip().split("\n")
        record = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                record[key.strip().lower()] = value.strip()

        if record:
            records.append({
                "id": record.get("id", ""),
                "book": record.get("book", "Mahabharata"),
                "parva": record.get("parva", ""),
                "context": record.get("context", ""),
                "speaker": record.get("speaker", ""),
                "listener": record.get("listener", ""),
                "concept": record.get("concept", ""),
                "situation": record.get("situation", ""),
                "meaning": record.get("teaching", ""),
                "explanation": record.get("explanation", "")
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(records, out, ensure_ascii=False, indent=2)

    print(f"✅ Mahabharata parsing completed. {len(records)} records saved.")

if __name__ == "__main__":
    parse_mahabharata()
