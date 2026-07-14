import streamlit as st
import pandas as pd

# เปลี่ยน URL ตรงนี้ให้เป็น URL ของไฟล์ Google Sheets ของคุณ
BASE_URL = "https://docs.google.com/spreadsheets/d/1v_nQrlA7MDS4uIzTiHq2n7uxUcC7gtGvbM3ZmMj908M/edit?gid=190743628#gid=190743628"

@st.cache_data(ttl=600)
def load_data(gid):
    # เชื่อมต่อ URL กับ gid ของแต่ละแท็บ
    url = f"{BASE_URL}&gid={gid}"
    return pd.read_csv(url)

# ระบุ GID ของแต่ละแท็บ (ดูเลข gid จาก URL เมื่อคุณกดเลือกแท็บนั้นๆ ใน Google Sheets)
GIDS = {
    "profile": "0", # เปลี่ยนเป็นเลข gid จริงของแท็บ profile
    "training": "123456789", # เปลี่ยนเป็นเลข gid จริงของแท็บ ประวัติการฝึกอบรม
    "license": "987654321"   # เปลี่ยนเป็นเลข gid จริงของแท็บ professional licence
}

st.title("ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

menu = st.sidebar.radio("เมนูหลัก", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

if menu == "ข้อมูลทั่วไป":
    st.header("ข้อมูลทั่วไป")
    df = load_data(GIDS["profile"]) # เรียกใช้ gid ของแท็บ profile
    st.dataframe(df)