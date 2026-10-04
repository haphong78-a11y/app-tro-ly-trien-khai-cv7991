Python
import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Hệ Thống Trợ Lý AI Giáo Viên THCS - CV 7991",
    page_icon="📚",
    layout="wide"
)

st.title("📚 TRỢ LÝ AI TẠO KHBD, SLIDE VÀ BÀI KIỂM TRA (CÔNG VĂN 7991)")
st.caption("Dành cho Giáo viên cấp THCS - Tự động hóa soạn giáo án, bài giảng và đề kiểm tra.")

# Thanh cấu hình API Key bên ngoài
with st.sidebar:
    st.header("⚙️ Cấu hình API")
    api_key = st.text_input("Nhập Google Gemini API Key:", type="password")
    st.markdown("[Lấy API Key miễn phí tại đây](https://aistudio.google.com/)")
    
    st.divider()
    st.markdown("**Thông tin chung:**")
    cap_hoc = "THCS"
    mon_hoc = st.selectbox("Môn học:", ["Ngữ văn", "Toán", "Tiếng Anh", "KHTN", "Lịch sử & Địa lí", "GDCD", "Tin học", "Công nghệ", "Nghệ thuật", "HĐTN-HN"])
    khoi_lop = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])

if not api_key:
    st.warning("⚠️ Vui lòng nhập Google Gemini API Key ở thanh bên trái để bắt đầu sử dụng ứng dụng.")
    st.stop()

# Khởi tạo Gemini Client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Tạo các tab tính năng chính
tab1, tab2, tab3 = st.tabs(["📝 Kế hoạch bài dạy (CV 7991)", "📊 Slide bài giảng", "📋 Đề kiểm tra"])

# ---------------------------------------------------------
# TAB 1: KẾ HOẠCH BÀI DẠY (CÔNG VĂN 7991)
# ---------------------------------------------------------
with tab1:
    st.subheader("Tạo Kế hoạch bài dạy (Giáo án) theo chuẩn Công văn 7991")
    ten_bai = st.text_input("Tên bài học / Chủ đề:", placeholder="Ví dụ: Bài 2. Nguyên tử - Nguyên tố hóa học (KHTN 7)")
    thoi_luong = st.text_input("Thời lượng (số tiết):", value="2 tiết")
    
    col1, col2 = st.columns(2)
    with col1:
        yeu_cau_can_dat = st.text_area("Yêu cầu cần đạt (theo CT GDPT 2018):", placeholder="Nêu các mục tiêu về Kiến thức, Năng lực, Phẩm chất...")
    with col2:
        thiet_bi = st.text_area("Thiết bị dạy học & Học liệu:", value="- GV: Sách giáo khoa, máy chiếu, phiếu học tập.\n- HS: SGK, vở ghi, đọc trước bài.")

    if st.button("🚀 Tạo Kế Hoạch Bài Dạy", type="primary", key="btn_khbd"):
        if not ten_bai:
            st.error("Vui lòng nhập tên bài học.")
        else:
            prompt_khbd = f"""
            Bạn là một chuyên gia giáo dục THCS xuất sắc tại Việt Nam. Hãy soạn Kế hoạch bài dạy (Giáo án) chuẩn theo khung cấu trúc Công văn 7991 cho môn {mon_hoc}, {khoi_lop}.
            
            Thông tin bài học:
            - Tên bài: {ten_bai}
            - Thời lượng: {thoi_luong}
            - Yêu cầu cần đạt: {yeu_cau_can_dat}
            - Thiết bị dạy học: {thiet_bi}
            
            Cấu trúc bài soạn phải tuân thủ nghiêm ngặt Công văn 7991 bao gồm:
            I. MỤC TIÊU (1. Về kiến thức, 2. Về năng lực, 3. Về phẩm chất)
            II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
            III. TIẾN TRÌNH DẠY HỌC (Gồm 4 hoạt động: 1. Mở đầu, 2. Hình thành kiến thức mới, 3. Luyện tập, 4. Vận dụng)
            Mỗi hoạt động cần làm rõ 4 bước: a) Mục tiêu, b) Nội dung, c) Sản phẩm, d) Tổ chức thực hiện (GV chuyển giao nhiệm vụ, HS thực hiện, Báo cáo thảo luận, Kết luận nhận định).
            
            Hãy trình bày rõ ràng, chi tiết, bằng tiếng Việt bằng định dạng Markdown.
            """
            with st.spinner("AI đang soạn Kế hoạch bài dạy..."):
                response = model.generate_content(prompt_khbd)
                st.markdown(response.text)
                st.download_button("💾 Tải giáo án (.md)", data=response.text, file_name=f"KHBD_{ten_bai}.md", mime="text/markdown")

