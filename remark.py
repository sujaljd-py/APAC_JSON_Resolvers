import re
import json

# Step 1: Read as raw text
with open("remark.json", "r", encoding="utf-8") as f:
    raw = f.read()

# Step 2: List of known problematic fields
fields = ["Remarks", "Remarks To Guest", "Additional Remarks"]

# Step 3: Fix line breaks inside strings for each field
for field in fields:
    pattern = rf'"{field}"\s*:\s*"((?:[^"\\]|\\.)*?)"'

    def fix_newlines(match):
        content = match.group(1)
        # Replace actual line breaks with comma + space
        fixed = content.replace('\n', ', ').replace('\r', ', ').replace('"', '\\"')
        return f'"{field}": "{fixed}"'

    raw = re.sub(pattern, fix_newlines, raw, flags=re.DOTALL)

# Step 4: Parse the cleaned text into JSON
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"❌ Still broken at: {e}")
    exit()

# Step 5: Save valid JSON
with open("final_fixed_remark.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ JSON has been successfully repaired and saved to 'final_fixed_remark.json'")
print(f"Total bookings: {len(data.get('BOOKINGS', {}))}")
