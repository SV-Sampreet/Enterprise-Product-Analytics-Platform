import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.analytics.kpis import KPIEngine


def main():
    KPIEngine().dashboard()


if __name__ == "__main__":
    main()