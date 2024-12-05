from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
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
        surname (str): The user's surname.
        name (str): The user's first name.
        api_key (str): The user's OpenAI API key.
    """
    username: str
    email: str
    password: str
    surname: str
    name: str
    api_key: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "example_username",
                "email": "example@example.com",
                "password": "example_password",
                "surname": "example_surname",
                "name": "example_name",
                "api_key": "example_api_key",
            }
        }


class UserLogin(BaseModel):
    """
    Data model for user login.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "example_username",
                "password": "example_password",
            }
        }


class UserUpdate(BaseModel):
    """
    Data model for updating user information.

    Attributes:
        id (int): The unique ID of the user.
        access_token (str): The access token for authentication.
        email (Optional[str]): The new email address for the user.
        surname (Optional[str]): The new surname for the user.
        name (Optional[str]): The new name for the user.
        api_key (Optional[str]): The new OpenAI API key for the user.
        phone_number (Optional[str]): The new phone number for the user.
    """
    id: int
    access_token: str
    email: Optional[str] = None
    surname: Optional[str] = None
    name: Optional[str] = None
    api_key: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "access_token": "valid_token",
                "email": "new_email@example.com",
                "surname": "New_Surname",
                "name": "New_Name",
                "api_key": "new_api_key",
                "phone_number": "new_phone_number",
            }
        }


