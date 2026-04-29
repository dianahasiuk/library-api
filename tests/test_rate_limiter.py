import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ─── Анонімний юзер ───────────────────────────────────────────

@patch("api.dependencies.is_rate_limited")
def test_anonymous_under_limit(mock_rate_limited):
    """Анонімний юзер ще не досяг ліміту - статус 200"""
    mock_rate_limited.return_value = False

    response = client.get("/books")

    assert response.status_code == 200
    mock_rate_limited.assert_called_once()
    args = mock_rate_limited.call_args[0]
    assert args[1] == False  # is_authenticated = False


@patch("api.dependencies.is_rate_limited")
def test_anonymous_over_limit(mock_rate_limited):
    """Анонімний юзер досяг ліміту - статус 429"""
    mock_rate_limited.return_value = True

    response = client.get("/books")

    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded. Try again later."
    mock_rate_limited.assert_called_once()
    args = mock_rate_limited.call_args[0]
    assert args[1] == False  # is_authenticated = False


# ─── Авторизований юзер ───────────────────────────────────────

@patch("api.dependencies.is_rate_limited")
@patch("api.dependencies.get_user_by_username")
@patch("api.dependencies.decode_token")
def test_authenticated_under_limit(mock_decode, mock_get_user, mock_rate_limited):
    """Авторизований юзер ще не досяг ліміту - статус 200"""
    mock_decode.return_value = {"sub": "testuser", "type": "access"}
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_get_user.return_value = mock_user
    mock_rate_limited.return_value = False

    response = client.get(
        "/books",
        headers={"Authorization": "Bearer faketoken"}
    )

    assert response.status_code == 200
    mock_rate_limited.assert_called_once()
    args = mock_rate_limited.call_args[0]
    assert args[0] == "testuser"
    assert args[1] == True  # is_authenticated = True


@patch("api.dependencies.is_rate_limited")
@patch("api.dependencies.get_user_by_username")
@patch("api.dependencies.decode_token")
def test_authenticated_over_limit(mock_decode, mock_get_user, mock_rate_limited):
    """Авторизований юзер досяг ліміту - статус 429"""
    mock_decode.return_value = {"sub": "testuser", "type": "access"}
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_get_user.return_value = mock_user
    mock_rate_limited.return_value = True

    response = client.get(
        "/books",
        headers={"Authorization": "Bearer faketoken"}
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded. Try again later."
    mock_rate_limited.assert_called_once()
    args = mock_rate_limited.call_args[0]
    assert args[0] == "testuser"
    assert args[1] == True  # is_authenticated = True
