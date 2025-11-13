import re
import json

input_file = "bookings_raw.json"
output_file = "bookings_fixed.json"

# Regex: match any string value in JSON
string_pattern = re.compile(r'(:\s*")(.*?)(?<!\\)(")', re.DOTALL)

def fix_strings(text):
    def replacer(match):
        value = match.group(2)
        fixed_value = value.replace("\r\n", "\\n").replace("\n", "\\n")
        return f'{match.group(1)}{fixed_value}{match.group(3)}'
    return string_pattern.sub(replacer, text)

with open(input_file, "r", encoding="utf-8") as f:
    raw_json = f.read()

# Fix all strings
fixed_json = fix_strings(raw_json)

# Validate
try:
    data = json.loads(fixed_json)
    print("✅ JSON is now valid!")
except json.JSONDecodeError as e:
    print("❌ Still invalid:", e)
    with open("debug.json", "w", encoding="utf-8") as dbg:
        dbg.write(fixed_json)
    raise

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
