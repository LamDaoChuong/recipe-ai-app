import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load biến môi trường (DATABASE_URL từ .env)
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# Khởi tạo kết nối DB
engine = create_engine(DB_URL)

# Khởi tạo model embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

def recommend(query: str, top_k: int = 5):
    """
    Gợi ý món ăn dựa trên nguyên liệu người dùng nhập vào.
    Trả về danh sách món ăn kèm độ tương đồng.
    """
    # Sinh embedding cho input
    query_emb = model.encode([query])[0].tolist()

    # Truy vấn PostgreSQL với pgvector
    with engine.connect() as conn:
        results = conn.execute(
            text("""
                SELECT
                    id,
                    ten_mon,
                    anh,
                    video,
                    url,
                    nguyen_lieu,
                    cach_lam,
                    1 - (embedding <=> :query_emb) AS similarity
                FROM recipes
                ORDER BY embedding <=> :query_emb
                LIMIT :top_k;
            """),
            {"query_emb": query_emb, "top_k": top_k}
        ).fetchall()

    return results

if __name__ == "__main__":
    test_query = "thịt gà, hành, tỏi"
    rs = recommend(test_query, top_k=3)
    for r in rs:
        print(f"🍲 {r.ten_mon} ({r.similarity:.2f})")
        print(f"Nguyên liệu: {r.nguyen_lieu}")
        print("---")