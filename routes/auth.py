from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
import uuid

from db.database import Database
from data.config import (
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE,
    ADMIN_USERNAME, ADMIN_PASSWORD
)
from functions.auth import create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database ulanish
db = Database(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
db.create_user_table()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    device_id: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
    device_id: Optional[str] = None

@router.post("/register")
def register(user: UserCreate):
    try:
        user_id = db.register_user(
            user.username, 
            user.email, 
            user.password, 
            user.device_id
        )
        token = create_access_token({"sub": str(user_id)})
        return {"user_id": user_id, "access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserLogin):
    db_user = db.login_user(user.username, user.password)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Device ID yangilash
    if user.device_id and user.device_id != db_user.get('device_id'):
        db.update_device_id(db_user['id'], user.device_id)
    
    token = create_access_token({"sub": str(db_user['id'])})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/device-login")
def device_login(device_id: str):
    db_user = db.login_by_device_id(device_id)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user found with this device"
        )
    
    token = create_access_token({"sub": str(db_user['id'])})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except Exception:
        raise credentials_exception