
from pathlib import Path
import shutil
import logging

# Project directories
INCOMING_DIR = Path("data/incoming")
RAW_DIR = Path("data/raw")
ARCHIVE_DIR = Path("data/archive")

# Create directories if they do not exist
for folder in [INCOMING_DIR, RAW_DIR, ARCHIVE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def ingest_files():
    """Validate and ingest incoming Excel files."""

    incoming_files = sorted(
        list(INCOMING_DIR.glob("*.xlsx"))
        + list(INCOMING_DIR.glob("*.xls"))
    )

    if not incoming_files:
        existing_raw = RAW_DIR / "Online Retail.xlsx"

        if existing_raw.exists():
            logging.info(
                "No incoming files found. Using existing raw dataset."
            )
            return existing_raw

        raise FileNotFoundError(
            "No incoming Excel files or existing raw dataset found."
        )

    if len(incoming_files) > 1:
        raise ValueError(
            "Multiple incoming Excel files found. "
            "Process one batch at a time."
        )

    source_file = incoming_files[0]

    if source_file.stat().st_size == 0:
        raise ValueError(f"Incoming file is empty: {source_file}")

    destination = RAW_DIR / "Online Retail.xlsx"

    # Preserve the original incoming file in the archive
    archive_destination = ARCHIVE_DIR / source_file.name

    if archive_destination.exists():
        raise FileExistsError(
            f"Archive already contains {source_file.name}. "
            "Rename the incoming file before retrying."
        )

    shutil.copy2(source_file, destination)
    shutil.move(str(source_file), str(archive_destination))

    logging.info("File ingested successfully: %s", source_file.name)
    logging.info("Raw dataset prepared: %s", destination)

    return destination


if __name__ == "__main__":
    ingested_file = ingest_files()
    print(f"\nINGESTION SUCCESSFUL: {ingested_file}")
