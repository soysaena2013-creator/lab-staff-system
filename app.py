import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล (ใช้ลิงก์ล่าสุดของคุณ)
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    return pd.read_csv(CSV_URLS[key])

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# ดึงข้อมูล
df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# เลือกบุคลากร (ใช้เลขบัตรเป็น Key เพื่อความแม่นยำ)
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])
selected_name = user_options[selected_id]

# เมนู
menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูล (แปลงเป็น str และ strip เพื่อป้องกันปัญหาช่องว่าง)
str_id = str(selected_id).strip()
df_p = df_profile[df_profile["เลขบัตรประชาชน"].astype(str).str.strip() == str_id]
df_t = df_training[df_training["เลขบัตรประชาชน"].astype(str).str.strip() == str_id]
df_l = df_license[df_license["เลขบัตรประชาชน"].astype(str).str.strip() == str_id]

st.header(f"ข้อมูลของ: {selected_name}")

# แสดงผลแบบแนวตั้งเสมอ (ไม่ใช้ dataframe เพื่อป้องกันการเลื่อน)
if menu == "ข้อมูลทั่วไป":
    if not df_p.empty:
        st.write(df_p.iloc[0].T)
    else:
        st.write("ไม่พบข้อมูล")

elif menu == "ประวัติการฝึกอบรม":
    if not df_t.empty:
        for i in range(len(df_t)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_t.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลการฝึกอบรม")

elif menu == "ใบประกอบวิชาชีพ":
    if not df_l.empty:
        for i in range(len(df_l)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        # หากไม่พบข้อมูล ให้แสดงข้อความแจ้งเตือนที่ชัดเจน
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพสำหรับบุคลากรท่านนี้")