from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth

app = FastAPI(title="User Authentication Service")

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Barcha domenlardan kirish
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Marshrutlarni qo'shish
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)