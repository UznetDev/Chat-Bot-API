from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loader import db
from routes import auth, user_page, promts


description = """
# Project: ChatBot Service

This project is a **FastAPI-based chatbot service** that provides various functionalities, such as user authentication, chatbot interaction, and model management. The service includes endpoints for user authentication, personalized user pages, and handling prompts.

---

## Features:
1. **User Authentication**:
   - User registration and login.
   - Secure authentication using tokens.

2. **Chatbot Interaction**:
   - Supports document retrieval-based AI models.
   - Enables chat history management.
   - Allows custom model creation and usage.

3. **Prompt Management**:
   - Handle and manage user prompts for conversational AI.

4. **Database Management**:
   - Dynamic database table creation for users, models, chats, and messages.

5. **CORS Support**:
   - Fully configurable Cross-Origin Resource Sharing (CORS) to enable interactions from different domains.

---


## Middleware:
### CORS Middleware
The project includes **CORS middleware** to allow cross-origin requests. This is configured with the following settings:
- `allow_origins`: Allows requests from any origin (`*`).
- `allow_credentials`: Permits cookies and other credentials.
- `allow_methods`: Allows all HTTP methods.
- `allow_headers`: Accepts all headers.

---

## API Routes:
### **Authentication (`/auth`)**
Handles user authentication, including registration, login, and token validation.
- **Tags**: `Authentication`

### **User (`/user`)**
Manages user-specific pages and functionalities.
- **Tags**: `User`

### **Prompts (`/promts`)**
Handles prompt interactions for the chatbot.
- **Tags**: `Promts`

---

## Database Tables:
1. **`Users Table`**:
   - Stores user data (e.g., username, password, tokens).


2. **`Models Table`**:
   - Stores AI model metadata (e.g., name, description, visibility).


3. **`Chats Table`**:
   - Stores chat session metadata.


4. **`Chat Messages Table`**:
   - Stores chat messages for history tracking.

---
"""

app = FastAPI(title="ChatBot Service",
            description=description,
            version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_page.router, prefix="/user", tags=["User"])
app.include_router(promts.router, prefix="/promts", tags=["Promts"])

db.create_user_table()
db.create_table_models()
db.create_chats_table()
db.create_table_chat_messages()