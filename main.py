from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loader import db
from routes import auth, user_page, promts



app = FastAPI(title="User Authentication Service")

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Barcha domenlardan kirish
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_page.router, prefix="/user", tags=["User"])
app.include_router(promts.router, prefix="/promts", tags=["Promts"])

db.create_chats_table()
db.create_table_chat_messages()
db.create_user_table()
db.create_table_models()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)