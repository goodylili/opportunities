import os
import psycopg2
from psycopg2 import OperationalError


def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'default_db_name'),
            user=os.getenv('DB_USER', 'default_user'),
            password=os.getenv('DB_PASSWORD', 'default_password'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        print("Connection to PostgreSQL DB successful")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")






