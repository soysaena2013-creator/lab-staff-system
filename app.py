import streamlit as st
import pandas as pd

CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    # นำลิงก์ใหม่จากรูปภาพมาวางที่นี่ครับ
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    df = pd.read_csv(CSV_URLS[key])
    # แปลงเลขบัตรเป็น string และตัดช่องว่างออก
    df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.strip()
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# เลือกบุคลากร
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])

# --- ส่วนเช็คข้อมูล (Debug) ---
st.write("เลขบัตรที่เลือก:", selected_id)
st.write("เลขบัตรในตาราง Training (ตัวอย่าง 5 แถวแรก):", df_training["เลขบัตรประชาชน"].head().tolist())
# ---------------------------

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูล
df_t = df_training[df_training["เลขบัตรประชาชน"] == selected_id.strip()]

if menu == "ประวัติการฝึกอบรม":
    if not df_t.empty:
        st.dataframe(df_t)
    else:
        st.error("ไม่พบข้อมูล: เลขบัตรในตาราง Training ไม่ตรงกับ Profile")