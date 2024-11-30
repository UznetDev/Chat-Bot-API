from fastapi import HTTPException
from loader import db
from fastapi import APIRouter


router = APIRouter()


@router.post("/get_chats")
def get_chat_list(token: str):
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
def create_chat(token: str):
    try:
        user_info = db.login_by_token(token)
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user_info["id"]
        chat_id = db.create_new_chat(user_id, 'Unknown')

        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))