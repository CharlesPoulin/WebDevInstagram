from unittest.mock import patch

import pytest

from ugram.src.main import app as main


def test_app_initialization(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test app initialization."""
    monkeypatch.setenv("APP_ENV", "testing")

    with patch("ugram.src.main.create_tables") as mock_create:
        # Import the app to trigger startup logic
        from ugram.src.main import app
        assert app.title == "uGram API"
