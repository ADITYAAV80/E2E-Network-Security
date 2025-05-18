import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import jwt
import bcrypt
from datetime import datetime, timedelta

from main import app, SECRET_KEY, ALGORITHM

client = TestClient(app)

@pytest.fixture
def mock_users_collection():
    with patch('main.users_collection') as mock_collection:
        yield mock_collection

@pytest.fixture
def mock_model():
    with patch('mlflow.pyfunc.load_model') as mock_load:
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        yield mock_model

@pytest.fixture
def auth_token():
    # Create a test token
    token = jwt.encode({
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "role": "customer"
    }, SECRET_KEY, algorithm=ALGORITHM)
    return f"Bearer {token}"

def test_login_success(mock_users_collection):
    # Arrange
    hashed_pwd = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
    mock_users_collection.find_one.return_value = {
        "email": "test@example.com",
        "password": hashed_pwd,
        "role": "customer"
    }
    
    # Act
    response = client.post(
        "/api/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    
    # Assert
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(mock_users_collection):
    # Arrange
    mock_users_collection.find_one.return_value = None
    
    # Act
    response = client.post(
        "/api/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    
    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_signup_success(mock_users_collection):
    # Arrange
    mock_users_collection.find_one.return_value = None
    
    # Act
    response = client.post(
        "/api/signup",
        json={"email": "new@example.com", "password": "newpassword"}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "token" in response.json()
    mock_users_collection.insert_one.assert_called_once()

def test_signup_user_exists(mock_users_collection):
    # Arrange
    mock_users_collection.find_one.return_value = {"email": "existing@example.com"}
    
    # Act
    response = client.post(
        "/api/signup",
        json={"email": "existing@example.com", "password": "password123"}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

@patch('main.run_pipeline_wrapper')
def test_train_route(mock_run_pipeline, auth_token):
    # Act
    response = client.post(
        "/api/train",
        headers={"Authorization": auth_token}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Training started in background!" in response.text

@patch('main.scaler')
def test_predict_route(mock_scaler, mock_model, auth_token):
    # Arrange
    mock_model.predict.return_value = [1]  # Mocking prediction result
    
    # Act
    response = client.post(
        "/api/predict",
        headers={"Authorization": auth_token},
        data={"feature1": "0.5", "feature2": "0.7"}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["prediction"] == 1 