import os
from environs import Env

# .env faylini yuklash
env = Env()
env.read_env()

# MySQL sozlamalari
MYSQL_HOST = env.str('MYSQL_HOST')
MYSQL_USER = env.str('MYSQL_USER')
MYSQL_PASSWORD = env.str('MYSQL_PASSWORD')
MYSQL_DATABASE = env.str('MYSQL_DATABASE')

# Admin ma'lumotlari
ADMIN_USERNAME = env.str('ADMIN_USERNAME')
ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')

OPENAI_API_KEY = env.str("OPENAI_API_KEY")


VECTOR_STORAGE_DIR = "./document_vectorstores"
METADATA_FILE = os.path.join(VECTOR_STORAGE_DIR, "document_metadata.json")