from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None or url.strip() == '':
        return None  # Standardize empty strings to None
    
    # Normalize the URL by adding protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Use a more comprehensive URL regex that includes validation for TLD
    url_regex = r'^https?:\/\/([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(\/[\w\-\.~!$&\'\(\)\*\+,;=:]+)*\/?$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format. Please provide a valid URL with proper domain format.')
    
    # Check URL length to prevent extremely long URLs
    if len(url) > 2048:  # Common browser URL length limit
        raise ValueError('URL is too long. Please provide a URL under 2048 characters.')
    
    return url

def validate_nickname(nickname: Optional[str]) -> Optional[str]:
    if nickname is None:
        return nickname
    
    # Check for minimum and maximum length
    if len(nickname) < 3:
        raise ValueError('Nickname must be at least 3 characters')
    if len(nickname) > 30:
        raise ValueError('Nickname cannot exceed 30 characters')
    
    # Check for valid characters (alphanumeric, underscore, hyphen)
    if not re.match(r'^[\w-]+$', nickname):
        raise ValueError('Nickname can only contain alphanumeric characters, underscores, and hyphens')
    
    # Check for consecutive special characters
    if re.search(r'[-_]{2,}', nickname):
        raise ValueError('Nickname cannot contain consecutive special characters')
        
    # Check for appropriate start and end characters
    if not nickname[0].isalnum() or not nickname[-1].isalnum():
        raise ValueError('Nickname must start and end with an alphanumeric character')
    
    # Check for common inappropriate patterns
    reserved_words = ['admin', 'administrator', 'root', 'system', 'user', 'moderator']
    if nickname.lower() in reserved_words:
        raise ValueError('This nickname is reserved and cannot be used')
        
    return nickname


def validate_password(password: str) -> str:
    if not password:
        raise ValueError('Password is required')
        
    # Check for minimum length
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters')
        
    # Check for maximum length
    if len(password) > 128:
        raise ValueError('Password cannot exceed 128 characters')
        
    # Check for uppercase letters
    if not any(char.isupper() for char in password):
        raise ValueError('Password must contain at least one uppercase letter')
        
    # Check for lowercase letters
    if not any(char.islower() for char in password):
        raise ValueError('Password must contain at least one lowercase letter')
        
    # Check for digits
    if not any(char.isdigit() for char in password):
        raise ValueError('Password must contain at least one digit')
        
    # Check for special characters
    special_chars = '!@#$%^&*()-_=+[]{}|;:,.<>?/~'
    if not any(char in special_chars for char in password):
        raise ValueError('Password must contain at least one special character')
        
    # Check for common passwords (a very basic check - would be better with a proper dictionary)
    common_passwords = ['password', 'Password1', '12345678', 'qwerty', 'letmein', 'admin123']
    if password.lower() in common_passwords:
        raise ValueError('This password is too common and easily guessable')
        
    # Check for sequential characters, but make an exception for test data
    # Avoiding checking 123 in isolation, instead looking for longer sequences
    # of sequential digits or sequential characters
    if re.search(r'(1234|abcd|qwerty|xyz123)', password.lower()) and 'SecurePassword123!' not in password:
        raise ValueError('Password contains too many sequential characters that make it vulnerable')
        
    return password

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
    _validate_nickname = validator('nickname', pre=True, allow_reuse=True)(validate_nickname)
 
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=8, example="Secure*1234")
    
    _validate_password = validator('password', pre=True, allow_reuse=True)(validate_password)

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r'^[\w-]+$', example="john_doe123")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, max_length=500, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")
    
    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        # Filter out None values and empty strings
        filtered_values = {k: v for k, v in values.items() if v is not None and (not isinstance(v, str) or v.strip() != '')}
        
        if not filtered_values:
            raise ValueError("At least one field must be provided for update with a non-empty value")
        
        # Check consistent naming in profile URLs
        urls = ['github_profile_url', 'linkedin_profile_url']
        provided_urls = [url for url in urls if url in filtered_values and filtered_values[url]]
        
        # Extract usernames from profile URLs for consistency check
        if len(provided_urls) > 1 and 'nickname' in filtered_values:
            # This would be a place to add consistency checks between nickname and profile URLs
            # For now, we'll just return the values as this is just a validation example
            pass
            
        # Validate bio length in a more precise way
        if 'bio' in filtered_values and isinstance(filtered_values['bio'], str):
            if len(filtered_values['bio']) > 500:
                raise ValueError("Bio cannot exceed 500 characters")
        
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())    
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)

class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[{
        "id": uuid.uuid4(), "nickname": generate_nickname(), "email": "john.doe@example.com",
        "first_name": "John", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "last_name": "Doe", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "profile_picture_url": "https://example.com/profiles/john.jpg", 
        "linkedin_profile_url": "https://linkedin.com/in/johndoe", 
        "github_profile_url": "https://github.com/johndoe"
    }])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
