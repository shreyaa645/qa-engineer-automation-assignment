import pytest
import requests

BASE_URL = "https://reqres.in/api"
HEADERS = {
    "x-api-key": "reqres-free-v1",
    "Content-Type": "application/json",
}


class TestReqresAPI:
    """Automated API test suite for Reqres endpoints."""

    def test_get_users_list_success(self):
        """TC01: Validate successful GET response (200) and pagination structure."""
        response = requests.get(f"{BASE_URL}/users", params={"page": 2}, headers=HEADERS, timeout=10)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        body = response.json()

        assert body["page"] == 2
        assert "data" in body and isinstance(body["data"], list)
        assert len(body["data"]) > 0

    def test_get_single_user_content(self):
        """TC02: Validate specific user data keys and values."""
        user_id = 2
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS, timeout=10)

        assert response.status_code == 200
        user_data = response.json().get("data", {})

        assert user_data.get("id") == user_id
        assert user_data.get("email") == "janet.weaver@reqres.in"
        assert user_data.get("first_name") == "Janet"
        assert user_data.get("last_name") == "Weaver"

    def test_create_user_post_success(self):
        """TC03: Validate POST resource creation returns 201 and echoed payload."""
        payload = {"name": "Shreya", "job": "QA Automation Engineer"}
        response = requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS, timeout=10)

        assert response.status_code == 201
        body = response.json()

        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert "id" in body
        assert "createdAt" in body

    def test_get_nonexistent_user_error_handling(self):
        """TC04: Validate error handling (404) when querying a non-existent user ID."""
        response = requests.get(f"{BASE_URL}/users/9999", headers=HEADERS, timeout=10)

        assert response.status_code == 404, f"Expected 404 for missing user, got {response.status_code}"
        assert response.json() == {}

    def test_login_missing_password_error_handling(self):
        """TC05: Validate error handling (400) when required password parameter is missing."""
        payload = {"email": "peter@klaven"}
        response = requests.post(f"{BASE_URL}/login", json=payload, headers=HEADERS, timeout=10)

        assert response.status_code == 400
        body = response.json()
        assert "error" in body
        assert body["error"] == "Missing password"