import pytest
import jwt
from datetime import datetime, timedelta
from app.services.jwt_service import create_access_token, decode_token
from app.dependencies import get_settings

settings = get_settings()

def test_create_access_token():
    # Test data
    data = {"sub": "test@example.com", "role": "AUTHENTICATED"}
    expires_delta = timedelta(minutes=15)
    
    # Create token
    token = create_access_token(data=data, expires_delta=expires_delta)
    
    # Verify token is a string
    assert isinstance(token, str)
    
    # Decode the token to verify contents
    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    
    # Check token contains expected data
    assert decoded["sub"] == "test@example.com"
    assert decoded["role"] == "AUTHENTICATED"
    
    # Check expiration time is set correctly
    assert "exp" in decoded
    expiration = datetime.fromtimestamp(decoded["exp"])
    # Verify expiration is in the future
    assert expiration > datetime.utcnow()

def test_create_access_token_default_expiry():
    # Test with default expiry time
    data = {"sub": "default@example.com", "role": "ADMIN"}
    
    # Create token without specifying expiry
    token = create_access_token(data=data)
    
    # Decode token
    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    
    # Check token contains expected data
    assert decoded["sub"] == "default@example.com"
    assert decoded["role"] == "ADMIN"
    
    # Check default expiration time is set correctly
    expiration = datetime.fromtimestamp(decoded["exp"])
    # Verify expiration is in the future and roughly 15 minutes from now
    delta = expiration - datetime.utcnow()
    minutes = delta.total_seconds() / 60
    assert 10 < minutes < 20  # Allowing some margin for test execution time

def test_decode_token_valid():
    # Create a token to decode
    test_data = {"sub": "decode@example.com", "role": "MANAGER"}
    token = create_access_token(data=test_data, expires_delta=timedelta(minutes=5))
    
    # Decode the token
    decoded = decode_token(token)
    
    # Verify decoded data
    assert decoded["sub"] == "decode@example.com"
    assert decoded["role"] == "MANAGER"

def test_decode_token_expired():
    # Create a token that's already expired
    test_data = {"sub": "expired@example.com", "role": "AUTHENTICATED"}
    
    # Create token with negative expiry (already expired)
    expires_delta = timedelta(seconds=-1)
    token = create_access_token(data=test_data, expires_delta=expires_delta)
    
    # Try to decode the expired token
    decoded = decode_token(token)
    assert decoded is None

def test_decode_token_invalid_signature():
    # Create a token with incorrect signature
    payload = {
        "sub": "invalid@example.com",
        "role": "AUTHENTICATED",
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    # Use wrong secret key
    invalid_token = jwt.encode(payload, "wrong_secret_key", algorithm=settings.jwt_algorithm)
    
    # Attempt to decode with correct secret key should fail
    decoded = decode_token(invalid_token)
    assert decoded is None

def test_decode_token_malformed():
    # Test with malformed token
    malformed_token = "not.a.valid.token"
    
    decoded = decode_token(malformed_token)
    assert decoded is None
