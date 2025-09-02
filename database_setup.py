import os
import pandas as pd
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def setup_db():
    """Tạo bảng recipes trong PostgreSQL"""
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text("DROP TABLE IF EXISTS recipes"))
        conn.execute(text("""
            CREATE TABLE recipes (
                id SERIAL PRIMARY KEY,
                ten_mon TEXT,
                anh TEXT,
                video TEXT,
                url TEXT,
                nguyen_lieu TEXT,
                cach_lam TEXT,
                embedding vector(384)
            );
        """))

    print("✅ Database setup completed")
    return engine

def insert_data(engine, csv_path="data/nguyen_lieu_sach2.csv"):
    """Đọc CSV và insert dữ liệu vào bảng recipes"""
    df = pd.read_csv(csv_path)

    # Khởi tạo model embedding
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Sinh embedding từ cột Nguyen_lieu
    embeddings = model.encode(df["Nguyen_lieu"].fillna("").tolist())

    with engine.begin() as conn:
        for i, row in df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO recipes (ten_mon, anh, video, url, nguyen_lieu, cach_lam, embedding)
                    VALUES (:ten_mon, :anh, :video, :url, :nguyen_lieu, :cach_lam, :embedding)
                """),
                {
                    "ten_mon": row.get("Ten_mon", ""),
                    "anh": row.get("Anh", ""),
                    "video": row.get("Video", ""),
                    "url": row.get("URL", ""),
                    "nguyen_lieu": row.get("Nguyen_lieu", ""),
                    "cach_lam": row.get("Cach_lam", ""),
                    "embedding": embeddings[i].tolist()
                }
            )

    print("✅ Inserted data into database")

if __name__ == "__main__":
    engine = setup_db()
    insert_data(engine)