from fastapi import HTTPException
from loader import db, model
from fastapi import File, Form, UploadFile, APIRouter
import shutil
from data.config import VECTOR_STORAGE_DIR
import openai


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
            db.update_chat_name(chat_id=chat_id, name=question[:10]+'...')

        model_info = db.get_model_infos(user_id=user_id, model_name=model_name)
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
        print(promts)
        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=question, role='user', model_id=model_info['id'])
        
        answer = model.get_answer(api_key=user_info['api_key'], prompt=promts, model_data=model_info, query=question)

        db.save_chat_message(chat_id=chat_id, 
                             user_id=user_id, 
                             content=answer, 
                             role="assistant", 
                             model_id=model_info['id'])
        
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
        data = db.get_model_infos(user_id=user_id, model_name=model_name)
        if data is None:
            raise HTTPException(status_code=404, detail="Model not found")
        return {"status": 200, "model_data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_model/")
async def upload_file(file: UploadFile = File(...), 
                      model_name: str = Form(...), 
                      description: str = Form(...),
                      system: str = Form(...),
                      visibility: bool = Form(...),
                      max_tokens: int = Form(...),
                      access_token: str = Form(...)):
    try:
        """
        
        """

        if not file.filename.endswith(".pdf"):
            return HTTPException(status_code=400, detail="Invalid file format. Only PDF files are allowed.")
        user_data = db.login_by_token(access_token)
        if user_data is None:
            return HTTPException(status_code=401, detail="Invalid token")
        
        save_path = f"{VECTOR_STORAGE_DIR}/{model_name}.pdf"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        user_id = user_data['id']
        
        doc_id = model.add_document(pdf_path=save_path, document_name=model_name, api_key=user_data['api_key'])

        save_db = db.insert_model(name=model_name, 
                                  description=description,
                                  system=system,
                                  visibility=visibility,
                                  max_tokens=max_tokens,
                                  creator_id=user_id,
                                  model_type='rag_model',
                                  doc_id=doc_id)
        if save_db is None:
            return HTTPException(status_code=401, detail="Moodel building fail in save to db")

        if doc_id is not None:
            return {"status_code": 200, "doc_id": doc_id}
        else:
            return HTTPException(status_code=401, detail="Moodel building fail in embedding")
    except openai.AuthenticationError as e:
        return HTTPException(status_code=401, detail=e.message)
    except Exception as err:
        return HTTPException(status_code=401, detail=str(err))
        

@router.delete("delete_model")
def delete_model(model_id: str, access_token: str):
    """
    
    """

    user_data = db.login_by_token(access_token)
    if user_data is None:
        return HTTPException(status_code=401, detail="Invalid token")
    user_id = user_data['id']
    model_info = db.get_model_infos(user_id=user_id, model_id=model_id)
    if model_info is None:
        return HTTPException(status_code=404, detail="Model not found")
    if model_info['creator_id'] != user_id:
        return HTTPException(status_code=403, detail="You are not the owner of this model")

    delete = db.delete_model(model_id=model_id, user_id=user_id)

    if delete:
        return {"status": 200, "message": "Model deleted successfully"}
    else:
        return HTTPException(status_code=500, detail="Failed to delete model")