# ---------------------------------------------------------
# TAB 2: SLIDE BÀI GIẢNG
# ---------------------------------------------------------
with tab2:
    st.subheader("Thiết kế kịch bản Slide bài giảng & Mã VBA xuất PowerPoint")
    slide_title = st.text_input("Tên bài giảng / Chủ đề Slide:", placeholder="Ví dụ: Bài 2. Nguyên tử")
    so_slide = st.slider("Số lượng slide mong muốn:", min_value=5, max_value=20, value=8)

    if st.button("🚀 Tạo Kịch Bản Slide & VBA", type="primary", key="btn_slide"):
        if not slide_title:
            st.error("Vui lòng nhập tên bài giảng.")
        else:
            prompt_slide = f"""
            Bạn là một chuyên gia thiết kế bài giảng điện tử THCS. Hãy tạo kịch bản Slide bài giảng cho môn {mon_hoc} {khoi_lop}, bài "{slide_title}" gồm {so_slide} slide.
            
            Yêu cầu:
            1. Chia rõ nội dung cho từng Slide:
               - Tiêu đề Slide
               - Nội dung chính (dạng gạch đầu dòng ngắn gọn)
               - Gợi ý hình ảnh/sơ đồ minh họa
               - Lời giảng/Gợi ý tương tác cho GV.
            2. Ở cuối câu trả lời, hãy cung cấp một đoạn mã VBA (Visual Basic for Applications) để có thể copy và dán vào Microsoft PowerPoint để tự động tạo khung các Slide này.
            """
            with st.spinner("AI đang tạo kịch bản slide..."):
                response = model.generate_content(prompt_slide)
                st.markdown(response.text)
                st.download_button("💾 Tải kịch bản Slide (.txt)", data=response.text, file_name=f"Slide_{slide_title}.txt", mime="text/plain")

# ---------------------------------------------------------
# TAB 3: BÀI KIỂM TRA / ĐỀ THI
# ---------------------------------------------------------
with tab3:
    st.subheader("Tạo Ma trận, Đặc tả & Đề kiểm tra (Trắc nghiệm + Tự luận)")
    ten_de_kt = st.text_input("Nội dung / Chủ đề kiểm tra:", placeholder="Ví dụ: Kiểm tra giữa kỳ 1 môn KHTN 7")
    thoi_gian_kt = st.selectbox("Thời gian làm bài:", ["15 phút", "45 phút (1 tiết)", "60 phút", "90 phút"])
    
    col_tn, col_tl = st.columns(2)
    with col_tn:
        so_cau_tn = st.number_input("Số câu trắc nghiệm (4 lựa chọn):", min_value=0, max_value=40, value=12)
    with col_tl:
        so_cau_tl = st.number_input("Số câu tự luận:", min_value=0, max_value=10, value=2)

    muc_do = st.multiselect("Các mức độ nhận thức:", ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"], default=["Nhận biết", "Thông hiểu", "Vận dụng"])

    if st.button("🚀 Tạo Đề Kiểm Tra & Đáp Án", type="primary", key="btn_dethi"):
        if not ten_de_kt:
            st.error("Vui lòng nhập nội dung kiểm tra.")
        else:
            prompt_dethi = f"""
            Bạn là chuyên gia ra đề thi THCS. Hãy lập Ma trận, Đề kiểm tra và Đáp án chi tiết cho môn {mon_hoc} {khoi_lop}.
            - Chủ đề: {ten_de_kt}
            - Thời gian: {thoi_gian_kt}
            - Mức độ nhận thức phân bổ: {', '.join(muc_do)}
            - Cấu trúc đề: {so_cau_tn} câu trắc nghiệm (4 phương án A, B, C, D) và {so_cau_tl} câu tự luận.
            
            Cấu trúc phản hồi:
            PHẦN 1: MA TRẬN VÀ BẢNG ĐẶC TẢ ĐỀ KIỂM TRA (Dạng bảng Markdown)
            PHẦN 2: ĐỀ KIỂM TRA (A. Trắc nghiệm, B. Tự luận)
            PHẦN 3: ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT
            """
            with st.spinner("AI đang thiết kế đề kiểm tra và ma trận..."):
                response = model.generate_content(prompt_dethi)
                st.markdown(response.text)
                st.download_button("💾 Tải đề kiểm tra (.md)", data=response.text, file_name=f"DeKiermTra_{ten_de_kt}.md", mime="text/markdown")

