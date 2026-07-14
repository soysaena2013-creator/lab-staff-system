import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล (ใช้ลิงก์ที่คุณยืนยันว่าถูกต้อง)
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(url):
    return pd.read_csv(url)

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# ดึงข้อมูล
df_profile = load_data(CSV_URLS["profile"])
df_training = load_data(CSV_URLS["training"])
df_license = load_data(CSV_URLS["license"])

# สร้างตัวเลือก (ตรวจสอบให้แน่ใจว่าเลขบัตรเป็น string ทั้งหมด)
df_profile["เลขบัตรประชาชน"] = df_profile["เลขบัตรประชาชน"].astype(str)
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()

# เลือกบุคลากร
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=list(user_options.keys()), format_func=lambda x: user_options[x])

# กรองข้อมูล (ทำที่นี่จุดเดียว)
df_p = df_profile[df_profile["เลขบัตรประชาชน"].astype(str) == selected_id]
df_t = df_training[df_training["เลขบัตรประชาชน"].astype(str) == selected_id]
df_l = df_license[df_license["เลขบัตรประชาชน"].astype(str) == selected_id]

# แสดงผล
st.header(f"ข้อมูลของ: {user_options[selected_id]}")
menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

if menu == "ข้อมูลทั่วไป":
    if not df_p.empty:
        st.write(df_p.iloc[0].T)

elif menu == "ประวัติการฝึกอบรม":
    if not df_t.empty:
        for i in range(len(df_t)):
            st.write(df_t.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลการฝึกอบรม")

elif menu == "ใบประกอบวิชาชีพ":
    if not df_l.empty:
        for i in range(len(df_l)):
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ")