"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database.session import get_db
from database.models import User, Organization
from services.auth_service import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user_by_email
)
from middleware.auth import get_current_user
from datetime import timedelta
from typing import Optional

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    organization_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    first_name: Optional[str]
    last_name: Optional[str]
    organization_id: str
    organization_name: str

    class Config:
        from_attributes = True


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user and organization"""
    # Check if user exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create organization
    org = Organization(name=user_data.organization_name)
    db.add(org)
    db.flush()
    
    # Create user
    user = User(
        organization_id=org.id,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role="admin",  # First user is admin
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.refresh(org)
    
    # Create token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_delta=timedelta(days=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": str(org.id),
            "organization_name": org.name
        }
    }


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_delta=timedelta(days=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": str(user.organization_id),
            "organization_name": user.organization.name
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "organization_id": str(current_user.organization_id),
        "organization_name": current_user.organization.name
    }


@router.post("/logout")
async def logout():
    """Logout (client should remove token)"""
    return {"message": "Logged out successfully"}




