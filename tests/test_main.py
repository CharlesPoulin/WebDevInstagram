from unittest.mock import patch

import pytest

from defaultpython.main import main


def test_main_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main function loads environment and logs correctly."""
    monkeypatch.setenv("APP_ENV", "testing")

    with patch("defaultpython.main.logger") as mock_logger:
        main()
        # Verify logger was called with the environment
        assert mock_logger.info.call_count == 2
        calls = [str(call) for call in mock_logger.info.call_args_list]
        assert any("testing" in str(call) for call in calls)
