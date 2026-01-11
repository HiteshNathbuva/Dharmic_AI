import json
import os

INPUT_FILE = "data/upanishads/isha_structured.txt"
OUTPUT_FILE = "data/metadata_isha_structured.json"

def parse_isha():
    records = []
    current = {}

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line == "---":
                if current:
                    current["book"] = "Isha Upanishad"
                    records.append(current)
                    current = {}
                continue

            if line.startswith("REF:"):
                current["ref"] = line.replace("REF:", "").strip()

            elif line.startswith("SANSKRIT:"):
                current["sanskrit"] = ""

            elif line.startswith("MEANING:"):
                current["meaning"] = ""

            elif line.startswith("TAGS:"):
                current["tags"] = []

            else:
                if "sanskrit" in current and current["sanskrit"] == "":
                    current["sanskrit"] = line
                elif "meaning" in current and current["meaning"] == "":
                    current["meaning"] = line
                elif "tags" in current:
                    current["tags"].extend([t.strip() for t in line.split(",")])

    if current:
        current["book"] = "Isha Upanishad"
        records.append(current)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"✅ Parsed {len(records)} Isha verses successfully")
    print(f"📁 Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_isha()
