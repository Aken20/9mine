import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Get JWT secret key from environment, or use a default for development
JWT_SECRET = os.getenv("JWT_SECRET", "test")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "30"))

# Security scheme for JWT bearer token authentication
security = HTTPBearer()

class JWTHandler:
    """
    Custom JWT handler for token creation and validation
    """
    def __init__(self):
        self.secret_key = JWT_SECRET
        self.algorithm = JWT_ALGORITHM

    def encode_token(self, username, user_type="regular", token_type="access"):
        """
        Generate a JWT token with username as the subject and user_type to distinguish between students and regular users
        """
        # Set appropriate expiration time based on token type
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": username,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": token_type,
            "user_type": user_type  # Add user_type to distinguish between students and regular users
        }
        
        # Create the JWT token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        """
        Decode and validate a JWT token
        """
        try:
            # Decode the token and extract the payload
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload["exp"] < datetime.timestamp(datetime.utcnow()):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return payload  # Return the full payload with username and user_type
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Dependency to be used in protected routes
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = JWTHandler().decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Return the full payload with username (sub) and user_type
    return payload