import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_processing.cleaners.events_cleaner import EventsCleaner
from src.data_processing.loaders.csv_loader import CSVLoader


def main():

    loader = CSVLoader()

    events = loader.load_csv("events")

    cleaner = EventsCleaner()

    clean_events = cleaner.clean(events)

    cleaner.report(clean_events)

    print(clean_events.head())


if __name__ == "__main__":
    main()