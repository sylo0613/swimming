import pandas as pd
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)

FILE_PATH = "data/swim_data.csv"

columns = [
    "date",
    "distance",
    "attempt",
    "type",
    "stroke",
    "5m",
    "10m",
    "15m",
    "20m",
    "25m",
    "30m",
    "35m",
    "40m",
    "45m",
    "50m"
]

if not os.path.exists(FILE_PATH):
    pd.DataFrame(columns=columns).to_csv(FILE_PATH, index=False)

df = pd.read_csv(FILE_PATH)

for column in columns:
    if column not in df.columns:
        df[column] = None

df = df[columns]

date = input("Date (DD/MM/YYYY, blank=today): ").strip()

if date == "":
    date = datetime.today().strftime("%d/%m/%Y")

distance = input("Distance: ").strip()
distance_num = int(distance)

set_type = input("Type: ").strip()
stroke = input("Stroke: ").strip()

today_rows = df[df["date"] == date]

if len(today_rows) == 0:
    attempt = 1
else:
    attempt = int(today_rows["attempt"].max()) + 1

print(f"\nAttempt #{attempt}\n")

def get_split(name):
    value = input(f"{name} (blank if none): ").strip()

    if value == "":
        return None

    return float(value)

split_distances = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

splits = {}

for split_distance in split_distances:
    column_name = f"{split_distance}m"

    if split_distance <= distance_num:
        splits[column_name] = get_split(column_name)
    else:
        splits[column_name] = None

new_row = {
    "date": date,
    "distance": distance_num,
    "attempt": attempt,
    "type": set_type,
    "stroke": stroke,
    **splits
}

df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

df.to_csv(FILE_PATH, index=False)

print("\nEntry added successfully.")
print(f"Saved to {FILE_PATH}")