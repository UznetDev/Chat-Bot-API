from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from functions.functions import generate_token
from loader import db


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    """
    Data model for user registration.
    
    Attributes:
        username (str): The desired username for the new user.
        email (str): The user's email address.
        password (str): The user's password.
    """
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    """
    Data model for user login.
    
    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """
    username: str
    password: str



@router.post("/register")
def register(user: UserCreate):
    """
    Registers a new user by validating their information and storing it in the database.

    Parameters:
        user (UserCreate): A Pydantic model containing the user's username, email, and password.

    Returns:
        dict: A dictionary containing the new user's ID and access token.

    Raises:
        HTTPException: If an error occurs during registration or if the email/username already exists.

    How it works:
        1. Extracts the `username`, `email`, and `password` from the `user` object.
        2. Checks if the `email` or `username` already exists using database methods.
        3. If unique, generates a token and registers the user in the database.
        4. Returns the newly created user ID and access token.

    Example:

        >>> user_data = {"username": "john_doe", "email": "john@example.com", "password": "secure123"}
        >>> response = register(UserCreate(**user_data))
        >>> response
        {"user_id": 1, "access_token": "random_token"}
    """
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
    """
    Logs in an existing user by validating their credentials.

    Parameters:
        user (UserLogin): A Pydantic model containing the user's username and password.

    Returns:
        dict: A dictionary containing the user's ID and a new access token.

    Raises:
        HTTPException: If the username or password is incorrect, or if an error occurs.

    How it works:
        1. Fetches the user from the database by matching the `username` and `password`.
        2. If a match is found, generates a new access token and updates it in the database.
        3. Returns the user ID and access token.

    Example:

        >>> user_data = {"username": "john_doe", "password": "secure123"}
        >>> response = login(UserLogin(**user_data))
        >>> response
        {"user_id": 1, "access_token": "new_random_token"}
    """
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
    """
    Logs in a user using an existing token.

    Parameters:
        token (str): The access token to authenticate the user.

    Returns:
        dict: A dictionary containing the user's ID, username, and the access token.

    Raises:
        HTTPException: If the token is invalid or if an error occurs.

    How it works:
        1. Fetches the user from the database using the provided token.
        2. If the token is valid, retrieves the user's information (ID and username).
        3. Returns the user ID, username, and token.

    Example:
    
        >>> response = login_with_token("valid_token")
        >>> response
        {"user_id": 1, "username": "john_doe", "access_token": "valid_token"}
    """
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