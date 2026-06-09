import pandas as pd
import os
from datetime import datetime
import shutil

os.makedirs("data", exist_ok=True)

FILE_PATH = "data/swim_data.csv"

columns = [
    "entry",
    "date",
    "distance",
    "attempt",
    "type",
    "stroke",
    "suited",
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


def get_split(name):
    while True:
        value = input(f"{name} (blank if none): ").strip()

        if value == "":
            return None

        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter again.")


def add_entry(distance_num=None, set_type=None, stroke=None, fixed_date=None, suited=None):

    if not os.path.exists(FILE_PATH):
        pd.DataFrame(columns=columns).to_csv(FILE_PATH, index=False)

    df = pd.read_csv(FILE_PATH)

    for column in columns:
        if column not in df.columns:
            df[column] = None

    df = df[columns]

    if fixed_date is not None:
        date = fixed_date
    else:
        date = input("Date (DD/MM/YYYY, blank=today): ").strip()

        if date == "":
            date = datetime.today().strftime("%d/%m/%Y")

    if distance_num is None:
        distance_num = int(input("Distance: ").strip())

    if set_type is None:
        set_type = input("Type: ").strip()

    if stroke is None:
        stroke = input("Stroke: ").strip()

    if suited is None:
        suited_input = input("Suited? (Y/N, blank=N): ").strip().upper()
        suited = "N" if suited_input == "" else suited_input

    today_rows = df[df["date"] == date]

    if len(today_rows) == 0:
        attempt = 1
    else:
        attempt = int(today_rows["attempt"].max()) + 1

    if len(df) == 0:
        entry = 1
    else:
        entry = int(df["entry"].max()) + 1

    print(f"\nEntry #{entry}")
    print(f"Attempt #{attempt}")
    print(f"{set_type} | {stroke} | {distance_num}m | Suited: {suited}\n")

    split_distances = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    while True:
        splits = {}

        for split_distance in split_distances:
            column_name = f"{split_distance}m"

            if split_distance <= distance_num:
                splits[column_name] = get_split(column_name)
            else:
                splits[column_name] = None

        print("\nCheck entry:")
        print(f"Entry   : {entry}")
        print(f"Date    : {date}")
        print(f"Distance: {distance_num}")
        print(f"Attempt : {attempt}")
        print(f"Type    : {set_type}")
        print(f"Stroke  : {stroke}")
        print(f"Suited  : {suited}")

        for split_distance in split_distances:
            column_name = f"{split_distance}m"
            if splits[column_name] is not None:
                print(f"{column_name:<8}: {splits[column_name]}")

        confirm = input("\nSave this entry? (Y/N): ").strip().upper()

        if confirm == "Y":
            break

        print("\nRe-enter splits.\n")

    new_row = {
        "entry": entry,
        "date": date,
        "distance": distance_num,
        "attempt": attempt,
        "type": set_type,
        "stroke": stroke,
        "suited": suited,
        **splits
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    print("\nEntry added successfully.")
    print(f"Saved to {FILE_PATH}")


def add_session():

    date = input("Date (DD/MM/YYYY, blank=today): ").strip()

    if date == "":
        date = datetime.today().strftime("%d/%m/%Y")

    set_type = input("Type: ").strip()
    distance_num = int(input("Distance: ").strip())
    stroke = input("Stroke: ").strip()

    suited_input = input("Suited? (Y/N, blank=N): ").strip().upper()
    suited = "N" if suited_input == "" else suited_input

    print("\nEnter attempts. Type 'stop' to finish.\n")

    while True:
        confirm = input(
            f"Add rep? {date} | {set_type} | {stroke} | {distance_num}m | suited {suited} (Y/stop): "
        ).strip().lower()

        if confirm == "stop":
            break

        if confirm != "y":
            print("Skipped.")
            continue

        add_entry(
            distance_num=distance_num,
            set_type=set_type,
            stroke=stroke,
            fixed_date=date,
            suited=suited
        )

    print("\nSession finished.")


def add_dive_25_fs():
    add_entry(
        distance_num=25,
        set_type="dive",
        stroke="FS"
    )


def create_data_backup():

    source_folder = "data"
    backup_root = os.path.join("data", "backups")

    os.makedirs(backup_root, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(backup_root, f"data_backup_{timestamp}")

    shutil.copytree(
        source_folder,
        backup_folder,
        ignore=shutil.ignore_patterns("backups")
    )

    print(f"Backup created: {backup_folder}")