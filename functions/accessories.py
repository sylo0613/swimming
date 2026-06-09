import shutil
from datetime import datetime
import os


def create_data_backup():

    source_folder = "data"

    backup_root = os.path.join("archives", "backups")

    os.makedirs(backup_root, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_folder = os.path.join(
        backup_root,
        f"data_backup_{timestamp}"
    )

    shutil.copytree(source_folder, backup_folder, ignore=shutil.ignore_patterns("backups"))

    print(f"Backup created: {backup_folder}")