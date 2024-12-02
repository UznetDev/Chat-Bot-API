from fastapi import HTTPException
from loader import db, model
from fastapi import APIRouter


router = APIRouter()


@router.get("/get_models")
def get_models(token: str):
    try:
        check_token = db.login_by_token(token) is None
        if check_token:
            return HTTPException(status_code=401, detail="Invalid token")
        
        models = db.get_models_list()
        return {"status": 200, "models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/answer")
def get_answer(question: str, chat_id: int, token: str, model_id=None):
    try:
        chat_info = db.check_chat_exists(chat_id)
        if chat_info is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        if model_id is None:
            model_id = chat_info['model_id']
        model_info = db.get_model_infos(model_id)
        if model_info is None:
            raise HTTPException(status_code=404, detail="Model not found")
        model_name = model_info['name']
        
        if not db.login_by_token(token):
            raise HTTPException(status_code=401, detail="Invalid token")
        
        db.update_chat_model(chat_id=chat_id, model_id=model_id)

        user_info = db.login_by_token(token)
        user_id = user_info['id']
        chat_history = db.get_chat_messages(chat_id, user_id)
        if not chat_history:
            chat_history = []
        
        chat_count = len(chat_history)
        if chat_count > 20:
            raise HTTPException(status_code=404, detail="Limt used up")

        promts = model.create_promts(question, chat_history)

        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=question, role='user', model_id=model_id)

        answer = """
Here's a simple Python code to print "Hello, World!":

```python
print("Hello, World!")
```

This is the standard way to output "Hello, World!" in Python. Let me know if you'd like variations or something more!
"""#model.get_answer(promts, model_name)

        db.save_chat_message(chat_id=chat_id, user_id=user_id, content=answer, role="assistant", model_id=model_id)
        
        return {"status": 200, "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
