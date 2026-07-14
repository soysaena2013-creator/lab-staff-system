import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบบุคลากรเทคนิคการแพทย์", layout="wide")

# ลิงก์ไปยัง Google Sheets ของคุณ (URL เต็ม)
SHEET_URL = "ใส่ URL ของไฟล์ Google Sheets ของคุณที่นี่"

@st.cache_data(ttl=600) # ให้ระบบจำข้อมูลไว้ 10 นาทีเพื่อความรวดเร็ว
def load_data(worksheet_name):
    # ใช้ pandas อ่านข้อมูลจาก Google Sheets
    url = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
    # หมายเหตุ: วิธีนี้ใช้ได้ผลดีหากไฟล์ตั้งค่าเป็น Anyone with the link
    return pd.read_csv(url + f"&sheet={worksheet_name}")

st.title("ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# สร้างเมนูทางด้านซ้าย
menu = st.sidebar.radio("เมนูหลัก", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ", "สถานะการฝึกอบรม"])

if menu == "ข้อมูลทั่วไป":
    st.header("ข้อมูลทั่วไป")
    df = load_data("profile")
    st.dataframe(df)

elif menu == "ประวัติการฝึกอบรม":
    st.header("ประวัติการฝึกอบรมและการศึกษาต่อเนื่อง")
    df = load_data("ประวัติการฝึกอบรมและการศึกษาต่อเนื่อง")
    st.dataframe(df)