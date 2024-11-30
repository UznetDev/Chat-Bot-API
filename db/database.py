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

    def create_user_table(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                device_id VARCHAR(255),
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Create table error: {err}")
            raise

    def hash_password(self, password):
        # Parolni hash qilish (salt bilan)
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${hashed_password}"

    def verify_password(self, stored_password, provided_password):
        # Kiritilgan parolni tekshirish
        salt, hash_value = stored_password.split('$')
        new_hash = hashlib.sha256((salt + provided_password).encode()).hexdigest()
        return new_hash == hash_value

    def register_user(self, username, email, password, device_id=None):
        try:
            hashed_password = self.hash_password(password)
            sql = """
            INSERT INTO users 
            (username, email, password, device_id) 
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

    def login_by_device_id(self, device_id):
        try:
            sql = "SELECT * FROM users WHERE device_id = %s"
            self.cursor.execute(sql, (device_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logging.error(f"Device login error: {err}")
            raise

    def update_device_id(self, user_id, device_id):
        try:
            sql = "UPDATE users SET device_id = %s WHERE id = %s"
            self.cursor.execute(sql, (device_id, user_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Device ID update error: {err}")
            raise

    def close(self):
        if hasattr(self, 'connection'):
            self.cursor.close()
            self.connection.close()