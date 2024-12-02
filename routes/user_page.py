from fastapi import HTTPException
from loader import db
from fastapi import APIRouter


router = APIRouter()


@router.post("/get_chats")
def get_chat_list(token: str):
    """
    Retrieves a list of chats for the authenticated user.

    Parameters:
        token (str): The authentication token to verify the user's identity.

    Returns:
        dict: A dictionary containing a list of the user's chats, each with details such as:
            - id (int): The chat ID.
            - name (str): The name of the chat.
            - timestamp (datetime): The creation time of the chat.

    Raises:
        HTTPException:
            - 404: If the user is not found (invalid token).
            - 500: If an internal server error occurs.

    Example:
    
        >>> response = get_chat_list("valid_token")
        >>> response
        {"chats": [{"id": 1, "name": "Chat 1", "timestamp": "2024-01-01T12:00:00"}]}

        >>> response = get_chat_list("invalid_token")
        HTTPException: {"status_code": 404, "detail": "User not found"}
    """
    try:
        user_info = db.login_by_token(token)
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user_info["id"]
        chats = db.get_user_chat_list(user_id)

        return {"chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get_chat_data")
def get_chat_data(token: str, chat_id: int):
    """
    Retrieves the details of a specific chat for the authenticated user.

    Parameters:
        token (str): The authentication token to verify the user's identity.
        chat_id (int): The ID of the chat to retrieve.

    Returns:
        dict: A dictionary containing the chat data, including messages.

    Raises:
        HTTPException:
            - 404: If the user or chat is not found.
            - 500: If an internal server error occurs.

    Example:


        >>> response = get_chat_data("valid_token", 1)
        >>> response
        {"chat_data": [{"role": "user", "content": "Hello!", "timestamp": "2024-01-01T12:01:00"}]}

        >>> response = get_chat_data("invalid_token", 1)
        HTTPException: {"status_code": 404, "detail": "User not found"}
    """
    try:
        user_info = db.login_by_token(token)
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user_info["id"]
        chat_data = db.get_chat_data(chat_id, user_id)

        return {"chat_data": chat_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_chat")
def create_chat(token: str, model_id=1):
    """
    Creates a new chat for the authenticated user.

    Parameters:
        token (str): The authentication token to verify the user's identity.
        model_id (int, optional): The ID of the model to associate with the new chat. Defaults to 1.

    Returns:
        dict: A dictionary containing the ID of the newly created chat.

    Raises:
        HTTPException:
            - 404: If the user is not found (invalid token).
            - 500: If an internal server error occurs.

    Example:


        >>> response = create_chat("valid_token", model_id=2)
        >>> response
        {"chat_id": 42}

        >>> response = create_chat("invalid_token", model_id=2)
        HTTPException: {"status_code": 404, "detail": "User not found"}
    """
    try:
        user_info = db.login_by_token(token)
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user_info["id"]
        chat_id = db.create_new_chat(user_id, 'Unknown', model_id)

        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
