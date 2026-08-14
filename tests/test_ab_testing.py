"""
Enterprise Product Analytics Platform
A/B Testing Analytics Test
"""

from src.analytics.ab_testing import ABTestingAnalytics


def main():
    analytics = ABTestingAnalytics()
    analytics.report()


if __name__ == "__main__":
    main()