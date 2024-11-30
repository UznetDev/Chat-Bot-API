import mysql.connector
import logging
from datetime import datetime
import hashlib
import uuid

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.reconnect()

    def reconnect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            logging.error(f"Database connection error: {err}")
            raise

    # User Guide
    def create_user_table(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                token VARCHAR(255) UNIQUE,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Create table error: {err}")
            raise


    def register_user(self, username, email, password, device_id=None):
        try:
            hashed_password = self.hash_password(password)
            sql = """
            INSERT INTO users 
            (username, email, password, token) 
            VALUES (%s, %s, %s, %s)
            """
            values = (username, email, hashed_password, device_id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            logging.error(f"User registration error: {err}")
            raise

    def login_user(self, username, password):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            user = self.cursor.fetchone()

            if user and self.verify_password(user['password'], password):
                return user
            return None
        except mysql.connector.Error as err:
            logging.error(f"Login error: {err}")
            raise

    def check_username_exists(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            logging.error(f"Username check error: {err}")
            raise

    def check_email_exists(self, email):
        try:
            sql = "SELECT * FROM users WHERE email = %s"
            self.cursor.execute(sql, (email,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            logging.error(f"Email check error: {err}")
            raise


    def login_by_token(self, token):
        try:
            sql = "SELECT * FROM users WHERE token = %s"
            self.cursor.execute(sql, (token,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logging.error(f"Token login error: {err}")
            raise

    def update_user_token(self, user_id, token):
        try:
            sql = "UPDATE users SET token = %s WHERE id = %s"
            self.cursor.execute(sql, (token, user_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Token update error: {err}")
            raise

    # Chat Guide
    def create_chats_table(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS chats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                name VARCHAR(50),
                model_id INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Create chat table error: {err}")
            raise
    
    def create_table_chat_messages(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id INT,
                user_id INT,
                role VARCHAR(100),
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Create chat messages table error: {err}")


    def get_user_chat_list(self, user_id):
        """
        This function retrieves a list of chats for a specific user.
        """

        try:
            sql = "SELECT id, name, timestamp FROM chats WHERE user_id = %s ORDER BY timestamp DESC "
            self.cursor.execute(sql, (user_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(f"Get chat list error: {err}")
            raise


    def get_chat_data(self, chat_id, user_id):
        try:
            sql = "SELECT * FROM chat_messages WHERE chat_id=%s AND user_id=%s"
            self.cursor.execute(sql, (chat_id, user_id))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logging.error(f"Get chat data error: {err}")


    def create_new_chat(self, user_id, name):
        try:
            sql = "INSERT INTO chats (user_id, name) VALUES (%s, %s)"
            self.cursor.execute(sql, (user_id, name))
            self.connection.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            logging.error(f"Create new chat error: {err}")
            raise

    def save_chat_message(self, chat_id, user_id, role, content):
        try:
            sql = "INSERT INTO chat_messages (chat_id, user_id, role, content) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (chat_id, user_id, role, content))
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Save chat message error: {err}")
            raise

    def get_chat_messages(self, chat_id, user_id):
        try:
            sql = "SELECT * FROM chat_messages WHERE chat_id = %s AND user_id = %s ORDER BY timestamp ASC"
            self.cursor.execute(sql, (chat_id, user_id))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(f"Get chat messages error: {err}")
            raise

    def check_chat_exists(self, chat_id):
        try:
            sql = "SELECT * FROM chats WHERE id = %s"
            self.cursor.execute(sql, (chat_id,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            logging.error(f"Check chat exists error: {err}")
            raise


    def delete_chat(self, chat_id, user_id):
        try:
            sql = "DELETE FROM chats WHERE id = %s AND user_id = %s"
            self.cursor.execute(sql, (chat_id, user_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Delete chat error: {err}")
            raise

    def delete_chat_messages(self, chat_id, user_id):
        try:
            sql = "DELETE FROM chat_messages WHERE chat_id = %s AND user_id = %s"
            self.cursor.execute(sql, (chat_id, user_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Delete chat messages error: {err}")
            raise

    def get_chat_name(self, chat_id, user_id):
        try:
            sql = "SELECT name FROM chats WHERE id = %s AND user_id = %s"
            self.cursor.execute(sql, (chat_id, user_id))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            logging.error(f"Get chat name error: {err}")
            raise

  


    # HASh
    def hash_password(self, password):
        """
        This function hashes a password using SHA-256.
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, hashed_password, user_password):
        """
        This function verifies a password by comparing its hashed version.
        """
        return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()
    
    # Model

    def create_table_models(self):
        """
        This function creates the models table in the database.
        """
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS models (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                type VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()

            # add 3 models
            models = [
                ("gpt-4o-mini", "More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration.", "chat"),
                ("gpt-3.5-turbo", "Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.", "chat"),
                ("gpt-4", "More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration.", "chat"),
    
            ]

            for model in models:
                self.cursor.execute("SELECT * FROM models WHERE name = %s", (model[0],))
                if self.cursor.fetchone() is None:
                    self.cursor.execute("INSERT INTO models (name, description, type) VALUES (%s, %s, %s)", model)
                    self.connection.commit()

        except mysql.connector.Error as err:
            logging.error(f"Create models table error: {err}")


    def get_models_list(self):
        try:
            sql = "SELECT * FROM models"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(f"Get models list error: {err}")

    def check_model_exists(self, model_name):
        try:
            sql = "SELECT * FROM models WHERE name = %s"
            self.cursor.execute(sql, (model_name,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            logging.error(f"Check model exists error: {err}")



    def close(self):
        if hasattr(self, 'connection'):
            self.cursor.close()
            self.connection.close()