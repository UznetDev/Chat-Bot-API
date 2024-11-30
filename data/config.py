import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# MySQL sozlamalari
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Admin ma'lumotlari
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")