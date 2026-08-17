"""
Enterprise Product Analytics Platform
User Journey Analytics Test
"""

from src.analytics.journey import JourneyAnalytics


def main():
    analytics = JourneyAnalytics()
    analytics.report()


if __name__ == "__main__":
    main()