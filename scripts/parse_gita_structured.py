import json

INPUT_FILE = "data/Gita/gita_structured.txt"
OUTPUT_FILE = "data/metadata_gita_structured.json"


def parse_gita_file(filepath):
    verses = []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("---")

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        verse = {
            "book": "Gita",
            "ref": "",
            "sanskrit": "",
            "meaning": "",
            "tags": []
        }

        lines = block.splitlines()
        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith("REF:"):
                verse["ref"] = line.replace("REF:", "").strip()

            elif line == "SANSKRIT:":
                current_section = "sanskrit"

            elif line == "MEANING:":
                current_section = "meaning"

            elif line == "TAGS:":
                current_section = "tags"

            else:
                if current_section == "sanskrit":
                    verse["sanskrit"] += line + " "
                elif current_section == "meaning":
                    verse["meaning"] += line + " "
                elif current_section == "tags":
                    verse["tags"] = [t.strip() for t in line.split(",")]

        verse["sanskrit"] = verse["sanskrit"].strip()
        verse["meaning"] = verse["meaning"].strip()

        if verse["ref"] and verse["meaning"]:
            verses.append(verse)

    return verses


def main():
    verses = parse_gita_file(INPUT_FILE)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(verses, f, indent=2, ensure_ascii=False)

    print(f"✅ Parsed {len(verses)} Gita verses successfully.")
    print(f"📁 Output saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
