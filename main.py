import json
import pandas as pd
from tqdm import tqdm
import os

# ✅ Input file
input_file = "48295new.json"

# ✅ Reservation sources to filter (exact match, case-insensitive)
FILTERED_SOURCES = [
    "Booking.com",
    "Agoda.com",
    "MakeMyTrip India Pvt Ltd",
    "Expedia.com",
    "CTRIP",
    "TIKET.COM"
]

# ✅ Check if file exists
if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit(1)

# ✅ Load JSON
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

bookings = data.get("BOOKINGS", {})
filtered = {}
unfiltered = {}
rows_for_excel = []
other_sources_found = set()

# ✅ Normalize source list for comparison
normalized_sources = [src.lower() for src in FILTERED_SOURCES]

# ✅ Process bookings with progress bar
for booking_id in tqdm(bookings, desc="Processing bookings"):
    booking = bookings[booking_id]
    source = booking.get("Reservation Source", "").strip()
    row = booking.copy()
    row["Booking ID"] = booking_id
    rows_for_excel.append(row)

    # ✅ Check for exact (case-insensitive) match
    if source.lower() in normalized_sources:
        filtered[booking_id] = booking
    else:
        unfiltered[booking_id] = booking
        if source:
            other_sources_found.add(source)

# ✅ Write filtered JSON
with open("filtered_bookings.json", "w", encoding='utf-8') as f:
    json.dump({"BOOKINGS": filtered}, f, indent=4, ensure_ascii=False)

# ✅ Write unfiltered JSON
with open("unfiltered_bookings.json", "w", encoding='utf-8') as f:
    json.dump({"BOOKINGS": unfiltered}, f, indent=4, ensure_ascii=False)

# ✅ Write Excel file
df = pd.DataFrame(rows_for_excel)
df.to_excel("all_bookings.xlsx", index=False)

# ✅ Summary Output
print("\n--- Summary ---")
print(f"Total bookings         : {len(bookings)}")
print(f"Filtered bookings      : {len(filtered)}")
print(f"Unfiltered bookings    : {len(unfiltered)}")

if other_sources_found:
    print("\nOther reservation sources found (outside filter list):")
    for src in sorted(other_sources_found):
        print(f" - {src}")
else:
    print("\nNo other reservation sources found.")
