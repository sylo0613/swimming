import pandas as pd
import os

# create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# file path
FILE_PATH = "data/swim_data.csv"

# columns
columns = [
    "date",
    "distance",
    "attempt",
    "type",
    "stroke",
    "5m",
    "10m",
    "15m",
    "25m",
    "30m",
    "35m",
    "40m",
    "45m",
    "50m"
]

# create empty dataframe
df = pd.DataFrame(columns=columns)

# save csv
df.to_csv(FILE_PATH, index=False)

print(f"Created: {FILE_PATH}")

