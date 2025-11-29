"""
Pytest configuration and fixtures for the Email Spam Classifier tests.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_spam_email():
    """Sample spam email for testing."""
    return "CONGRATULATIONS!!! You've WON $1,000,000 in our EXCLUSIVE lottery! Click here NOW!"


@pytest.fixture
def sample_ham_email():
    """Sample legitimate email for testing."""
    return "Hi John, just wanted to follow up on our meeting yesterday. Let me know when you're available."


@pytest.fixture
def sample_emails_batch():
    """Batch of sample emails for testing."""
    return [
        {"id": "1", "text": "Meeting at 3pm tomorrow"},
        {"id": "2", "text": "WIN FREE MONEY NOW!!!"},
        {"id": "3", "text": "Your order has been shipped"}
    ]
