from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from prometheus_fastapi_instrumentator import Instrumentator

from jwt import (
    create_access_token,
    get_current_user,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from password import verify_password, validate_password
from models import AuthUser
from schemas import (
    AuthUserCreate,
    AuthUser as AuthUserSchema,
    Token,
    PasswordReset,
    PasswordChange
)
from database import get_db_session
from crud import (
    get_user_by_email,
    create_user,
    blacklist_token,
    update_password,
    update_last_login
)

# Create router for auth endpoints first
router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

# Define all router endpoints
@router.post("/register", response_model=AuthUserSchema)
async def register_user(
    user: AuthUserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Register a new user."""
    # Validate password strength
    if error_msg := validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
    
    # Check if user exists
    if await get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        db_user = await create_user(db, user)
        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Registration failed"
        )

@router.post("/logout")
async def logout(
    current_user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Logout and blacklist the current token."""
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    await blacklist_token(db, token, expires_at, current_user.id)
    return {"message": "Successfully logged out"}

@router.post("/password-reset", response_model=dict)
async def request_password_reset(
    reset_request: PasswordReset,
    db: AsyncSession = Depends(get_db_session)
):
    """Request a password reset."""
    user = await get_user_by_email(db, email=reset_request.email)
    if user:
        # In a real application, send password reset email here
        pass
    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Change user password."""
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )
    
    # Validate new password
    if error_msg := validate_password(password_change.new_password):
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
    
    await update_password(db, current_user, password_change.new_password)
    return {"message": "Password updated successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """Authenticate user and return JWT token."""
    # Get user by email
    user = await get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user_id
    access_token = create_access_token(
        data={"sub": user.email},
        user_id=user.id
    )
    
    # Update last login timestamp
    await update_last_login(db, user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 

@router.get("/verify")
async def verify_token(
    current_user: AuthUser = Depends(get_current_active_user),
    response: Response = None
):
    """Verify token and return user information for routing."""
    response.headers["X-User-Id"] = str(current_user.id)
    return {"valid": True, "user_id": current_user.id} 

# Create FastAPI app instance after defining all router endpoints
app = FastAPI(
    title="Auth API",
    description="Authentication service with JWT tokens",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add metrics instrumentation
Instrumentator().instrument(app).expose(app)

# Add ping endpoint
@app.get("/ping", tags=["health"])
def ping():
    return {"message": "pong"}

# Include the router in the app
app.include_router(router) 