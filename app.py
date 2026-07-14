import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล (ตรวจสอบลิงก์ training อีกครั้งให้ตรงนะครับ)
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=949946920&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    return pd.read_csv(CSV_URLS[key])

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

menu = st.sidebar.radio("เมนูหลัก", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# ดึงข้อมูลมาเตรียมไว้
df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# เลือกชื่อบุคลากรเพื่อกรองข้อมูล
selected_name = st.selectbox("เลือกบุคลากรที่ต้องการดูข้อมูล:", df_profile["ชื่อ สกุล"].unique())

# กรองข้อมูลตามชื่อ
df_p = df_profile[df_profile["ชื่อ สกุล"] == selected_name]
# สมมติว่าทุกตารางมีคอลัมน์ "ชื่อ สกุล" หรือ "เลขบัตรประชาชน" ที่เชื่อมโยงกันได้
df_t = df_training[df_training["ชื่อ สกุล"] == selected_name] if "ชื่อ สกุล" in df_training.columns else df_training
df_l = df_license[df_license["ชื่อ สกุล"] == selected_name] if "ชื่อ สกุล" in df_license.columns else df_license

# แสดงผลตามเมนู
if menu == "ข้อมูลทั่วไป":
    st.header(f"ข้อมูลของ: {selected_name}")
    st.dataframe(df_p, hide_index=True, use_container_width=True)

elif menu == "ประวัติการฝึกอบรม":
    st.header(f"ประวัติการฝึกอบรมของ: {selected_name}")
    st.dataframe(df_t, hide_index=True, use_container_width=True)

elif menu == "ใบประกอบวิชาชีพ":
    st.header(f"ใบประกอบวิชาชีพของ: {selected_name}")
    st.dataframe(df_l, hide_index=True, use_container_width=True)