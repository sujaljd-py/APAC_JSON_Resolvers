import json
import re
from tqdm import tqdm
from collections import defaultdict
import os

# ✅ Input and output file names
input_file = "Export (1).json"
output_json = "all_extra_charges.json"

# ✅ Check file existence
if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit(1)

# ✅ Step 1: Read raw text
with open(input_file, "r", encoding="utf-8") as f:
    raw = f.read()

# ✅ Step 2: Escape unescaped control characters in strings (e.g. real \n, \r, \t)
# Replace unescaped newline, carriage return, or tab characters with space
raw = re.sub(r'(?<!\\)(\n|\r|\t)', ' ', raw)

# ✅ Step 3: Load cleaned JSON
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"❌ JSON is still invalid after cleaning: {e}")
    exit(1)

print("✅ JSON loaded successfully after cleaning.")

# ✅ Step 4: Extract extra charges
bookings = data.get("BOOKINGS", {})
all_charges = []
charge_counts = defaultdict(int)

for booking_id, booking in tqdm(bookings.items(), desc="Collecting Extra Charges"):
    extra_charges = booking.get("Extra charges", [])
    if isinstance(extra_charges, list):
        for charge in extra_charges:
            if isinstance(charge, dict):
                all_charges.append(charge)
                name = charge.get("ChargeName", "Unknown")
                charge_counts[name] += 1

# ✅ Step 5: Save all charges to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(all_charges, f, indent=4, ensure_ascii=False)

# ✅ Step 6: Print summary
print("\n--- Extra Charges Summary ---")
print(f"Total extra charge records: {len(all_charges)}")
print(f"Unique charge names found : {len(charge_counts)}")
print("\nCounts by ChargeName:")
for name, count in sorted(charge_counts.items(), key=lambda x: x[1], reverse=True):
    print(f" - {name}: {count}")

print(f"\n✅ Full extra charge list saved to: {output_json}")