@router.post("/register")
def register(user: UserCreate):
    """
    ## Registers a new user by validating their information and storing it in the database.


    ## Parameters:

    * `user (UserCreate)`: A Pydantic model containing the user's username, email, password, surname, surnarme api api_key.

    ## Returns:

    * `dict`: A dictionary containing the new user's ID and access token: {"user_id": 1, "access_token": "random_token"}.

    ## Raises:

    * `HTTPException(status_code=400, detail='Error message')`: If an error occurs during registration.

    ## How it works:
    1. Extracts the `username`, `email`, and `password` from the `user` object.
    2. Checks if the `email` or `username` already exists using database methods.
    3. If email and username is unique than generates a access_token and registers the user in the database.
    4. Returns the newly created user ID and access token.
    5. if email already exist's return ```HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already exists.")```
    6. if username already exist's return ```HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username already exists.")```

    ## Example:

        >>> import requests
        >>> # API URL
        >>> url = "http://api_url/auth/register"  # Replace with actual API URL
        >>> # Request payload
        >>> user_data = {
        >>>     "api_key": "example_api_key",
        >>>     "email": "example@example.com",
        >>>     "name": "example_name",
        >>>     "password": "example_password",
        >>>     "surname": "example_surname",
        >>>     "username": "example_username"
        >>> }
        >>> # Sending a POST request
        >>> response = requests.post(url, json=user_data)
        >>> # Checking the response
        >>> if response.status_code == 200:
        >>>     print("User registered successfully:", response.json())
        >>> else:
        >>>     print("Error:", response.status_code, response.json())
        >>> # Output
        >>> User registered successfully: {'user_id': 1, 'access_token': 'random_token'}
    """
    try:
        email = user.email
        username = user.username
        password = user.password
        surname = user.surname
        name = user.name
        api_key = user.api_key

        if db.check_email_exists(email):
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                 detail="Email already exists.")
        if db.check_username_exists(username):
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                 detail="Username already exists.")

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
def login(user: UserLogin):
    """
    ## Logs in an existing user by validating their credentials.

    ## Parameters:
    * `user (UserLogin)`: *A Pydantic model containing the user's username and password.*

    ## Returns:
    * `dict`: *A dictionary containing the user's data and a new access token.*

    ## Raises:
    * `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")`: *Raised if the username or password is incorrect.*
    * `HTTPException(status_code=400, detail='Error message')`: *Raised for any other error during the login process.*

    ## How it works:
    1. *Fetches the user from the database by matching the `username` and `password`.*
    2. *If a match is found, generates a new access token using `generate_token` and updates it in the database.*
    3. *Removes the `password` from the user data for security reasons.*
    4. *Returns the user's information, including the new access token.*

    ## Example:

        >>> import requests
        >>> # API URL
        >>> url = "http://api_url/auth/login"  # Replace with actual API URL
        >>> # Request payload
        >>> user_data = {"username": "john_doe", "password": "secure123"}
        >>> # Sending a POST request
        >>> response = requests.post(url, json=user_data)
        >>> # Checking the response
        >>> if response.status_code == 200:
        >>>     print("Login successful:", response.json())
        >>> else:
        >>>     print("Error:", response.status_code, response.json())
        >>> # Example Response
        >>> {
        >>>     "id": 1433,
        >>>     "username": "john_doe",
        >>>     "name": "John",
        >>>     "surname": "Doe",
        >>>     "api_key": "sk_.....",
        >>>     "phone_number": "DATE" or null,
        >>>     "last_login": "DATE" or null,
        >>>     "date_joined": "DATETIME",
        >>>     "email": "john@gmail.com",
        >>>     "access_token": "unique_access_token"
        >>> }
    """
    try:
        # Attempt to fetch user data from the database
        user_data = db.login_user(user.username, user.password)

        # If no user data is returned, raise an unauthorized exception
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Generate a new access token for the user
        user_data['access_token'] = generate_token()

        # Update the user's token in the database
        db.update_user_token(user_data['id'], user_data['access_token'])

        # Remove the password from the returned data for security
        user_data.pop('password')

        # Return the user data with the new access token
        return user_data
    except Exception as e:
        # Catch any unexpected errors and raise an HTTPException with details
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login_with_token")
def login_with_token(access_token: str):
    """
    ## Logs in a user using an access token.

    ## Parameters:
    * `access_token (str)`: *A string representing the user's access token.*

    ## Returns:
    * `dict`: *A dictionary containing the user's data, excluding the password.*

    ## Raises:
    * `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")`: *Raised if the provided access token is invalid.*
    * `HTTPException(status_code=400, detail='Error message')`: *Raised for any other errors during the login process.*

    ## How it works:
    1. *Fetches the user data from the database using the provided `access_token`.*
    2. *If no user data is found, raises an `HTTPException` with a 401 status code and the message "Invalid token".*
    3. *Removes the `password` from the user data for security purposes.*
    4. *Returns the user's data.*

    ## Example:

        >>> import requests
        >>> # API URL
        >>> url = "http://api_url/auth/login_with_token"  # Replace with actual API URL
        >>> # Access token payload
        >>> token_payload = {"access_token": "unique_access_token"}
        >>> # Sending a POST request
        >>> response = requests.post(url, json=token_payload)
        >>> # Checking the response
        >>> if response.status_code == 200:
        >>>     print("Login successful:", response.json())
        >>> else:
        >>>     print("Error:", response.status_code, response.json())
        >>> # Example Response
        >>> {
        >>>     "id": 1433,
        >>>     "username": "john_doe",
        >>>     "name": "John",
        >>>     "surname": "Doe",
        >>>     "api_key": "sk_.....",
        >>>     "phone_number": "DATE" or null,
        >>>     "last_login": "DATE" or null,
        >>>     "date_joined": "DATETIME",
        >>>     "email": "john@gmail.com"
        >>> }
    """
    try:
        # Attempt to fetch user data using the provided access token
        user_data = db.login_by_token(access_token)

        # If no user data is found, raise an unauthorized exception
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Remove the password from the returned data for security
        user_data.pop('password')

        # Return the user data
        return user_data
    except Exception as e:
        # Catch any unexpected errors and raise an HTTPException with details
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/update_user')
def update_user(user: UserUpdate):
    """
    ## Updates an existing user's information.

    ## Parameters:
    * `user (UserUpdate)`: *A Pydantic model containing the following fields:*
        - *`id (int)`: The user's ID.*
        - *`access_token (str)`: The user's access token.*
        - *`email (str, optional)`: The user's updated email address.*
        - *`surname (str, optional)`: The user's updated surname.*
        - *`name (str, optional)`: The user's updated name.*
        - *`api_key (str, optional)`: The user's updated API key.*
        - *`phone_number (str, optional)`: The user's updated phone number.*

    ## Returns:
    * `dict`: *A dictionary containing the status of the update and the saved user data.*

    ## Raises:
    * `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")`: *Raised if the provided access token is invalid.*
    * `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Id")`: *Raised if the provided user ID does not match the authenticated user's ID.*
    * `HTTPException(status_code=400, detail="Error message")`: *Raised for any other errors during the update process.*

    ## How it works:
    1. *Fetches the user data from the database using the provided `access_token`.*
    2. *If no user data is found or the `access_token` is invalid, raises an `HTTPException`.*
    3. *Validates that the authenticated user's ID matches the ID provided in the `user` object.*
    4. *Updates the user's information in the database with the provided fields.*
    5. *If the update fails, raises an `HTTPException` with a 401 status code.*
    6. *Returns a status of 200 and the updated user data upon successful completion.*

    ## Example:

        >>> import requests
        >>> # API URL
        >>> url = "http://api_url/auth/update_user"  # Replace with actual API URL
        >>> # Update payload
        >>> user_data = {
        >>>     "id": 1433,
        >>>     "access_token": "valid_access_token",
        >>>     "email": "new_email@example.com",
        >>>     "surname": "UpdatedSurname",
        >>>     "name": "UpdatedName",
        >>>     "api_key": "new_api_key",
        >>>     "phone_number": "+123456789"
        >>> }
        >>> # Sending a PUT request
        >>> response = requests.put(url, json=user_data)
        >>> # Checking the response
        >>> if response.status_code == 200:
        >>>     print("User updated successfully:", response.json())
        >>> else:
        >>>     print("Error:", response.status_code, response.json())
        >>> # Example Response
        >>> {
        >>>     "status": 200,
        >>>     "save": {
        >>>         "id": 1433,
        >>>         "email": "new_email@example.com",
        >>>         "surname": "UpdatedSurname",
        >>>         "name": "UpdatedName",
        >>>         "api_key": "new_api_key",
        >>>         "phone_number": "+123456789"
        >>>     }
        >>> }
    """
    try:
        # Verify the user using their access token
        user_data = db.login_by_token(user.access_token)

        # If the token is invalid, raise an exception
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Verify that the user ID matches the authenticated user's ID
        if user_data['id'] != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Id"
            )
        
        # Update the user's data in the database
        user_data = db.update_user(
            user_id=user.id, 
            email=user.email, 
            surname=user.surname, 
            name=user.name, 
            api_key=user.api_key, 
            phone_number=user.phone_number
        )

        # If the update fails, raise an exception
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Return the status and updated data
        return {"status": 200, "save": user_data}

    except Exception as e:
        # Catch any unexpected errors and raise an HTTPException with details
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/delete_user')
def delete_user(user: UserLogin):
    """
    ## Deletes a user from the database based on the provided credentials.

    ## Parameters:
    * `user (UserLogin)`: *A Pydantic model containing the following fields:*
        - *`username (str)`: The username of the user to be deleted.*
        - *`password (str)`: The password of the user to be deleted.*

    ## Returns:
    * `dict`: *A dictionary containing a success message if the user is deleted successfully.*

    ## Raises:
    * `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")`: *Raised if the username or password is incorrect or the user does not exist.*
    * `HTTPException(status_code=400, detail="Error message")`: *Raised for any other errors during the deletion process.*

    ## How it works:
    1. *Fetches the user from the database using the provided `username` and `password`.*
    2. *If no matching user is found, raises an `HTTPException` with a 401 status code and the message "User not found".*
    3. *Deletes the user from the database if the credentials are valid.*
    4. *Returns a success message upon successful deletion.*

    ## Example:

        >>> import requests
        >>> # API URL
        >>> url = "http://api_url/auth/delete_user"  # Replace with actual API URL
        >>> # Delete payload
        >>> user_data = {
        >>>     "username": "john_doe",
        >>>     "password": "password123"
        >>> }
        >>> # Sending a POST request
        >>> response = requests.post(url, json=user_data)
        >>> # Checking the response
        >>> if response.status_code == 200:
        >>>     print("User deleted successfully:", response.json())
        >>> else:
        >>>     print("Error:", response.status_code, response.json())
        >>> # Example Response
        >>> {"message": "User deleted successfully"}
    """
    try:
        # Attempt to delete the user from the database
        user_data = db.delete_user(user.username, user.password)

        # If no matching user is found, raise an exception
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Return a success message
        return {"message": "User deleted successfully"}

    except Exception as e:
        # Catch any unexpected errors and raise an HTTPException with details
        raise HTTPException(status_code=400, detail=str(e))
