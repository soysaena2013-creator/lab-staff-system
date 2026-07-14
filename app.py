import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=949946920&single=true&output=csv",
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

# เลือกบุคลากร
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])
selected_name = user_options[selected_id]

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูล
df_p = df_profile[df_profile["เลขบัตรประชาชน"].astype(str) == str(selected_id)]
df_t = df_training[df_training["เลขบัตรประชาชน"].astype(str) == str(selected_id)]
df_l = df_license[df_license["เลขบัตรประชาชน"].astype(str) == str(selected_id)]

# กำหนดคอลัมน์ที่ต้องการแสดง (แก้ไขชื่อคอลัมน์ให้ตรงกับไฟล์ของคุณ)
cols_p = ["คำนำหน้านาม", "ชื่อ สกุล", "วัน เดือน ปีเกิด", "อายุปัจจุบัน (ปี)"]
cols_t = ["หัวข้อการอบรม", "ปี พ.ศ.", "หน่วยงานผู้จัด", "ชั่วโมงการอบรม"] # เปลี่ยนชื่อคอลัมน์ตามไฟล์จริงของคุณ
cols_l = ["เลขที่ใบประกอบ", "วันที่ออกใบอนุญาต", "วันหมดอายุ", "สถานะ"]      # เปลี่ยนชื่อคอลัมน์ตามไฟล์จริงของคุณ

st.header(f"ข้อมูลของ: {selected_name}")

with st.container(height=400):
    if menu == "ข้อมูลทั่วไป":
        st.dataframe(df_p[cols_p], hide_index=True, use_container_width=True)
    elif menu == "ประวัติการฝึกอบรม":
        # ตรวจสอบว่าคอลัมน์มีอยู่จริงก่อนแสดง เพื่อป้องกัน Error
        available_cols = [c for c in cols_t if c in df_t.columns]
        st.dataframe(df_t[available_cols], hide_index=True, use_container_width=True)
    elif menu == "ใบประกอบวิชาชีพ":
        available_cols = [c for c in cols_l if c in df_l.columns]
        st.dataframe(df_l[available_cols], hide_index=True, use_container_width=True)