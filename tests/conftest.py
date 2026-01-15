from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from defaultpython.api import app


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c
