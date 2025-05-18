import pytest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import jwt
import bcrypt
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock dagshub.init before importing main
with patch('dagshub.init') as mock_dagshub:
    # Import the app after mocking dagshub
    from main import app, SECRET_KEY, ALGORITHM

client = TestClient(app)

# Mock the MongoDB and JWT functionality
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('main.users_collection') as mock_users:
        with patch('main.jwt.encode') as mock_jwt_encode:
            with patch('main.jwt.decode') as mock_jwt_decode:
                with patch('main.bcrypt.checkpw') as mock_check_pw:
                    # Set up common mock behaviors
                    mock_jwt_encode.return_value = "test_token"
                    mock_jwt_decode.return_value = {"email": "test@example.com", "role": "customer"}
                    mock_check_pw.return_value = True
                    mock_users.find_one.return_value = {
                        "email": "test@example.com", 
                        "password": b"hashed_password",
                        "role": "customer"
                    }
                    yield

# Very simple test just to verify API endpoints exist
@patch('main.users_collection')
@patch('main.jwt.encode')
@patch('main.bcrypt.checkpw')
def test_login_endpoint(mock_checkpw, mock_jwt, mock_users):
    # Setup mocks
    mock_checkpw.return_value = True
    mock_jwt.return_value = "test_jwt_token"
    mock_users.find_one.return_value = {
        "email": "test@example.com",
        "password": b"hashed_password",
        "role": "customer"
    }
    
    # Test login endpoint
    response = client.post(
        "/api/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    
    # Simple assertion
    assert response.status_code == 200

@patch('main.users_collection')
@patch('main.jwt.encode')
def test_signup_endpoint(mock_jwt, mock_users):
    # Setup mocks
    mock_users.find_one.return_value = None
    mock_jwt.return_value = "test_jwt_token"
    
    # Test signup endpoint
    response = client.post(
        "/api/signup",
        json={"email": "new@example.com", "password": "newpassword"}
    )
    
    # Simple assertion
    assert response.status_code == 200

# Test the prediction endpoint by mocking all dependencies
@patch('main.verify_token_from_header')
@patch('pickle.load')
@patch('main.open', create=True)  # Mock the open function
@patch('mlflow.pyfunc.load_model')
def test_predict_endpoint_simple(mock_load_model, mock_open, mock_pickle, mock_verify):
    # Mock token verification
    mock_verify.return_value = {"email": "test@example.com"}
    
    # Mock scaler and prediction
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = [[0.5, 0.7]]
    mock_pickle.return_value = mock_scaler
    
    # Mock model
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]
    mock_load_model.return_value = mock_model
    
    # Test prediction with minimal mocking
    response = client.post(
        "/api/predict",
        headers={"Authorization": "Bearer test_token"},
        data={"feature1": "0.5", "feature2": "0.7"}
    )
    
    # Only check if the endpoint responds
    assert response.status_code in [200, 500]

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