import json
from tqdm import tqdm
import os

# ✅ Input and output file paths
input_file = "unfiltered_bookings.json"
output_file = "cleaned_positive_rates.json"

# ✅ Check file existence
if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit(1)

# ✅ Load the JSON
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

bookings = data.get("BOOKINGS", {})
corrected_count = 0
total_rates_checked = 0

# ✅ Process each booking
for booking_id, booking in tqdm(bookings.items(), desc="Fixing Custom Rates"):
    if "Custom Rates" in booking and isinstance(booking["Custom Rates"], list):
        new_rates = []
        for rate_entry in booking["Custom Rates"]:
            new_entry = {}
            for date, rate in rate_entry.items():
                try:
                    clean_rate = abs(float(rate))
                    clean_rate_str = f"{clean_rate:.4f}"
                    new_entry[date] = clean_rate_str
                    total_rates_checked += 1
                    if float(rate) < 0:
                        corrected_count += 1
                except (ValueError, TypeError):
                    new_entry[date] = rate  # Leave it as is if it fails
            new_rates.append(new_entry)
        booking["Custom Rates"] = new_rates

# ✅ Save the cleaned JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ✅ Summary
print("\n--- Custom Rate Cleanup Summary ---")
print(f"Total bookings processed     : {len(bookings)}")
print(f"Total rates checked          : {total_rates_checked}")
print(f"Negative rates converted     : {corrected_count}")
print(f"✅ Cleaned file saved as      : {output_file}")
