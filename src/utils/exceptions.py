"""
Custom exceptions for the Email Spam Classifier application.

This module defines a hierarchy of custom exceptions to provide
better error handling and more descriptive error messages.
"""


class SpamClassifierException(Exception):
    """Base exception for all spam classifier errors."""
    pass


class ModelLoadError(SpamClassifierException):
    """Raised when there's an error loading the ML model or vectorizer."""
    pass


class PredictionError(SpamClassifierException):
    """Raised when there's an error during email classification."""
    pass


class ValidationError(SpamClassifierException):
    """Raised when input validation fails."""
    pass


class ConfigurationError(SpamClassifierException):
    """Raised when there's a configuration error."""
    pass
