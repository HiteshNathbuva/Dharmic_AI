import json

OUTPUT_FILE = "data/metadata_merged.json"

INPUT_FILES = [
    "data/metadata_gita_structured.json",
    "data/metadata_isha_structured.json",
    "data/metadata_ramayana_structured.json",
    "data/metadata_mahabharata_structured.json"
]

def merge_metadata():
    merged_data = []

    for file_path in INPUT_FILES:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                merged_data.extend(data)
                print(f"✅ Loaded {len(data)} records from {file_path}")
        except FileNotFoundError:
            print(f"⚠️ File not found, skipped: {file_path}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(merged_data, out, ensure_ascii=False, indent=2)

    print(f"\n🎯 Metadata merge completed.")
    print(f"📊 Total records in merged file: {len(merged_data)}")

if __name__ == "__main__":
    merge_metadata()
