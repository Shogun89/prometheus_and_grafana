from passlib.context import CryptContext
from typing import Optional

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to check against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash from a plain password.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def validate_password(password: str) -> Optional[str]:
    """
    Validate password strength.
    
    Args:
        password (str): The password to validate
        
    Returns:
        Optional[str]: Error message if validation fails, None if password is valid
    """
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter"
        
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter"
        
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number"
        
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return "Password must contain at least one special character"
    
    return None 