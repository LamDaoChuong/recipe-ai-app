# 🍲 Recipe AI App

Ứng dụng **gợi ý món ăn từ nguyên liệu có sẵn**.  
Xây dựng bằng **Streamlit + Supabase (PostgreSQL + pgvector) + SentenceTransformers**.  

---

## 🚀 Tính năng
- Người dùng nhập nguyên liệu (ví dụ: *thịt gà, hành, tỏi*).  
- Hệ thống sinh **embedding** cho nguyên liệu nhập vào.  
- Truy vấn **pgvector** trong Supabase để tìm các món ăn có nguyên liệu gần nhất.  
- Hiển thị: tên món, ảnh, video hướng dẫn, link tham khảo, nguyên liệu, cách làm.  

---

Cấu trúc dự án

recipe-ai-app/
│
├── data/
│ └── nguyen_lieu_sach2.csv # dữ liệu gốc
│
├── app.py # Giao diện Streamlit
├── recommender.py # Hàm gợi ý từ pgvector
├── database_setup.py # Tạo bảng & nạp dữ liệu vào Supabase
├── data_processor.py # Xử lý dữ liệu + sinh embedding
├── requirements.txt # Thư viện cần thiết
├── .env.example # Config DB mẫu
└── README.md # Tài liệu này

---

## ⚙️ Cài đặt & chạy local

1. Clone repo
```bash
git clone https://github.com/chuong-pqag/recipe-ai-app.git
cd recipe-ai-app

2. Cài thư viện
pip install -r requirements.txt

3. Cấu hình Supabase

Tạo project tại Supabase.

Lấy connection string từ Supabase → copy vào file .env:
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxxx.supabase.co:5432/postgres

Vào SQL Editor trong Supabase, chạy:
CREATE EXTENSION IF NOT EXISTS vector;

4. Tạo bảng & nạp dữ liệu
python database_setup.py

5. Chạy ứng dụng
streamlit run app.py
🌐 Deploy lên Streamlit Cloud

Push code lên GitHub.

Vào Streamlit Cloud
, chọn New App → Connect GitHub → chọn repo.

Thêm biến môi trường DATABASE_URL trong Secrets Manager (dán connection string của Supabase).

Deploy và chạy app online 🎉.

📦 Dependencies

streamlit

pandas

numpy

psycopg2-binary

pgvector

sentence-transformers

scikit-learn

python-dotenv

requests

📜 License

MIT License © 2025