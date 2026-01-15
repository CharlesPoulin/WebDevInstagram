from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from ugram.src.main import app


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c
