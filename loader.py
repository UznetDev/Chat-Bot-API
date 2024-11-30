from db.database import Database
from fastapi import FastAPI
from models.openai_models import Models
from data.config import (
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
)


db = Database(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)

db.create_user_table()

app = FastAPI(
    title="ChatGPT Clone API",
    description="OpenAI Clone Platform API",
    version="1.0.0"
)

model = Models()
