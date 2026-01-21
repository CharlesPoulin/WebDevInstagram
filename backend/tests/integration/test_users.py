"""Integration tests for Users API happy paths.

These tests verify the full CRUD lifecycle for users, ensuring
the API endpoints work correctly end-to-end with a clean database.
"""

from dataclasses import dataclass
from uuid import UUID

import pytest
from fastapi.testclient import TestClient


@dataclass
class UserPayload:
    """Test data factory for user payloads."""

    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str | None = None
    profile_photo_url: str | None = None

    def to_dict(self) -> dict:
        """Convert to API request payload."""
        data = {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        if self.phone_number:
            data["phone_number"] = self.phone_number
        if self.profile_photo_url:
            data["profile_photo_url"] = self.profile_photo_url
        return data


class UserAPIClient:
    """Helper class for user API operations - Single Responsibility."""

    def __init__(self, client: TestClient) -> None:
        self.client = client

    def create(self, payload: UserPayload) -> tuple[int, dict]:
        """Create a user and return (status_code, response_json)."""
        response = self.client.post("/users", json=payload.to_dict())
        return response.status_code, response.json()

    def get(self, user_id: str) -> tuple[int, dict]:
        """Get a user by ID."""
        response = self.client.get(f"/users/{user_id}")
        return response.status_code, response.json()

    def list(self, limit: int = 20, offset: int = 0) -> tuple[int, dict]:
        """List users with pagination."""
        response = self.client.get("/users", params={"limit": limit, "offset": offset})
        return response.status_code, response.json()

    def update(self, user_id: str, updates: dict) -> tuple[int, dict]:
        """Update a user's profile."""
        response = self.client.put(f"/users/{user_id}", json=updates)
        return response.status_code, response.json()


@pytest.fixture
def api(client: TestClient) -> UserAPIClient:
    """Provide a UserAPIClient wrapper."""
    return UserAPIClient(client)


@pytest.fixture
def sample_user() -> UserPayload:
    """Standard test user payload."""
    return UserPayload(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone_number="+15551234567",
    )


@pytest.fixture
def created_user(api: UserAPIClient, sample_user: UserPayload) -> dict:
    """Create and return a user for tests that need an existing user."""
    status, data = api.create(sample_user)
    assert status == 201
    return data


class TestCreateUser:
    """Tests for user creation endpoint."""

    def test_creates_user_with_all_fields(self, api: UserAPIClient) -> None:
        """Creating a user returns all provided fields."""
        payload = UserPayload(
            username="fulluser",
            email="full@example.com",
            first_name="Full",
            last_name="User",
            phone_number="+15551234567",
            profile_photo_url="https://example.com/photo.jpg",
        )

        status, data = api.create(payload)

        assert status == 201
        assert data["username"] == payload.username
        assert data["email"] == payload.email
        assert data["first_name"] == payload.first_name
        assert data["last_name"] == payload.last_name
        assert data["phone_number"] == payload.phone_number
        assert data["profile_photo_url"] == payload.profile_photo_url
        UUID(data["id"])  # Valid UUID

    def test_creates_user_with_minimal_fields(self, api: UserAPIClient) -> None:
        """Creating a user works with only required fields."""
        payload = UserPayload(
            username="minimal",
            email="minimal@example.com",
            first_name="Min",
            last_name="User",
        )

        status, data = api.create(payload)

        assert status == 201
        assert data["phone_number"] is None
        assert data["profile_photo_url"] is None


class TestGetUser:
    """Tests for retrieving a user."""

    def test_retrieves_existing_user(self, api: UserAPIClient, created_user: dict) -> None:
        """Getting a user by ID returns correct data."""
        status, data = api.get(created_user["id"])

        assert status == 200
        assert data["id"] == created_user["id"]
        assert data["username"] == created_user["username"]


class TestListUsers:
    """Tests for listing users."""

    def test_returns_paginated_list(self, api: UserAPIClient) -> None:
        """Listing users returns paginated response structure."""
        # Create test users
        for i in range(3):
            payload = UserPayload(
                username=f"listuser{i}",
                email=f"list{i}@example.com",
                first_name=f"List{i}",
                last_name="User",
            )
            api.create(payload)

        status, data = api.list(limit=10, offset=0)

        assert status == 200
        assert "users" in data
        assert "total" in data
        assert data["limit"] == 10
        assert data["offset"] == 0
        assert len(data["users"]) >= 3

    def test_pagination_returns_different_pages(self, api: UserAPIClient) -> None:
        """Different offsets return different users."""
        for i in range(4):
            payload = UserPayload(
                username=f"pageuser{i}",
                email=f"page{i}@example.com",
                first_name=f"Page{i}",
                last_name="User",
            )
            api.create(payload)

        _, page1 = api.list(limit=2, offset=0)
        _, page2 = api.list(limit=2, offset=2)

        page1_ids = {u["id"] for u in page1["users"]}
        page2_ids = {u["id"] for u in page2["users"]}
        assert page1_ids.isdisjoint(page2_ids)


class TestUpdateUser:
    """Tests for updating user profile."""

    def test_updates_user_profile(self, api: UserAPIClient, created_user: dict) -> None:
        """Updating a user modifies the specified fields."""
        updates = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com",
        }

        status, data = api.update(created_user["id"], updates)

        assert status == 200
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
        assert data["email"] == "updated@example.com"
        assert data["username"] == created_user["username"]  # Unchanged


class TestUserLifecycle:
    """End-to-end lifecycle test."""

    def test_full_crud_lifecycle(self, api: UserAPIClient) -> None:
        """Complete create -> read -> update -> verify flow."""
        # Create
        payload = UserPayload(
            username="lifecycle",
            email="lifecycle@example.com",
            first_name="Life",
            last_name="Cycle",
            phone_number="+15550001111",
        )
        status, user = api.create(payload)
        assert status == 201
        user_id = user["id"]

        # Read
        status, fetched = api.get(user_id)
        assert status == 200
        assert fetched["first_name"] == "Life"

        # Update
        status, updated = api.update(user_id, {"first_name": "Updated"})
        assert status == 200

        # Verify persistence
        status, final = api.get(user_id)
        assert status == 200
        assert final["first_name"] == "Updated"
        assert final["phone_number"] == "+15550001111"  # Unchanged
