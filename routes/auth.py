from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from functions.functions import generate_token
from loader import db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str



@router.post("/register")
def register(user: UserCreate):
    try:
        email = user.email
        username = user.username
        password = user.password
        
        if db.check_email_exists(email):
            return {"message": "Email already exists."}
        if db.check_username_exists(username):
            return {"message": "Username already exists."}

        token = generate_token()
        user_id = db.register_user(username, email, password, token)

        return {"user_id": user_id, "access_token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    try:
        db_user = db.login_user(user.username, user.password)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        user_id = db_user['id']
        token = generate_token()
        db.update_user_token(user_id, token)
        return {"user_id": user_id, "access_token": token}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/login_with_token")
def login_with_token(token: str):
    try:
        db_user = db.login_by_token(token)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        user_id = db_user['id']
        username = db_user['username']
        return {"user_id": user_id, "username": username,  "access_token": token}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = decode_access_token(token)
#         if payload is None:
#             raise credentials_exception
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         return user_id
#     except Exception:
#         raise credentials_exception