from fastapi import HTTPException
from loader import db, model
from fastapi import APIRouter


router = APIRouter()


@router.get("/get_models")
def get_models(access_token: str):
    """
    Fetches a list of available models for the authenticated user.

    Parameters:
        access_token (str): The authentication token to verify the user's identity.

    Returns:
        dict: A dictionary containing the status code and a list of models.

    Raises:
        HTTPException:
            - 401: If the token is invalid.
            - 500: If an internal server error occurs.

    How it works:
        1. Verifies the provided token.
        2. If the token is valid, retrieves the list of models from the database.
        3. Returns the list of models in a dictionary with a status code.

    Example:

        >>> response = get_models("valid_token")
        >>> response
        {"status": 200, "models": ["model1", "model2", "model3"]}

        
        >>> response = get_models("invalid_token")
        HTTPException: {"status_code": 401, "detail": "Invalid token"}
    """
    try:
        user_data = db.login_by_token(access_token)
        if user_data is None:
            return HTTPException(status_code=401, detail="Invalid token")
        user_id = user_data['id']
        models = db.get_models_list(user_id)
        return {"status": 200, "models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/answer")
def get_answer(question: str, chat_id: int, access_token: str, model_name: str):
    """
    Retrieves an AI-generated answer based on the user's question, chat history, and the specified model.

    Parameters:
        question (str): The user's question.
        chat_id (int): The unique identifier of the chat.
        token (str): The authentication token to verify the user's identity.
        model_id (Optional[int]): The ID of the AI model to use. If not provided, the chat's default model is used.

    Returns:
        dict: A dictionary containing the status code and the AI-generated answer.

    Raises:
        HTTPException:
            - 401: If the token is invalid.
            - 404: If the chat or model is not found, or if the chat message limit is exceeded.
            - 500: If an internal server error occurs.

    How it works:
        1. Verifies the `chat_id` exists in the database.
        2. Retrieves the model ID if not provided, and validates its existence.
        3. Authenticates the user using the token.
        4. Updates the chat's associated model in the database.
        5. Fetches the user's chat history for the specified chat.
        6. Limits the chat history to 20 messages. If exceeded, returns an error.
        7. Constructs a prompt using the user's question and chat history.
        8. Saves the user's question to the database.
        9. Generates an AI answer using the specified model and saves it to the database.
        10. Returns the AI-generated answer.

    Example:


        >>> response = get_answer(
                question="What is AI?",
                chat_id=123,
                token="valid_token",
                model_id=1
            )
        >>> response
        {"status": 200, "answer": "AI stands for Artificial Intelligence."}

        

        >>> response = get_answer(
                question="What is AI?",
                chat_id=123,
                token="invalid_token",
                model_id=1
            )
        HTTPException: {"status_code": 401, "detail": "Invalid token"}
    """
    try:
        user_info = db.login_by_token(access_token)
        user_id = user_info['id']
        chat_info = db.get_chat_info(chat_id, user_id)
        if chat_info is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        if chat_info['name'] == "Unknown":
            db.update_chat_name(chat_id=chat_id, name=question)

        model_info = db.get_model_infos(model_name, user_id)
        if model_info is None:
            raise HTTPException(status_code=404, detail="Model not found")
        
        if not db.login_by_token(access_token):
            raise HTTPException(status_code=401, detail="Invalid token")
        
        db.update_chat_model(chat_id=chat_id, model_id=model_info['id'])


        chat_history = db.get_chat_messages(chat_id, user_id)
        if not chat_history:
            chat_history = []
        
        chat_count = len(chat_history)
        if chat_count > 200:
            raise HTTPException(status_code=404, detail="Limit used up")

        promts = model.create_promts(question, chat_history)

        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=question, role='user', model_id=model_info['id'])

        answer = """
Here's a simple Python code to print "Hello, World!":

```python
print("Hello, World!")
```

This is the standard way to output "Hello, World!" in Python. Let me know if you'd like variations or something more!
"""
        
        #model.get_answer(promts, model_name)

        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=answer, role="assistant", model_id=model_info['id'])
        
        return {"status": 200, "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_model_info")
def get_model_info(model_name: str, access_token: str):

    """
    
    """
    try:
        user_data = db.login_by_token(access_token)
        if user_data is None:
            return HTTPException(status_code=401, detail="Invalid token")
        user_id = user_data['id']
        data = db.get_model_infos(model_name, user_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Model not found")
        return {"status": 200, "model_data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))