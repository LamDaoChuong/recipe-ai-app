import os
import streamlit as st
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# Kết nối DB
engine = create_engine(DB_URL)


# Load model embedding
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


model = load_model()


# Hàm lấy gợi ý món ăn
def get_recommendations(ingredient_query, top_k=5):
    query_embedding = model.encode(ingredient_query).tolist()

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, ten_mon, anh, video, url, nguyen_lieu, cach_lam,
                       1 - (embedding <=> (:query_embedding)::vector) AS similarity
                FROM recipes
                ORDER BY embedding <=> (:query_embedding)::vector
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        )
        return result.fetchall()


# 🚀 UI Streamlit
st.set_page_config(page_title="AI Gợi ý món ăn", page_icon="🍲", layout="wide")

st.title("🍲 AI Gợi ý món ăn từ nguyên liệu có sẵn")
st.write("Nhập nguyên liệu bạn đang có, hệ thống sẽ gợi ý món ăn phù hợp.")

# Input từ người dùng
user_input = st.text_area("👉 Nhập nguyên liệu:", placeholder="Ví dụ: gà, hành, ớt, tỏi")

if st.button("🔍 Gợi ý món ăn"):
    if user_input.strip() == "":
        st.warning("⚠️ Vui lòng nhập ít nhất 1 nguyên liệu.")
    else:
        results = get_recommendations(user_input, top_k=5)

        if not results:
            st.error("❌ Không tìm thấy món ăn phù hợp.")
        else:
            for row in results:
                with st.container():
                    st.subheader(f"{row.ten_mon}  (⭐ {row.similarity:.2f})")
                    cols = st.columns([1, 2])

                    # Ảnh minh hoạ
                    with cols[0]:
                        if row.anh:
                            st.image(row.anh, use_container_width=True)  # ✅ đã fix

                        if row.video and "youtube" in row.video:
                            st.video(row.video)

                    # Thông tin chi tiết
                    with cols[1]:
                        st.markdown(f"**Nguyên liệu:** {row.nguyen_lieu}")
                        st.markdown(f"**Cách làm:** {row.cach_lam}")
                        if row.url:
                            st.markdown(f"[🔗 Xem chi tiết]({row.url})")

                    st.markdown("---")