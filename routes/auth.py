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
        surname: (str): The user's Surname.
        name: (str): The user's Name.
        api_key: (str): The user's OpenAI API key.

    """
    username: str
    email: str
    password: str
    surname: str
    name: str
    api_key: str


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
@router.get("/register")
def register(user: UserCreate):
    """
    Registers a new user by validating their information and storing it in the database.

    Parameters:
        user (UserCreate): A Pydantic model containing the user's username, email, password, surname, surnarme api api_key.

    Returns:
        dict: A dictionary containing the new user's ID and access token: {"user_id": 1, "access_token": "random_token"}.

    Raises:
        HTTPException(status_code=400, detail='Error message'): If an error occurs during registration.

    How it works:
        1. Extracts the `username`, `email`, and `password` from the `user` object.
        2. Checks if the `email` or `username` already exists using database methods.
        3. If unique, generates a token and registers the user in the database.
        4. Returns the newly created user ID and access token.
        5. if email already exist's return {"message": "Email already exists."}
        6. if username already exist's return {"message": "Username already exists."}

    Note:
        This function assumes that the `db` object has methods `check_email_exists`, `check_username_exists`, and `register_user`.

    Example:

        >>> user_data = {"username": "john_doe", "email": "john@example.com", "password": "secure123"}
        >>> response = register(UserCreate(**user_data))
        >>> response
        >>> {"user_id": 1, "access_token": "random_token"}
    """
    try:
        email = user.email
        username = user.username
        password = user.password
        surname = user.surname
        name = user.name
        api_key = user.api_key

        
        if db.check_email_exists(email):
            return {"message": "Email already exists."}
        if db.check_username_exists(username):
            return {"message": "Username already exists."}

        access_token = generate_token()
        user_id = db.register_user(username=username,
                                   email=email,
                                   password=password,
                                   surname=surname,
                                   name=name,
                                   api_key=api_key,
                                   access_token=access_token)

        return {"user_id": user_id, "access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
@router.get("/login")
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
        3. Returns the user data and new access token.

    Example:

        >>> user_data = {"username": "john_doe", "password": "secure123"}
        >>> response = login(UserLogin(**user_data))
        >>> response
        >>> {"id": 1433,
        >>> "username": "john_doe",
        >>> "name": "John",
        >>> "surname": "Doe",
        >>> "api_key": "sk_.....",
        >>> "phone_number": "DATE" or null,
        >>> "last_login": 'DATE"  or null, 
        >>> "date_joined": "DATETIME",
        >>> "email": "john@gmail.com",
        >>> "access_token": "unique acses token"
        >>> }
    """
    try:
        user_data = db.login_user(user.username, user.password)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        

        user_data['access_token'] = generate_token()

        db.update_user_token(user_data['id'], user_data['access_token'])
        user_data.pop('password')
        return user_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login_with_token")
@router.get("/login_with_token")
def login_with_token(access_token: str):
    """
    Logs in a user using an existing token.

    Parameters:
        access_token (str): The access token to authenticate the user.

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
        user_data = db.login_by_token(access_token)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        user_data.pop('password')
        return user_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))