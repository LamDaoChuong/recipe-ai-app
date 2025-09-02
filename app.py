import streamlit as st
from recommender import recommend

st.set_page_config(page_title="🍲 Recipe AI App", page_icon="🍲", layout="wide")

st.title("🍲 Gợi ý món ăn từ nguyên liệu có sẵn")

user_input = st.text_input("👉 Nhập nguyên liệu bạn có (ví dụ: thịt gà, hành, tỏi)")

if st.button("🔍 Gợi ý món ăn"):
    if user_input.strip():
        results = recommend(user_input, top_k=5)

        if results:
            st.subheader("✅ Kết quả gợi ý:")

            for r in results:
                with st.container():
                    st.markdown(f"## 🍴 {r.ten_mon}  (🔗 {r.similarity:.2f})")

                    cols = st.columns([1, 2])

                    # Ảnh món ăn
                    with cols[0]:
                        if r.anh:
                            st.image(r.anh, use_container_width=True)
                        else:
                            st.write("📷 Không có ảnh")

                    # Thông tin chi tiết
                    with cols[1]:
                        if r.video:
                            st.markdown(f"[▶️ Xem video]({r.video})")
                        if r.url:
                            st.markdown(f"[🌐 Xem công thức]({r.url})")

                        st.markdown("**📝 Nguyên liệu:**")
                        st.write(r.nguyen_lieu)

                        st.markdown("**👨‍🍳 Cách làm:**")
                        st.write(r.cach_lam)

                    st.markdown("---")
        else:
            st.warning("❌ Không tìm thấy món ăn phù hợp.")
    else:
        st.warning("⚠️ Vui lòng nhập nguyên liệu trước khi tìm kiếm!")