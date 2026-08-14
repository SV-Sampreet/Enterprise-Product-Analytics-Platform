"""
Enterprise Product Analytics Platform
Feature Adoption Analytics Test
"""

from src.analytics.feature_adoption import FeatureAdoptionAnalytics


def main():
    analytics = FeatureAdoptionAnalytics()
    analytics.report()


if __name__ == "__main__":
    main()