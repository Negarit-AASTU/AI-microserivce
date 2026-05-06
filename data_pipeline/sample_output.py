import json

INPUT_FILE = "negarit_dataset.json"
OUTPUT_FILE = "sample_negarit_dataset.json"

SAMPLE_SIZE = 5000  

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

sample = data[:SAMPLE_SIZE]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(sample, f, indent=2)

print(f"Sample dataset created: {OUTPUT_FILE} ({len(sample)} records)")