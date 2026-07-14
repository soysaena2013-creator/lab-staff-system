import streamlit as st
import pandas as pd

# ใช้ลิงก์ที่คุณคัดลอกมาจากการ Publish to web
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=949946920&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    return pd.read_csv(CSV_URLS[key])

st.title("ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

menu = st.sidebar.radio("เมนูหลัก", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

if menu == "ข้อมูลทั่วไป":
    st.header("ข้อมูลทั่วไป")
    st.dataframe(load_data("profile"))

elif menu == "ประวัติการฝึกอบรม":
    st.header("ประวัติการฝึกอบรมและการศึกษาต่อเนื่อง")
    st.dataframe(load_data("training"))

# ทำแบบเดียวกันสำหรับเมนูอื่นๆ