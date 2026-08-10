"""
Enterprise Product Analytics Platform
Custom Application Exceptions
"""


class EnterpriseAnalyticsError(Exception):
    """Base exception for the analytics platform."""


class DataProcessingError(EnterpriseAnalyticsError):
    """Raised when data processing fails."""


class DataValidationError(EnterpriseAnalyticsError):
    """Raised when data validation fails."""


class WarehouseError(EnterpriseAnalyticsError):
    """Raised when warehouse operations fail."""


class AnalyticsError(EnterpriseAnalyticsError):
    """Raised when analytics calculations fail."""


class ConfigurationError(EnterpriseAnalyticsError):
    """Raised when application configuration is invalid."""