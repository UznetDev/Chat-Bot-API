from fastapi import HTTPException
from loader import db, model
from fastapi import APIRouter



router = APIRouter()



@router.get("/get_models")
def get_models(token: str):
    try:
        check_token = db.login_by_token(token) is None
        if check_token:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        models = db.get_models_list()
        return {"status": 200, "models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/answer")
def get_answer(question: str, model_name: str, chat_id: int, token: str):
    try:
        if not db.login_by_token(token):
            raise HTTPException(status_code=401, detail="Invalid token")

        check_model = db.check_model_exists(model_name)
        if not check_model:
            raise HTTPException(status_code=404, detail="Model not found")

        check_chat = db.check_chat_exists(chat_id)
        if not check_chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        user_info = db.login_by_token(token)
        user_id = user_info['id']
        chat_history = db.get_chat_messages(chat_id, user_id)
        if not chat_history:
            chat_history = []
        
        chat_count = len(chat_history)
        if chat_count > 20:
            raise HTTPException(status_code=404, detail="Limt used up")

        promts = model.create_promts(question, chat_history)

        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=question, role='user')

        answer = model.get_answer(promts, model_name)

        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=answer, role="assistant")
        
        return {"status": 200, "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
