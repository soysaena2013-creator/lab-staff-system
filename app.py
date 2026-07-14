import streamlit as st
import pandas as pd
# --- เพิ่มส่วนนี้เข้าไปเพื่อให้โปรแกรมรู้จักฟังก์ชัน load_data ---
@st.cache_data(ttl=600)
def load_data(sheet_name):
    # ใส่ลิงก์ CSV จากเมนู Publish to web ของคุณที่นี่
    # คุณต้องสร้างตัวแปรเพื่อเก็บ URL สำหรับแต่ละ sheet
    URLS = {
        "Profile": "ลิงก์_CSV_สำหรับ_Profile_ของคุณ",
        "Training": "ลิงก์_CSV_สำหรับ_Training_ของคุณ"
    }
    return pd.read_csv(URLS[sheet_name])
# โหลดข้อมูลหลัก
df_staff = load_data("Profile") # ฟังก์ชันดึงข้อมูลจาก Sheets

st.sidebar.title("ระบบงานเทคนิคการแพทย์")
selected_name = st.sidebar.selectbox("เลือกรายชื่อบุคลากร", df_staff["ชื่อ สกุล"].unique())

# กรองข้อมูลตามชื่อที่เลือก
person = df_staff[df_staff["ชื่อ สกุล"] == selected_name].iloc[0]

# สร้าง Tab ข้อมูล
tab1, tab2, tab3 = st.tabs(["ข้อมูลทั่วไป/ใบประกอบ", "ประวัติสุขภาพ/วัคซีน", "การประเมิน/อบรม"])

with tab1:
    st.image(person["รูปถ่าย"], width=150)
    st.write(f"ตำแหน่ง: {person['ตำแหน่ง']}")
    st.image(person["รูปใบประกอบวิชาชีพ"], caption="ใบประกอบวิชาชีพ") # แสดงรูปไฟล์แนบ

with tab2:
    st.subheader("ประวัติการตรวจสุขภาพ")
    # แสดงลิงก์ให้กดดาวน์โหลดไฟล์ผลตรวจสุขภาพ
    st.link_button("เปิดไฟล์ผลตรวจสุขภาพ", person["Link_ผลตรวจสุขภาพ"])
    st.write(f"สถานะวัคซีน: {person['วัคซีน']}")

with tab3:
    st.subheader("ผลการประเมิน/อบรม")
    st.write(f"ผลคะแนนสอบล่าสุด: {person['คะแนนสอบออนไลน์']}")
    st.write(f"ความต้องการการอบรม (Training Needs): {person['Training_Needs']}")