from unittest.mock import patch

import pytest

from src.main import app as main


def test_app_initialization(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test app initialization."""
    monkeypatch.setenv("APP_ENV", "testing")

    with patch("src.main.create_tables") as mock_create:
        # Import the app to trigger startup logic
        from src.main import app
        assert app.title == "uGram API"
