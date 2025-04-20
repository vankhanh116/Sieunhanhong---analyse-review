import json
import psycopg2

global cur
global conn

import dotenv
import os
dotenv.load_dotenv()


POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

def init_db():
    global conn, cur  # Khai báo cả hai biến global trên cùng một dòng
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user="POSTGRES_USER",
        password="POSTGRES_PASSWORD",
        host="POSTGRES_HOST",
        port="POSTGRES_PORT"
    )
    cur = conn.cursor()  # Khởi tạo con trỏ sau khi kết nối thành công


# Hàm lưu dữ liệu
def save_to_db(review: str, topics: list[str], embedding: list[float]):
    # Create table if not exists
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO review_store (review, topics, embedding) VALUES (%s, %s, %s)",
        (review, json.dumps(topics), json.dumps(embedding))
    )
    conn.commit()
    return "Review saved to PostgreSQL"

def create_table_if_not_exists():
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS review_store (
            id SERIAL PRIMARY KEY,
            review TEXT NOT NULL,
            topics JSONB NOT NULL,
            embedding JSONB NOT NULL
        )
        """
    )
    conn.commit()


